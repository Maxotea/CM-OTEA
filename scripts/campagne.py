#!/usr/bin/env python3
"""Campagnes Meta : la moitié hors ligne de l'outil (le connecteur Meta Ads fait l'autre).

    python3 scripts/campagne.py check   campagnes/otea-production/2026-09-voeux-2027.json
    python3 scripts/campagne.py check   campagnes/            # valide toutes les specs
    python3 scripts/campagne.py plan    <spec.json>           # les appels MCP à passer, dans l'ordre
    python3 scripts/campagne.py journal <spec.json> --statut creee_en_pause \
            --set campaign_id=123 --set adset_id=456 --set ad_ids=789,1011 --note "..."
    python3 scripts/campagne.py liste                         # l'état de toutes les campagnes

Le circuit complet est dans .claude/skills/cm-meta-ads/SKILL.md. En résumé : une spec JSON par
campagne dans campagnes/<client>/, validée ici contre le registre campagnes/comptes.json ; `plan`
imprime les appels du connecteur Meta Ads avec leurs paramètres exacts (budgets en centimes,
dates ISO 8601 Europe/Paris, DSA rempli depuis le registre) ; la session Claude les exécute, tout
est créé en PAUSE ; `journal` consigne les identifiants dans la spec et dans campagnes/etat/.

Aucun identifiant Meta, aucun jeton : ce script ne parle pas à Meta. C'est voulu, la partie
authentifiée passe par le connecteur, dans la session, sous les yeux de Maxime.

Garde-fous codés ici (les autres sont dans le skill) :
  - le client doit exister dans le registre, être actif, et avoir un compte pub rattaché ;
  - objectif ODAX seulement, et optimisation compatible avec l'objectif (table du connecteur) ;
  - budget au-dessus du minimum du compte, au-dessous des plafonds du registre ;
  - fin après début, budget total => date de fin obligatoire ;
  - aucun texte à trous [ENTRE CROCHETS] ni média sans URL/hash : `check` passe mais `plan` refuse ;
  - catégorie spéciale du registre reportée d'office (immobilier = HOUSING) ;
  - site du client signalé hors ligne dans le registre => aucune destination WEBSITE ni lien vers lui ;
  - jamais d'activation : `plan` s'arrête à l'aperçu, l'activation est un geste de Maxime.
"""

import argparse
import json
import re
import signal
import sys
from datetime import date, datetime, time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
CAMPAGNES = ROOT / "campagnes"
REGISTRE = CAMPAGNES / "comptes.json"
ETAT = CAMPAGNES / "etat"
PARIS = ZoneInfo("Europe/Paris")

PLACEHOLDER = re.compile(r"\[[A-ZÀ-Ü0-9][^\]]*\]")

OBJECTIFS = {
    "OUTCOME_AWARENESS": "Notoriété",
    "OUTCOME_TRAFFIC": "Trafic",
    "OUTCOME_ENGAGEMENT": "Interaction",
    "OUTCOME_LEADS": "Prospects",
    "OUTCOME_SALES": "Ventes",
    "OUTCOME_APP_PROMOTION": "Application",
}

# Objectif → optimisations acceptées par le connecteur (la première est celle par défaut).
OPTIMISATIONS = {
    "OUTCOME_AWARENESS": ["REACH", "IMPRESSIONS", "AD_RECALL_LIFT", "THRUPLAY",
                          "TWO_SECOND_CONTINUOUS_VIDEO_VIEWS"],
    "OUTCOME_TRAFFIC": ["LINK_CLICKS", "LANDING_PAGE_VIEWS", "OFFSITE_CONVERSIONS", "IMPRESSIONS",
                        "POST_ENGAGEMENT", "REACH", "CONVERSATIONS", "THRUPLAY",
                        "VISIT_INSTAGRAM_PROFILE", "PROFILE_VISIT", "QUALITY_CALL", "REMINDERS_SET"],
    "OUTCOME_ENGAGEMENT": ["THRUPLAY", "POST_ENGAGEMENT", "EVENT_RESPONSES", "PAGE_LIKES",
                           "IMPRESSIONS", "REACH", "TWO_SECOND_CONTINUOUS_VIDEO_VIEWS",
                           "VIDEO_VIEWS", "LINK_CLICKS", "CONVERSATIONS", "OFFSITE_CONVERSIONS",
                           "LANDING_PAGE_VIEWS", "QUALITY_CALL", "PROFILE_AND_PAGE_ENGAGEMENT"],
    "OUTCOME_LEADS": ["OFFSITE_CONVERSIONS", "LEAD_GENERATION", "QUALITY_LEAD",
                      "LANDING_PAGE_VIEWS", "LINK_CLICKS", "IMPRESSIONS", "REACH", "VALUE",
                      "CONVERSATIONS", "QUALITY_CALL"],
    "OUTCOME_SALES": ["OFFSITE_CONVERSIONS", "VALUE", "LANDING_PAGE_VIEWS", "IMPRESSIONS",
                      "POST_ENGAGEMENT", "REACH", "LINK_CLICKS", "CONVERSATIONS"],
    "OUTCOME_APP_PROMOTION": ["APP_INSTALLS", "OFFSITE_CONVERSIONS", "IMPRESSIONS", "LINK_CLICKS",
                              "REACH", "VALUE", "VIDEO_VIEWS"],
}

# Optimisations qui imposent une destination précise.
DESTINATIONS_IMPOSEES = {
    "CONVERSATIONS": {"MESSENGER", "WHATSAPP", "INSTAGRAM_DIRECT"},
    "VISIT_INSTAGRAM_PROFILE": {"INSTAGRAM_PROFILE"},
    "PROFILE_VISIT": {"FACEBOOK_PAGE", "INSTAGRAM_PROFILE"},
    "PROFILE_AND_PAGE_ENGAGEMENT": {"INSTAGRAM_PROFILE", "FACEBOOK_PAGE",
                                    "INSTAGRAM_PROFILE_AND_FACEBOOK_PAGE"},
}
MESSAGERIES = {"MESSENGER", "WHATSAPP", "INSTAGRAM_DIRECT"}
DESTINATIONS_INSTAGRAM = {"INSTAGRAM_PROFILE", "INSTAGRAM_DIRECT",
                          "INSTAGRAM_PROFILE_AND_FACEBOOK_PAGE"}
# Optimisations qui exigent un promoted_object (pixel, formulaire…).
OPTIMISATIONS_PIXEL = {"OFFSITE_CONVERSIONS", "VALUE", "LANDING_PAGE_VIEWS"}
OPTIMISATIONS_LEADFORM = {"LEAD_GENERATION", "QUALITY_LEAD"}
FACTURATIONS = {"IMPRESSIONS", "LINK_CLICKS", "POST_ENGAGEMENT", "VIDEO_VIEWS"}
FORMATS = {"image", "video", "carrousel", "post_existant"}
STATUTS = ["brouillon", "prete", "creee_en_pause", "active", "en_pause", "terminee", "archivee"]
STATUTS_INSTAGRAM = {"VISIT_INSTAGRAM_PROFILE"}

# Longueurs au-delà desquelles Meta tronque à l'écran (repères, pas des limites API).
TEXTE_VISIBLE = 125
TITRE_MAX = 40
DESCRIPTION_MAX = 30


# ------------------------------------------------------------------ lecture

def charger_registre():
    data = json.loads(REGISTRE.read_text(encoding="utf-8"))
    return {c["slug"]: c for c in data["comptes"]}


def charger_spec(chemin):
    spec = json.loads(Path(chemin).read_text(encoding="utf-8"))
    spec.pop("_doc", None)
    return spec


def specs_dans(chemin):
    p = Path(chemin)
    if p.is_file():
        return [p]
    return sorted(f for f in p.glob("*/*.json") if f.parent.name not in {"etat"}
                  and not f.name.startswith("_"))


def eur_vers_cents(montant):
    return int(round(float(montant) * 100))


def iso_paris(jour, heure):
    d = date.fromisoformat(jour)
    return datetime.combine(d, heure, tzinfo=PARIS).isoformat()


# ------------------------------------------------------------------ check

class Rapport:
    def __init__(self, nom):
        self.nom = nom
        self.bloquants, self.avertissements = [], []

    def bloque(self, msg):
        self.bloquants.append(msg)

    def avertit(self, msg):
        self.avertissements.append(msg)

    def ok(self):
        return not self.bloquants

    def afficher(self):
        etat = "✅" if self.ok() else "⛔"
        print(f"{etat} {self.nom}")
        for b in self.bloquants:
            print(f"   ⛔ {b}")
        for a in self.avertissements:
            print(f"   ⚠️  {a}")


def verifier(spec, registre, pour_plan=False):
    """Retourne un Rapport. pour_plan durcit : médias et textes doivent être prêts."""
    r = Rapport(f"{spec.get('client', '?')}/{spec.get('slug', '?')}")

    for champ in ("client", "slug", "titre", "mois", "objectif", "optimisation", "budget",
                  "ciblage", "publicites"):
        if champ not in spec:
            r.bloque(f"champ manquant : {champ}")
    if not r.ok():
        return r

    compte = registre.get(spec["client"])
    if compte is None:
        r.bloque(f"client inconnu du registre : {spec['client']}")
        return r
    if not compte.get("actif"):
        r.bloque(f"client désactivé dans le registre : {spec['client']}")
    if not compte.get("ad_account_id"):
        r.bloque("client non rattaché : pas de compte pub (voir onboarding-compte-pub.md)")
    if not compte.get("page_id"):
        r.bloque("pas de page Facebook dans le registre : une publicité doit être signée par une page")

    if not re.fullmatch(r"\d{4}-\d{2}", spec["mois"]):
        r.bloque("mois attendu au format AAAA-MM (rattachement au mois, règle transverse 6)")

    obj, opt = spec["objectif"], spec["optimisation"]
    if obj not in OBJECTIFS:
        r.bloque(f"objectif hors liste ODAX : {obj} (attendu : {', '.join(OBJECTIFS)})")
    elif opt not in OPTIMISATIONS[obj]:
        r.bloque(f"optimisation {opt} incompatible avec {obj} "
                 f"(possibles : {', '.join(OPTIMISATIONS[obj])})")

    dest = spec.get("destination")
    if opt in DESTINATIONS_IMPOSEES and dest not in DESTINATIONS_IMPOSEES[opt]:
        r.bloque(f"{opt} exige destination dans {sorted(DESTINATIONS_IMPOSEES[opt])}, reçu {dest}")
    if dest in DESTINATIONS_INSTAGRAM and not compte.get("ig_account_id"):
        r.bloque(f"destination {dest} mais aucun compte Instagram rattaché au compte pub "
                 "(ig_account_id null dans le registre)")
    if opt in OPTIMISATIONS_PIXEL and not compte.get("pixel_id"):
        r.bloque(f"{opt} exige un pixel (promoted_object) et le registre n'en connaît pas")
    if opt in OPTIMISATIONS_LEADFORM and not compte.get("leadgen_tos_accepte"):
        r.bloque(f"{opt} exige que la page ait accepté les conditions Lead Ads "
                 "(leadgen_tos_accepte=false dans le registre)")
    hors_ligne = compte.get("site_indisponible_depuis")
    site_hote = None
    if compte.get("site"):
        site_hote = re.sub(r"^https?://(www\.)?", "", compte["site"]).split("/")[0].lower()
    if hors_ligne and dest == "WEBSITE":
        r.bloque(f"destination WEBSITE alors que le site du client est hors ligne depuis {hors_ligne} "
                 "(site_indisponible_depuis dans le registre)")
    fact = spec.get("facturation", "IMPRESSIONS")
    if fact not in FACTURATIONS:
        r.bloque(f"facturation hors liste : {fact}")

    # Budget et dates
    b = spec["budget"]
    try:
        montant = float(b["montant_eur"])
    except (KeyError, TypeError, ValueError):
        r.bloque("budget.montant_eur manquant ou non numérique")
        montant = None
    typ = b.get("type")
    if typ not in {"journalier", "total"}:
        r.bloque("budget.type doit valoir journalier ou total")
    debut, fin = b.get("debut"), b.get("fin")
    try:
        d_debut = date.fromisoformat(debut) if debut else None
        d_fin = date.fromisoformat(fin) if fin else None
    except ValueError:
        r.bloque("budget.debut / budget.fin au format AAAA-MM-JJ")
        d_debut = d_fin = None
    if d_debut is None:
        r.bloque("budget.debut manquant")
    if typ == "total" and d_fin is None:
        r.bloque("budget total : la date de fin est obligatoire")
    if d_debut and d_fin and d_fin <= d_debut:
        r.bloque("budget.fin doit être après budget.debut")
    if d_debut and d_debut < date.today():
        r.avertit(f"début {debut} déjà passé : Meta lancera dès l'activation")
    jours = (d_fin - d_debut).days + 1 if (d_debut and d_fin) else None

    if montant is not None:
        cents = eur_vers_cents(montant)
        mini = compte.get("budget_journalier_min_cents") or 0
        plafonds = compte.get("plafonds") or {}
        pj, pt = plafonds.get("journalier_eur"), plafonds.get("total_par_campagne_eur")
        if typ == "journalier":
            if cents < mini:
                r.bloque(f"budget journalier {montant:.2f} € sous le minimum du compte ({mini / 100:.2f} €)")
            if pj is not None and montant > pj:
                r.bloque(f"budget journalier {montant:.2f} € au-dessus du plafond du registre ({pj} €)")
            if jours and pt is not None and montant * jours > pt:
                r.bloque(f"{montant:.2f} € × {jours} j = {montant * jours:.0f} € dépasse le plafond "
                         f"par campagne ({pt} €)")
            if jours and jours < 4:
                r.avertit("moins de 4 jours : la phase d'apprentissage n'aura pas le temps de se stabiliser")
        elif typ == "total" and jours:
            par_jour = montant / jours
            if eur_vers_cents(par_jour) < mini:
                r.bloque(f"budget total {montant:.2f} € sur {jours} j = {par_jour:.2f} €/j, sous le minimum "
                         f"({mini / 100:.2f} €)")
            if pj is not None and par_jour > pj:
                r.bloque(f"{par_jour:.2f} €/j dépasse le plafond journalier du registre ({pj} €)")
            if pt is not None and montant > pt:
                r.bloque(f"budget total {montant:.2f} € au-dessus du plafond par campagne ({pt} €)")

    # Ciblage
    c = spec["ciblage"]
    if not c.get("pays"):
        r.bloque("ciblage.pays vide : le ciblage géographique est obligatoire")
    if compte.get("categories_speciales"):
        if c.get("age_min") or c.get("age_max"):
            r.avertit(f"catégorie spéciale {compte['categories_speciales']} : Meta ignore l'âge, "
                      "le sexe et le code postal, ne pas les promettre au client")
    if c.get("interets"):
        for i in c["interets"]:
            if not re.fullmatch(r"\d{10,20}", str(i.get("id", ""))):
                r.bloque(f"intérêt sans identifiant Meta réel : {i}")

    # Publicités
    pubs = spec["publicites"]
    if not pubs:
        r.bloque("aucune publicité dans la spec")
    for i, pub in enumerate(pubs, 1):
        tag = f"pub {i} ({pub.get('nom', 'sans nom')})"
        fmt = pub.get("format")
        if fmt not in FORMATS:
            r.bloque(f"{tag} : format {fmt} hors {sorted(FORMATS)}")
        for champ in ("texte", "titre", "description"):
            val = pub.get(champ) or ""
            if PLACEHOLDER.search(val):
                (r.bloque if pour_plan else r.avertit)(f"{tag} : {champ} contient un texte à trous")
        if len(pub.get("texte") or "") > TEXTE_VISIBLE:
            r.avertit(f"{tag} : texte de {len(pub['texte'])} caractères, seuls {TEXTE_VISIBLE} sont visibles "
                      "avant « voir plus »")
        if len(pub.get("titre") or "") > TITRE_MAX:
            r.avertit(f"{tag} : titre de {len(pub['titre'])} caractères, {TITRE_MAX} max conseillé")
        if len(pub.get("description") or "") > DESCRIPTION_MAX:
            r.avertit(f"{tag} : description de {len(pub['description'])} caractères, {DESCRIPTION_MAX} max conseillé")
        if fmt == "image" and not pub.get("lien") and dest not in MESSAGERIES:
            r.bloque(f"{tag} : une pub image exige un lien de destination")
        lien = (pub.get("lien") or "").lower()
        if hors_ligne and site_hote and site_hote in lien:
            r.bloque(f"{tag} : le lien pointe vers {site_hote}, hors ligne depuis {hors_ligne}")
        if lien.startswith("http") and pour_plan:
            r.avertit(f"{tag} : vérifier que {pub['lien']} répond avant de créer (le script ne le fait pas)")
        if fmt == "post_existant":
            if not pub.get("post_id"):
                r.bloque(f"{tag} : post_existant exige post_id (format pageID_postID)")
        else:
            media = pub.get("media") or {}
            pret = bool(media.get("url") or media.get("hash") or media.get("video_id"))
            if not pret:
                (r.bloque if pour_plan else r.avertit)(f"{tag} : média non hébergé (ni url, ni hash, ni video_id)")
            if fmt == "video" and pour_plan and not media.get("video_id"):
                r.bloque(f"{tag} : vidéo sans video_id (passer par ads_creative_upload_media d'abord)")
            if fmt == "video" and pour_plan and not (media.get("vignette_url") or media.get("hash")):
                r.bloque(f"{tag} : vidéo sans vignette (vignette_url ou hash)")
            note = (media.get("note") or "").lower()
            if " ia " in f" {note} " or "générée" in note or "generee" in note:
                r.avertit(f"{tag} : la note du média mentionne l'IA, rappel : images 100 % IA interdites "
                          "sur un compte qui a de vraies photos, jamais de personne réelle générée")
        if pub.get("ia_generative") not in {None, "OPT_IN", "OPT_OUT"}:
            r.bloque(f"{tag} : ia_generative doit valoir OPT_IN, OPT_OUT ou null")
        if pub.get("ia_generative") is None:
            r.avertit(f"{tag} : ia_generative non renseigné, la déclaration IA est une décision de Maxime")

    statut = (spec.get("meta") or {}).get("statut", "brouillon")
    if statut not in STATUTS:
        r.bloque(f"meta.statut hors liste : {statut}")
    return r


# ------------------------------------------------------------------ plan

def nom_campagne(spec, compte):
    return f"[{compte['prefixe']}] {spec['mois']} · {OBJECTIFS[spec['objectif']]} · {spec['titre']}"


def nom_ensemble(spec, compte):
    c = spec["ciblage"]
    zone = "+".join(c.get("pays", []))
    ages = f"{c.get('age_min', '')}-{c.get('age_max', '')}".strip("-")
    plac = "auto" if spec.get("placements", "automatiques") == "automatiques" else "placements choisis"
    return f"[{compte['prefixe']}] {zone} {ages} · {plac}".replace("  ", " ")


def ciblage_meta(spec, compte):
    c = spec["ciblage"]
    t = {"geo_locations": {"countries": c["pays"]}}
    if c.get("age_min"):
        t["age_min"] = c["age_min"]
    if c.get("age_max"):
        t["age_max"] = c["age_max"]
    if c.get("interets"):
        t["flexible_spec"] = [{"interests": [{"id": str(i["id"]), "name": i.get("name", "")}
                                             for i in c["interets"]]}]
    t["targeting_automation"] = {"advantage_audience": 1 if c.get("advantage_audience", True) else 0}
    if spec.get("placements") not in (None, "automatiques"):
        t["publisher_platforms"] = spec["placements"]
    return t


def plan(spec, compte):
    """Imprime les appels du connecteur Meta Ads, dans l'ordre, prêts à copier."""
    b = spec["budget"]
    cents = eur_vers_cents(b["montant_eur"])
    debut = iso_paris(b["debut"], dtime(9, 0))
    fin = iso_paris(b["fin"], dtime(23, 59)) if b.get("fin") else None
    aa = compte["ad_account_id"]
    etapes = []

    etapes.append(("Vérifier le compte (lecture seule)", "ads_get_ad_accounts", {},
                   f"contrôler que {aa} ({compte['ad_account_nom']}) est ACTIVE, is_queryable=true, "
                   f"devise {compte['devise']}, et que budget_journalier_min_cents du registre est à jour"))

    for i, pub in enumerate(spec["publicites"], 1):
        media = pub.get("media") or {}
        if pub["format"] in {"image", "carrousel"} and media.get("url") and not media.get("hash"):
            etapes.append((f"Héberger le média de la pub {i} dans le compte", "ads_creative_upload_media",
                           {"ad_account_id": aa, "upload_source": "URL", "media_type": "IMAGE",
                            "media_url": media["url"], "name": f"{spec['client']}-{spec['slug']}-{i}"},
                           "reporter le hash renvoyé dans media.hash de la spec"))

    camp = {"ad_account_id": aa, "campaign_name": nom_campagne(spec, compte), "objective": spec["objectif"],
            "buying_type": "AUCTION",
            "special_ad_categories": json.dumps(compte.get("categories_speciales") or [])}
    if compte.get("categories_speciales"):
        camp["special_ad_category_country"] = json.dumps(spec["ciblage"]["pays"])
    if b["type"] == "journalier":
        camp["campaign_daily_budget"] = cents
    else:
        camp["campaign_lifetime_budget"] = cents
    if fin:
        camp["campaign_stop_time"] = fin
    etapes.append(("Créer la campagne (CBO, PAUSE)", "ads_create_campaign", camp,
                   "noter campaign_id ; relire valid_optimization_goals dans la réponse"))

    ens = {"ad_account_id": aa, "campaign_id": "<campaign_id>", "ad_set_name": nom_ensemble(spec, compte),
           "optimization_goal": spec["optimisation"], "billing_event": spec.get("facturation", "IMPRESSIONS"),
           "targeting": json.dumps(ciblage_meta(spec, compte), ensure_ascii=False),
           "start_time": debut, "dsa_payor": compte["dsa_payor"], "dsa_beneficiary": compte["dsa_beneficiary"]}
    if spec.get("destination"):
        ens["destination_type"] = spec["destination"]
    if fin:
        ens["end_time"] = fin
    if spec["optimisation"] == "CONVERSATIONS" or spec.get("destination") in MESSAGERIES:
        ens["promoted_object"] = json.dumps({"page_id": compte["page_id"]})
    if spec["optimisation"] in OPTIMISATIONS_PIXEL and compte.get("pixel_id"):
        ens["promoted_object"] = json.dumps({"pixel_id": compte["pixel_id"]})
    if spec["optimisation"] in OPTIMISATIONS_LEADFORM:
        ens["promoted_object"] = json.dumps({"page_id": compte["page_id"]})
    etapes.append(("Créer l'ensemble de publicités (PAUSE, pas de budget : le budget est sur la campagne)",
                   "ads_create_ad_set", ens, "noter adset_id"))

    for i, pub in enumerate(spec["publicites"], 1):
        media = pub.get("media") or {}
        cr = {"ad_account_id": aa, "page_id": compte["page_id"], "name": f"{nom_campagne(spec, compte)} · {pub['nom']}"}
        if compte.get("ig_account_id"):
            cr["instagram_user_id"] = compte["ig_account_id"]
        if pub["format"] == "post_existant":
            cr["object_story_id"] = pub["post_id"]
        else:
            cr.update({"message": pub.get("texte"), "headline": pub.get("titre"),
                       "call_to_action_type": pub.get("cta") or "LEARN_MORE"})
            if pub.get("description"):
                cr["description"] = pub["description"]
            if pub.get("lien"):
                cr["link_url"] = pub["lien"]
            if pub.get("lien_affiche"):
                cr["display_link"] = pub["lien_affiche"]
            if pub.get("ia_generative"):
                cr["self_ai_disclosure"] = pub["ia_generative"]
            if pub["format"] == "image":
                if media.get("hash"):
                    cr["image_hash"] = media["hash"]
                else:
                    cr["image_url"] = media.get("url")
            elif pub["format"] == "video":
                cr["video_id"] = media.get("video_id")
                if media.get("hash"):
                    cr["image_hash"] = media["hash"]
                else:
                    cr["image_url"] = media.get("vignette_url")
            elif pub["format"] == "carrousel":
                cr["cards"] = pub.get("cartes", [])
        etapes.append((f"Créer la creative de la pub {i}", "ads_create_creative", cr, "noter creative_id"))
        etapes.append((f"Créer la publicité {i} (PAUSE)", "ads_create_ad",
                       {"ad_account_id": aa, "ad_set_id": "<adset_id>", "ad_name": f"[{compte['prefixe']}] {pub['nom']}",
                        "creative": json.dumps({"creative_id": "<creative_id>"})}, "noter ad_id"))
        etapes.append((f"Aperçu de la publicité {i}", "ads_get_ad_preview",
                       {"ad_id": "<ad_id>", "ad_format": "INSTAGRAM_STANDARD" if pub["format"] != "video" else "INSTAGRAM_REELS"},
                       "donner preview_url tel quel à Maxime, et le noter dans meta.preview_url"))

    etapes.append(("Contrôler les erreurs bloquantes", "ads_get_errors", {"entity_ids": ["<campaign_id>"]},
                   "toute erreur se corrige avant de rendre compte"))

    print(f"# Plan · {nom_campagne(spec, compte)}")
    print(f"# Compte pub {aa} ({compte['ad_account_nom']}) · page {compte['page_nom']} ({compte['page_id']})")
    print(f"# Budget : {b['montant_eur']} € {b['type']} = {cents} centimes · du {b['debut']} au {b.get('fin') or 'sans fin'}")
    print("# Tout est créé en PAUSE. Ce plan s'arrête à l'aperçu : l'activation n'en fait pas partie.\n")
    for n, (titre, outil, params, suite) in enumerate(etapes, 1):
        print(f"## {n}. {titre}")
        print(f"outil : {outil}")
        print("params : " + json.dumps(params, ensure_ascii=False, indent=2))
        print(f"puis : {suite}\n")
    print("## Ensuite")
    print(f"python3 scripts/campagne.py journal <spec> --statut creee_en_pause "
          f"--set campaign_id=… --set adset_id=… --set creative_ids=… --set ad_ids=… --set preview_url=…")
    print("Rendre compte à Maxime (nom, budget, dates, cible, aperçu) et s'arrêter. L'activation attend sa phrase "
          "explicite ; elle se fait campagne → ensemble → publicité, avec ads_activate_entity, puis relecture de "
          "effective_status et ads_get_errors.")


# ------------------------------------------------------------------ journal

def journal(chemin, statut, sets, note):
    spec = json.loads(Path(chemin).read_text(encoding="utf-8"))
    meta = spec.setdefault("meta", {})
    if statut:
        if statut not in STATUTS:
            sys.exit(f"statut hors liste : {statut} (attendu : {', '.join(STATUTS)})")
        meta["statut"] = statut
    for kv in sets or []:
        if "=" not in kv:
            sys.exit(f"--set attend cle=valeur, reçu {kv}")
        k, v = kv.split("=", 1)
        if k in {"creative_ids", "ad_ids"}:
            meta[k] = [x for x in v.split(",") if x]
        else:
            meta[k] = v or None
    horodatage = datetime.now(PARIS).isoformat(timespec="minutes")
    entree = {"date": horodatage, "statut": meta.get("statut"), "note": note}
    entree.update({k: meta.get(k) for k in ("campaign_id", "adset_id", "ad_ids")})
    meta.setdefault("journal", []).append(entree)
    Path(chemin).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ETAT.mkdir(exist_ok=True)
    fichier = ETAT / f"{spec['client']}.json"
    etat = json.loads(fichier.read_text(encoding="utf-8")) if fichier.exists() else {"client": spec["client"], "campagnes": {}}
    cle = Path(chemin).stem
    entree_etat = dict(entree)
    chemin_abs = Path(chemin).resolve()
    chemin_rel = str(chemin_abs.relative_to(ROOT)) if chemin_abs.is_relative_to(ROOT) else str(chemin_abs)
    entree_etat.update({"titre": spec.get("titre"), "mois": spec.get("mois"),
                        "budget": spec.get("budget"), "spec": chemin_rel})
    etat["campagnes"].setdefault(cle, []).append(entree_etat)
    fichier.write_text(json.dumps(etat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"journal : {cle} → {meta.get('statut')} ({horodatage})")


# ------------------------------------------------------------------ liste

def liste(registre):
    lignes = []
    for f in specs_dans(CAMPAGNES):
        s = charger_spec(f)
        m = s.get("meta") or {}
        b = s.get("budget") or {}
        lignes.append((s.get("client"), s.get("mois"), s.get("slug"), m.get("statut", "brouillon"),
                       f"{b.get('montant_eur')} € {b.get('type')}", f"{b.get('debut')} → {b.get('fin') or '…'}",
                       m.get("campaign_id") or ""))
    if not lignes:
        print("aucune spec dans campagnes/")
        return
    print(f"{'client':<24}{'mois':<9}{'slug':<22}{'statut':<16}{'budget':<18}{'période':<26}campaign_id")
    for l in sorted(lignes):
        print(f"{l[0]:<24}{l[1]:<9}{l[2]:<22}{l[3]:<16}{l[4]:<18}{l[5]:<26}{l[6]}")
    non_rattaches = [c for c in registre.values() if not c.get("ad_account_id")]
    if non_rattaches:
        print("\nclients sans compte pub rattaché : " + ", ".join(c["slug"] for c in non_rattaches))


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check", help="valide une spec ou un dossier de specs")
    p.add_argument("chemin")
    p = sub.add_parser("plan", help="imprime les appels MCP à passer, dans l'ordre")
    p.add_argument("chemin")
    p = sub.add_parser("journal", help="consigne un changement d'état et des identifiants")
    p.add_argument("chemin")
    p.add_argument("--statut", choices=STATUTS)
    p.add_argument("--set", action="append", metavar="cle=valeur")
    p.add_argument("--note", default="")
    sub.add_parser("liste", help="l'état de toutes les campagnes du dépôt")
    args = ap.parse_args()

    registre = charger_registre()
    if args.cmd == "check":
        fichiers = specs_dans(args.chemin)
        if not fichiers:
            sys.exit(f"aucune spec trouvée dans {args.chemin}")
        tout_ok = True
        for f in fichiers:
            r = verifier(charger_spec(f), registre)
            r.afficher()
            tout_ok &= r.ok()
        sys.exit(0 if tout_ok else 1)
    if args.cmd == "plan":
        spec = charger_spec(args.chemin)
        r = verifier(spec, registre, pour_plan=True)
        if not r.ok():
            r.afficher()
            sys.exit("plan refusé : corriger les points bloquants ci-dessus")
        for a in r.avertissements:
            print(f"⚠️  {a}")
        plan(spec, registre[spec["client"]])
    if args.cmd == "journal":
        journal(args.chemin, args.statut, args.set, args.note)
    if args.cmd == "liste":
        liste(registre)


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()

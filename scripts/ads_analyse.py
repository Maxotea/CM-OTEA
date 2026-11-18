#!/usr/bin/env python3
"""Analyse des campagnes Meta : la lecture chiffrée du media buyer.

    python3 scripts/ads_analyse.py diagnostic <spec.json> <releve.json> [--prospects N] [--le AAAA-MM-JJ]
    python3 scripts/ads_analyse.py taille --taux 0.015 --hausse 0.30 --cpm 6
    python3 scripts/ads_analyse.py tableau <mois AAAA-MM>

Un relevé est la réponse de `ads_get_ad_entities` (niveau pub, champs de reporting.md), enregistrée
telle quelle dans campagnes/etat/releves/<client>/<slug>-<AAAA-MM-JJ>.json. Le script ne parle
jamais à Meta : il lit ce que la session a relevé, et dit quoi en penser.

Ce qu'il calcule :
  - le jour de diffusion (J+n) et la phase : apprentissage (J<3), lecture (J3 à J6), décision (J7+) ;
  - le rythme de dépense contre le budget prévu (au-delà de 120 % : couper d'office, règle du skill) ;
  - par pub : CPM, CTR avec son intervalle de confiance à 95 % (Wilson), taux de résultat, coût
    par résultat, répétition ;
  - entre pubs : la probabilité que chacune soit la meilleure (modèle bêta-binomial, tirages
    simulés), et si l'écart est assez net pour trancher ;
  - le coût par prospect qualifié, quand Maxime donne le nombre relevé à la main, face aux paliers
    de la spec (kpi.cout_par_lead_cible_eur) ;
  - le verdict, aligné sur l'Étape 6 du skill : ne rien toucher, corriger, continuer, couper, ou
    proposer +20 % (toujours sur OK de Maxime, dans les plafonds du registre).

`taille` répond à « combien faut-il dépenser pour qu'un test A/B veuille dire quelque chose ».
`tableau` produit le tableau mensuel de reporting.md à partir des derniers relevés du mois.

Aucun repère inventé : les seuils de comparaison viennent de campagnes/reperes.json, chacun avec
sa source. Un repère absent n'est pas comparé, le script le dit.
"""

import argparse
import json
import math
import random
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAMPAGNES = ROOT / "campagnes"
RELEVES = CAMPAGNES / "etat" / "releves"
REPERES = CAMPAGNES / "reperes.json"
REGISTRE = CAMPAGNES / "comptes.json"

Z95 = 1.959964
Z80 = 0.841621
SEUIL_PROBA = 0.95          # probabilité d'être la meilleure pour déclarer une pub gagnante
IMPRESSIONS_MIN = 1000      # en dessous, une pub n'a pas assez diffusé pour être jugée
REPETITION_MAX = 3.0        # reporting.md : au-delà de 3 sur une semaine, lassitude
SURDEPENSE = 1.20           # skill, Étape 5 : dépense au-delà du prévu => couper d'office
TIRAGES = 20000


# ---------------------------------------------------------------- lecture des relevés

def nombre(valeur):
    """Un chiffre Meta, quelle que soit sa forme : 12, "12.5", {"value": ..}, {"values": [..]}."""
    if valeur is None or valeur == "":
        return 0.0
    if isinstance(valeur, bool):
        return float(valeur)
    if isinstance(valeur, (int, float)):
        return float(valeur)
    if isinstance(valeur, str):
        try:
            return float(valeur.replace(",", ".").replace("%", "").strip())
        except ValueError:
            return 0.0
    if isinstance(valeur, dict):
        if "value" in valeur:
            return nombre(valeur["value"])
        if "values" in valeur:
            return nombre(valeur["values"])
        return 0.0
    if isinstance(valeur, list):
        return nombre(valeur[0]) if valeur else 0.0
    return 0.0


def lignes_du_releve(donnees):
    """La liste des pubs d'un relevé, que la réponse soit brute (chaîne JSON) ou déjà décodée."""
    if isinstance(donnees, dict):
        for cle in ("ad_entities", "data", "lignes"):
            if cle in donnees:
                donnees = donnees[cle]
                break
    if isinstance(donnees, str):
        donnees = json.loads(donnees)
    if not isinstance(donnees, list):
        raise ValueError("relevé illisible : on attend la liste ad_entities de ads_get_ad_entities")
    return donnees


def pub_depuis_ligne(ligne):
    impressions = nombre(ligne.get("impressions"))
    clics = nombre(ligne.get("clicks"))
    couverture = nombre(ligne.get("reach"))
    depense = nombre(ligne.get("amount_spent", ligne.get("spend")))
    resultats = nombre(ligne.get("results"))
    repetition = nombre(ligne.get("frequency")) or (impressions / couverture if couverture else 0.0)
    return {
        "id": str(ligne.get("id", "")),
        "nom": ligne.get("name") or ligne.get("id") or "pub",
        "statut": ligne.get("effective_status", ""),
        "depense": depense,
        "impressions": impressions,
        "couverture": couverture,
        "clics": clics,
        "resultats": resultats,
        "repetition": repetition,
    }


# ---------------------------------------------------------------- statistiques

def wilson(succes, essais, z=Z95):
    """Intervalle de confiance d'une proportion, fiable même sur de petits volumes."""
    if essais <= 0:
        return (0.0, 0.0)
    p = succes / essais
    d = 1 + z * z / essais
    centre = (p + z * z / (2 * essais)) / d
    marge = z * math.sqrt(p * (1 - p) / essais + z * z / (4 * essais * essais)) / d
    return (max(0.0, centre - marge), min(1.0, centre + marge))


def proba_meilleure(pubs, cle="clics", tirages=TIRAGES, graine=7):
    """Probabilité que chaque pub ait le meilleur taux (cle / impressions), a priori Beta(1, 1)."""
    rng = random.Random(graine)
    gagnes = [0] * len(pubs)
    params = [(p[cle] + 1, max(p["impressions"] - p[cle], 0) + 1) for p in pubs]
    for _ in range(tirages):
        tirage = [rng.betavariate(a, b) for a, b in params]
        gagnes[tirage.index(max(tirage))] += 1
    return [g / tirages for g in gagnes]


def taille_echantillon(taux, hausse, z_a=Z95, z_b=Z80):
    """Impressions par pub pour détecter « taux » contre « taux × (1 + hausse) » (α 5 %, puissance 80 %)."""
    p1, p2 = taux, taux * (1 + hausse)
    if not (0 < p1 < 1 and 0 < p2 < 1) or p1 == p2:
        raise ValueError("taux et hausse doivent donner deux proportions distinctes entre 0 et 1")
    pm = (p1 + p2) / 2
    n = (z_a * math.sqrt(2 * pm * (1 - pm)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(n / (p2 - p1) ** 2)


# ---------------------------------------------------------------- repères

def charger_reperes():
    if not REPERES.exists():
        return {}
    return json.loads(REPERES.read_text(encoding="utf-8")).get("reperes", {})


def repere_pour(client, reperes):
    """Le repère du client, sinon celui du compte pub partagé, sinon rien."""
    return reperes.get(client) or {}


# ---------------------------------------------------------------- diagnostic

def jour_de_diffusion(spec, le):
    debut = date.fromisoformat(spec["budget"]["debut"])
    return (le - debut).days + 1


def budget_prevu_a_date(spec, jour):
    b = spec["budget"]
    if jour <= 0:
        return 0.0
    if b["type"] == "journalier":
        return b["montant_eur"] * jour
    debut, fin = date.fromisoformat(b["debut"]), date.fromisoformat(b["fin"])
    duree = (fin - debut).days + 1
    return b["montant_eur"] * min(jour, duree) / duree


def phase(jour, terminee):
    if terminee:
        return "terminee"
    if jour < 3:
        return "apprentissage"
    if jour < 7:
        return "lecture"
    return "decision"


def diagnostic(spec, lignes, le, prospects=None, reperes=None):
    """Le diagnostic complet, en données. `afficher_diagnostic` le met en mots."""
    reperes = reperes if reperes is not None else charger_reperes()
    pubs = [pub_depuis_ligne(l) for l in lignes]
    jour = jour_de_diffusion(spec, le)
    fin = date.fromisoformat(spec["budget"]["fin"]) if spec["budget"].get("fin") else None
    terminee = bool(fin and le > fin)
    ph = phase(jour, terminee)

    total = {k: sum(p[k] for p in pubs) for k in ("depense", "impressions", "clics", "resultats")}
    prevu = budget_prevu_a_date(spec, jour)
    rythme = total["depense"] / prevu if prevu else None

    for p in pubs:
        p["cpm"] = p["depense"] / p["impressions"] * 1000 if p["impressions"] else None
        p["ctr"] = p["clics"] / p["impressions"] if p["impressions"] else None
        p["ctr_ic"] = wilson(p["clics"], p["impressions"])
        p["taux_resultat"] = p["resultats"] / p["impressions"] if p["impressions"] else None
        p["cout_resultat"] = p["depense"] / p["resultats"] if p["resultats"] else None
        p["jugeable"] = p["impressions"] >= IMPRESSIONS_MIN

    comparaison = None
    jugeables = [p for p in pubs if p["jugeable"]]
    if len(jugeables) >= 2:
        cle = "resultats" if all(p["resultats"] for p in jugeables) else "clics"
        probas = proba_meilleure(jugeables, cle=cle)
        meilleure = max(range(len(jugeables)), key=lambda i: probas[i])
        comparaison = {
            "critere": "taux de résultat" if cle == "resultats" else "CTR",
            "probas": [(jugeables[i]["nom"], probas[i]) for i in range(len(jugeables))],
            "gagnante": jugeables[meilleure]["nom"] if probas[meilleure] >= SEUIL_PROBA else None,
        }

    rep = repere_pour(spec["client"], reperes)
    alertes, actions = [], []

    if rythme is not None and rythme > SURDEPENSE:
        alertes.append(f"dépense à {rythme:.0%} du prévu à date")
        actions.append("COUPER : la dépense dépasse le budget prévu (ads_update_entity status PAUSED, sans attendre)")
    if jour >= 2 and total["impressions"] == 0:
        alertes.append("aucune impression depuis le lancement")
        actions.append("CORRIGER : ads_get_errors et revue de la pub, la campagne ne diffuse pas")
    for p in pubs:
        if p["repetition"] > REPETITION_MAX:
            alertes.append(f"{p['nom']} : répétition {p['repetition']:.1f}, l'audience sature")
            actions.append(f"REMPLACER {p['nom']} : nouvelle pub dans le même ensemble, ou arrêt")
    ctr_min = rep.get("ctr_min")
    if ctr_min and ph in ("decision", "terminee"):
        for p in jugeables:
            if p["ctr_ic"][1] < ctr_min:
                alertes.append(f"{p['nom']} : CTR nettement sous le repère ({p['ctr_ic'][1]:.2%} au mieux, repère {ctr_min:.2%})")
                actions.append(f"REMPLACER {p['nom']} : le visuel ou la première ligne ne prend pas")

    cpl = None
    paliers = (spec.get("kpi") or {}).get("cout_par_lead_cible_eur") or {}
    if prospects is not None:
        cpl = total["depense"] / prospects if prospects else None

    if not actions:
        if ph == "apprentissage":
            actions.append("NE RIEN TOUCHER : phase d'apprentissage, aucune lecture avant J+3")
        elif ph == "lecture":
            actions.append("LIRE SANS DÉCIDER : premières tendances, décision à J+7")
        else:
            actions.append(verdict_final(cpl, prospects, paliers, comparaison, ph))

    return {
        "jour": jour, "phase": ph, "total": total, "prevu": prevu, "rythme": rythme,
        "pubs": pubs, "comparaison": comparaison, "repere": rep, "cpl": cpl,
        "prospects": prospects, "paliers": paliers, "alertes": alertes, "actions": actions,
    }


def verdict_final(cpl, prospects, paliers, comparaison, ph):
    gagnante = comparaison and comparaison["gagnante"]
    suffixe = f" ; garder « {gagnante} », couper les autres" if gagnante else ""
    if prospects is None:
        return ("DONNÉE MANQUANTE : relever à la main les prospects qualifiés (messages, DM, "
                "commentaires qui demandent une date ou un devis), puis relancer avec --prospects N" + suffixe)
    if prospects == 0:
        return ("COUPER" if ph == "decision" else "NE PAS REFAIRE") + \
            " : aucun prospect qualifié, changer d'angle ou de format avant de remettre du budget"
    bien, wow = paliers.get("bien"), paliers.get("wow")
    if wow and cpl <= wow:
        geste = "proposer +20 % de budget à Maxime (dans les plafonds du registre)" if ph == "decision" \
            else "refaire ce format à la prochaine campagne"
        return f"CONTINUER, palier wow ({cpl:.2f} € par prospect) : {geste}{suffixe}"
    if bien and cpl <= bien:
        return f"CONTINUER, palier bien ({cpl:.2f} € par prospect) : budget inchangé{suffixe}"
    return f"CONTINUER SOUS SURVEILLANCE, palier moyen ({cpl:.2f} € par prospect) : pas de hausse de budget{suffixe}"


# ---------------------------------------------------------------- affichage

def eur(x):
    return "n/d" if x is None else f"{x:.2f} €".replace(".", ",")


def pct(x):
    return "n/d" if x is None else f"{x * 100:.2f} %".replace(".", ",")


def afficher_diagnostic(spec, d):
    print(f"# Diagnostic · {spec['client']}/{spec['slug']} · J+{d['jour'] - 1} (jour {d['jour']}) · phase {d['phase']}")
    t = d["total"]
    print(f"Dépense {eur(t['depense'])} pour {eur(d['prevu'])} prévus à date"
          + (f" (rythme {d['rythme']:.0%})" if d["rythme"] is not None else ""))
    print(f"Impressions {int(t['impressions'])} · clics {int(t['clics'])} · résultats Meta {int(t['resultats'])}")
    print()
    print("| Pub | Dépense | Impr. | CPM | CTR (IC 95 %) | Coût / résultat | Répétition |")
    print("|---|---:|---:|---:|---|---:|---:|")
    for p in d["pubs"]:
        ic = f"{pct(p['ctr'])} ({pct(p['ctr_ic'][0])} à {pct(p['ctr_ic'][1])})" if p["ctr"] is not None else "n/d"
        if not p["jugeable"]:
            ic += ", trop tôt"
        print(f"| {p['nom']} | {eur(p['depense'])} | {int(p['impressions'])} | {eur(p['cpm'])} | {ic} "
              f"| {eur(p['cout_resultat'])} | {p['repetition']:.2f} |")
    if d["comparaison"]:
        c = d["comparaison"]
        print()
        print(f"Quelle pub est la meilleure ({c['critere']}) :")
        for nom, pr in c["probas"]:
            print(f"  - {nom} : {pr:.0%}")
        print(f"  → {'gagnante nette : ' + c['gagnante'] if c['gagnante'] else 'aucune gagnante nette, on laisse tourner'}")
    rep = d["repere"]
    print()
    if rep:
        print(f"Repère du compte : {rep.get('libelle', '')} (source : {rep.get('source', 'n/d')})")
    else:
        print("Repère du compte : aucun encore, la comparaison au secteur passe par ads_insights_industry_benchmark")
    if d["prospects"] is not None:
        print(f"Prospects qualifiés relevés : {d['prospects']} · coût par prospect {eur(d['cpl'])}"
              + (f" · paliers bien {eur(d['paliers'].get('bien'))}, wow {eur(d['paliers'].get('wow'))}" if d["paliers"] else ""))
    for a in d["alertes"]:
        print(f"⚠️  {a}")
    print()
    for a in d["actions"]:
        print(f"→ {a}")


def cmd_taille(args):
    n = taille_echantillon(args.taux, args.hausse)
    print(f"Pour voir un taux de {pct(args.taux)} passer à {pct(args.taux * (1 + args.hausse))} "
          f"(+{args.hausse:.0%}) avec 95 % de confiance et 80 % de chances de le détecter :")
    print(f"  {n} impressions par pub, {2 * n} pour un test à deux pubs")
    if args.cpm:
        print(f"  au CPM de {eur(args.cpm)} : {eur(2 * n * args.cpm / 1000)} de budget au total")
    print("Sous ce volume, un écart entre deux pubs reste du hasard : on ne tranche pas.")


def dernier_releve(client, slug, mois=None):
    dossier = RELEVES / client
    if not dossier.exists():
        return None
    candidats = sorted(dossier.glob(f"{slug}-*.json"))
    if mois:
        candidats = [c for c in candidats if c.stem[len(slug) + 1:].startswith(mois)] or candidats
    return candidats[-1] if candidats else None


def cmd_tableau(args):
    print(f"| Campagne | Objectif | Période | Dépense | Couverture | Résultats | Coût / résultat |")
    print("|---|---|---|---:|---:|---:|---:|")
    total = 0.0
    for chemin in sorted(CAMPAGNES.glob("*/*.json")):
        if chemin.parent.name == "etat":
            continue
        spec = json.loads(chemin.read_text(encoding="utf-8"))
        if spec.get("mois") != args.mois or "client" not in spec:
            continue
        releve = dernier_releve(spec["client"], spec["slug"], args.mois)
        if not releve:
            continue
        pubs = [pub_depuis_ligne(l) for l in lignes_du_releve(json.loads(releve.read_text(encoding="utf-8")))]
        dep = sum(p["depense"] for p in pubs)
        res = sum(p["resultats"] for p in pubs)
        cou = sum(p["couverture"] for p in pubs)
        total += dep
        b = spec["budget"]
        print(f"| {spec['client']} · {spec['titre']} | {spec['objectif']} | {b['debut']} → {b.get('fin', '')} "
              f"| {eur(dep)} | {int(cou)} | {int(res)} | {eur(dep / res if res else None)} |")
    print()
    print(f"Budget publicitaire payé à Meta sur le mois : {eur(total)} (hors prestation de gestion, à part)")


def cmd_diagnostic(args):
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    lignes = lignes_du_releve(json.loads(Path(args.releve).read_text(encoding="utf-8")))
    le = date.fromisoformat(args.le) if args.le else date.today()
    afficher_diagnostic(spec, diagnostic(spec, lignes, le, args.prospects))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("diagnostic", help="lit un relevé et dit quoi faire")
    p.add_argument("spec")
    p.add_argument("releve")
    p.add_argument("--prospects", type=int, default=None, help="prospects qualifiés relevés à la main")
    p.add_argument("--le", help="date de lecture AAAA-MM-JJ (par défaut aujourd'hui)")
    p = sub.add_parser("taille", help="budget nécessaire pour un test A/B concluant")
    p.add_argument("--taux", type=float, required=True, help="taux de référence, ex. 0.015 pour 1,5 %%")
    p.add_argument("--hausse", type=float, required=True, help="écart relatif à détecter, ex. 0.30")
    p.add_argument("--cpm", type=float, default=None, help="CPM attendu en euros")
    p = sub.add_parser("tableau", help="tableau mensuel du reporting")
    p.add_argument("mois")
    args = ap.parse_args(argv)
    {"diagnostic": cmd_diagnostic, "taille": cmd_taille, "tableau": cmd_tableau}[args.cmd](args)


if __name__ == "__main__":
    main()

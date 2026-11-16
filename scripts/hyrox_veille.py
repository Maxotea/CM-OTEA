#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Veille résultats HYROX : repère une course de Pierre, Antoine ou Julie et pose le post.

    python3 scripts/hyrox_veille.py                 # un passage (GitHub Actions, toutes les 20 min)
    python3 scripts/hyrox_veille.py --dry-run       # montrer, sans rien écrire ni publier
    python3 scripts/hyrox_veille.py --resultat LR3MS4JI5CA8BD --dry-run   # rejouer une course
    python3 scripts/hyrox_veille.py --initialiser   # marquer l'historique comme déjà vu

Demande de Maxime du 14/11/2026 : « repérer à chaque fois que Pierre, Julie ou Antoine font
une course, récupérer les stats, et anticiper un post dans l'heure avec une photo ».

Chaîne, pour chaque résultat jamais vu (hyrox/veille-etat.json) :
  1. HYRESULT : la fiche athlète liste les résultats ; la fiche résultat donne le chrono, le
     rang, le nombre de classés, la catégorie d'âge, la division et les splits.
  2. Le compte qui poste : celui du premier athlète du résultat qui en a un (hyrox/veille.json).
     Aucun compte : notification seule.
  3. Le visuel : scripts/hyrox_visuel.py, sur une vraie photo du stock du compte
     (photos/<compte>.json), en N&B + masque + glow. Jamais une image générée.
  4. Le post : Instagram, daté à maintenant + delai_minutes, en BROUILLON (règle n°1 du
     CLAUDE.md). `armer_auto: true` le passe en publication comme la relève validation_auto.
  5. La notification : NOTIF_WEBHOOK (Zapier → WhatsApp, SMS…) et une issue GitHub, avec le
     lien de l'image pour la transférer.

Aucun chiffre n'est inventé : tout ce qui est écrit vient de la fiche résultat. Un résultat
illisible (pas de chrono ou pas de rang) n'est jamais posté, il est signalé.

Secrets : METRICOOL_USER_ID, METRICOOL_TOKEN, IMGBB_API_KEY ; NOTIF_WEBHOOK, GITHUB_TOKEN.
"""
import argparse
import datetime as dt
import html
import io
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

CONFIG = ROOT / "hyrox" / "veille.json"
ETAT = ROOT / "hyrox" / "veille-etat.json"
SORTIES = ROOT / "hyrox" / "visuels"
SITE = "https://www.hyresult.com"
PARIS = ZoneInfo("Europe/Paris")
UA = {"User-Agent": "Mozilla/5.0 (compatible; otea-veille-hyrox)"}


# ---------------------------------------------------------------- lecture HYRESULT

def lire(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def resultats_athlete(slug):
    """Identifiants de résultat listés sur la fiche athlète, dans l'ordre de la page."""
    page = lire(f"{SITE}/athlete/{slug}")
    vus, ids = set(), []
    for rid in re.findall(r'href="/result/([A-Z0-9]+)"', page):
        if rid not in vus:
            vus.add(rid)
            ids.append(rid)
    return ids


def hms(s):
    s = int(s)
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def division_lisible(slug):
    """« pro-doubles-men » -> « Pro Doubles Men »."""
    mots = {"men": "Men", "women": "Women", "mixed": "Mixed", "pro": "Pro", "doubles": "Doubles",
            "team": "Team", "relay": "Relay", "adaptive": "Adaptive", "elite": "Elite"}
    return " ".join(mots.get(m, m.capitalize()) for m in slug.split("-"))


def lire_resultat(rid, page=None):
    page = page or lire(f"{SITE}/result/{rid}")
    t = page.replace('\\"', '"')
    m = re.search(r'"place":"([^"]+)","athletes":(\[[^\]]*\])', t)
    if not m:
        raise ValueError(f"{rid} : lieu et athlètes introuvables")
    lieu = html.unescape(m.group(1))                      # « Cairo 2026 »
    ville = re.sub(r"\s*\d{4}$", "", lieu).strip()
    athletes = [{"slug": s, "nom": html.unescape(n)}
                for s, n in re.findall(r'"slug":"([^"]+)","name":"([^"]+)"', m.group(2))]
    rang = re.search(r'/ranking/(s\d+-\d{4}-[a-z0-9-]+?-hyrox-([a-z-]+))"', page)
    division = division_lisible(rang.group(2)) if rang else None

    temps = {}
    for nom, sec, rg, nb in re.findall(
            r'"name":"([^"]+)","time":(\d+),"rank":(\d+),"num_idps":(\d+)', t):
        temps.setdefault(nom, (int(sec), int(rg), int(nb)))
    if "Total Time" not in temps:
        raise ValueError(f"{rid} : chrono absent (course en cours ou fiche incomplète)")
    total, classement, partants = temps["Total Time"]

    ag = re.search(r'"children":\["#",(\d+)\]\}\],"in AG"," ","([^"]+)"', t)
    stations = {n: v for n, v in temps.items()
                if n not in ("Total Time", "Runs", "Stations", "Roxzone") and not n.startswith("Run ")}
    return {
        "id": rid, "lieu": lieu, "ville": ville, "athletes": athletes, "division": division,
        "temps": hms(total), "secondes": total, "rang": classement, "partants": partants,
        "rang_ag": int(ag.group(1)) if ag else None, "ag": ag.group(2) if ag else None,
        "runs": hms(temps["Runs"][0]) if "Runs" in temps else None,
        "roxzone": hms(temps["Roxzone"][0]) if "Roxzone" in temps else None,
        "stations": {n: [hms(v[0]), v[1]] for n, v in stations.items()},
        "source": f"{SITE}/result/{rid}",
    }


# ---------------------------------------------------------------- textes

def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def partenaires(res, config, titulaire):
    """Les autres athlètes du résultat, avec leur @ à la première mention s'il est connu."""
    connus = {a["slug"]: a for a in config["athletes"]}
    out = []
    for a in res["athletes"]:
        if a["slug"] == titulaire:
            continue
        c = connus.get(a["slug"], {})
        out.append({"prenom": c.get("prenom") or a["nom"].split()[0],
                    "tag": c.get("instagram") or a["nom"]})
    return out


def textes(res, config, compte_cfg):
    """(spec du visuel, légende). Ne dit que ce que la fiche résultat dit."""
    titulaire = compte_cfg["athlete"]
    autres = partenaires(res, config, titulaire)
    ville, div = res["ville"], res["division"] or "HYROX"
    meilleure = min(res["stations"].items(), key=lambda kv: kv[1][1]) if res["stations"] else None

    if res["rang_ag"] == 1:
        titre = ["Age group", "winner."]
    elif res["rang_ag"] and res["rang_ag"] <= 3:
        titre = ["On the podium", f"in {res['ag']}."]
    elif autres:
        titre = ["Two engines,", "one finish line."] if len(autres) == 1 else ["One team,", "one finish line."]
    else:
        titre = ["Every race,", "a step closer."]

    stats = [[ordinal(res["rang"]), f" / {res['partants']}"]]
    if res["rang_ag"]:
        stats.append([ordinal(res["rang_ag"]), f" AG {res['ag']}"])
    spec = {"label": f"HYROX {ville.upper()} · {div.upper()}", "titre": titre,
            "chrono": res["temps"], "stats": stats, "facette": "ATHLETE",
            "pied": compte_cfg.get("pied", "ROAD TO HONG KONG · JUNE 2027")}

    avec = ""
    if autres:
        noms = [p["tag"] for p in autres]
        avec = " with " + (noms[0] if len(noms) == 1 else ", ".join(noms[:-1]) + " and " + noms[-1])
    lignes = [f"HYROX {ville}, {div}{avec}.", ""]
    ligne = f"{res['temps']}. {ordinal(res['rang'])} out of {res['partants']}"
    if res["rang_ag"]:
        ligne += f", {ordinal(res['rang_ag'])} in the {res['ag']} age group"
    lignes += [ligne + ".", ""]
    if meilleure:
        rg = meilleure[1][1]
        place = "fastest in the field" if rg == 1 else f"{ordinal(rg)} fastest in the field"
        lignes += [f"Best station of the day: {meilleure[0]}, {meilleure[1][0]} ({place}).", ""]
    lignes += ["Every race teaches me where the next minutes are hiding. "
               "One more step on the road to Hong Kong.", ""]
    merci = "Thank you for the support, always ❤️"
    if autres:
        merci = f"Thank you {' and '.join(p['prenom'] for p in autres)}, and thank you all for the support ❤️"
    lignes += [merci + " I read everything 🙏", ""]
    tags = compte_cfg.get("hashtags", ["#hyrox"]) + [f"#hyrox{re.sub(r'[^a-z]', '', ville.lower())}"]
    lignes.append(" ".join(dict.fromkeys(tags)))
    legende = "\n".join(lignes)
    if "—" in legende:                                   # règle « rédaction sans tirets »
        legende = legende.replace("—", ",")
    return spec, legende


# ---------------------------------------------------------------- planification

def creneau(maintenant, delai, plage):
    """maintenant + délai, arrondi au quart d'heure suivant, ramené dans la plage du compte."""
    t = maintenant.astimezone(PARIS) + dt.timedelta(minutes=delai)
    t = t.replace(second=0, microsecond=0)
    t += dt.timedelta(minutes=(-t.minute) % 15)
    debut = dt.time.fromisoformat(plage[0])
    fin = dt.time.fromisoformat(plage[1])
    if t.time() > fin:
        t = (t + dt.timedelta(days=1)).replace(hour=debut.hour, minute=debut.minute)
    elif t.time() < debut:
        t = t.replace(hour=debut.hour, minute=debut.minute)
    return t


def choisir_photo(compte, etat):
    stock = json.loads((ROOT / compte["photos"]).read_text(encoding="utf-8"))["photos"]
    n = etat.setdefault("rotation", {}).get(compte["athlete"], 0)
    etat["rotation"][compte["athlete"]] = n + 1
    return stock[n % len(stock)]


def rendre(res, spec, photo):
    from PIL import Image
    import hyrox_visuel
    with urllib.request.urlopen(urllib.request.Request(photo["url"], headers=UA), timeout=120) as r:
        img = Image.open(io.BytesIO(r.read()))
        img.load()
    masque = Image.open(ROOT / photo["masque"]) if photo.get("masque") else None
    SORTIES.mkdir(parents=True, exist_ok=True)
    sortie = SORTIES / f"{res['id']}.jpg"
    hyrox_visuel.composer(img, spec, masque, photo.get("decalage", 0.12)).save(
        sortie, quality=93, subsampling=0)
    return sortie


def poster(compte, sortie, legende, quand):
    from publier import heberger, metricool, normaliser
    url = normaliser(heberger([sortie])[0])
    date_time = quand.strftime("%Y-%m-%dT%H:%M:%S")
    corps = {"text": legende,
             "publicationDate": {"dateTime": date_time, "timezone": "Europe/Paris"},
             "draft": True, "autoPublish": False, "media": [url],
             "providers": [{"network": "instagram"}],
             "instagramData": {"type": "POST", "isAiGenerated": False}}
    cree = metricool("/scheduler/posts", "POST", corps, blogId=compte["blog_id"]).get("data", {})
    if cree.get("draft") is not True and not compte.get("armer_auto"):
        raise RuntimeError(f"post {cree.get('id')} créé hors brouillon : à vérifier tout de suite")
    statut = "brouillon"
    if compte.get("armer_auto"):
        from review import passer_en_publication
        statut, _ = passer_en_publication(compte["blog_id"], cree, legende, date_time)
    return {"id": cree.get("id"), "uuid": cree.get("uuid"), "image": url, "date": date_time,
            "statut": statut}


# ---------------------------------------------------------------- notification

def notifier(titre, detail, lien=None, image=None, dry_run=False):
    print(f"🔔 {titre}\n   {detail}")
    if dry_run:
        return
    from notifier import _poster
    webhook = os.environ.get("NOTIF_WEBHOOK")
    if webhook:
        _poster(webhook, {"source": "veille-hyrox", "titre": titre, "detail": detail,
                          "lien": lien, "image": image}, {})
    jeton, depot = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if jeton and depot:
        corps = detail + (f"\n\n![visuel]({image})\n\n[Image]({image})" if image else "") + \
            (f"\n\n[Ouvrir dans Metricool]({lien})" if lien else "")
        _poster(f"https://api.github.com/repos/{depot}/issues",
                {"title": f"🏁 {titre}", "body": corps, "labels": ["veille-hyrox"]},
                {"Authorization": f"Bearer {jeton}", "Accept": "application/vnd.github+json"})


# ---------------------------------------------------------------- passage

def traiter(res, config, etat, dry_run, maintenant):
    compte_cle = next((a["compte"] for a in config["athletes"]
                       if a["compte"] and a["slug"] in {x["slug"] for x in res["athletes"]}), None)
    qui = ", ".join(a["nom"] for a in res["athletes"])
    resume = (f"{qui} : HYROX {res['ville']}, {res['division']}. {res['temps']}, "
              f"{ordinal(res['rang'])}/{res['partants']}"
              + (f", {ordinal(res['rang_ag'])} en {res['ag']}" if res["rang_ag"] else "")
              + f". Source : {res['source']}")
    if not compte_cle:
        notifier(f"Course détectée : {qui} à {res['ville']}",
                 resume + "\nAucun compte Metricool rattaché : pas de post créé.", dry_run=dry_run)
        return {"statut": "notifie"}

    compte = config["comptes"][compte_cle]
    spec, legende = textes(res, config, compte)
    photo = choisir_photo(compte, etat)
    sortie = rendre(res, spec, photo)
    quand = creneau(maintenant, config.get("delai_minutes", 60), compte["plage"])
    print(f"→ {res['id']} {qui} {res['ville']} : visuel {sortie.relative_to(ROOT)} "
          f"(photo {photo['cle']}), post {quand:%d/%m %H:%M}\n{legende}\n")
    if dry_run:
        return {"statut": "dry-run"}
    post = poster(compte, sortie, legende, quand)
    lien = (f"https://app.metricool.com/planner/calendar?blogId={compte['blog_id']}"
            f"&openWithPostUuid={post['uuid']}")
    notifier(f"Post résultat prêt : {qui} à {res['ville']}",
             resume + f"\nPost Instagram {post['statut']} pour le {quand:%d/%m à %H:%M} "
             f"(photo d'attente {photo['cle']}, à remplacer par une photo de la course).",
             lien, post["image"])
    return {"statut": post["statut"], "post": post, "photo": photo["cle"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--initialiser", action="store_true",
                    help="marquer tous les résultats actuels comme vus, sans rien poster")
    ap.add_argument("--resultat", help="traiter ce résultat même s'il est déjà vu")
    a = ap.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    etat = json.loads(ETAT.read_text(encoding="utf-8")) if ETAT.exists() else {"vus": {}}
    maintenant = dt.datetime.now(dt.timezone.utc)

    if a.resultat:
        nouveaux = [a.resultat]
    else:
        nouveaux = []
        for ath in config["athletes"]:
            try:
                ids = resultats_athlete(ath["slug"])
            except Exception as exc:                       # un site lent ne bloque pas les autres
                print(f"! {ath['slug']} : fiche illisible ({exc})", file=sys.stderr)
                continue
            for rid in ids:
                if rid not in etat["vus"] and rid not in nouveaux:
                    nouveaux.append(rid)
        if a.initialiser or not etat.get("initialise"):
            for rid in nouveaux:
                etat["vus"][rid] = {"statut": "historique", "vu_le": maintenant.isoformat()[:16]}
            etat["initialise"] = True
            print(f"Initialisation : {len(nouveaux)} résultat(s) d'historique marqués vus, rien posté.")
            if not a.dry_run:
                ETAT.write_text(json.dumps(etat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return 0

    if not nouveaux:
        print("Aucune nouvelle course.")
        return 0
    erreurs = 0
    for rid in nouveaux:
        try:
            res = lire_resultat(rid)
        except ValueError as exc:
            # Fiche incomplète : on réessaiera au passage suivant, sans la marquer vue.
            print(f"… {exc}")
            continue
        try:
            sortie = traiter(res, config, etat, a.dry_run, maintenant)
        except Exception as exc:
            erreurs += 1
            print(f"✗ {rid} : {exc}", file=sys.stderr)
            sortie = {"statut": "erreur", "erreur": str(exc)[:300]}
            # Réessayé aux passages suivants ; signalé une fois, abandonné au 3e échec
            # pour ne pas notifier toutes les 20 minutes.
            echecs = etat.setdefault("echecs", {})
            echecs[rid] = echecs.get(rid, 0) + 1
            if echecs[rid] == 1:
                try:
                    notifier(f"Veille HYROX : échec sur {rid}", f"{exc}\n{SITE}/result/{rid}",
                             dry_run=a.dry_run)
                except Exception:
                    pass
            if echecs[rid] >= 3:
                sortie["statut"] = "abandon"
        if not a.dry_run and sortie["statut"] != "erreur":
            etat["vus"][rid] = {**sortie, "vu_le": maintenant.isoformat()[:16],
                                "resultat": {k: res[k] for k in
                                             ("lieu", "division", "temps", "rang", "partants",
                                              "rang_ag", "ag")},
                                "athletes": [x["slug"] for x in res["athletes"]]}
    if not a.dry_run:
        ETAT.write_text(json.dumps(etat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())

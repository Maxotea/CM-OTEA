#!/usr/bin/env python3
"""Publie les carrousels de la semaine dans Metricool, en brouillon.

    python3 scripts/publier.py --semaine 2026-08-12
    python3 scripts/publier.py --semaine 2026-08-12 --dry-run

Conçu pour tourner dans GitHub Actions, pas dans une session Claude : la politique
réseau des sessions distantes bloque app.metricool.com et les hébergeurs d'images, un
runner Actions ne les bloque pas.

Attaque l'API Metricool en direct plutôt que de passer par Zapier. Deux conséquences
qui justifient à elles seules le détour :
  - pas de décalage horaire (le bug +7h est un artefact de l'intégration Zapier),
    donc plus de bulk_update_post_times ni de bulk_set_draft derrière ;
  - pas de rate limit à ~6 créations, donc plus de vagues avec pauses de 90 s.

Secrets attendus dans l'environnement :
  METRICOOL_USER_ID, METRICOOL_TOKEN   (Metricool, plan Advanced minimum)
  IMGBB_API_KEY                        (hébergement des slides, gratuit)
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://app.metricool.com/api/v2"
NORMALIZE = "https://app.metricool.com/api/actions/normalize/image/url"

BLOG_IDS = {
    "le-loft": 6191921,
    "gossip-beauty-center": 5733306,
    "jlawsongolf": 6563137,
    "la-galerie-immobiliere": 5733302,
    "otea-production": 5733269,
    "pierre-huiban": 6572293,
}


def _req(url, method="GET", body=None, headers=None):
    """Appel HTTP. Retourne un objet si la réponse est du JSON, la chaîne brute sinon.

    Tous les endpoints Metricool ne répondent pas en JSON : `normalize/image/url` renvoie
    l'URL en texte brut. Exiger du JSON partout fait échouer la planification sur un
    « Expecting value » incompréhensible.

    Sur erreur HTTP, le corps de la réponse est remonté dans le message : sans lui, un 4xx
    de Metricool ne dit rien et coûte un run entier pour être diagnostiqué.
    """
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode().strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:400]
        raise RuntimeError(f"HTTP {exc.code} sur {url.split('?')[0]} — {detail}") from None
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def metricool(path, method="GET", body=None, **query):
    """Appel API Metricool. Le token va dans X-Mc-Auth — surtout pas en Bearer, c'est un 401."""
    query = {"userId": os.environ["METRICOOL_USER_ID"], **query}
    url = f"{API}{path}?{urllib.parse.urlencode(query)}"
    return _req(url, method, body, {"X-Mc-Auth": os.environ["METRICOOL_TOKEN"]})


def heberger(chemins):
    """Rend chaque slide accessible par une URL publique. Retourne les URLs, dans l'ordre.

    Metricool exige une URL publique **qui n'expire pas** : une URL signée ou temporaire est
    ignorée silencieusement. D'où le passage par un hébergeur d'images plutôt que par un lien
    présigné. En pratique l'URL ne sert qu'une fois, `normaliser` ci-dessous faisant recopier
    le fichier sur le CDN de Metricool.

    Implémentation : imgbb, gratuit, une clé suffit (https://api.imgbb.com/). C'est le seul
    point de contact avec l'hébergeur — pour basculer sur un bucket S3/R2 ou un dépôt public,
    seule cette fonction change.
    """
    key = os.environ["IMGBB_API_KEY"]
    urls = []
    for p in chemins:
        corps = urllib.parse.urlencode({
            "key": key,
            "name": p.stem,
            "image": base64.b64encode(p.read_bytes()).decode(),
        }).encode()
        req = urllib.request.Request(
            "https://api.imgbb.com/1/upload", data=corps, method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req, timeout=120) as r:
            rep = json.loads(r.read().decode())
        if not rep.get("success"):
            raise RuntimeError(f"hébergement de {p.name} refusé : {rep}")
        urls.append(rep["data"]["url"])
    return urls


def normaliser(url):
    """Fait recopier le média par Metricool sur son CDN, et retourne l'URL à utiliser.

    La forme exacte de la réponse n'est pas documentée : on accepte une chaîne nue comme un
    objet, et on retombe sur l'URL d'origine plutôt que de glisser un dict dans `media`, ce
    qui produirait un post accepté mais sans image.
    """
    rep = _req(f"{NORMALIZE}?{urllib.parse.urlencode({'url': url})}",
               headers={"X-Mc-Auth": os.environ["METRICOOL_TOKEN"]})
    if isinstance(rep, str):
        return rep
    if isinstance(rep, dict):
        for cle in ("data", "url", "result"):
            val = rep.get(cle)
            if isinstance(val, str) and val.startswith("http"):
                return val
            if isinstance(val, dict) and isinstance(val.get("url"), str):
                return val["url"]
    return url


def poste_du_jour(blog_id, date_iso):
    """Le post feed simple déjà planifié ce jour-là — celui que le carrousel remplace.

    Ne retient QUE le type POST. Un REEL coûte un tournage et un montage : il ne se
    remplace pas par un carrousel généré, et une story ne consomme pas le quota feed.
    Ne retient que les brouillons non validés : ce que le client a validé lui appartient.
    """
    jour = date_iso[:10]
    posts = metricool("/scheduler/posts", blogId=blog_id,
                      start=f"{jour}T00:00:00", end=f"{jour}T23:59:59").get("data", [])
    return [p for p in posts
            if p.get("instagramData", {}).get("type") == "POST"
            and p.get("providers", [{}])[0].get("status") == "PENDING"
            and p.get("draft") is True
            and p.get("autoPublish") is False]


def publier(spec_path, dry_run=False):
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    client, slug = spec["client"], spec["slug"]
    blog_id = BLOG_IDS[client]
    dossier = ROOT / "medias" / client / "carrousels" / slug
    manifest = json.loads((dossier / "manifest.json").read_text(encoding="utf-8"))
    slides = [dossier / f for f in manifest["slides_in_order"]]
    legende = (dossier / "caption.txt").read_text(encoding="utf-8").strip()

    manquantes = [p.name for p in slides if not p.exists()]
    if manquantes:
        raise SystemExit(f"{slug} : slides absentes {manquantes} — lancer scripts/carrousel.py d'abord")

    remplaces = poste_du_jour(blog_id, spec["date_time"])
    if dry_run:
        print(f"[dry-run] {client} {spec['date_time']} — {len(slides)} slides, "
              f"réseaux {'+'.join(manifest['networks'])}, "
              f"{len(remplaces)} post(s) feed à remplacer")
        for p in remplaces:
            print(f"           └ supprimerait {p['id']} : {p.get('text', '')[:60]}…")
        return

    urls = [normaliser(u) for u in heberger(slides)]

    corps = {
        "text": legende,
        "publicationDate": {"dateTime": spec["date_time"], "timezone": "Europe/Paris"},
        "draft": True,
        "autoPublish": False,
        "media": urls,
        "providers": [{"network": n} for n in manifest["networks"]],
    }
    cree = metricool("/scheduler/posts", "POST", corps, blogId=blog_id)
    post_id = cree.get("data", {}).get("id")

    # Ne supprimer l'ancien post qu'une fois le carrousel confirmé créé : en cas d'échec,
    # mieux vaut un doublon visible qu'un mercredi vide.
    for p in remplaces:
        metricool(f"/scheduler/posts/{p['id']}", "DELETE", blogId=blog_id)

    print(f"✓ {client} {spec['date_time']} — carrousel {post_id}, {len(slides)} slides, "
          f"{len(remplaces)} post(s) remplacé(s)")
    return post_id


def main():
    ap = argparse.ArgumentParser(description="Publie les carrousels d'une semaine.")
    ap.add_argument("--semaine", required=True,
                    help="date du mercredi (YYYY-MM-DD). Un préfixe vaut lot : 2026-08 traite "
                         "tous les mercredis d'août")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--client", help="ne traiter qu'un compte, ex. le-loft. "
                                     "À utiliser pour le premier run réel : on vérifie sur un "
                                     "compte avant d'écrire sur les six.")
    args = ap.parse_args()

    requis = ["METRICOOL_USER_ID", "METRICOOL_TOKEN"] + ([] if args.dry_run else ["IMGBB_API_KEY"])
    absents = [v for v in requis if not os.environ.get(v)]
    if absents:
        raise SystemExit(f"secrets manquants : {', '.join(absents)}")

    motif = f"{args.client or '*'}/{args.semaine}-*.json"
    specs = sorted((ROOT / "carrousels").glob(motif))
    if not specs:
        raise SystemExit(f"aucun carrousel pour {motif}")

    echecs = 0
    for s in specs:
        try:
            publier(s, args.dry_run)
        except Exception as exc:
            echecs += 1
            print(f"✗ {s.name} : {exc}", file=sys.stderr)
        time.sleep(1)

    verbe = "vérifiés (rien n'a été écrit)" if args.dry_run else "publiés en brouillon"
    print(f"\n{len(specs) - echecs}/{len(specs)} carrousels {verbe}.")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())

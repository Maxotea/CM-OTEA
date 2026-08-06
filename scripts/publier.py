#!/usr/bin/env python3
"""Publie les carrousels de la semaine dans Metricool, en brouillon.

    python3 scripts/publier.py --semaine 2026-08-12
    python3 scripts/publier.py --semaine 2026-08-12 --dry-run

Conçu pour tourner dans GitHub Actions, pas dans une session Claude : la politique
réseau des sessions distantes bloque app.metricool.com et upload.higgsfield.ai, un
runner Actions ne les bloque pas.

Attaque l'API Metricool en direct plutôt que de passer par Zapier. Deux conséquences
qui justifient à elles seules le détour :
  - pas de décalage horaire (le bug +7h est un artefact de l'intégration Zapier),
    donc plus de bulk_update_post_times ni de bulk_set_draft derrière ;
  - pas de rate limit à ~6 créations, donc plus de vagues avec pauses de 90 s.

Secrets attendus dans l'environnement :
  METRICOOL_USER_ID, METRICOOL_TOKEN   (Metricool, plan Advanced minimum)
  HIGGSFIELD_API_KEY                   (hébergement des slides)
"""

import argparse
import json
import os
import sys
import time
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
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode()
    return json.loads(raw) if raw.strip() else {}


def metricool(path, method="GET", body=None, **query):
    """Appel API Metricool. Le token va dans X-Mc-Auth — surtout pas en Bearer, c'est un 401."""
    query = {"userId": os.environ["METRICOOL_USER_ID"], **query}
    url = f"{API}{path}?{urllib.parse.urlencode(query)}"
    return _req(url, method, body, {"X-Mc-Auth": os.environ["METRICOOL_TOKEN"]})


def heberger(chemins):
    """Rend chaque slide accessible par une URL publique. Retourne les URLs, dans l'ordre.

    Passe par Higgsfield, déjà utilisé pour les stories : presigned PUT puis confirmation.
    L'URL n'a besoin de vivre que jusqu'à l'appel de `normaliser` ci-dessous, Metricool
    recopiant ensuite le média sur son propre CDN.

    ⚠️ Les deux chemins REST ci-dessous n'ont pas pu être vérifiés depuis la session qui a
    écrit ce fichier (upload.higgsfield.ai y est bloqué par la politique réseau). À valider
    au premier run de l'action, ou à remplacer par un bucket S3/R2 : seule cette fonction
    change, elle est le seul point de contact avec l'hébergeur.
    """
    key = os.environ["HIGGSFIELD_API_KEY"]
    auth = {"Authorization": f"Bearer {key}"}
    payload = {"files": [{"filename": p.name, "content_type": "image/png"} for p in chemins]}
    uploads = _req("https://api.higgsfield.ai/v1/media/upload", "POST", payload, auth)["uploads"]

    for p, up in zip(chemins, uploads):
        req = urllib.request.Request(up["upload_url"], data=p.read_bytes(),
                                     method="PUT", headers={"Content-Type": "image/png"})
        urllib.request.urlopen(req, timeout=120).read()

    _req("https://api.higgsfield.ai/v1/media/confirm", "POST",
         {"type": "image", "media_ids": [u["media_id"] for u in uploads]}, auth)
    return [u["url"] for u in uploads]


def normaliser(url):
    """Fait recopier le média par Metricool sur son CDN. C'est ce qui rend l'hébergement jetable."""
    return _req(f"{NORMALIZE}?{urllib.parse.urlencode({'url': url})}",
                headers={"X-Mc-Auth": os.environ["METRICOOL_TOKEN"]})


def poste_du_jour(blog_id, date_iso):
    """Le post feed déjà planifié ce jour-là — celui que le carrousel remplace."""
    jour = date_iso[:10]
    posts = metricool("/scheduler/posts", blogId=blog_id,
                      start=f"{jour}T00:00:00", end=f"{jour}T23:59:59").get("data", [])
    return [p for p in posts
            if p.get("instagramData", {}).get("type") != "STORY"
            and p.get("providers", [{}])[0].get("status") == "PENDING"
            and p.get("draft") is True]


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
              f"{len(remplaces)} post(s) feed à remplacer")
        return

    urls = [normaliser(u).get("data", u) for u in heberger(slides)]

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
                    help="date du mercredi, format YYYY-MM-DD (les specs sont nommées ainsi)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    requis = ["METRICOOL_USER_ID", "METRICOOL_TOKEN"] + ([] if args.dry_run else ["HIGGSFIELD_API_KEY"])
    absents = [v for v in requis if not os.environ.get(v)]
    if absents:
        raise SystemExit(f"secrets manquants : {', '.join(absents)}")

    specs = sorted((ROOT / "carrousels").glob(f"*/{args.semaine}-*.json"))
    if not specs:
        raise SystemExit(f"aucun carrousel pour le {args.semaine}")

    echecs = 0
    for s in specs:
        try:
            publier(s, args.dry_run)
        except Exception as exc:
            echecs += 1
            print(f"✗ {s.name} : {exc}", file=sys.stderr)
        time.sleep(1)

    print(f"\n{len(specs) - echecs}/{len(specs)} carrousels publiés en brouillon.")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())

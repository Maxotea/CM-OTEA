#!/usr/bin/env python3
"""Ingère les vraies photos d'un client depuis Google Drive et les héberge pour Metricool.

    python3 scripts/photos.py gossip-beauty-center
    python3 scripts/photos.py gossip-beauty-center --dry-run

Pourquoi ce détour plutôt qu'un lien Drive donné directement à Metricool : Metricool exige
une URL publique **et stable**, et les liens de téléchargement Drive renvoient parfois une page
HTML d'interstitiel au lieu du fichier. On télécharge donc une fois depuis Drive, on héberge
sur un hôte prévisible, et c'est cette URL-là qui part dans le post.

Le Drive reste la source : Maxime y dépose les photos, ce script les récupère. Il ne renomme
rien et ne modifie rien côté Drive.

Prérequis côté Drive : le dossier doit être partagé **« Tous les utilisateurs disposant du
lien — Lecteur »**. Sans ça le téléchargement renvoie une page de connexion, et le script le
dit explicitement au lieu d'héberger un fichier HTML de 2 ko.

Comme scripts/publier.py, conçu pour GitHub Actions : les sessions Claude distantes n'ont accès
ni à Drive ni aux hébergeurs d'images.
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publier import heberger  # noqa: E402  — même hébergeur que les carrousels

ROOT = Path(__file__).resolve().parent.parent
DRIVE = "https://drive.google.com/uc?export=download&id={}"


def telecharger(file_id, destination):
    """Récupère un fichier Drive partagé par lien. Vérifie que c'est bien une image."""
    req = urllib.request.Request(DRIVE.format(file_id),
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        octets = r.read()
        ctype = r.headers.get("Content-Type", "")
    if not ctype.startswith("image/"):
        raise RuntimeError(
            f"Drive a renvoyé « {ctype} » et non une image — le dossier n'est probablement pas "
            f"partagé « Tous les utilisateurs disposant du lien ». Fichier {file_id}.")
    destination.write_bytes(octets)
    return len(octets)


def main():
    ap = argparse.ArgumentParser(description="Ingère les photos Drive d'un client.")
    ap.add_argument("client")
    ap.add_argument("--dry-run", action="store_true",
                    help="télécharge et vérifie, sans héberger")
    args = ap.parse_args()

    manifeste = ROOT / "photos" / f"{args.client}.json"
    if not manifeste.exists():
        raise SystemExit(f"manifeste absent : {manifeste.relative_to(ROOT)}")
    spec = json.loads(manifeste.read_text(encoding="utf-8"))

    dossier = ROOT / "medias" / args.client / "photos"
    dossier.mkdir(parents=True, exist_ok=True)

    chemins, echecs = [], 0
    for photo in spec["photos"]:
        cible = dossier / f"{photo['nom']}.jpg"
        try:
            poids = telecharger(photo["drive_id"], cible)
        except Exception as exc:
            echecs += 1
            print(f"✗ {photo['nom']} : {exc}", file=sys.stderr)
            continue
        chemins.append((photo, cible))
        print(f"✓ {photo['nom']} — {poids // 1024} Ko · {photo['sujet']}")

    if echecs:
        raise SystemExit(f"\n{echecs} photo(s) non récupérée(s) — rien n'a été hébergé.")
    if args.dry_run:
        print(f"\n[dry-run] {len(chemins)} photos récupérées, aucune hébergée.")
        return 0

    urls = heberger([c for _, c in chemins])
    for (photo, _), url in zip(chemins, urls):
        photo["url"] = url
    manifeste.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n{len(urls)} photos hébergées, URLs écrites dans {manifeste.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Récupère les médias déposés par un client dans son dossier Drive partagé.

    python3 scripts/drive_sync.py gossip-beauty-center
    python3 scripts/drive_sync.py --tous --dry-run

Le travail est coupé en deux, et c'est ce qui rend la chaîne gratuite :

  1. REPÉRAGE — Claude liste le dossier Drive du client via le connecteur Drive déjà connecté,
     et ajoute les nouveaux fichiers au manifeste `photos/<client>.json` (drive_id + nom).
     Aucune clé d'API Google n'est nécessaire : le connecteur est authentifié.

  2. RÉCUPÉRATION — ce script, dans GitHub Actions. Il télécharge chaque entrée non traitée
     par le lien public du fichier, la dédoublonne, l'héberge, et complète le manifeste.
     Là non plus, aucune clé Google : un dossier partagé « tous ceux qui ont le lien » se
     télécharge sans authentification.

Sens unique, Drive → dépôt. Le script ne crée, ne renomme et ne supprime jamais rien côté
Drive : c'est la boîte du client, pas la nôtre.

Déduplication par empreinte du contenu, jamais par nom. Un même fichier déposé deux fois — ce
qui arrive constamment quand on envoie depuis un téléphone — n'entre qu'une fois. C'est
exactement ce qui nous a fait cataloguer deux fois la même photo sous deux sujets différents.

Secret attendu : IMGBB_API_KEY, le même que pour les slides.
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publier import heberger  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "photos"
LIEN = "https://drive.google.com/uc?export=download&id={}"

EXTENSIONS = {"image/jpeg": "jpg", "image/png": "png", "image/heic": "heic",
              "video/mp4": "mp4", "video/quicktime": "mov"}


def telecharger(drive_id):
    """Récupère un fichier d'un dossier Drive partagé par lien. Aucune authentification."""
    req = urllib.request.Request(LIEN.format(drive_id), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        octets = r.read()
        ctype = r.headers.get("Content-Type", "").split(";")[0]
    if ctype not in EXTENSIONS:
        raise RuntimeError(
            f"Drive a renvoyé « {ctype or 'rien' } » et non un média — le dossier n'est "
            f"probablement plus partagé « tous ceux qui ont le lien ».")
    return octets, EXTENSIONS[ctype]


def _nom(m):
    """Le nom à afficher pour un média, sans supposer qu'un champ existe."""
    return m.get("drive_nom") or m.get("drive_id") or m.get("cle") or "?"


def synchroniser(client, dry_run=False):
    manifeste = PHOTOS / f"{client}.json"
    spec = json.loads(manifeste.read_text(encoding="utf-8"))
    medias = spec.get("photos") if isinstance(spec, dict) else None
    if not isinstance(medias, list):
        # Un fichier de photos/ qui n'est pas un manifeste de dépôt (une note de banque, par
        # exemple) n'a rien à récupérer : on le saute au lieu de faire tomber tout le job.
        print(f"{client} : pas de liste « photos », rien à récupérer")
        return 0

    connus = {m["empreinte"]: m for m in medias if m.get("empreinte")}
    sans_empreinte = [m for m in medias if not m.get("empreinte")]
    # Seul un média déposé dans le Drive porte un drive_id. Une photo hébergée ailleurs (banque
    # cloudfront, image générée) n'a rien à télécharger ici : elle ne doit pas planter le job.
    a_traiter = [m for m in sans_empreinte if m.get("drive_id")]
    hors_drive = len(sans_empreinte) - len(a_traiter)
    if hors_drive:
        print(f"{client} : {hors_drive} média(s) sans drive_id ni empreinte, ignoré(s)")
    if not a_traiter:
        print(f"{client} : rien de nouveau ({len(connus)} média(s) déjà récupéré(s))")
        return 0

    cible = ROOT / "medias" / client / "photos"
    cible.mkdir(parents=True, exist_ok=True)

    prets, doublons, echecs = [], [], 0
    for m in a_traiter:
        try:
            octets, ext = telecharger(m["drive_id"])
        except Exception as exc:
            echecs += 1
            print(f"  ✗ {_nom(m)} : {exc}", file=sys.stderr)
            continue
        empreinte = hashlib.sha256(octets).hexdigest()[:16]
        if empreinte in connus:
            doublons.append((m, connus[empreinte]))
            continue
        chemin = cible / f"{empreinte}.{ext}"
        chemin.write_bytes(octets)
        m.update(empreinte=empreinte, type=ext)
        connus[empreinte] = m
        prets.append((m, chemin))
        print(f"  + {_nom(m)} → {empreinte}.{ext} "
              f"({len(octets) // 1024} Ko)")

    for m, deja in doublons:
        print(f"  = {_nom(m)} — contenu identique à "
              f"« {deja.get('drive_nom') or deja['empreinte']} », écarté")
    # Un doublon n'a pas à encombrer le manifeste : on le retire plutôt que de le garder vide.
    spec["photos"] = [m for m in medias if m not in [d for d, _ in doublons]]

    if echecs:
        raise SystemExit(f"{client} : {echecs} échec(s) — manifeste non modifié.")
    if dry_run:
        print(f"[dry-run] {client} : {len(prets)} nouveau(x), {len(doublons)} doublon(s). "
              f"Rien n'a été hébergé ni écrit.")
        return len(prets)

    images = [(m, c) for m, c in prets if m["type"] in ("jpg", "png")]
    if images:
        for m, url in zip((m for m, _ in images), heberger([c for _, c in images])):
            m["url"] = url
    manifeste.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  → {len(images)} image(s) hébergée(s), manifeste à jour")
    if any(m.get("sujet") is None for m in spec["photos"]):
        print("  ⚠ des médias n'ont ni sujet ni pilier : à qualifier avant tout usage")
    return len(prets)


def main():
    ap = argparse.ArgumentParser(description="Récupère les médias déposés dans le Drive.")
    ap.add_argument("client", nargs="?")
    ap.add_argument("--tous", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.dry_run and not os.environ.get("IMGBB_API_KEY"):
        raise SystemExit("secret manquant : IMGBB_API_KEY")

    clients = ([p.stem for p in sorted(PHOTOS.glob("*.json"))] if args.tous
               else ([args.client] if args.client else []))
    if not clients:
        raise SystemExit("préciser un client ou --tous")

    total = sum(synchroniser(c, args.dry_run) for c in clients)
    verbe = "à récupérer" if args.dry_run else "récupéré(s)"
    print(f"\n{total} nouveau(x) média(s) {verbe} au total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

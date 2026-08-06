#!/usr/bin/env python3
"""Synchronise la boîte de dépôt Drive d'un client vers le dépôt.

    python3 scripts/drive_sync.py gossip-beauty-center
    python3 scripts/drive_sync.py --tous --dry-run

Le principe : chaque client a UN dossier Drive partagé avec lui, dans lequel il dépose ses
photos et vidéos depuis son téléphone. Ce script le lit, repère ce qui est nouveau, héberge les
fichiers et tient à jour le manifeste du dépôt. Le client n'a rien à installer, rien à nommer.

Sens unique, Drive → dépôt. Le script ne crée, ne renomme et ne supprime jamais rien côté Drive :
c'est la boîte du client, pas la nôtre. Le dépôt reste la source de vérité de ce qui est publié ;
le Drive n'est qu'une porte d'entrée.

Déduplication par empreinte du contenu, pas par nom. Un même fichier déposé deux fois — ce qui
arrive tout le temps quand on envoie depuis un téléphone — n'entre qu'une fois dans le manifeste,
et le doublon est signalé. C'est exactement ce qui nous a fait cataloguer deux fois la même photo
sous deux sujets différents.

Secrets attendus :
  GOOGLE_API_KEY   clé API Google avec l'API Drive activée — suffit pour lire un dossier
                   partagé par lien, aucun compte de service à créer
  IMGBB_API_KEY    hébergement (le même que pour les slides)
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publier import _req, heberger  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "photos"
LISTE = "https://www.googleapis.com/drive/v3/files"
FICHIER = "https://www.googleapis.com/drive/v3/files/{}?alt=media&key={}"

# Ce qu'on accepte dans une boîte de dépôt client. Le reste est ignoré sans bruit : les clients
# y laissent des captures d'écran, des PDF de devis, des .DS_Store.
EXTENSIONS = {"image/jpeg": "jpg", "image/png": "png", "image/heic": "heic",
              "video/mp4": "mp4", "video/quicktime": "mov"}


def lister(dossier_id, cle):
    """Liste récursivement les médias d'un dossier Drive public. Retourne des dicts plats."""
    trouves, a_voir = [], [dossier_id]
    while a_voir:
        parent = a_voir.pop()
        page = None
        while True:
            params = {
                "q": f"'{parent}' in parents and trashed = false",
                "key": cle,
                "fields": "nextPageToken,files(id,name,mimeType,size,modifiedTime)",
                "pageSize": "200",
            }
            if page:
                params["pageToken"] = page
            rep = _req(f"{LISTE}?{urllib.parse.urlencode(params)}")
            for f in rep.get("files", []):
                if f["mimeType"] == "application/vnd.google-apps.folder":
                    a_voir.append(f["id"])
                elif f["mimeType"] in EXTENSIONS:
                    trouves.append(f)
            page = rep.get("nextPageToken")
            if not page:
                break
    return trouves


def telecharger(file_id, cle):
    req = urllib.request.Request(FICHIER.format(file_id, cle),
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        octets = r.read()
        ctype = r.headers.get("Content-Type", "")
    if not ctype.split(";")[0] in EXTENSIONS:
        raise RuntimeError(f"Drive a renvoyé « {ctype} » — dossier probablement non partagé")
    return octets


def synchroniser(client, cle_drive, dry_run=False):
    manifeste = PHOTOS / f"{client}.json"
    spec = json.loads(manifeste.read_text(encoding="utf-8"))
    dossier_id = spec.get("drive_folder")
    if not dossier_id:
        raise SystemExit(f"{client} : aucun drive_folder dans le manifeste")

    connus = {p["empreinte"]: p for p in spec["photos"] if p.get("empreinte")}
    par_id = {p["drive_id"]: p for p in spec["photos"]}
    cible = ROOT / "medias" / client / "photos"
    cible.mkdir(parents=True, exist_ok=True)

    nouveaux, doublons, inchanges = [], [], 0
    for f in lister(dossier_id, cle_drive):
        if f["id"] in par_id and par_id[f["id"]].get("empreinte"):
            inchanges += 1
            continue
        octets = telecharger(f["id"], cle_drive)
        empreinte = hashlib.sha256(octets).hexdigest()[:16]
        if empreinte in connus:
            doublons.append((f["name"], connus[empreinte]["nom"]))
            continue
        chemin = cible / f"{empreinte}.{EXTENSIONS[f['mimeType']]}"
        chemin.write_bytes(octets)
        entree = {
            "nom": empreinte,
            "drive_id": f["id"],
            "drive_nom": f["name"],
            "empreinte": empreinte,
            "type": EXTENSIONS[f["mimeType"]],
            "sujet": None,          # à qualifier à la main : c'est un travail d'œil, pas de script
            "pilier": None,
            "url": None,
        }
        connus[empreinte] = entree
        nouveaux.append((entree, chemin))

    print(f"{client} : {inchanges} déjà connus, {len(nouveaux)} nouveaux, "
          f"{len(doublons)} doublon(s)")
    for nom, deja in doublons:
        print(f"  = {nom} — contenu identique à « {deja} », ignoré")
    for entree, _ in nouveaux:
        print(f"  + {entree['drive_nom']} → {entree['nom']}.{entree['type']} (à qualifier)")

    if dry_run or not nouveaux:
        return 0

    images = [(e, c) for e, c in nouveaux if e["type"] in ("jpg", "png")]
    if images:
        for entree, url in zip((e for e, _ in images), heberger([c for _, c in images])):
            entree["url"] = url
    spec["photos"].extend(e for e, _ in nouveaux)
    manifeste.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  → manifeste mis à jour, {len(images)} image(s) hébergée(s)")
    return len(nouveaux)


def main():
    ap = argparse.ArgumentParser(description="Synchronise les boîtes de dépôt Drive.")
    ap.add_argument("client", nargs="?")
    ap.add_argument("--tous", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cle = os.environ.get("GOOGLE_API_KEY")
    if not cle:
        raise SystemExit("secret manquant : GOOGLE_API_KEY")
    if not args.dry_run and not os.environ.get("IMGBB_API_KEY"):
        raise SystemExit("secret manquant : IMGBB_API_KEY")

    clients = ([p.stem for p in sorted(PHOTOS.glob("*.json"))]
               if args.tous else [args.client])
    if not clients or clients == [None]:
        raise SystemExit("préciser un client ou --tous")

    total = 0
    for c in clients:
        total += synchroniser(c, cle, args.dry_run)
    print(f"\n{total} nouveau(x) média(s) au total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

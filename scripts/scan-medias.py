#!/usr/bin/env python3
"""
Détecteur de nouveaux médias déposés dans les dossiers clients.

Utilisé par la tâche planifiée du lundi (recap-hebdo-publications) : repère les
photos/vidéos ajoutées depuis la dernière exécution pour les brancher sur les
stories et posts de la semaine (voir SKILL.md, étape « Nouveaux médias »).

L'identité d'un fichier est le SHA1 de son contenu : renommer ou déplacer une
photo ne la fait pas repasser pour neuve, et un doublon déposé deux fois est vu
une seule fois.

    python3 scan-medias.py                 # rapport JSON des nouveaux médias
    python3 scan-medias.py --client le-loft
    python3 scan-medias.py --seed          # marque l'existant comme déjà connu
    python3 scan-medias.py --register FICHIER.json   # enregistre après branchement

Les dossiers `ia/`, `ia-stories/` (banques générées) et les fichiers cachés sont
ignorés : on ne surveille que les VRAIS médias fournis par le client.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MEDIAS = RACINE / "medias"
INDEX = RACINE / "recaps" / "medias-index.json"

EXT_IMAGE = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
EXT_VIDEO = {".mp4", ".mov", ".m4v"}
DOSSIERS_IGNORES = {"ia", "ia-stories", "stories", "__pycache__"}


def charger_index() -> dict:
    if INDEX.exists():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return {"_doc": "Médias clients déjà vus par scan-medias.py. Clé = SHA1 du contenu.", "clients": {}}


def enregistrer_index(index: dict) -> None:
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")


def sha_fichier(chemin: Path) -> str:
    h = hashlib.sha1()
    with chemin.open("rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()[:12]


def dimensions(chemin: Path) -> tuple[int, int] | None:
    if chemin.suffix.lower() in EXT_IMAGE:
        try:
            from PIL import Image

            with Image.open(chemin) as im:
                return im.size
        except Exception:
            return None
    try:
        sortie = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(chemin)],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        l, h = sortie.split("x")[:2]
        return int(l), int(h)
    except Exception:
        return None


def cadrage(taille: tuple[int, int] | None) -> str:
    """Oriente vers le bon usage : une verticale fait une story plein cadre."""
    if not taille:
        return "inconnu"
    largeur, hauteur = taille
    ratio = largeur / hauteur if hauteur else 1
    if ratio < 0.85:
        return "portrait"      # story 9:16 sans recadrage
    if ratio > 1.2:
        return "paysage"       # post feed, ou story sur fond flouté
    return "carre"             # feed 4:5 / 1:1


def parcourir(dossier_client: Path):
    for chemin in sorted(dossier_client.rglob("*")):
        if not chemin.is_file() or chemin.name.startswith("."):
            continue
        if any(p in DOSSIERS_IGNORES for p in chemin.relative_to(dossier_client).parts[:-1]):
            continue
        if chemin.suffix.lower() not in EXT_IMAGE | EXT_VIDEO:
            continue
        yield chemin


def scanner(client_filtre: str | None = None) -> dict:
    index = charger_index()
    connus = index.get("clients", {})
    rapport = {"date_scan": datetime.now().strftime("%Y-%m-%d %H:%M"), "clients": {}}

    for dossier in sorted(p for p in MEDIAS.iterdir() if p.is_dir()):
        client = dossier.name
        if client_filtre and client != client_filtre:
            continue
        deja_vus = connus.get(client, {})
        nouveaux = []
        for chemin in parcourir(dossier):
            sha = sha_fichier(chemin)
            if sha in deja_vus:
                continue
            taille = dimensions(chemin)
            nouveaux.append({
                "sha": sha,
                "fichier": str(chemin.relative_to(RACINE)),
                "nom": chemin.name,
                "type": "video" if chemin.suffix.lower() in EXT_VIDEO else "photo",
                "dimensions": f"{taille[0]}x{taille[1]}" if taille else None,
                "cadrage": cadrage(taille),
                "poids_mo": round(chemin.stat().st_size / 1e6, 1),
                "depose_le": datetime.fromtimestamp(chemin.stat().st_mtime).strftime("%Y-%m-%d"),
            })
        if nouveaux:
            rapport["clients"][client] = {
                "nouveaux": len(nouveaux),
                "portrait": sum(n["cadrage"] == "portrait" for n in nouveaux),
                "paysage": sum(n["cadrage"] == "paysage" for n in nouveaux),
                "carre": sum(n["cadrage"] == "carre" for n in nouveaux),
                "videos": sum(n["type"] == "video" for n in nouveaux),
                "fichiers": nouveaux,
            }
    rapport["total_nouveaux"] = sum(c["nouveaux"] for c in rapport["clients"].values())
    return rapport


def semer(statut: str = "en-reserve", client_filtre: str | None = None) -> int:
    """Marque l'existant comme déjà vu (à ne lancer qu'une fois par lot)."""
    index = charger_index()
    index.setdefault("clients", {})
    total = 0
    for dossier in sorted(p for p in MEDIAS.iterdir() if p.is_dir()):
        if client_filtre and dossier.name != client_filtre:
            continue
        entrees = index["clients"].setdefault(dossier.name, {})
        for chemin in parcourir(dossier):
            sha = sha_fichier(chemin)
            if sha not in entrees:
                taille = dimensions(chemin)
                entrees[sha] = {
                    "nom": chemin.name,
                    "fichier": str(chemin.relative_to(RACINE)),
                    "cadrage": cadrage(taille),
                    "vu_le": datetime.now().strftime("%Y-%m-%d"),
                    "statut": statut,
                }
                total += 1
    enregistrer_index(index)
    return total


def reserve(client_filtre: str | None = None) -> dict:
    """Médias déjà vus mais jamais branchés — le vivier où puiser quand aucune
    nouvelle photo n'est arrivée cette semaine."""
    index = charger_index()
    sortie = {"clients": {}}
    for client, entrees in index.get("clients", {}).items():
        if client_filtre and client != client_filtre:
            continue
        dispo = [
            {"sha": sha, **{k: v for k, v in e.items() if k in ("nom", "fichier", "cadrage")}}
            for sha, e in entrees.items()
            if e.get("statut") == "en-reserve"
        ]
        if dispo:
            sortie["clients"][client] = {
                "disponibles": len(dispo),
                "portrait": sum(d.get("cadrage") == "portrait" for d in dispo),
                "paysage": sum(d.get("cadrage") == "paysage" for d in dispo),
                "fichiers": dispo,
            }
    sortie["total_disponibles"] = sum(c["disponibles"] for c in sortie["clients"].values())
    return sortie


def enregistrer(fichier_json: Path) -> int:
    """Après branchement : [{client, sha, nom, url_hebergee, utilise_dans}]."""
    index = charger_index()
    index.setdefault("clients", {})
    for item in json.loads(fichier_json.read_text(encoding="utf-8")):
        entrees = index["clients"].setdefault(item["client"], {})
        entrees[item["sha"]] = {
            "nom": item.get("nom"),
            "vu_le": datetime.now().strftime("%Y-%m-%d"),
            "statut": item.get("statut", "branche"),
            "url_hebergee": item.get("url_hebergee"),
            "utilise_dans": item.get("utilise_dans"),
        }
    enregistrer_index(index)
    return len(index["clients"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client", help="limiter à un dossier client")
    ap.add_argument("--seed", action="store_true", help="marquer l'existant comme déjà vu")
    ap.add_argument("--statut", default="en-reserve",
                    choices=["en-reserve", "deja-exploite"], help="statut posé par --seed")
    ap.add_argument("--reserve", action="store_true", help="lister les médias jamais branchés")
    ap.add_argument("--register", type=Path, help="enregistrer des médias branchés (JSON)")
    args = ap.parse_args()

    if args.seed:
        n = semer(args.statut, args.client)
        print(f"{n} médias enregistrés ({args.statut}) dans {INDEX.name}")
        return 0
    if args.reserve:
        print(json.dumps(reserve(args.client), ensure_ascii=False, indent=1))
        return 0
    if args.register:
        enregistrer(args.register)
        print("index mis à jour")
        return 0

    print(json.dumps(scanner(args.client), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

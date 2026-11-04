#!/usr/bin/env python3
"""
Tirage au sort d'un jeu concours Instagram, avec les chances en plus.

Règle (.claude/memories/jeu-concours-mecanique-virale.md) :
  - 1 chance de base par participant ;
  - +1 chance par ami identifié distinct dans ses commentaires ;
  - +1 chance s'il a partagé le post en story en identifiant le compte.

Fichier des commentaires : une ligne par commentaire, « pseudo : texte ».
On peut le remplir à la main ou coller l'export d'un outil de relevé.

    python3 tirage-concours.py commentaires.txt
    python3 tirage-concours.py commentaires.txt --stories stories.txt --exclure @oteafilmakers @agence
    python3 tirage-concours.py commentaires.txt --graine 20261112

stories.txt : un pseudo par ligne (les comptes dont la story a été repartagée).
La graine est affichée : avec la même graine et les mêmes fichiers, le tirage
donne le même gagnant, ce qui permet de le prouver.
"""

from __future__ import annotations

import argparse
import random
import re
import sys
import time
from pathlib import Path

MENTION = re.compile(r"@([A-Za-z0-9._]+)")


def pseudo(brut: str) -> str:
    return brut.strip().lstrip("@").lower()


def lire_commentaires(chemin: Path) -> dict[str, set[str]]:
    """Renvoie, pour chaque participant, l'ensemble des amis qu'il a identifiés."""
    amis: dict[str, set[str]] = {}
    for n, ligne in enumerate(chemin.read_text(encoding="utf-8").splitlines(), 1):
        if not ligne.strip():
            continue
        if ":" not in ligne:
            sys.exit(f"Ligne {n} sans « : ». Écris chaque commentaire sous la forme « pseudo : texte ».")
        auteur, texte = ligne.split(":", 1)
        auteur = pseudo(auteur)
        if not auteur:
            continue
        identifies = {pseudo(m) for m in MENTION.findall(texte)} - {auteur}
        amis.setdefault(auteur, set()).update(identifies)
    return amis


def calculer_chances(amis: dict[str, set[str]], stories: set[str], exclus: set[str]) -> dict[str, int]:
    chances = {}
    for auteur, identifies in amis.items():
        if auteur in exclus:
            continue
        chances[auteur] = 1 + len(identifies - exclus) + (1 if auteur in stories else 0)
    return chances


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("commentaires", type=Path)
    p.add_argument("--stories", type=Path, help="pseudos ayant partagé en story, un par ligne")
    p.add_argument("--exclure", nargs="*", default=[], help="pseudos exclus (compte, comptes pro)")
    p.add_argument("--graine", type=int, help="pour refaire un tirage à l'identique")
    a = p.parse_args()

    if not a.commentaires.exists():
        sys.exit(f"Je ne trouve pas {a.commentaires}. Vérifie le chemin du fichier des commentaires.")
    stories = set()
    if a.stories:
        stories = {pseudo(l) for l in a.stories.read_text(encoding="utf-8").splitlines() if l.strip()}
    exclus = {pseudo(x) for x in a.exclure}

    chances = calculer_chances(lire_commentaires(a.commentaires), stories, exclus)
    if not chances:
        sys.exit("Aucun participant valide. Vérifie le fichier des commentaires et la liste des exclus.")

    graine = a.graine if a.graine is not None else int(time.time())
    tirage = random.Random(graine)
    participants = sorted(chances)
    gagnant = tirage.choices(participants, weights=[chances[x] for x in participants], k=1)[0]

    total = sum(chances.values())
    print(f"{len(chances)} participants, {total} chances au total.\n")
    for nom in sorted(chances, key=lambda x: (-chances[x], x)):
        print(f"  @{nom:<30} {chances[nom]} chance(s)")
    print(f"\nGraine du tirage : {graine}")
    print(f"Gagnant : @{gagnant} ({chances[gagnant]} chance(s) sur {total})")


if __name__ == "__main__":
    main()

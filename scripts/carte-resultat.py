#!/usr/bin/env python3
"""
Compose une carte « résultat de tournoi » 4:5 pour un post feed.

Pensée pour les posts réaction J+1 (pilier actu secteur) quand aucune photo
de l'événement n'est utilisable : les photos de tournoi sont des images
d'agence, interdites sur un compte commercial. Une carte typographique dit
le résultat sans exposer le client.

    python3 carte-resultat.py sortie.jpg \
        --surtitre "AIG WOMEN'S OPEN 2026 · ROYAL LYTHAM & ST ANNES" \
        --nom "SHIHO KUWAKI" \
        --score "-5" \
        --mention "VICTOIRE EN PLAYOFF" \
        --detail "Bat Esther Henseleit au 2e trou de mort subite" \
        --note "PREMIER MAJEUR"

Palette par défaut : DA J Lawson Golf (bleu marine + vert, accent ambré).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LARGEUR, HAUTEUR = 1080, 1350

MARINE = (14, 27, 42)
MARINE_BAS = (8, 16, 26)
VERT = (62, 158, 116)
AMBRE = (217, 154, 78)
CREME = (242, 240, 236)
GRIS = (168, 178, 190)

POLICES_CANDIDATES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    str(Path(__file__).resolve().parent.parent / "assets" / "fonts" / "titre.ttf"),
]


def trouver_police() -> str:
    for chemin in POLICES_CANDIDATES:
        if Path(chemin).exists():
            return chemin
    raise SystemExit(
        "Aucune police trouvée. Déposez un .ttf dans assets/fonts/titre.ttf."
    )


POLICE = trouver_police()


def charger_police(taille: int, gras: bool = False) -> ImageFont.FreeTypeFont:
    """Même repli que carte-story.py : l'index gras n'existe que sur les .ttc."""
    if gras:
        try:
            return ImageFont.truetype(POLICE, taille, index=1)
        except OSError:
            pass
    return ImageFont.truetype(POLICE, taille, index=0)


def largeur_tracked(dessin, texte, police, tracking):
    return sum(dessin.textlength(c, font=police) + tracking for c in texte) - tracking


def texte_tracked(dessin, xy, texte, police, couleur, tracking=0, ancre="centre"):
    """Dessine un texte interlettré (PIL ne gère pas le letter-spacing)."""
    x, y = xy
    largeur = largeur_tracked(dessin, texte, police, tracking)
    if ancre == "centre":
        x -= largeur / 2
    for c in texte:
        dessin.text((x, y), c, font=police, fill=couleur, anchor="lm")
        x += dessin.textlength(c, font=police) + tracking
    return largeur


def ajuster(dessin, texte, tracking, taille_max, taille_min, largeur_max):
    """Réduit la taille jusqu'à ce que le texte tienne dans la largeur."""
    taille = taille_max
    while taille > taille_min:
        police = charger_police(taille, gras=True)
        if largeur_tracked(dessin, texte, police, tracking) <= largeur_max:
            return police
        taille -= 4
    return charger_police(taille_min, gras=True)


def composer(sortie: Path, surtitre: str, nom: str, score: str, mention: str,
             detail: str, note: str) -> Path:
    image = Image.new("RGB", (LARGEUR, HAUTEUR), MARINE)
    dessin = ImageDraw.Draw(image)

    # Dégradé vertical discret : évite l'aplat mort sur un grand format.
    for y in range(HAUTEUR):
        t = y / HAUTEUR
        dessin.line(
            [(0, y), (LARGEUR, y)],
            fill=tuple(int(MARINE[i] + (MARINE_BAS[i] - MARINE[i]) * t) for i in range(3)),
        )

    marge = 90
    utile = LARGEUR - 2 * marge

    # Surtitre ambré, interlettré large
    police_sur = ajuster(dessin, surtitre, 3, 30, 18, utile)
    texte_tracked(dessin, (LARGEUR / 2, 190), surtitre, police_sur, AMBRE, tracking=3)

    dessin.rectangle([LARGEUR / 2 - 40, 240, LARGEUR / 2 + 40, 244], fill=AMBRE)

    # Nom de la gagnante : le bloc dominant
    police_nom = ajuster(dessin, nom, 2, 118, 56, utile)
    texte_tracked(dessin, (LARGEUR / 2, 400), nom, police_nom, CREME, tracking=2)

    # Score + mention, séparés par un filet vert
    police_score = charger_police(150, gras=True)
    largeur_score = dessin.textlength(score, font=police_score)
    dessin.text((LARGEUR / 2, 600), score, font=police_score, fill=VERT, anchor="mm")

    dessin.rectangle(
        [LARGEUR / 2 - largeur_score / 2 - 28, 690, LARGEUR / 2 + largeur_score / 2 + 28, 694],
        fill=VERT,
    )

    police_mention = ajuster(dessin, mention, 4, 46, 26, utile)
    texte_tracked(dessin, (LARGEUR / 2, 760), mention, police_mention, CREME, tracking=4)

    # Détail factuel, sur deux lignes si besoin
    police_detail = charger_police(34)
    mots, lignes, courante = detail.split(), [], ""
    for mot in mots:
        essai = (courante + " " + mot).strip()
        if dessin.textlength(essai, font=police_detail) <= utile:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    lignes.append(courante)
    y = 900
    for ligne in lignes:
        dessin.text((LARGEUR / 2, y), ligne, font=police_detail, fill=GRIS, anchor="mm")
        y += 52

    # Note de bas de carte
    if note:
        police_note = ajuster(dessin, note, 5, 32, 20, utile)
        dessin.rectangle([LARGEUR / 2 - 40, 1090, LARGEUR / 2 + 40, 1093], fill=AMBRE)
        texte_tracked(dessin, (LARGEUR / 2, 1160), note, police_note, AMBRE, tracking=5)

    image.save(sortie, quality=95)
    return sortie


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("sortie", type=Path)
    ap.add_argument("--surtitre", required=True)
    ap.add_argument("--nom", required=True)
    ap.add_argument("--score", required=True)
    ap.add_argument("--mention", default="")
    ap.add_argument("--detail", default="")
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    chemin = composer(args.sortie, args.surtitre.upper(), args.nom.upper(),
                      args.score, args.mention.upper(), args.detail,
                      args.note.upper())
    print(f"carte résultat : {chemin}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

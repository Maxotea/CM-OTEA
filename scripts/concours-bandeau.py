#!/usr/bin/env python3
"""
Ajoute le bandeau « plus de chances » en bas d'une story de jeu concours.

Un jeu concours sans mécanique de partage ne rayonne pas (Maxime, 04/11/2026).
Chaque story de relance doit donc rappeler les deux leviers qui font circuler
le jeu : identifier des amis en commentaire, et partager en story en
identifiant le compte (on repartage chaque story reçue).

    python3 concours-bandeau.py story.jpg sortie.jpg
    python3 concours-bandeau.py story.jpg sortie.jpg --compte @oteafilmakers --haut 1585

Le bandeau se pose dans la zone libre sous le texte de la story, au-dessus
de la barre de réponse d'Instagram (les 160 derniers pixels restent vides).
La règle complète : .claude/memories/jeu-concours-mecanique-virale.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ORANGE = (255, 88, 0)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)
DOSSIER_POLICES = Path("/usr/share/fonts/opentype/inter")


def police(nom: str, taille: int) -> ImageFont.FreeTypeFont:
    for chemin in (DOSSIER_POLICES / nom, Path(__file__).resolve().parent.parent / "assets" / "fonts" / nom):
        if chemin.exists():
            return ImageFont.truetype(str(chemin), taille)
    raise SystemExit(f"Police {nom} introuvable : dépose-la dans assets/fonts/ puis relance.")


def bandeau(source: Path, sortie: Path, compte: str, haut: int) -> None:
    img = Image.open(source).convert("RGBA")
    largeur = img.width
    marge = 70
    calque = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)

    f_titre = police("InterDisplay-Black.otf", 31)
    f_sous = police("InterDisplay-Medium.otf", 26)
    f_plus = police("InterDisplay-Black.otf", 40)

    lignes = [
        ("1 AMI TAGUÉ EN COMMENTAIRE", "= 1 chance de plus"),
        ("TA STORY + " + compte.upper(), "= 1 chance, je repartage"),
    ]
    droite = largeur - marge - 50          # laisse libre le coin orange du cadre
    hauteur_ligne = 58
    d.rounded_rectangle((marge, haut, droite, haut + 24 + hauteur_ligne * len(lignes)), radius=12,
                        fill=(18, 18, 18, 230), outline=(255, 88, 0, 255), width=3)
    # Réduit les deux polices tant qu'une ligne dépasse du cadre.
    taille = 31
    while taille > 20 and any(
        marge + 100 + d.textlength(t + " ", font=f_titre) + d.textlength(u, font=f_sous) > droite - 20
        for t, u in lignes
    ):
        taille -= 1
        f_titre = police("InterDisplay-Black.otf", taille)
        f_sous = police("InterDisplay-Medium.otf", taille - 5)
    y = haut + 12
    for titre, suite in lignes:
        d.text((marge + 24, y + 6), "+1", font=f_plus, fill=ORANGE)
        x = marge + 100
        d.text((x, y + 10), titre, font=f_titre, fill=BLANC)
        x += d.textlength(titre + " ", font=f_titre)
        d.text((x, y + 14), suite, font=f_sous, fill=GRIS)
        y += hauteur_ligne
    y += 12

    if y > img.height - 160:
        raise SystemExit("Le bandeau déborde sur la barre de réponse d'Instagram : baisse --haut.")
    Image.alpha_composite(img, calque).convert("RGB").save(sortie, quality=93)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", type=Path)
    p.add_argument("sortie", type=Path)
    p.add_argument("--compte", default="@oteafilmakers")
    p.add_argument("--haut", type=int, default=1606, help="ordonnée du haut du bandeau, en pixels")
    a = p.parse_args()
    bandeau(a.source, a.sortie, a.compte, a.haut)


if __name__ == "__main__":
    main()

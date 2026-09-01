#!/usr/bin/env python3
"""
Compose une carte story 9:16 à partir d'une VRAIE photo.

Aucune IA générative n'intervient sur l'image : la photo est reprise telle
quelle, seuls le fond flouté et le texte sont ajoutés. C'est la règle de
l'agence dès qu'un visage réel apparaît (clients, équipe, Maxime).

    python3 carte-story.py photo.jpg "HEAD SPA" "Le rituel qui fait la différence" sortie.jpg
    python3 carte-story.py photo.jpg "TITRE" "sous-titre" sortie.jpg --couleur "#FF5800"

Le fichier `sortie-fond.jpg` est écrit à côté : c'est la même carte SANS texte,
à donner au modèle image-to-vidéo si la story doit être animée (le texte est
réincrusté net par-dessus la vidéo, sinon il se déforme).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

LARGEUR, HAUTEUR = 1080, 1920
ZONE_TEXTE = 430          # hauteur réservée au bandeau titre, en haut
MARGE_BAS = 90

# Polices : on cherche dans l'ordre macOS, Windows, Linux, puis une police
# déposée dans assets/fonts/ du repo. Permet de faire tourner le script sur
# n'importe quelle plateforme sans modifier le code.
POLICES_CANDIDATES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",              # macOS
    "/System/Library/Fonts/Helvetica.ttc",                  # macOS
    "C:/Windows/Fonts/arialbd.ttf",                         # Windows
    "C:/Windows/Fonts/arial.ttf",                           # Windows
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # Linux (Debian/Ubuntu)
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    str(Path(__file__).resolve().parent.parent / "assets" / "fonts" / "titre.ttf"),
]


def trouver_police() -> str:
    """Renvoie la première police disponible sur la machine."""
    for chemin in POLICES_CANDIDATES:
        if Path(chemin).exists():
            return chemin
    raise SystemExit(
        "Aucune police trouvée. Déposez un fichier .ttf dans assets/fonts/titre.ttf "
        "ou ajoutez le chemin de votre police dans POLICES_CANDIDATES."
    )


POLICE = trouver_police()


def charger_police(taille: int, gras: bool = False) -> ImageFont.FreeTypeFont:
    """Charge la police à la taille voulue, en gras si la police le permet.

    Les .ttc de macOS sont des collections : le gras est un sous-fichier
    (index 1). Les .ttf de Linux/Windows n'ont qu'un seul index — demander
    index=1 y lève « invalid argument ». On tente donc l'index gras, puis on
    retombe sur l'index unique.
    """
    if gras:
        try:
            return ImageFont.truetype(POLICE, taille, index=1)
        except OSError:
            pass
    return ImageFont.truetype(POLICE, taille, index=0)


def hex_vers_rgb(valeur: str) -> tuple[int, int, int]:
    valeur = valeur.lstrip("#")
    return tuple(int(valeur[i:i + 2], 16) for i in (0, 2, 4))


def composer(photo: Path, titre: str, sous_titre: str, sortie: Path,
             couleur: str = "#FF5800") -> tuple[Path, Path]:
    image = Image.open(photo).convert("RGB")

    fond = image.copy()
    ratio = max(LARGEUR / fond.width, HAUTEUR / fond.height)
    fond = fond.resize((int(fond.width * ratio), int(fond.height * ratio)))
    gauche, haut = (fond.width - LARGEUR) // 2, (fond.height - HAUTEUR) // 2
    fond = fond.crop((gauche, haut, gauche + LARGEUR, haut + HAUTEUR))
    fond = fond.filter(ImageFilter.GaussianBlur(30))
    fond = ImageEnhance.Brightness(fond).enhance(0.45)

    avant = image.copy()
    ratio_avant = min((LARGEUR - 120) / avant.width, (HAUTEUR - ZONE_TEXTE - MARGE_BAS - 40) / avant.height)
    avant = avant.resize((int(avant.width * ratio_avant), int(avant.height * ratio_avant)))
    y = ZONE_TEXTE + (HAUTEUR - MARGE_BAS - ZONE_TEXTE - avant.height) // 2
    fond.paste(avant, ((LARGEUR - avant.width) // 2, y))

    chemin_fond = sortie.with_name(sortie.stem + "-fond" + sortie.suffix)
    fond.save(chemin_fond, quality=95)

    calque = Image.new("RGBA", (LARGEUR, HAUTEUR), (0, 0, 0, 0))
    dessin = ImageDraw.Draw(calque)

    # Voile dégradé : garantit la lisibilité du titre quelle que soit la photo.
    for ligne in range(ZONE_TEXTE):
        dessin.line([(0, ligne), (LARGEUR, ligne)],
                    fill=(10, 10, 10, int(160 * (1 - ligne / ZONE_TEXTE))))

    taille = 92
    police_titre = charger_police(taille, gras=True)
    while dessin.textlength(titre, font=police_titre) > LARGEUR - 100 and taille > 40:
        taille -= 4
        police_titre = charger_police(taille, gras=True)
    police_sous = charger_police(46)

    largeur_titre = dessin.textlength(titre, font=police_titre)
    dessin.rectangle([(LARGEUR - largeur_titre) / 2 - 20, 150,
                      (LARGEUR + largeur_titre) / 2 + 20, 162],
                     fill=hex_vers_rgb(couleur) + (255,))
    dessin.text((LARGEUR / 2, 235), titre, font=police_titre, fill="white", anchor="mm")
    if sous_titre:
        dessin.text((LARGEUR / 2, 330), sous_titre, font=police_sous,
                    fill=(230, 230, 230, 255), anchor="mm")

    chemin_texte = sortie.with_name(sortie.stem + "-texte.png")
    calque.save(chemin_texte)

    finale = fond.convert("RGBA")
    finale.alpha_composite(calque)
    finale.convert("RGB").save(sortie, quality=92)
    return chemin_fond, chemin_texte


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photo", type=Path)
    ap.add_argument("titre")
    ap.add_argument("sous_titre")
    ap.add_argument("sortie", type=Path)
    ap.add_argument("--couleur", default="#FF5800", help="couleur de la barre (charte du client)")
    args = ap.parse_args()

    fond, texte = composer(args.photo, args.titre.upper(), args.sous_titre, args.sortie, args.couleur)
    print(f"carte : {args.sortie}\nfond sans texte (pour animation) : {fond}\ncalque texte : {texte}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Génère les cartes story typographiques 9:16 depuis un manifest JSON.

Cartes 100 % dessinées en PIL — ni photo, ni IA, ni marque tierce. C'est le
format autorisé pour les stories quand aucune vraie photo n'est disponible
(même statut que les cartes typographiques Pierre Huiban).

    python3 carte-story-typo.py assets/stories/manifest-stories-2sem.json assets/stories/

Écrit <dossier>/<client>/<slot>.jpg pour chaque slot du manifest.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LARGEUR, HAUTEUR = 1080, 1920

SANS_CANDIDATES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    str(Path(__file__).resolve().parent.parent / "assets" / "fonts" / "titre.ttf"),
]
SERIF_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Didot.ttc",
    "C:/Windows/Fonts/georgia.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    str(Path(__file__).resolve().parent.parent / "assets" / "fonts" / "serif.ttf"),
]
SERIF_REG_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Baskerville.ttc",
    "C:/Windows/Fonts/georgia.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def premiere(candidats):
    for c in candidats:
        if Path(c).exists():
            return c
    raise SystemExit(f"Aucune police trouvée parmi : {candidats}")


SANS = premiere(SANS_CANDIDATES)
SERIF = premiere(SERIF_CANDIDATES)
SERIF_REG = premiere(SERIF_REG_CANDIDATES)


def police(chemin, taille, gras=False):
    if gras:
        try:
            return ImageFont.truetype(chemin, taille, index=1)
        except OSError:
            pass
    return ImageFont.truetype(chemin, taille, index=0)


def tracked(dessin, xy, texte, fonte, couleur, tracking=0):
    x, y = xy
    total = sum(dessin.textlength(c, font=fonte) + tracking for c in texte) - tracking
    x -= total / 2
    for c in texte:
        dessin.text((x, y), c, font=fonte, fill=couleur, anchor="lm")
        x += dessin.textlength(c, font=fonte) + tracking


def ajuster(dessin, texte, chemin, tracking, tmax, tmin, largeur_max, gras=True):
    taille = tmax
    while taille > tmin:
        f = police(chemin, taille, gras)
        total = sum(dessin.textlength(c, font=f) + tracking for c in texte) - tracking
        if total <= largeur_max:
            return f
        taille -= 4
    return police(chemin, tmin, gras)


def wrap(dessin, texte, fonte, largeur_max):
    mots, lignes, courante = texte.split(), [], ""
    for mot in mots:
        essai = (courante + " " + mot).strip()
        if dessin.textlength(essai, font=fonte) <= largeur_max:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    lignes.append(courante)
    return lignes


def degrade(image, haut, bas):
    d = ImageDraw.Draw(image)
    for y in range(HAUTEUR):
        t = y / HAUTEUR
        d.line([(0, y), (LARGEUR, y)],
               fill=tuple(int(haut[i] + (bas[i] - haut[i]) * t) for i in range(3)))


def carte_jlawson(titre, sous):
    """DA J Lawson : marine profond, arcs de green, accents ambre."""
    MARINE, MARINE_BAS = (14, 27, 42), (8, 16, 26)
    VERT, AMBRE = (62, 158, 116), (217, 154, 78)
    CREME, GRIS = (242, 240, 236), (168, 178, 190)

    im = Image.new("RGB", (LARGEUR, HAUTEUR), MARINE)
    degrade(im, MARINE, MARINE_BAS)

    calque = Image.new("RGBA", (LARGEUR, HAUTEUR), (0, 0, 0, 0))
    tr = ImageDraw.Draw(calque)
    cx, cy = LARGEUR / 2, 900
    for rayon, ep, alpha in ((640, 3, 24), (500, 2, 18), (380, 2, 13)):
        tr.ellipse([cx - rayon, cy - rayon, cx + rayon, cy + rayon],
                   outline=VERT + (alpha,), width=ep)
    tr.ellipse([cx - 250, cy - 250, cx + 250, cy + 250], fill=VERT + (10,))
    im = Image.alpha_composite(im.convert("RGBA"), calque).convert("RGB")
    d = ImageDraw.Draw(im)

    marge, utile = 100, LARGEUR - 200
    f_over = ajuster(d, "J LAWSON GOLF · STUDIO DE FITTING", SANS, 4, 34, 20, utile)
    tracked(d, (LARGEUR / 2, 300), "J LAWSON GOLF · STUDIO DE FITTING", f_over, AMBRE, 4)
    d.rectangle([LARGEUR / 2 - 45, 370, LARGEUR / 2 + 45, 375], fill=AMBRE)

    f_titre = ajuster(d, titre, SANS, 3, 110, 52, utile)
    tracked(d, (LARGEUR / 2, 860), titre, f_titre, CREME, 3)

    d.rectangle([LARGEUR / 2 - 70, 960, LARGEUR / 2 + 70, 964], fill=VERT)

    f_sous = police(SANS, 44)
    y = 1060
    for ligne in wrap(d, sous, f_sous, utile):
        d.text((LARGEUR / 2, y), ligne, font=f_sous, fill=GRIS, anchor="mm")
        y += 64

    f_pied = ajuster(d, "TON MATÉRIEL À TES MESURES", SANS, 5, 30, 18, utile)
    d.rectangle([LARGEUR / 2 - 45, 1660, LARGEUR / 2 + 45, 1663], fill=AMBRE)
    tracked(d, (LARGEUR / 2, 1730), "TON MATÉRIEL À TES MESURES", f_pied, AMBRE, 5)
    return im


def carte_galerie(titre, sous):
    """DA La Galerie : crème, liseré doré, serif taupe — prestige haussmannien."""
    CREME_H, CREME_B = (246, 241, 232), (236, 228, 214)
    TAUPE, TAUPE_CLAIR = (63, 54, 43), (122, 108, 90)
    DORE = (168, 124, 79)

    im = Image.new("RGB", (LARGEUR, HAUTEUR), CREME_H)
    degrade(im, CREME_H, CREME_B)
    d = ImageDraw.Draw(im)

    # Double liseré doré, signature des supports prestige
    d.rectangle([50, 50, LARGEUR - 50, HAUTEUR - 50], outline=DORE, width=3)
    d.rectangle([66, 66, LARGEUR - 66, HAUTEUR - 66], outline=DORE + (0,) and DORE, width=1)

    marge, utile = 130, LARGEUR - 260
    f_over = ajuster(d, "LA GALERIE IMMOBILIÈRE", SANS, 6, 32, 20, utile)
    tracked(d, (LARGEUR / 2, 320), "LA GALERIE IMMOBILIÈRE", f_over, DORE, 6)

    # Losange ornemental
    cx, cy = LARGEUR / 2, 420
    d.polygon([(cx, cy - 14), (cx + 14, cy), (cx, cy + 14), (cx - 14, cy)], outline=DORE, width=2)

    f_titre = ajuster(d, titre, SERIF, 2, 104, 48, utile)
    tracked(d, (LARGEUR / 2, 880), titre, f_titre, TAUPE, 2)

    d.rectangle([LARGEUR / 2 - 60, 980, LARGEUR / 2 + 60, 983], fill=DORE)

    f_sous = police(SERIF_REG, 44)
    y = 1080
    for ligne in wrap(d, sous, f_sous, utile):
        d.text((LARGEUR / 2, y), ligne, font=f_sous, fill=TAUPE_CLAIR, anchor="mm")
        y += 66

    f_pied = ajuster(d, "PARIS & ÎLE-DE-FRANCE", SANS, 6, 28, 18, utile)
    cx, cy = LARGEUR / 2, 1630
    d.polygon([(cx, cy - 10), (cx + 10, cy), (cx, cy + 10), (cx - 10, cy)], outline=DORE, width=2)
    tracked(d, (LARGEUR / 2, 1700), "PARIS & ÎLE-DE-FRANCE", f_pied, DORE, 6)
    return im


STYLES = {"jlawson": carte_jlawson, "galerie": carte_galerie}


def main():
    manifest = json.loads(Path(sys.argv[1]).read_text())
    sortie = Path(sys.argv[2])
    for client, conf in manifest.items():
        if client.startswith("_"):
            continue
        rendu = STYLES[conf["style"]]
        dossier = sortie / client
        dossier.mkdir(parents=True, exist_ok=True)
        for slot, s in conf["slots"].items():
            im = rendu(s["titre"], s["sous"])
            chemin = dossier / f"{slot}.jpg"
            im.save(chemin, quality=85, optimize=True)
            print(f"{chemin}  ({chemin.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()

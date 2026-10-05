#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pierre Huiban, stories 1080x1920 : une VRAIE photo d'entraînement en plein cadre.

Remplace les cartes typographiques sur fond uni du 05/10, jugées fades par Maxime
le jour même (« je préfère qu'en fond on ait une photo de lui en train de faire un
exercice »). La photo vient de la banque de Pierre (dossier Drive des 81 photos,
voir references/clients/banque-photos-pierre-huiban.md) : aucune image générée,
aucune retouche du visage, juste un recadrage 9:16 et un dégradé sombre pour que
le texte se lise.

Le texte reste dans la DA « trois vies » : registre ATHLETE · FATHER · EXECUTIVE
en tête, jour en couleur aube, une seule phrase en Fraunces, pied ROAD TO HONG
KONG. Pas de paragraphe : la photo porte la story.

Usage :
    python3 pierre-story-photo-v2.py PHOTO.jpg SPEC.json CLE SORTIE.jpg [POLICES] [DECALAGE]

CLE = lun|mar|mer|jeu|ven|sam|dim (une entrée de SPEC["cartes"]).
DECALAGE = position horizontale du recadrage, de 0 (bord gauche) à 1 (bord
droit), 0.5 par défaut : sert à garder Pierre dans le cadre quand il n'est pas
au centre de la photo.
"""
import importlib.util
import json
import os
import sys

from PIL import Image, ImageDraw, ImageOps

_ici = os.path.dirname(os.path.abspath(__file__))
_moteur = os.path.join(_ici, "pierre-carousel-v2.py")
if not os.path.exists(_moteur):          # sandbox : le moteur est à côté sous le nom pc2.py
    _moteur = os.path.join(_ici, "pc2.py")
_spec = importlib.util.spec_from_file_location("pc2", _moteur)
pc2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc2)

W, H, M = 1080, 1920, 96
BLANC = (250, 248, 244)


def cadrer(photo, decalage=0.5):
    """Recadrage 9:16 plein cadre, sans déformation."""
    im = ImageOps.exif_transpose(photo).convert("RGB")
    return ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(decalage, 0.45))


def degrade(img):
    """Assombrit le haut (registre) et le bas (texte) ; le milieu, où est Pierre, reste net."""
    voile = Image.new("L", (1, H))
    for y in range(H):
        if y < 420:
            a = int(150 * (1 - y / 420) ** 1.6)
        elif y > H * 0.48:
            t = (y - H * 0.48) / (H * 0.52)
            a = int(225 * min(1, t) ** 1.3)
        else:
            a = 0
        voile.putpixel((0, y), a)
    noir = Image.new("RGB", (W, H), (12, 14, 18))
    return Image.composite(noir, img, voile.resize((W, H)))


def story(photo, c, polices, decalage=0.5):
    img = degrade(cadrer(photo, decalage))
    d = ImageDraw.Draw(img)
    P = lambda k, t: pc2.police(polices, k, t)

    # registre en tête, sous la barre de progression d'Instagram
    y0 = 230
    pc2.espace(d, (M, y0), "PIERRE HUIBAN", P("label", 24), BLANC, 3.4)
    fl = P("label", 22)
    mots = []
    for i, fac in enumerate(pc2.FACETS):
        mots.append((fac, fac == c["facette"]))
        if i < 2:
            mots.append(("·", False))
    larg = sum(pc2.largeur_espacee(d, m, fl, 2.6) for m, _ in mots) + 14 * (len(mots) - 1)
    x = W - M - larg
    for m, on in mots:
        x = pc2.espace(d, (x, y0 + 2), m, fl, pc2.DAWN if on else (205, 200, 192), 2.6) + 14

    # bloc texte posé au-dessus du pied, aligné en bas
    def poser(dd, y):
        pc2.espace(dd, (M, y), c["jour"].upper(), P("label", 30), pc2.DAWN, 3.4)
        y += 84
        return pc2.bloc(dd, (M, y), c["titre"], P("titre", 104), BLANC, pc2.DAWN, W - 2 * M, 116)
    fin = poser(ImageDraw.Draw(Image.new("RGB", (W, H))), 0)
    yb = H - 330
    poser(d, yb - 70 - fin)

    d.line([(M, yb), (W - M, yb)], fill=(120, 116, 110), width=2)
    pc2.espace(d, (M, yb + 30), "ROAD TO HONG KONG · JUNE 2027", P("label", 22), (215, 210, 202), 2.8)
    return img


def main():
    photo, spec, cle, sortie = sys.argv[1:5]
    polices = sys.argv[5] if len(sys.argv) > 5 else "fonts"
    decalage = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
    cartes = {c["cle"]: c for c in json.load(open(spec, encoding="utf-8"))["cartes"]}
    story(Image.open(photo), cartes[cle], polices, decalage).save(sortie, quality=92, subsampling=0)
    print(sortie)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""R.O.I. · carrousel de lancement de l'identité V3 (26/11/2026, Instagram et LinkedIn).

Cinq slides 1080×1350 dans les trois familles de la charte (Terracotta, Encre, photo voilée),
rendues avec les briques de scripts/roi-charte.py (logo officiel recoloré, Archivo seule).

    python3 carrousels/run-on-invest/2026-11-26-lancement-identite-v3.py <dossier de sortie>
"""
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw

RACINE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("charte", RACINE / "scripts" / "roi-charte.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

W, H = 1080, 1350
M = round(0.065 * W)


def fond(famille, photo=None, couloirs=0):
    if famille == "terracotta":
        return Image.new("RGBA", (W, H), c.TERRACOTTA + (255,)), c.CRAIE, c.CRAIE
    if famille == "encre":
        img = Image.new("RGBA", (W, H), c.ENCRE + (255,))
        if couloirs:
            ph = c.voile(c.photo_nb(c.SRC / photo, W - 2 * M, round(H * 0.42)), 0.15)
            img.paste(ph, (M, round(H * 0.17)), c.couloir(ph.width, ph.height, couloirs))
        return img, c.CRAIE, c.TERRACOTTA_CLAIR
    img = c.voile(c.photo_nb(c.SRC / photo, W, H), 0.45).convert("RGBA")
    return img, c.CRAIE, c.TERRACOTTA_CLAIR


def page(d, n, coul):
    c.repere(d, W - M, H - M, f"{n} / 5", coul, 22, "r")


def slide1():
    img, txt, acc = fond("terracotta")
    d = ImageDraw.Draw(img)
    c.repere(d, M, M + 30, "R.O.I. · NOUVELLE IDENTITÉ", txt, 24)
    lg = c.colorer(c.masque_depose(W - 2 * M), txt)
    img.alpha_composite(lg, (M, round(H * 0.30)))
    c.titre(d, ["NOUVELLE", "PEAU."], M, H * 0.62, W - 2 * M, 150, txt)
    c.repere(d, M, H - M, "LA DÉFENSE · PLÉNITUDE ARENA", txt, 22)
    page(d, 1, txt)
    return img


def slide2():
    img, txt, acc = fond("encre")
    d = ImageDraw.Draw(img)
    c.coin(img, txt, M, cap=30)
    p = c.colorer(c.masque_piste(300), acc)
    img.alpha_composite(p, (M, round(H * 0.20)))
    c.repere(d, M, H * 0.50, "01 · LE LOGO", acc, 24)
    bas = c.titre(d, ["LE O DEVIENT", "LA PISTE."], M, H * 0.53, W - 2 * M, 130, txt)
    y = bas + 100
    for l in ("Un R, une piste d'athlétisme vue du ciel, un I.",
              "Trois points : la course, les échanges,", "la croissance."):
        c.texte(d, M, y, l, txt, 40)
        y += 56
    page(d, 2, txt)
    return img


def slide3():
    img, txt, acc = fond("encre", "photo-defense-peloton-16x9.jpg", couloirs=3)
    d = ImageDraw.Draw(img)
    c.coin(img, txt, M, cap=30)
    c.repere(d, M, H * 0.64, "02 · LE TON", acc, 24)
    c.titre(d, ["WE RUN.", "WE TALK.", "WE INVEST."], M, H * 0.67, W - 2 * M, 120, txt)
    page(d, 3, txt)
    return img


def slide4():
    img, txt, acc = fond("terracotta")
    d = ImageDraw.Draw(img)
    c.coin(img, txt, M, cap=30)
    c.repere(d, M, H * 0.36, "03 · LA COULEUR", txt, 24)
    bas = c.titre(d, ["TERRA", "COTTA."], M, H * 0.39, W - 2 * M, 220, txt)
    y = bas + 110
    for l in ("La couleur d'une piste d'athlétisme.", "Tout le reste en noir et blanc."):
        c.texte(d, M, y, l, txt, 42)
        y += 60
    page(d, 4, txt)
    return img


def slide5():
    img, txt, acc = fond("photo", "photo-defense-arche-9x16.jpg")
    d = ImageDraw.Draw(img)
    c.coin(img, txt, M, cap=30)
    c.repere(d, M, H * 0.52, "LE NOM NE CHANGE PAS", acc, 24)
    bas = c.titre(d, ["RUN ON", "INVESTMENT."], M, H * 0.55, W - 2 * M, 130, txt)
    y = bas + 100
    for l in ("5 ou 10 km à La Défense,", "puis un vrai temps d'échange.", "Zéro pitch."):
        c.texte(d, M, y, l, txt, 42)
        y += 60
    c.repere(d, M, H - M, "ÉCRIS-NOUS EN MESSAGE PRIVÉ", acc, 22)
    page(d, 5, txt)
    return img


if __name__ == "__main__":
    sortie = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    sortie.mkdir(parents=True, exist_ok=True)
    for k, f in enumerate((slide1, slide2, slide3, slide4, slide5), 1):
        chemin = sortie / f"roi-lancement-v3-{k}.jpg"
        c.grain(f()).save(chemin, quality=90)
        print(chemin)

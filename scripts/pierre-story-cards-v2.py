#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pierre Huiban, cartes de story 1080x1920 dans la DA « trois vies ».

Remplacent les 7 cartes de l'ancienne DA (noir, rouge, « LFG ») qui tournaient
sur les stories quotidiennes. Même grammaire que les carrousels : papier, encre,
accent aube, registre ATHLETE · FATHER · EXECUTIVE en tête. Cartes purement
typographiques : aucune image générée, aucun visage.

Usage :
    python3 pierre-story-cards-v2.py SPEC.json DOSSIER_SORTIE [DOSSIER_POLICES]
"""
import importlib.util
import json
import os
import sys

from PIL import Image, ImageDraw

_ici = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("pc2", os.path.join(_ici, "pierre-carousel-v2.py"))
if not os.path.exists(_spec.origin):          # sandbox : le moteur est à côté sous le nom pc2.py
    _spec = importlib.util.spec_from_file_location("pc2", os.path.join(_ici, "pc2.py"))
pc2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc2)

W, H, M = 1080, 1920, 96


def carte(c, polices):
    fond = c.get("fond", "paper")
    bg = {"paper": pc2.PAPER, "ink": pc2.INK, "dawn": pc2.DAWN}[fond]
    fg = pc2.INK if fond in ("paper", "dawn") else pc2.PAPER
    sec = pc2.STONE if fond == "paper" else (pc2.INK if fond == "dawn" else pc2.INK_SOFT)
    acc = pc2.DAWN if fond != "dawn" else pc2.PAPER
    regle = pc2.RULE if fond == "paper" else (pc2.INK if fond == "dawn" else pc2.RULE_DARK)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    P = lambda k, t: pc2.police(polices, k, t)

    # zone haute laissée libre pour l'interface Instagram (barre de progression, avatar)
    y0 = 250
    pc2.espace(d, (M, y0), "PIERRE HUIBAN", P("label", 24), fg, 3.4)
    fl = P("label", 22)
    mots = []
    for i, fac in enumerate(pc2.FACETS):
        mots.append((fac, fac == c["facette"]))
        if i < 2:
            mots.append(("·", False))
    larg = sum(pc2.largeur_espacee(d, m, fl, 2.6) for m, _ in mots) + 14 * (len(mots) - 1)
    x = W - M - larg
    for m, on in mots:
        x = pc2.espace(d, (x, y0 + 2), m, fl, acc if on else (sec if fond != "dawn" else (90, 40, 20)), 2.6) + 14
    d.line([(M, y0 + 56), (W - M, y0 + 56)], fill=regle, width=2)

    # bloc central, centré verticalement en deux passes
    def poser(dd, y):
        pc2.espace(dd, (M, y), c["jour"].upper(), P("label", 30), acc, 3.4)
        y += 92
        y = pc2.bloc(dd, (M, y), c["titre"], P("titre", 120), fg, acc, W - 2 * M, 134) + 30
        dd.line([(M, y), (M + 140, y)], fill=acc, width=6)
        y += 50
        return pc2.bloc(dd, (M, y), c["texte"], P("texte", 46), sec if fond != "dawn" else pc2.INK, acc, W - 2 * M, 66)
    brouillon = Image.new("RGB", (W, H))
    fin = poser(ImageDraw.Draw(brouillon), 0)
    poser(d, int((H - fin) / 2) - 40)

    # pied, au-dessus de la zone de réponse Instagram
    yb = H - 330
    d.line([(M, yb), (W - M, yb)], fill=regle, width=2)
    pc2.espace(d, (M, yb + 30), "ROAD TO HONG KONG · JUNE 2027", P("label", 22), sec, 2.8)
    return img


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    sortie = sys.argv[2]
    polices = sys.argv[3] if len(sys.argv) > 3 else "fonts"
    os.makedirs(sortie, exist_ok=True)
    for c in spec["cartes"]:
        chemin = os.path.join(sortie, f"story-{c['cle']}.png")
        carte(c, polices).save(chemin, optimize=True)
        print(chemin)


if __name__ == "__main__":
    main()

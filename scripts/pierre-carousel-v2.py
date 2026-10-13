#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pierre Huiban, carrousels 1080x1350, DA « trois vies » (octobre 2026).

Pourquoi une nouvelle DA. L'ancienne (noir et rouge sang, capitales Anton) avait
été construite pour une ligne « rage silencieuse » que Pierre a rejetée en août.
Son persona, transmis par Maxime le 03/10/2026, dit autre chose : un père, un
dirigeant commercial, un athlète, et l'envie de montrer qu'on peut viser haut
sans sacrifier le reste. La DA suit ce texte :

    fond papier #F2EEE6 et encre #14171C : la sobriété d'un magazine, lisible
      par un pratiquant comme par une marque partenaire ;
    un seul accent, « aube » #E8622C : les séances tôt le matin du persona ;
    titres en Fraunces, en casse normale : une voix posée, pas un cri ;
    chiffres en JetBrains Mono : la donnée reste la preuve ;
    le « registre » en tête de chaque slide, ATHLETE · FATHER · EXECUTIVE,
      avec la facette du jour allumée. C'est le persona, en une ligne.

Usage :
    python3 pierre-carousel-v2.py SPEC.json DOSSIER_SORTIE [DOSSIER_POLICES]

Le spec décrit les slides (voir projets/pierre-huiban/carrousels-v2/2026-10-*.json). Aucun
chiffre n'est calculé ici : tout ce qui est affiché vient du spec, et les specs
ne contiennent que des valeurs relevées sur HYRESULT ou dites par Pierre.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
M = 88                                  # marge latérale
PAPER, INK, DAWN = (242, 238, 230), (20, 23, 28), (232, 98, 44)
STONE, RULE = (124, 121, 115), (214, 207, 194)
INK_SOFT, RULE_DARK = (169, 165, 157), (52, 56, 63)
FACETS = ("ATHLETE", "FATHER", "EXECUTIVE")

POLICES = {
    "titre": "Fraunces-SemiBold.ttf", "titre_it": "Fraunces-Italic.ttf",
    "texte": "Inter-Regular.ttf", "label": "Inter-SemiBold.ttf",
    "fort": "Inter-ExtraBold.ttf", "mono": "JBMono-Bold.ttf", "mono_m": "JBMono-Medium.ttf",
}


def police(dossier, cle, taille):
    return ImageFont.truetype(os.path.join(dossier, POLICES[cle]), taille)


def espace(d, xy, texte, f, fill, track=0.0):
    """Texte interlettré (les petits labels en capitales)."""
    x, y = xy
    for c in texte:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return x


def largeur_espacee(d, texte, f, track):
    return sum(d.textlength(c, font=f) + track for c in texte) - track


def segments(texte):
    """« Un **mot** » -> [(Un, False), (mot, True)] : l'accent se pose en couleur aube."""
    out, fort = [], False
    for i, morceau in enumerate(texte.split("**")):
        if morceau:
            out.append((morceau, i % 2 == 1))
    return out


def paragraphe(d, xy, texte, f, fill, accent, largeur, interligne):
    """Paragraphe justifié à gauche avec mots accentués. Renvoie le y de fin."""
    x0, y = xy
    mots = []
    for morceau, fort in segments(texte):
        for m in morceau.split(" "):
            if m:
                mots.append((m, fort))
    ligne, lx = [], 0
    def poser(ligne, y):
        x = x0
        for m, fort in ligne:
            d.text((x, y), m, font=f, fill=accent if fort else fill)
            x += d.textlength(m + " ", font=f)
    esp = d.textlength(" ", font=f)
    for m, fort in mots:
        if m == "\n":
            continue
        w = d.textlength(m, font=f)
        if ligne and lx + w > largeur:
            poser(ligne, y)
            y += interligne
            ligne, lx = [], 0
        ligne.append((m, fort))
        lx += w + esp
    if ligne:
        poser(ligne, y)
        y += interligne
    return y


def bloc(d, xy, texte, f, fill, accent, largeur, interligne):
    """Plusieurs paragraphes séparés par \n."""
    x, y = xy
    for i, p in enumerate(texte.split("\n")):
        y = paragraphe(d, (x, y), p, f, fill, accent, largeur, interligne)
        if i < len(texte.split("\n")) - 1:
            y += interligne * 0.35
    return y


def rendre(slide, n, total, spec, polices):
    """Deux passes : la première mesure la hauteur du contenu, la seconde le pose
    centré dans la zone utile, entre le registre et le pied."""
    _, fin = _rendre(slide, n, total, spec, polices, 0)
    haut, bas = 196, H - 170
    decalage = max(0, int(((bas - haut) - (fin - haut)) / 2))
    if slide.get("fond") == "ink":
        decalage = int(decalage * 0.8)
    img, _ = _rendre(slide, n, total, spec, polices, decalage)
    return img


def _rendre(slide, n, total, spec, polices, decalage):
    fond = slide.get("fond", "paper")
    bg = {"paper": PAPER, "ink": INK, "dawn": DAWN}[fond]
    fg = INK if fond in ("paper", "dawn") else PAPER
    sec = STONE if fond == "paper" else (INK if fond == "dawn" else INK_SOFT)
    acc = DAWN if fond != "dawn" else PAPER
    regle = RULE if fond == "paper" else (INK if fond == "dawn" else RULE_DARK)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    P = lambda k, t: police(polices, k, t)

    # en-tête : nom à gauche, registre des trois facettes à droite
    espace(d, (M, 74), "PIERRE HUIBAN", P("label", 22), fg, 3.2)
    actif = slide.get("facette", spec.get("facette", "ATHLETE"))
    fl = P("label", 20)
    mots = []
    for i, fac in enumerate(FACETS):
        mots.append((fac, fac == actif))
        if i < 2:
            mots.append(("·", False))
    larg = sum(largeur_espacee(d, m, fl, 2.4) for m, _ in mots) + 14 * (len(mots) - 1)
    x = W - M - larg
    for m, on in mots:
        couleur = acc if on else (sec if fond != "dawn" else (90, 40, 20))
        x = espace(d, (x, 76), m, fl, couleur, 2.4) + 14
    d.line([(M, 126), (W - M, 126)], fill=regle, width=2)

    y = 196 + decalage
    if slide.get("kicker"):
        espace(d, (M, y), slide["kicker"].upper(), P("label", 24), acc, 3.0)
        y += 66
    larg_txt = W - 2 * M

    if slide.get("stat"):
        taille = slide.get("stat_taille", 236 if len(slide["stat"]) <= 5 else 180)
        fs = P("mono", taille)
        d.text((M - 8, y - 22), slide["stat"], font=fs, fill=fg)
        y += int(taille * 0.98)
        if not slide.get("stat_label"):
            y += 40
        if slide.get("stat_label"):
            d.line([(M, y + 6), (M + 120, y + 6)], fill=acc, width=5)
            y += 34
            y = bloc(d, (M, y), slide["stat_label"], P("mono_m", 34), fg, acc, larg_txt, 48) + 26

    if slide.get("titre"):
        taille = slide.get("titre_taille", 84)
        y = bloc(d, (M, y), slide["titre"], P("titre", taille), fg, acc, larg_txt, int(taille * 1.12)) + 26

    if slide.get("tableau"):
        fl, fv = P("texte", 32), P("mono", 34)
        y += 8
        for lab, val in slide["tableau"]:
            d.line([(M, y), (W - M, y)], fill=regle, width=2)
            yy = paragraphe(d, (M, y + 26), lab, fl, fg, acc, larg_txt - 300, 42)
            vw = d.textlength(val, font=fv)
            d.text((W - M - vw, y + 24), val, font=fv, fill=acc if val.startswith(("−", "1st")) else fg)
            y = max(yy, y + 92) + 10
        d.line([(M, y), (W - M, y)], fill=regle, width=2)
        y += 30

    if slide.get("texte"):
        y = bloc(d, (M, y + 6), slide["texte"], P("texte", 40), sec if fond != "dawn" else INK, acc, larg_txt, 58)

    # pied : campagne à gauche, pagination à droite
    d.line([(M, H - 112), (W - M, H - 112)], fill=regle, width=2)
    espace(d, (M, H - 82), spec.get("pied", "ROAD TO HONG KONG · JUNE 2027"), P("label", 20), sec, 2.6)
    pg = f"{n:02d} / {total:02d}"
    fp = P("mono_m", 24)
    d.text((W - M - d.textlength(pg, font=fp), H - 86), pg, font=fp, fill=sec)
    if n < total and slide.get("swipe", True):
        sw = "SWIPE  →"
        espace(d, (W - M - largeur_espacee(d, sw, P("label", 20), 2.6) - 150, H - 82), sw, P("label", 20), acc, 2.6)
    return img, y


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    sortie = sys.argv[2]
    polices = sys.argv[3] if len(sys.argv) > 3 else "fonts"
    os.makedirs(sortie, exist_ok=True)
    total = len(spec["slides"])
    for i, s in enumerate(spec["slides"], 1):
        chemin = os.path.join(sortie, f"{spec['slug']}-{i:02d}.png")
        rendre(s, i, total, spec, polices).save(chemin, optimize=True)
        print(chemin)


if __name__ == "__main__":
    main()

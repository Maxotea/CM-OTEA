#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pierre Huiban, HYROX Cairo 14/11/2026 : visuel résultat 1080x1350, DA « trois vies ».

Vraie photo de la banque de Pierre en plein cadre (aucune image générée), voile sombre
en haut et en bas, registre ATHLETE · FATHER · EXECUTIVE avec ATHLETE allumé, chrono
en JetBrains Mono, titre en Fraunces, pied ROAD TO HONG KONG · JUNE 2027.

Chiffres relevés sur HYRESULT le 14/11/2026 (résultat LR3MS4JI5CA8BD) :
1:06:12, 30e sur 176 en Pro Men, 4e des 35-39, première course Pro en solo.

Usage : python3 visuel_resultat.py PHOTO.jpg SORTIE.jpg [DECALAGE_VERTICAL 0..1]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H, M = 1080, 1350, 88
DAWN, BLANC, PALE, NUIT = (232, 98, 44), (246, 243, 237), (210, 205, 197), (12, 14, 18)
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F = {
    "titre": os.path.join(RACINE, "fonts/fraunces/Fraunces-SemiBold.ttf"),
    "label": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "mono": "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf",
    "mono_m": "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf",
}
FACETS = ("ATHLETE", "FATHER", "EXECUTIVE")

TEXTE = {
    "label": "HYROX CAIRO · PRO MEN",
    "titre": ["First Pro race", "on my own."],
    "chrono": "1:06:12",
    "stats": [("30th", " / 176"), ("4th", " AG 35-39")],
}


def p(k, t):
    return ImageFont.truetype(F[k], t)


def espace(d, xy, s, f, fill, track):
    x, y = xy
    for c in s:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return x


def larg(d, s, f, track):
    return sum(d.textlength(c, font=f) + track for c in s) - track


def cadrer(photo, dec):
    im = ImageOps.exif_transpose(photo).convert("RGB")
    w, h = im.size
    if w / h > W / H:
        nw = int(h * W / H)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w * H / W)
        y = int((h - nh) * dec)
        im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def voile():
    v = Image.new("L", (1, H))
    for y in range(H):
        if y < 300:
            a = int(190 * (1 - y / 300) ** 1.6)
        elif y > 470:
            t = min(1, (y - 470) / 300)
            a = int(238 * t ** 0.85)
        else:
            a = 0
        v.putpixel((0, y), a)
    return v.resize((W, H))


def main():
    photo, sortie = sys.argv[1:3]
    dec = float(sys.argv[3]) if len(sys.argv) > 3 else 0.12
    img = Image.composite(Image.new("RGB", (W, H), NUIT), cadrer(Image.open(photo), dec), voile())
    d = ImageDraw.Draw(img)

    # registre
    y0 = 72
    espace(d, (M, y0), "PIERRE HUIBAN", p("label", 24), BLANC, 3.4)
    fl = p("label", 21)
    mots = []
    for i, fac in enumerate(FACETS):
        mots.append((fac, fac == "ATHLETE"))
        if i < 2:
            mots.append(("·", False))
    total = sum(larg(d, m, fl, 2.6) for m, _ in mots) + 14 * (len(mots) - 1)
    x = W - M - total
    for m, on in mots:
        x = espace(d, (x, y0 + 2), m, fl, DAWN if on else PALE, 2.6) + 14

    # bloc bas, construit de bas en haut
    yb = H - 118                      # filet du pied
    d.line([(M, yb), (W - M, yb)], fill=(110, 106, 100), width=2)
    espace(d, (M, yb + 30), "ROAD TO HONG KONG · JUNE 2027", p("label", 22), PALE, 2.8)

    # stats
    fs, fsm = p("mono", 40), p("mono_m", 32)
    ys = yb - 92
    x = M
    for i, (fort, reste) in enumerate(TEXTE["stats"]):
        d.text((x, ys), fort, font=fs, fill=DAWN)
        x += d.textlength(fort, font=fs)
        d.text((x, ys + 7), reste, font=fsm, fill=BLANC)
        x += d.textlength(reste, font=fsm)
        if i < len(TEXTE["stats"]) - 1:
            x += 26
            d.text((x, ys + 4), "·", font=fsm, fill=PALE)
            x += d.textlength("·", font=fsm) + 26

    # chrono
    fc = p("mono", 196)
    bb = d.textbbox((0, 0), TEXTE["chrono"], font=fc)
    yc = ys - 34 - bb[3]
    d.text((M - bb[0] + 2, yc), TEXTE["chrono"], font=fc, fill=BLANC)

    # titre
    ft = p("titre", 78)
    yt = yc + bb[1] - 40 - 2 * 88
    for i, ligne in enumerate(TEXTE["titre"]):
        d.text((M, yt + i * 88), ligne, font=ft, fill=BLANC)

    # label
    espace(d, (M, yt - 62), TEXTE["label"], p("label", 26), DAWN, 3.4)

    img.save(sortie, quality=93, subsampling=0)
    print(sortie)


if __name__ == "__main__":
    main()

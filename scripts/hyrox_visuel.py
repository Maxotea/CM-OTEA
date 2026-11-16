#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Visuel « résultat de course » HYROX, 1080x1350, DA « trois vies » de Pierre Huiban.

    python3 scripts/hyrox_visuel.py PHOTO.jpg SPEC.json SORTIE.jpg [--masque M.png] [--decalage 0.1]

SPEC.json : {"label": "HYROX CAIRO · PRO MEN", "titre": ["First Pro race", "on my own."],
             "chrono": "1:06:12", "stats": [["30th", " / 176"], ["4th", " AG 35-39"]],
             "facette": "ATHLETE"}

La photo suit la règle de Maxime du 14/11/2026 (.claude/memories/pierre-photo-nb-glow.md) :
noir et blanc contrasté, léger masque qui relève Pierre, glow sur les hautes lumières. La
couleur ne vit que dans la typo (accent « aube » #E8622C).

Le masque est un PNG en niveaux de gris (blanc = Pierre), fait une fois par photo et rangé
dans photos/pierre-huiban/masques/. Sans masque, un ovale doux centré sur `sujet` (x, y en
fractions de l'image source) fait office de masque : moins fin, mais jamais une découpe dure.

Dépendances : Pillow et numpy seulement, pour tourner tel quel dans GitHub Actions.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, M = 1080, 1350, 88
DAWN, BLANC, PALE, NUIT = (232, 98, 44), (246, 243, 237), (210, 205, 197), (10, 10, 10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACETS = ("ATHLETE", "FATHER", "EXECUTIVE")

# Polices : celles du dépôt d'abord, puis celles du système (runner Ubuntu ou session).
_CANDIDATS = {
    "titre": ["fonts/fraunces/Fraunces-SemiBold.ttf"],
    "label": ["fonts/inter/Inter-SemiBold.otf", "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
              "fonts/inter-display/InterDisplay-Medium.ttf"],
    "mono": ["fonts/jetbrains-mono/JetBrainsMono-Bold.ttf",
             "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", "fonts/space-mono/SpaceMono-Bold.ttf"],
    "mono_m": ["fonts/jetbrains-mono/JetBrainsMono-Medium.ttf",
               "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf", "fonts/space-mono/SpaceMono-Regular.ttf"],
}


def police(cle, taille):
    for c in _CANDIDATS[cle]:
        p = c if os.path.isabs(c) else os.path.join(ROOT, c)
        if os.path.exists(p):
            return ImageFont.truetype(p, taille)
    raise FileNotFoundError(f"aucune police pour « {cle} » : {_CANDIDATS[cle]}")


# ---------------------------------------------------------------- étalonnage

def _courbe_s(y, force=0.55, pivot=0.46):
    """Courbe en S douce autour du pivot : noirs profonds, blancs nets, médiums tenus."""
    t = np.where(y < pivot, y / pivot, (y - pivot) / (1 - pivot))
    s = t * t * (3 - 2 * t)                      # smoothstep
    t2 = t + force * (s - t)
    return np.where(y < pivot, t2 * pivot, pivot + t2 * (1 - pivot))


def _flou(a, rayon):
    im = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(rayon)), np.float32) / 255


def masque_ovale(taille, sujet=(0.45, 0.45), rx=0.32, ry=0.48):
    w, h = taille
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx / w - sujet[0]) / rx) ** 2 + ((yy / h - sujet[1]) / ry) ** 2
    return np.clip(1.4 - d, 0, 1)


def etalonner(img, masque=None, glow=0.42, relief=0.10):
    """RGB -> N&B contrasté, Pierre relevé par le masque, glow sur les hautes lumières."""
    a = np.asarray(img.convert("RGB"), np.float32) / 255
    y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    y = _courbe_s(np.clip((y - 0.03) / 0.95, 0, 1))

    if masque is None:
        m = masque_ovale(img.size)
    else:
        m = np.asarray(masque.convert("L").resize(img.size, Image.LANCZOS), np.float32) / 255
    m = _flou(m, max(img.size) * 0.012)          # « léger » : la découpe ne se voit pas

    # Pierre : +exposition et micro-contraste ; le fond descend d'un cran.
    local = y - _flou(y, max(img.size) * 0.01)
    sujet = np.clip(y * (1 + relief) + local * 0.22, 0, 1)
    fond = y * (1 - relief * 1.6)
    y = sujet * m + fond * (1 - m)

    # Glow : hautes lumières seuillées, deux flous, posées en écran.
    seuil = 0.62
    hl = np.clip((y - seuil) / (1 - seuil), 0, 1) ** 1.4
    g = 0.6 * _flou(hl, max(img.size) * 0.012) + 0.4 * _flou(hl, max(img.size) * 0.04)
    y = 1 - (1 - y) * (1 - np.clip(g * glow, 0, 1))

    # Grain léger sur la luminance, comme les reels monologue.
    rng = np.random.default_rng(7)
    y = np.clip(y + rng.normal(0, 0.012, y.shape).astype(np.float32), 0, 1)
    out = (y * 255).astype(np.uint8)
    return Image.merge("RGB", [Image.fromarray(out)] * 3)


# ---------------------------------------------------------------- mise en page

def _espace(d, xy, s, f, fill, track):
    x, y = xy
    for c in s:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return x


def _larg(d, s, f, track):
    return sum(d.textlength(c, font=f) + track for c in s) - track


def cadrer(img, dec=0.12):
    im = ImageOps.exif_transpose(img).convert("RGB")
    w, h = im.size
    if w / h > W / H:
        nw = int(h * W / H)
        box = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
    else:
        nh = int(w * H / W)
        y = int((h - nh) * dec)
        box = (0, y, w, y + nh)
    return box


def _voile():
    v = Image.new("L", (1, H))
    for y in range(H):
        if y < 300:
            a = int(190 * (1 - y / 300) ** 1.6)
        elif y > 470:
            a = int(238 * min(1, (y - 470) / 300) ** 0.85)
        else:
            a = 0
        v.putpixel((0, y), a)
    return v.resize((W, H))


def composer(photo, spec, masque=None, decalage=0.12):
    photo = ImageOps.exif_transpose(photo).convert("RGB")
    box = cadrer(photo, decalage)
    if masque is not None:
        masque = masque.convert("L").resize(photo.size, Image.LANCZOS).crop(box).resize((W, H))
    fond = photo.crop(box).resize((W, H), Image.LANCZOS)
    fond = etalonner(fond, masque)
    img = Image.composite(Image.new("RGB", (W, H), NUIT), fond, _voile())
    d = ImageDraw.Draw(img)

    # registre
    y0 = 72
    _espace(d, (M, y0), "PIERRE HUIBAN", police("label", 24), BLANC, 3.4)
    fl = police("label", 21)
    mots = []
    for i, fac in enumerate(FACETS):
        mots.append((fac, fac == spec.get("facette", "ATHLETE")))
        if i < 2:
            mots.append(("·", False))
    x = W - M - (sum(_larg(d, m, fl, 2.6) for m, _ in mots) + 14 * (len(mots) - 1))
    for m, on in mots:
        x = _espace(d, (x, y0 + 2), m, fl, DAWN if on else PALE, 2.6) + 14

    # pied
    yb = H - 118
    d.line([(M, yb), (W - M, yb)], fill=(110, 110, 110), width=2)
    _espace(d, (M, yb + 30), spec.get("pied", "ROAD TO HONG KONG · JUNE 2027"), police("label", 22), PALE, 2.8)

    # stats
    fs, fsm = police("mono", 40), police("mono_m", 32)
    ys = yb - 92
    x = M
    stats = spec.get("stats", [])
    for i, (fort, reste) in enumerate(stats):
        d.text((x, ys), fort, font=fs, fill=DAWN)
        x += d.textlength(fort, font=fs)
        d.text((x, ys + 7), reste, font=fsm, fill=BLANC)
        x += d.textlength(reste, font=fsm)
        if i < len(stats) - 1:
            x += 26
            d.text((x, ys + 4), "·", font=fsm, fill=PALE)
            x += d.textlength("·", font=fsm) + 26

    # chrono
    taille = 196
    fc = police("mono", taille)
    while d.textlength(spec["chrono"], font=fc) > W - 2 * M and taille > 120:
        taille -= 8
        fc = police("mono", taille)
    bb = d.textbbox((0, 0), spec["chrono"], font=fc)
    yc = ys - 34 - bb[3]
    d.text((M - bb[0] + 2, yc), spec["chrono"], font=fc, fill=BLANC)

    # titre et label
    ft = police("titre", 78)
    lignes = spec.get("titre", [])
    yt = yc + bb[1] - 40 - len(lignes) * 88
    for i, ligne in enumerate(lignes):
        d.text((M, yt + i * 88), ligne, font=ft, fill=BLANC)
    _espace(d, (M, yt - 62), spec["label"], police("label", 26), DAWN, 3.4)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("spec")
    ap.add_argument("sortie")
    ap.add_argument("--masque")
    ap.add_argument("--decalage", type=float, default=0.12)
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    masque = Image.open(a.masque) if a.masque else None
    composer(Image.open(a.photo), spec, masque, a.decalage).save(a.sortie, quality=93, subsampling=0)
    print(a.sortie)


if __name__ == "__main__":
    main()

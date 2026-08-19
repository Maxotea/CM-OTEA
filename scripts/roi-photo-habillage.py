#!/usr/bin/env python3
"""Run On Invest — habillage typographique par-dessus une photo IA.

Complète `roi-visuels.py` (cartes 100 % typographiques). Ici la DA du kit V2.1
est posée sur une photo IA ultra réaliste, autorisée par Maxime le 04/08/2026
pour ce seul compte, feed ET stories.

    ⚠️ Limite absolue : aucune personne réelle identifiable.
       Coureurs génériques, plans larges ou de dos. On ne génère jamais le
       visage d'un client, d'un participant ou de Maxime.

Deux sorties :
  * `feed(src, dst, lignes, kick)`  → 1080×1350, la photo est aplatie dans le JPG
  * `story(dst, lignes, kick)`      → 1080×1920, calque PNG transparent à
    superposer en ffmpeg sur la vidéo i2v (voir plus bas)

Prérequis (sandbox Higgsfield) :
    mkdir -p f o
    curl -sL -o f/archivo.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf"
    curl -sL -o f/mono.ttf    "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/SpaceMono-Regular.ttf"

Assemblage story (photo IA → i2v kling3_0_turbo 9:16 5 s → calque → MUET) :
    ffmpeg -y -i o/v1.mp4 -i o/o1.png -filter_complex \
      "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,\
crop=1080:1920,fps=25[bg];[bg][1:v]overlay=0:0[v]" \
      -map "[v]" -an -c:v libx264 -preset veryfast -crf 21 -t 5.2 o/r1.mp4

Le `-an` n'est pas optionnel : règle « stories sans son »
(`.claude/memories/stories-sans-son.md`).
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageChops

B = (255, 74, 23); E = (237, 231, 221); N = (17, 17, 17)
FD = "f"                       # dossier des polices
LIEU = "LA DÉFENSE"            # déverrouillé par Maxime le 04/08/2026


def af(s, w=125, g=900):
    """Archivo variable, axe wdth=125 (Expanded), wght=900."""
    f = ImageFont.truetype(FD + "/archivo.ttf", s)
    try:
        f.set_variation_by_axes([w, g])
    except Exception:
        pass
    return f


def mo(s):
    return ImageFont.truetype(FD + "/mono.ttf", s)


def ls(d, x, y, t, f, c, tr):
    """Texte lettre à lettre, interlettrage négatif du kit (−3,5 %)."""
    for ch in t:
        d.text((x, y), ch, font=f, fill=c)
        x += d.textlength(ch, font=f) + tr


def wid(d, t, f, tr):
    return sum(d.textlength(c, font=f) for c in t) + tr * (len(t) - 1)


def _fit(d, lines, maxw, start):
    """Plus grand corps qui tient en pleine largeur."""
    s = start
    ft = af(s)
    while max(wid(d, x, ft, -0.035 * s) for x in lines) > maxw and s > 34:
        s -= 4
        ft = af(s)
    return s, ft


def _bloc(d, W, H, y_logo, y0, lines, kick, s, ft):
    """Logo + mention lieu + titre + barre Blaze + accroche."""
    m = int(W * 0.065)
    lg = int(W * 0.040)
    ls(d, m, y_logo, "R.O.I.", af(lg), E, -0.035 * lg)
    mm = mo(int(W * 0.021))
    d.text((W - m - d.textlength(LIEU, font=mm), y_logo + int(lg * 0.3)),
           LIEU, font=mm, fill=E)
    lh = int(s * 1.02)
    for i, x in enumerate(lines):
        ls(d, m, y0 + i * lh - int(s * 0.24), x, ft, E, -0.035 * s)
    by = y0 + lh * len(lines) + int(W * 0.035)
    d.rectangle([m, by, m + int(W * 0.20), by + int(W * 0.009)], fill=B)
    d.text((m, by + int(W * 0.038)), kick, font=mo(int(W * 0.022)), fill=E)


def feed(src, dst, lines, kick, W=1080, H=1350):
    """Photo IA recadrée + voile Encre + habillage. Sortie JPG aplatie."""
    im = Image.open(src).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    l = (im.width - W) // 2
    t = (im.height - H) // 2
    im = im.crop((l, t, l + W, t + H)).convert("RGBA")

    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sc)
    hgt = int(H * 0.55)                                   # voile bas
    for i in range(hgt):
        sd.line([(0, H - hgt + i), (W, H - hgt + i)], fill=N + (int(225 * (i / hgt) ** 1.5),))
    hat = int(H * 0.16)                                   # voile haut (logo)
    for i in range(hat):
        sd.line([(0, i), (W, i)], fill=N + (int(130 * (1 - i / hat) ** 1.4),))
    im = Image.alpha_composite(im, sc)

    d = ImageDraw.Draw(im)
    m = int(W * 0.065)
    s, ft = _fit(d, lines, W - 2 * m, int(W * 0.115))
    th = int(s * 1.02) * len(lines)
    _bloc(d, W, H, int(H * 0.055), H - int(H * 0.085) - th - int(W * 0.115),
          lines, kick, s, ft)

    n = Image.effect_noise((W, H), 22).convert("RGB")     # grain à moyenne nulle
    ImageChops.add(im.convert("RGB"), n, 1, -128).save(dst, quality=93)


def story(dst, lines, kick, W=1080, H=1920):
    """Calque PNG transparent 9:16 à superposer sur la vidéo i2v.

    Zones libres du kit respectées : logo à y=250, bloc titre calé sur 1450."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(im)
    hg = int(H * 0.46)
    for i in range(hg):
        sd.line([(0, H - hg + i), (W, H - hg + i)], fill=N + (int(220 * (i / hg) ** 1.5),))
    for i in range(340):
        sd.line([(0, i), (W, i)], fill=N + (int(140 * (1 - i / 340) ** 1.4),))

    d = ImageDraw.Draw(im)
    m = int(W * 0.065)
    s, ft = _fit(d, lines, W - 2 * m, int(W * 0.115))
    _bloc(d, W, H, 250, 1450 - int(s * 1.02) * len(lines), lines, kick, s, ft)
    im.save(dst)


# --- Contenu produit le 19/08/2026 ------------------------------------------
FEED = [("o/p1.png", "o/rf1.jpg", ["TROIS CAFÉS.", "OU UNE HEURE", "DE COURSE."],
         "ON COURT D'ABORD. ON PARLE ENSUITE."),
        ("o/p2.png", "o/rf2.jpg", ["LE FORMAT,", "SIMPLE."],
         "COURSE & NETWORKING — ENTREPRENEURS")]
STORY = [("o/o1.png", ["5 OU 10 KM.", "TON RYTHME."], "CE N'EST PAS UNE COURSE"),
         ("o/o2.png", ["LE", "FORMAT"], "COURSE, PUIS ÉCHANGE")]

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "feed"):
        for src, dst, lines, kick in FEED:
            feed(src, dst, lines, kick)
    if what in ("all", "story"):
        for dst, lines, kick in STORY:
            story(dst, lines, kick)

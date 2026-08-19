#!/usr/bin/env python3
"""J Lawson Golf — calque typographique des stories « vraies photos ».

Produit le PNG 1080×1920 transparent qui se pose sur la vidéo i2v animée
depuis une VRAIE photo du compte (règle `.claude/memories/stories-vraies-photos-sans-ia.md`).

DA J Lawson : Marine #0E1B2A · Vert #3E9E74 · Ambre #D99A4E · Crème #F2F0EC ·
Gris #A8B2BE. Titre Montserrat 800 auto-ajusté en pleine largeur, surtitre
ambre souligné, barre verte, sous-titre gris, signature verte.

Prérequis (sandbox Higgsfield) :
    mkdir -p f o
    curl -sL -o f/m.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
    python3 jlawson-photo-story.py

Chaîne complète d'un slot :
  1. crop 9:16 de la photo source, SANS texte incrusté
  2. `generate_video` kling3_0_turbo, 5 s, 9:16, prompt verrouillé sur l'identité,
     declined_preset_id 24bae836-2c4a-48e0-89b6-49fcc0b21612
  3. **contrôle visuel de la DERNIÈRE frame contre la photo source** — non négociable
  4. assemblage :
     ffmpeg -y -i o/v.mp4 -i o/a.png -filter_complex \
       "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,\
crop=1080:1920,fps=25[bg];[bg][1:v]overlay=0:0[v]" \
       -map "[v]" -an -c:v libx264 -preset veryfast -crf 21 -t 5.2 o/r.mp4
  5. media_upload / PUT / media_confirm, puis `bulk_schedule_stories` en BROUILLON

⚠️ Le `-an` est obligatoire : les stories partent muettes, Maxime pose l'audio
   lui-même dans Instagram (`.claude/memories/stories-sans-son.md`).
   `jlwav()` reste ici pour d'éventuels formats longs — il n'est PLUS appelé
   pour les stories.
"""
import math, struct, wave
from PIL import Image, ImageDraw, ImageFont

MAR = (14, 27, 42); VERT = (62, 158, 116); AMB = (217, 154, 78)
CRE = (242, 240, 236); GRI = (168, 178, 190)
FD = "f"


def F(sz, w=700):
    """Montserrat variable, axe wght."""
    f = ImageFont.truetype(FD + "/m.ttf", sz)
    try:
        f.set_variation_by_axes([w])
    except Exception:
        pass
    return f


def ls(d, x, y, t, f, c, tr):
    for ch in t:
        d.text((x, y), ch, font=f, fill=c)
        x += d.textlength(ch, font=f) + tr


def wid(d, t, f, tr):
    return sum(d.textlength(c, font=f) for c in t) + tr * (len(t) - 1)


def overlay(path, titre, sous):
    """Calque PNG transparent : voile marine haut et bas + bloc texte."""
    W, H = 1080, 1920
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sc)
    for i in range(760):                                  # voile bas
        sd.line([(0, H - 760 + i), (W, H - 760 + i)], fill=MAR + (int(215 * (i / 760.0) ** 1.6),))
    for i in range(300):                                  # voile haut
        sd.line([(0, i), (W, i)], fill=MAR + (int(150 * (1 - i / 300.0) ** 1.4),))
    im = Image.alpha_composite(im, sc)
    d = ImageDraw.Draw(im)

    fm = F(30, 600)
    ls(d, 88, 250, "J LAWSON GOLF", fm, AMB, 7)
    d.rectangle([88, 300, 88 + wid(d, "J LAWSON GOLF", fm, 7), 303], fill=AMB)

    s = 96; ft = F(s, 800)
    while wid(d, titre, ft, -2) > W - 176 and s > 44:
        s -= 4
        ft = F(s, 800)
    ty = 1330
    ls(d, 88, ty, titre, ft, CRE, -2)
    d.rectangle([88, ty + s + 34, 196, ty + s + 40], fill=VERT)
    d.text((88, ty + s + 78), sous, font=F(38, 500), fill=GRI)
    ls(d, 88, ty + s + 150, "TON MATÉRIEL À TES MESURES", F(27, 600), VERT, 5)
    im.save(path)


def jlwav(path, dur=5.6, sr=44100):
    """Nappe J Lawson (Am9 + appuis) — synthèse pure, zéro sample, zéro droits.

    ⚠️ Plus appelé pour les stories depuis la règle du 04/08/2026.
    Conservé pour reels ou montages longs si Maxime le redemande."""
    n = int(dur * sr); acc = [110.0, 164.81, 220.0, 277.18, 329.63]; bt = 0.6
    a = []
    for i in range(n):
        t = i / sr
        pad = sum(math.sin(2 * math.pi * f * t) + 0.15 * math.sin(2 * math.pi * f * 2 * t)
                  for f in acc) / len(acc)
        pad *= min(1.0, t / 1.2) * (0.82 + 0.18 * math.sin(2 * math.pi * 0.25 * t))
        ph = (t / (bt / 2)) % 1.0
        bas = math.sin(2 * math.pi * 55.0 * t) * math.exp(-6.0 * ph) * 0.55
        e = 0.30 * pad + 0.22 * bas
        e *= 1.0 if t < dur - 0.9 else max(0.0, 1 - (t - (dur - 0.9)) / 0.9)
        e *= min(1.0, t / 0.25)
        a.append(max(-1, min(1, e)))
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b"".join(struct.pack("<h", int(v * 32767)) for v in a)); w.close()


# --- Slots produits (photos réelles 03, 06, 09 du compte) -------------------
SLOTS = [("a", "LE SHAFT", "Flex, poids, torque : le moteur de ton club"),
         ("b", "LA DATA PARLE", "Chaque club validé au launch monitor"),
         ("c", "CÔTÉ ATELIER", "Montage, gripping, loft-lie : fait ici")]

if __name__ == "__main__":
    for tag, ti, so in SLOTS:
        overlay("o/%s.png" % tag, ti, so)

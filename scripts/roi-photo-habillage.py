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
    """Archivo variable : wdth=125 (Expanded), wght=900.

    ⚠️ L'ordre des axes du fichier Archivo est **[Weight, Width]**, pas
    l'inverse — vérifié le 20/08/2026 avec `ImageFont.get_variation_axes()`.
    Passer [w, g] écrivait donc en graisse 125 (Thin) au lieu de 900."""
    f = ImageFont.truetype(FD + "/archivo.ttf", s)
    try:
        f.set_variation_by_axes([g, w])
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


def scrim(W, H, grad_h, grad_max, flat_h):
    """Voile Encre : dégradé bas + palier plat + voile haut pour le logo.

    Le palier plat (alpha 100, fondu sur 150 px) est ce qui garantit la
    lisibilité du titre même sur une photo claire — le dégradé seul ne
    suffisait pas sur les plans de verre en plein jour."""
    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sc)
    hgt = int(H * grad_h)
    for i in range(hgt):
        sd.line([(0, H - hgt + i), (W, H - hgt + i)],
                fill=N + (int(grad_max * (i / hgt) ** 1.25),))
    fl = int(H * flat_h); fe = 150
    for i in range(fl):
        a = 100 if i > fe else int(100 * i / fe)
        sd.line([(0, H - fl + i), (W, H - fl + i)], fill=N + (a,))
    hat = int(H * 0.16)
    for i in range(hat):
        sd.line([(0, i), (W, i)], fill=N + (int(130 * (1 - i / hat) ** 1.4),))
    return sc


def feed(src, dst, lines, kick, W=1080, H=1350):
    """Photo IA recadrée + voile Encre + habillage. Sortie JPG aplatie."""
    im = Image.open(src).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    l = (im.width - W) // 2
    t = (im.height - H) // 2
    im = im.crop((l, t, l + W, t + H)).convert("RGBA")

    im = Image.alpha_composite(im, scrim(W, H, 0.62, 238, 0.52))

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
    im = scrim(W, H, 0.50, 232, 0.42)
    d = ImageDraw.Draw(im)
    m = int(W * 0.065)
    s, ft = _fit(d, lines, W - 2 * m, int(W * 0.115))
    _bloc(d, W, H, 250, 1450 - int(s * 1.02) * len(lines), lines, kick, s, ft)
    im.save(dst)


# --- Vague 24/08 -> 11/09 (produite le 19/08/2026) --------------------------
# n : (photo, lignes feed, accroche feed, lignes story, accroche story)
SPEC = {
 1: ("b", ["ON COURT À", "LA DÉFENSE"], "5 OU 10 KM À TON RYTHME",
          ["LA", "DÉFENSE"], "LE PARVIS AVANT TOUT LE MONDE"),
 2: ("d", ["CE N'EST PAS", "UN CLUB DE", "RUNNING."], "NI UN AFTERWORK.",
          ["NI CLUB.", "NI AFTERWORK."], "UNE HEURE D'EFFORT PARTAGÉ"),
 3: ("e", ["POUR", "QUI ?"], "ENTREPRENEURS & INDÉPENDANTS",
          ["AUCUN", "NIVEAU", "REQUIS"], "5 KM, C'EST DÉJÀ ASSEZ"),
 4: ("g", ["PERSONNE", "NE VEND", "EN MONTÉE."], "ZÉRO PITCH",
          ["ZÉRO", "PITCH"], "C'EST LA RÈGLE"),
 5: ("f", ["AU 3E KM,", "PLUS PERSONNE", "NE JOUE", "UN RÔLE."], "L'EFFORT CRÉE LE LIEN",
          ["AU 3E KM"], "L'EFFORT CRÉE LE LIEN"),
 6: ("c", ["PUIS ON SE", "POSE À LA", "PLÉNITUDE", "ARENA."], "LA MOITIÉ LA PLUS IMPORTANTE",
          ["PUIS ON", "SE POSE"], "PLÉNITUDE ARENA"),
 7: ("h", ["LA", "RÉGULARITÉ", "PAIE."], "UN RENDEZ-VOUS QUI REVIENT",
          ["REVENIR."], "SIX SORTIES, ET TU AS UN RÉSEAU"),
 8: ("j", ["TON", "RYTHME.", "PAS LE", "LEUR."], "AUCUN CHRONO, AUCUN CLASSEMENT",
          ["TON", "RYTHME"], "AUCUN CHRONO, AUCUN CLASSEMENT"),
 9: ("k", ["ON COURT", "D'ABORD.", "ON PARLE", "ENSUITE."], "COURSE & NETWORKING — ENTREPRENEURS",
          ["TU", "VIENS ?"], "ÉCRIS-NOUS EN MESSAGE PRIVÉ"),
}

# Photos IA sources (Higgsfield soul_2, 9:16, « La Défense au petit matin »).
# Le nom de fichier contient le job_id, réutilisable tel quel en i2v.
PHOTOS = {
 "b": "hf_20260819_061202_7a4cbd5c-5e4d-4a2b-94f7-1a96527ac368",
 "c": "hf_20260819_061209_5ae1591b-c2f4-4f81-8136-37ef6dd7653f",
 "d": "hf_20260819_062155_d7f350d9-ae44-4f74-902e-039c6c66404d",
 "e": "hf_20260819_062203_ab8461bc-f68b-41fa-96fa-4689a2c12734",
 "f": "hf_20260819_062210_d92d19d2-2b71-42ff-bc10-2b6882de0063",
 "g": "hf_20260819_062216_9d594010-ca3c-4346-a997-52822c3be685",
 "h": "hf_20260819_062225_e79651fd-40dc-49c5-8b78-27c25a59a608",
 "j": "hf_20260819_093549_af7695fd-3b2b-46f7-a4a9-b9d0035cd182",
 "k": "hf_20260819_093549_43d3c644-db6d-4dc0-912b-95a7f1ed1dc8",
}
CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/"

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    todo = [int(x) for x in sys.argv[2:]] or sorted(SPEC)
    for n in todo:
        ph, fl, fk, sl, sk = SPEC[n]
        if mode in ("all", "feed"):
            feed("r/%s.png" % ph, "o/f%d.jpg" % n, fl, fk)
        if mode in ("all", "story"):
            story("o/s%d.png" % n, sl, sk)

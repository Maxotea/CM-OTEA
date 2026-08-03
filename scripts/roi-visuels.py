#!/usr/bin/env python3
"""Visuels Run On Invest — DA typographique du kit V2.1.

Génère les cartes feed (1080x1350) et les stories animées (1080x1920 + son)
du compte R.O.I. Zéro IA générative, zéro photo, zéro sample tiers :
tout est dessiné en PIL et animé/sonorisé en ffmpeg + oscillateurs purs.

Prérequis (à exécuter dans la sandbox Higgsfield, qui a ffmpeg) :
    mkdir -p f o
    curl -sL -o f/archivo.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf"
    curl -sL -o f/mono.ttf    "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/SpaceMono-Regular.ttf"
    curl -sL -o f/monob.ttf   "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/SpaceMono-Bold.ttf"
    python3 roi-visuels.py s1 s2 f1 f2 ...

DA : Blaze #FF4A17 · Encre #111111 · Écru #EDE7DD · Craie #F7F4EF.
Trois familles jamais mélangées : "e" = fond Écru, "n" = fond Encre, "b" = aplat Blaze.
Archivo Expanded 900 pour les titres (interlettrage -3,5 %), Space Mono pour les mentions.
"""
import sys, os, math, wave, struct, random
from PIL import Image, ImageDraw, ImageFont, ImageChops

B = (255, 74, 23); E = (237, 231, 221); N = (17, 17, 17); C = (247, 244, 239)
F = os.environ.get("ROI_FONTS", "/home/user/f")


def af(s, w=125, g=900):
    """Archivo variable, axe wdth=125 (Expanded), wght=900."""
    f = ImageFont.truetype(F + "/archivo.ttf", s)
    try:
        f.set_variation_by_axes([w, g])
    except Exception:
        pass
    return f


def mo(s, b=0):
    return ImageFont.truetype(F + "/mono%s.ttf" % ("b" if b else ""), s)


def tw(d, t, f, tr):
    return sum(d.textlength(c, font=f) for c in t) + tr * (len(t) - 1)


def dt(d, x, y, t, f, col, tr):
    """Texte lettre à lettre pour appliquer l'interlettrage négatif."""
    for c in t:
        d.text((x, y), c, font=f, fill=col)
        x += d.textlength(c, font=f) + tr


def fit(d, lines, maxw, cap):
    """Plus grand corps qui tient en pleine largeur, interlettrage -3,5 %."""
    s = cap
    while s > 24:
        f = af(s); tr = -0.035 * s
        if max(tw(d, l, f, tr) for l in lines) <= maxw:
            return f, tr
        s -= 4
    return af(24), -0.84


def grain(im, k=26):
    """Grain 26 % à moyenne nulle (n'altère pas la luminance des aplats)."""
    n = Image.effect_noise(im.size, k).convert("RGB")
    return ImageChops.add(im, n, 1, -128)


def card(it, W, H, story):
    fam = it["f"]
    bg, tx, ac = (E, N, B) if fam == "e" else ((N, C, B) if fam == "n" else (B, N, N))
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    m = int(W * 0.065)
    top = int(H * 0.105) if story else m          # story : sous la zone libre de 200 px
    ls = int(W * 0.040); lf = af(ls)
    dt(d, m, top, "R.O.I.", lf, tx, -0.035 * ls)
    mm = mo(int(W * 0.021))
    t = it["m"]; wt = d.textlength(t, font=mm)
    d.text((W - m - wt, top + int(ls * 0.30)), t, font=mm, fill=tx)
    lines = it["t"]
    f, tr = fit(d, lines, W - 2 * m, int(W * 0.135) if len(lines) > 2 else int(W * 0.20))
    lh = int(f.size * 1.00); th = lh * len(lines)
    y0 = (H - th) // 2 - int(H * 0.02)
    for i, l in enumerate(lines):
        dt(d, m, y0 + i * lh - int(f.size * 0.24), l, f, tx, tr)
    by = y0 + th + int(W * 0.045)
    d.rectangle([m, by, m + int(W * 0.20), by + int(W * 0.008)], fill=ac)   # barre Blaze
    kf = mo(int(W * 0.022), 1)
    d.text((m, by + int(W * 0.042)), it["k"], font=kf, fill=tx)
    ff = mo(int(W * 0.018))
    fy = H - int(H * 0.115) - int(W * 0.018) if story else H - m - int(W * 0.018)
    d.text((m, fy), "COURSE & NETWORKING — ENTREPRENEURS", font=ff, fill=tx)
    return grain(im)


def wav(p, dur=5.6, sr=44100):
    """Lit sonore R.O.I. : cadence de foulée ~168 BPM + drone + motif clair.
    Synthèse pure (sinus + enveloppes), aucun sample, aucun modèle → zéro droits."""
    n = int(dur * sr); a = [0.0] * n; spb = 60.0 / 168
    random.seed(7)
    for k in range(int(dur / spb) + 1):                 # appuis au sol
        s = int(k * spb * sr)
        for i in range(int(0.16 * sr)):
            if s + i >= n: break
            t = i / sr; env = math.exp(-t * 26)
            a[s + i] += 0.44 * env * math.sin(2 * math.pi * 54 * t)
        for i in range(int(0.05 * sr)):                 # souffle court
            if s + i >= n: break
            t = i / sr; env = math.exp(-t * 70)
            a[s + i] += 0.05 * env * (random.random() * 2 - 1)
    for i in range(n):                                  # drone
        t = i / sr
        a[i] += 0.055 * math.sin(2 * math.pi * 110 * t) + 0.03 * math.sin(2 * math.pi * 165 * t)
    for k, fq in enumerate([440.0, 587.33, 659.25, 587.33]):   # motif
        s = int((0.35 + k * 1.30) * sr)
        for i in range(int(1.0 * sr)):
            if s + i >= n: break
            t = i / sr; env = math.exp(-t * 3.4) * min(1, t * 60)
            a[s + i] += 0.10 * env * math.sin(2 * math.pi * fq * t)
    for i in range(n):                                  # fondus + limiteur
        g = min(1, i / (0.25 * sr)) * min(1, (n - i) / (0.45 * sr))
        a[i] = max(-1, min(1, a[i] * g * 0.9))
    w = wave.open(p, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b"".join(struct.pack("<h", int(v * 32767)) for v in a)); w.close()


# --- Contenu : (nom, famille, lignes de titre, mention mono, accroche) -------
S = [("s1", "b", ["ÇA", "DÉMARRE"], "R.O.I. — 03.08", "QUELQUE CHOSE COMMENCE"),
     ("s2", "n", ["NI CLUB.", "NI AFTERWORK."], "R.O.I. — 05.08", "UNE HEURE D'EFFORT PARTAGÉ"),
     ("s3", "e", ["POUR LES", "ENTREPRENEURS", "ET LES", "INDÉPENDANTS"], "R.O.I. — 07.08", "AUCUN NIVEAU REQUIS"),
     ("s4", "n", ["ON COURT", "D'ABORD.", "ON PARLE", "ENSUITE."], "R.O.I. — 10.08", "5 OU 10 KM À TON RYTHME"),
     ("s5", "e", ["AU 3E KM,", "PLUS PERSONNE", "NE PITCHE"], "R.O.I. — 12.08", "L'EFFORT CRÉE LE LIEN"),
     ("s6", "b", ["ZÉRO", "PITCH"], "R.O.I. — 14.08", "C'EST LA RÈGLE"),
     ("s7", "e", ["LA", "RÉGULARITÉ", "PAIE"], "R.O.I. — 17.08", "UN RENDEZ-VOUS QUI REVIENT"),
     ("s8", "n", ["5 OU 10 KM.", "TON RYTHME."], "R.O.I. — 19.08", "CE N'EST PAS UNE COURSE"),
     ("s9", "b", ["LE", "FORMAT"], "R.O.I. — 21.08", "COURSE, PUIS ÉCHANGE")]
FD = [("f1", "b", ["RUN", "ON", "INVEST"], "COURSE & NETWORKING", "ON COURT D'ABORD. ON PARLE ENSUITE."),
      ("f2", "n", ["CE N'EST PAS", "UN CLUB DE", "RUNNING."], "R.O.I.", "NI UN AFTERWORK."),
      ("f3", "e", ["POUR", "QUI ?"], "R.O.I.", "ENTREPRENEURS & INDÉPENDANTS"),
      ("f4", "n", ["ON COURT", "D'ABORD.", "ON PARLE", "ENSUITE."], "RUN ON INVEST", "COURSE & NETWORKING"),
      ("f5", "e", ["ON NE SE", "PRÉSENTE PAS.", "ON SE", "DÉCOUVRE."], "PILIER 01", "L'EFFORT CRÉE LE LIEN"),
      ("f6", "b", ["PERSONNE", "NE VEND", "EN MONTÉE."], "PILIER 02", "ZÉRO PITCH"),
      ("f7", "e", ["LA", "RÉGULARITÉ", "PAIE."], "PILIER 03", "UN RENDEZ-VOUS QUI REVIENT"),
      ("f8", "n", ["TROIS CAFÉS", "RÉSEAU.", "OU UNE HEURE", "DE COURSE."], "R.O.I.", "ON COURT D'ABORD."),
      ("f9", "e", ["LE FORMAT,", "SIMPLE."], "R.O.I.", "5 OU 10 KM · PUIS UN CAFÉ")]
ALL = {x[0]: {"f": x[1], "t": x[2], "m": x[3], "k": x[4]} for x in S + FD}

STORY_FILTER = (
    "[0:v]scale=1350:2400,"
    "zoompan=z='min(1.0+0.055*on/135,1.06)':d=138:s=1080x1920:fps=25,"
    "drawbox=x=88:y=ih-260:w='min(904,904*t/1.8)':h=10:color=0xFF4A17@1:t=fill,"
    "fade=t=in:st=0:d=0.45,fade=t=out:st=5.05:d=0.45,format=yuv420p[v]"
)


def build(name):
    it = ALL[name]; story = name[0] == "s"
    im = card(it, 1350, 2400 if story else 1688, story)
    im.save("o/%s.png" % name)
    if story:
        if not os.path.exists("o/roi.wav"):
            wav("o/roi.wav")
        os.system(
            'ffmpeg -y -loglevel error -loop 1 -i o/%s.png -i o/roi.wav '
            '-filter_complex "%s" -map "[v]" -map 1:a '
            '-c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k -shortest -t 5.5 o/%s.mp4'
            % (name, STORY_FILTER, name))
    else:
        os.system("ffmpeg -y -loglevel error -i o/%s.png -vf scale=1080:1350 -q:v 2 o/%s.jpg"
                  % (name, name))


if __name__ == "__main__":
    for a in sys.argv[1:]:
        build(a)

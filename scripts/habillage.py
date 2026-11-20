#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Habillage dynamique d'une vidéo montée : textes animés, voix off, ducking.

Deuxième passe après `scripts/aftermovie.py`. On part de la vidéo montée
(bout-à-bout validé) et d'un fichier `habillage.json` qui dit **quoi
incruster, quand, et dans quel style**. Le script rend chaque élément en
séquence d'images RGBA (PIL), l'incruste avec ffmpeg, et mixe la voix off
par-dessus la bande son en la faisant passer devant (ducking).

## Le fichier habillage.json

    {
      "accent": "#FF5800",          # couleur des barres et surlignages
      "police": null,               # chemin d'une .ttf/.ttc, sinon auto
      "voix": "vocal.m4a",          # voix off à mixer (optionnel)
      "voix_decalage": 0.0,         # la voix commence à cette seconde
      "elements": [
        {"t": 3.2, "duree": 2.2, "style": "punch",
         "texte": "KHADIJA\\nSALOMON"},
        {"t": 8.0, "duree": 3.5, "style": "bandeau",
         "texte": "Khadija Salomon", "sous": "Fondatrice"},
        {"t": 15.0, "duree": 2.5, "style": "chiffre",
         "valeur": 120, "suffixe": "", "texte": "participants"},
        {"t": 20.0, "duree": 2.0, "style": "mot",
         "texte": "Innovation", "position": "haut-droite"},
        {"t": 30.0, "duree": 4.0, "style": "liste",
         "lignes": ["Ateliers", "Conférences", "Networking"]}
      ]
    }

## Les cinq styles

- **punch** — un ou plusieurs mots en très gros, centrés, qui claquent
  à l'image (arrivée en sur-échelle avec rebond, un mot après l'autre),
  sur un surlignage accent. Pour un nom, une idée forte.
- **bandeau** — le synthé bas-gauche : barre accent qui glisse, nom et
  fonction révélés à sa suite. Pour présenter une personne.
- **chiffre** — un grand nombre qui compte de 0 à la valeur, avec son
  unité et une légende. Pour un résultat.
- **mot** — une étiquette dans un coin (`position` : haut-gauche,
  haut-droite, bas-gauche, bas-droite), qui pop. Pour un mot-clé.
- **liste** — jusqu'à cinq lignes qui apparaissent l'une après l'autre
  avec un tiret accent. Pour un programme, des étapes.

Chaque élément a `t` (seconde d'apparition) et `duree` (secondes à
l'écran, sortie comprise). Les entrées/sorties sont animées.

## La voix off

`voix` est mixée au-dessus de la piste existante (ambiance + musique). La
piste existante est compressée par la voix (sidechain) : elle baisse quand
la voix parle, revient quand elle se tait. Le tout est normalisé -14 LUFS.

## Usage

    python3 scripts/habillage.py o/salomon-aftermovie.mp4 \\
        aftermovies/salomon/habillage.json --sortie o/salomon-final.mp4

`--apercu 12.5` sort une seule image PNG à cette seconde pour vérifier un
élément sans rendre tout le film.
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

FPS = 25
BLANC = (241, 241, 241)
ENCRE = (32, 30, 30)
ACCENT_DEFAUT = "#FF5800"

POLICES = [
    os.path.expanduser("~/Desktop/DOC/CHARTRE GRAPHIQUE OTEA PRODUCTION/FONT/"
                       "FormaDJRDisplay-Black-Testing.ttf"),
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


# ---------------------------------------------------------------- outils ---

def log(msg):
    print(msg, flush=True)


def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True)
    if r.returncode != 0:
        sys.exit("✗ %s …\n%s" % (" ".join(cmd[:3]), r.stderr[-2000:]))
    return r


def trouver_ffmpeg(indice):
    if indice and os.path.exists(indice):
        return indice
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("✗ ffmpeg introuvable : PATH ou --ffmpeg")


def dimensions(ffmpeg, video):
    r = subprocess.run([ffmpeg, "-hide_banner", "-i", video],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", r.stderr)
    d = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", r.stderr)
    if not m or not d:
        sys.exit("✗ vidéo illisible : %s" % video)
    return int(m[1]), int(m[2]), int(d[1]) * 3600 + int(d[2]) * 60 + float(d[3])


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


_polices = {}


def police(taille, chemin=None):
    cle = (taille, chemin)
    if cle in _polices:
        return _polices[cle]
    for c in ([chemin] if chemin else []) + POLICES:
        if c and os.path.exists(c):
            try:
                _polices[cle] = ImageFont.truetype(c, taille)
                return _polices[cle]
            except OSError:
                continue
    _polices[cle] = ImageFont.load_default()
    return _polices[cle]


# ------------------------------------------------------------- easings ---

def clamp(x):
    return max(0.0, min(1.0, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x ** 3


def ease_back(x):
    """Arrivée avec léger dépassement puis retour : le « claque »."""
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def sortie(x, duree, fin=0.35):
    """Facteur 1 → 0 sur les `fin` dernières secondes."""
    return 1.0 - ease_in((x - (duree - fin)) / fin) if x > duree - fin else 1.0


def texte_dims(font, texte):
    b = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), texte, font=font)
    return b[2] - b[0], b[3] - b[1], b[0], b[1]


def coller_texte(calque, xy, texte, font, fill, alpha=1.0, echelle=1.0,
                 ombre=True):
    """Écrit un texte avec transparence, échelle et ombre douce, centré sur xy."""
    w, h, ox, oy = texte_dims(font, texte)
    if w == 0 or h == 0:
        return
    marge = max(8, h // 6)
    tmp = Image.new("RGBA", (w + 2 * marge, h + 2 * marge), (0, 0, 0, 0))
    if ombre:
        # ombre portée floue : lisible sur n'importe quel plan
        om = Image.new("RGBA", tmp.size, (0, 0, 0, 0))
        ImageDraw.Draw(om).text((marge - ox + h * 0.03, marge - oy + h * 0.05),
                                texte, font=font,
                                fill=(0, 0, 0, int(150 * clamp(alpha))))
        tmp.alpha_composite(om.filter(ImageFilter.GaussianBlur(max(2, h // 12))))
    ImageDraw.Draw(tmp).text((marge - ox, marge - oy), texte, font=font,
                             fill=fill + (int(255 * clamp(alpha)),))
    if abs(echelle - 1.0) > 0.001:
        tmp = tmp.resize((max(1, int(tmp.width * echelle)),
                          max(1, int(tmp.height * echelle))), Image.LANCZOS)
    calque.alpha_composite(tmp, (int(xy[0] - tmp.width / 2),
                                 int(xy[1] - tmp.height / 2)))


# --------------------------------------------------------------- styles ---
# Chaque style est une fonction (W, H, el, cfg, x) -> image RGBA pleine
# taille pour l'instant x (secondes depuis l'apparition de l'élément).

def style_punch(W, H, el, cfg, x):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mots = [m for m in re.split(r"\\n|\n", el["texte"]) if m.strip()]
    taille = int(H * el.get("taille", 0.16))
    f = police(taille, cfg.get("police"))
    interligne = int(taille * 1.15)
    y0 = H // 2 - interligne * (len(mots) - 1) // 2
    s = sortie(x, el["duree"])
    for i, mot in enumerate(mots):
        debut = i * 0.18                        # un mot après l'autre
        p = (x - debut) / 0.32
        if p <= 0:
            continue
        e = ease_back(p)
        echelle = 1.9 - 0.9 * e                 # arrive en sur-échelle
        alpha = ease_out(p * 2) * s
        w, h, _, _ = texte_dims(f, mot)
        y = y0 + i * interligne
        # surlignage accent qui s'ouvre de gauche à droite sous le mot
        larg = int((w + taille * 0.5) * ease_out(p) * s)
        if larg > 0:
            bar = Image.new("RGBA", (larg, int(taille * 0.42)),
                            cfg["accent"] + (int(235 * s),))
            im.alpha_composite(bar, (int(W / 2 - (w + taille * 0.5) / 2),
                                     int(y + taille * 0.35)))
        coller_texte(im, (W // 2, y + taille * 0.45), mot, f, BLANC,
                     alpha, echelle * (0.92 + 0.08 * s))
    return im


def style_bandeau(W, H, el, cfg, x):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    marge = int(W * 0.06)
    t_nom = int(H * 0.06)
    t_sous = int(H * 0.03)
    f_nom = police(t_nom, cfg.get("police"))
    f_sous = police(t_sous, cfg.get("police"))
    s = sortie(x, el["duree"])
    y = H - int(H * 0.16)
    # la barre accent glisse depuis la gauche
    p = ease_out(x / 0.4)
    haut = t_nom + t_sous + int(H * 0.035)
    larg_barre = int(W * 0.012)
    bx = int(-larg_barre + (marge + larg_barre) * p * s)
    d.rectangle([bx, y - haut // 2, bx + larg_barre, y + haut // 2],
                fill=cfg["accent"] + (255,))
    # le texte se révèle à droite de la barre (masque qui s'ouvre)
    p2 = ease_out((x - 0.15) / 0.45)
    w_nom, _, _, _ = texte_dims(f_nom, el["texte"])
    w_sous, _, _, _ = texte_dims(f_sous, el.get("sous", ""))
    w_max = max(w_nom, w_sous) + int(W * 0.02)
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(calque)
    tx = marge + larg_barre + int(W * 0.015)
    # fond semi-transparent derrière le texte pour la lisibilité
    dc.rectangle([tx - int(W * 0.012), y - haut // 2, tx + w_max,
                  y + haut // 2], fill=ENCRE + (150,))
    dc.text((tx, y - haut // 2 + int(H * 0.012)), el["texte"], font=f_nom,
            fill=BLANC + (255,))
    if el.get("sous"):
        dc.text((tx, y + haut // 2 - t_sous - int(H * 0.018)), el["sous"],
                font=f_sous, fill=cfg["accent"] + (255,))
    masque = Image.new("L", (W, H), 0)
    ImageDraw.Draw(masque).rectangle(
        [0, 0, tx + int((w_max + int(W * 0.012)) * p2 * s), H], fill=255)
    calque.putalpha(ImageChops.multiply(calque.split()[3], masque))
    im.alpha_composite(calque)
    return im


def style_chiffre(W, H, el, cfg, x):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    valeur = float(el["valeur"])
    p = ease_out(x / min(1.2, el["duree"] * 0.5))
    s = sortie(x, el["duree"])
    courant = valeur * p
    decimales = el.get("decimales", 0)
    txt = ("%%.%df" % decimales % courant).replace(".", ",") + el.get("suffixe", "")
    if el.get("prefixe"):
        txt = el["prefixe"] + txt
    t_chiffre = int(H * el.get("taille", 0.22))
    f = police(t_chiffre, cfg.get("police"))
    f_leg = police(int(H * 0.045), cfg.get("police"))
    cx = W // 2 if el.get("position", "centre") == "centre" else \
        (int(W * 0.25) if el["position"] == "gauche" else int(W * 0.75))
    cy = int(H * 0.46)
    alpha = ease_out(x / 0.3) * s
    coller_texte(im, (cx, cy), txt, f, BLANC, alpha, 1.0 + 0.15 * (1 - p))
    if el.get("texte"):
        # la légende glisse de bas en haut sous le chiffre
        p2 = ease_out((x - 0.25) / 0.4)
        coller_texte(im, (cx, cy + t_chiffre * 0.7 + (1 - p2) * H * 0.03),
                     el["texte"].upper(), f_leg, cfg["accent"], p2 * s)
    return im


def style_mot(W, H, el, cfg, x):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    t = int(H * 0.042)
    f = police(t, cfg.get("police"))
    w, h, _, _ = texte_dims(f, el["texte"])
    pad_x, pad_y = int(t * 0.8), int(t * 0.45)
    marge = int(W * 0.05)
    pos = el.get("position", "haut-droite")
    bw, bh = w + 2 * pad_x, h + 2 * pad_y
    x0 = marge if "gauche" in pos else W - marge - bw
    y0 = int(H * 0.08) if "haut" in pos else H - int(H * 0.08) - bh
    p = ease_back(x / 0.3)
    s = sortie(x, el["duree"])
    echelle = max(0.01, p * s)
    pill = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle([0, 0, bw - 1, bh - 1],
                                           radius=bh // 2,
                                           fill=cfg["accent"] + (255,))
    coller_texte(pill, (bw / 2, bh / 2), el["texte"], f, BLANC, ombre=False)
    pill = pill.resize((max(1, int(bw * echelle)), max(1, int(bh * echelle))),
                       Image.LANCZOS)
    im.alpha_composite(pill, (x0 + (bw - pill.width) // 2,
                              y0 + (bh - pill.height) // 2))
    return im


def style_liste(W, H, el, cfg, x):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lignes = el["lignes"][:5]
    t = int(H * 0.055)
    f = police(t, cfg.get("police"))
    marge = int(W * 0.08)
    interligne = int(t * 1.7)
    y0 = H // 2 - interligne * (len(lignes) - 1) // 2
    s = sortie(x, el["duree"])
    if el.get("titre"):
        f_t = police(int(H * 0.035), cfg.get("police"))
        coller_texte(im, (marge + texte_dims(f_t, el["titre"].upper())[0] / 2,
                          y0 - interligne), el["titre"].upper(), f_t,
                     cfg["accent"], ease_out(x / 0.3) * s)
    for i, l in enumerate(lignes):
        p = ease_out((x - 0.2 - i * 0.35) / 0.4)
        if p <= 0:
            continue
        y = y0 + i * interligne
        dx = int((1 - p) * W * 0.04)
        tiret = int(t * 0.7)
        d.rectangle([marge + dx, y - t * 0.05, marge + dx + int(tiret * p),
                     y + t * 0.1], fill=cfg["accent"] + (int(255 * p * s),))
        w, h, _, _ = texte_dims(f, l)
        coller_texte(im, (marge + dx + tiret + int(t * 0.5) + w / 2, y), l,
                     f, BLANC, p * s)
    return im


STYLES = dict(punch=style_punch, bandeau=style_bandeau, chiffre=style_chiffre,
              mot=style_mot, liste=style_liste)


# ---------------------------------------------------------------- rendu ---

def rendre_sequence(el, cfg, W, H, dossier):
    """Une PNG par image pour la durée de l'élément."""
    fn = STYLES[el["style"]]
    n = int(round(el["duree"] * FPS))
    os.makedirs(dossier, exist_ok=True)
    for i in range(n):
        im = fn(W, H, el, cfg, i / FPS)
        im.save(os.path.join(dossier, "%04d.png" % i), compress_level=1)
    return n


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("video", help="vidéo montée (sortie de aftermovie.py)")
    p.add_argument("habillage", help="fichier habillage.json")
    p.add_argument("--sortie", help="mp4 de sortie (défaut : *-habille.mp4)")
    p.add_argument("--voix", help="voix off, prime sur le json")
    p.add_argument("--apercu", type=float,
                   help="rend une seule image PNG à cette seconde")
    p.add_argument("--ffmpeg")
    a = p.parse_args()

    ffmpeg = trouver_ffmpeg(a.ffmpeg)
    cfg = json.load(open(a.habillage, encoding="utf-8"))
    cfg["accent"] = hex_rgb(cfg.get("accent") or ACCENT_DEFAUT)
    elements = cfg.get("elements", [])
    for el in elements:
        if el.get("style") not in STYLES:
            sys.exit("✗ style inconnu « %s » (choix : %s)"
                     % (el.get("style"), ", ".join(STYLES)))
    W, H, duree_video = dimensions(ffmpeg, a.video)
    sortie_mp4 = a.sortie or os.path.splitext(a.video)[0] + "-habille.mp4"

    if a.apercu is not None:
        # on compose les éléments visibles à cet instant sur l'image vidéo
        png = os.path.splitext(sortie_mp4)[0] + "-apercu-%.1fs.png" % a.apercu
        tmp = tempfile.mkdtemp(prefix="habillage-")
        fond = os.path.join(tmp, "fond.png")
        run([ffmpeg, "-hide_banner", "-y", "-ss", "%.3f" % a.apercu,
             "-i", a.video, "-frames:v", "1", fond])
        im = Image.open(fond).convert("RGBA")
        for el in elements:
            if el["t"] <= a.apercu < el["t"] + el["duree"]:
                im.alpha_composite(STYLES[el["style"]](W, H, el, cfg,
                                                       a.apercu - el["t"]))
        im.convert("RGB").save(png)
        shutil.rmtree(tmp, ignore_errors=True)
        log("✓ aperçu : %s" % png)
        return

    tmp = tempfile.mkdtemp(prefix="habillage-")
    try:
        cmd = [ffmpeg, "-hide_banner", "-y", "-i", a.video]
        filtres = []
        prev = "[0:v]"
        for k, el in enumerate(elements):
            dossier = os.path.join(tmp, "el-%02d" % k)
            n = rendre_sequence(el, cfg, W, H, dossier)
            log("  ▸ %-8s %6.2f s  +%.1f s  %s" % (
                el["style"], el["t"], el["duree"],
                el.get("texte") or el.get("valeur") or el.get("lignes")))
            cmd += ["-framerate", str(FPS), "-itsoffset", "%.3f" % el["t"],
                    "-i", os.path.join(dossier, "%04d.png")]
            out = "[v%d]" % (k + 1)
            filtres.append("%s[%d:v]overlay=0:0:eof_action=pass:"
                           "enable='between(t,%.3f,%.3f)'%s"
                           % (prev, k + 1, el["t"], el["t"] + n / FPS, out))
            prev = out
        filtres.append("%sformat=yuv420p[vout]" % prev)
        # --- audio : voix off en sidechain sur la piste existante
        voix = a.voix or cfg.get("voix")
        if voix:
            i_voix = len(elements) + 1
            cmd += ["-itsoffset", "%.3f" % float(cfg.get("voix_decalage", 0)),
                    "-i", voix]
            filtres.append(
                "[%d:a]aresample=48000,aformat=channel_layouts=stereo,"
                "highpass=f=80,asplit=2[vx][vsc]" % i_voix)
            filtres.append(
                "[0:a][vsc]sidechaincompress=threshold=0.05:ratio=6:attack=40:"
                "release=600:makeup=1[fond]")
            filtres.append(
                "[fond][vx]amix=inputs=2:duration=first:normalize=0,"
                "loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
            maps = ["-map", "[vout]", "-map", "[aout]"]
        else:
            maps = ["-map", "[vout]", "-map", "0:a?"]
        cmd += ["-filter_complex", ";".join(filtres)] + maps + [
            "-t", "%.3f" % duree_video, "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            sortie_mp4]
        log("• incrustation de %d éléments%s…" % (
            len(elements), " + voix off" if voix else ""))
        run(cmd)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    w, h, d = dimensions(ffmpeg, sortie_mp4)
    log("✓ %s — %.1f s, %dx%d" % (sortie_mp4, d, w, h))


if __name__ == "__main__":
    main()

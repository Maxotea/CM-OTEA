#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Étalonnage « punch » d'un montage DaVinci Resolve : noirs profonds, contraste,
peau chaude, ombres froides, glow sur les hautes lumières.

Né du teaser HYROX d'Otea Filmakers (13/10/2026). Maxime avait jugé la V7
« beaucoup trop flat », sans « profondeur sur la lumière », sans « glow qui fait
un peu briller l'image », aux « contrastes très ternes ». Ce script est la
réponse, rendue réutilisable pour les reels suivants.

## Principe

L'API de Resolve ne sait pas ajouter de nœud ; elle sait poser une LUT sur un
nœud existant. Dans Resolve, la LUT d'un nœud s'applique après ses
corrections primaires (vérifié le 13/10 : écart moyen de 0,3 % entre la
prévision et le rendu). La correction est donc cuite dans une LUT par plan,
« LUT de départ puis correction », posée à la place de la LUT d'origine sur le
nœud 1. L'étalonnage reste dans le projet, modifiable par Maxime.

Le glow est spatial : aucune LUT ne peut le faire. Il est posé après le rendu,
à partir de trois rendus Resolve en 1080×1920 :

- `images` : la piste des plans seule (autres pistes désactivées) ;
- `complet` : le montage entier, titres compris ;
- `titres` : les pistes de titres seules, avec alpha (FFV1 RGBA), pour que
  le glow ne bave pas sur le texte.

## Sous-commandes

    mesurer  RENDU_IMAGES PLANS.json REGLAGES.json [--apercu DOSSIER]
        Image du milieu de chaque plan (rendu avec l'étalonnage de départ),
        réglages dérivés des mesures (point noir, point blanc, dominante),
        planche avant / après.
    cuire    REGLAGES.json --look LUT_DE_DEPART --sortie DOSSIER_LUT --prefixe NOM
        Une LUT .cube par plan. Les plans marqués "stock" (images déjà en
        Rec.709, sans LUT d'origine) reçoivent la correction seule.
    finition RENDU_IMAGES RENDU_COMPLET RENDU_TITRES PLANS.json SORTIE.mov
        Glow sur les hautes lumières, en écran, masqué sous les titres.
        Sortie ProRes 422 HQ.

## Fichier PLANS.json

    [{"plan": 1, "debut": 0, "fin": 51, "nom": "FX320260212_0569",
      "neutraliser": 0.55,             # part de la dominante retirée (défaut 0,35)
      "stock": false,                  # true : image Rec.709 sans LUT d'origine
      "reglages": {"wb": [1.06, 0.95, 0.80]},   # priment sur l'automatique
      "glow": {"amount": 0.25, "threshold": 0.72}}, ...]

`debut` et `fin` sont en images de la timeline (25 i/s). Exemple complet :
`plans/otea/reels/F1-etalonnage-v9.json`.
"""
import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

W, H = 1080, 1920
LUM = np.array([0.2126, 0.7152, 0.0722], np.float32)
LUT_RESOLVE = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT"

# Le look commun : noirs profonds, peau chaude, ombres froides, couleur plus riche
LOOK = {"contrast": 1.45, "sat": 1.22, "pivot": 0.40,
        "shadow_tint": [-0.012, 0.0, 0.010], "high_tint": [0.014, 0.004, -0.014]}
GLOW = {"amount": 0.5, "threshold": 0.55, "size": 0.022}


# ---------------------------------------------------------------- correction

def luma(x):
    return x @ LUM


def scurve(t, pivot, c):
    """Courbe en S autour du pivot : pente c au pivot, noirs et blancs adoucis."""
    t = np.clip(t, 0, 1)
    lo = pivot * np.power(np.clip(t / pivot, 0, None), c)
    hi = 1 - (1 - pivot) * np.power(np.clip((1 - t) / (1 - pivot), 0, None), c)
    return np.where(t < pivot, lo, hi)


def corr(x, p):
    """Correction ponctuelle (cuisable en LUT). x : (..., 3) Rec.709 dans [0, 1]."""
    x = x.astype(np.float32) * np.array(p.get("wb", [1, 1, 1]), np.float32)
    b, w = p.get("black", 0.0), p.get("white", 1.0)
    x = np.power(np.clip((x - b) / (w - b), 0, None), p.get("gamma", 1.0))
    x = scurve(x, p.get("pivot", 0.40), p.get("contrast", 1.45))
    y = luma(x)[..., None]
    ws = np.clip(1 - y / 0.45, 0, 1) ** 2
    wh = np.clip((y - 0.45) / 0.55, 0, 1) ** 2
    x = x + ws * np.array(p.get("shadow_tint", LOOK["shadow_tint"]), np.float32) \
          + wh * np.array(p.get("high_tint", LOOK["high_tint"]), np.float32)
    y = luma(x)[..., None]
    cur = np.max(x, -1, keepdims=True) - np.min(x, -1, keepdims=True)
    seff = 1 + (p.get("sat", 1.22) - 1) * np.clip(1 - cur * 1.6, 0.25, 1)
    return np.clip(y + (x - y) * seff, 0, 1)


def glow_layer(x, amount, threshold, size):
    """Couche de glow : hautes lumières seuillées en douceur, deux flous, teinte chaude."""
    h, w = x.shape[:2]
    m = np.clip((luma(x) - threshold) / (1 - threshold), 0, 1) ** 1.5
    small = cv2.resize(x * m[..., None], (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    s1 = cv2.GaussianBlur(small, (0, 0), size * h / 4)
    s2 = cv2.GaussianBlur(small, (0, 0), size * 3 * h / 4)
    bl = cv2.resize(0.65 * s1 + 0.35 * s2, (w, h), interpolation=cv2.INTER_LINEAR)
    return bl * np.array([1.0, 0.92, 0.80], np.float32) * amount


def screen(x, layer):
    return 1 - (1 - x) * (1 - np.clip(layer, 0, 1))


# ---------------------------------------------------------------- LUT .cube

def read_cube(path):
    n, rows = None, []
    for line in open(path):
        s = line.strip()
        if not s or s[0] == "#" or s.startswith(("TITLE", "DOMAIN")):
            continue
        if s.startswith("LUT_3D_SIZE"):
            n = int(s.split()[1])
            continue
        rows.append([float(v) for v in s.split()])
    return np.array(rows, np.float32).reshape(n, n, n, 3)  # [b][g][r], r varie le plus vite


def write_cube(path, title, a):
    with open(path, "w") as f:
        f.write('TITLE "%s"\nLUT_3D_SIZE %d\n' % (title, a.shape[0]))
        for v in a.reshape(-1, 3):
            f.write("%.6f %.6f %.6f\n" % tuple(v))


def identity(n):
    r = np.linspace(0, 1, n, dtype=np.float32)
    b, g, rr = np.meshgrid(r, r, r, indexing="ij")
    return np.stack([rr, g, b], -1)


# ---------------------------------------------------------------- vidéo

def lire_image(path, n):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", "select=eq(n\\,%d)" % n,
                          "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(out, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535


def flux(path, fmt, bpp):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", fmt, "-"],
                            stdout=subprocess.PIPE, bufsize=W * H * bpp)


def zone_image(x):
    """Ignore les bandes noires d'un plan cadré dans une partie seulement de l'écran."""
    rows = x.mean(axis=(1, 2)) > 0.02
    return x[rows] if rows.sum() > 50 else x


def deriver(x, plan):
    a = zone_image(x)
    y = luma(a)
    p05, p50, p997 = np.percentile(y, [0.5, 50, 99.7])
    black = float(np.clip(p05 - 0.012, 0, 0.17))
    white = float(np.clip(p997 + 0.03, 0.62, 1.0))
    if white - black < 0.55:
        white = black + 0.55
    mid = (y > 0.12) & (y < 0.8)
    my = float(y[mid].mean())
    cast = a[mid].mean(0) - my
    k = plan.get("neutraliser", 0.35)
    wb = [float((my - k * c) / my) for c in cast]
    wb = [v / wb[1] for v in wb]
    m = (p50 - black) / (white - black)
    gamma = float(np.clip(np.log(0.36) / np.log(np.clip(m, 0.05, 0.95)), 0.8, 1.25)) if m > 0 else 1.0
    p = dict(LOOK, wb=wb, black=black, white=white, gamma=1 + (gamma - 1) * 0.5)
    p.update(plan.get("reglages", {}))
    return p


def vignette(im, label):
    t = Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8)).resize((216, 384))
    d = ImageDraw.Draw(t)
    d.rectangle([0, 0, 58, 18], fill=(0, 0, 0))
    d.text((4, 3), label, fill=(255, 255, 0))
    return t


# ---------------------------------------------------------------- commandes

def cmd_mesurer(a):
    plans = json.load(open(a.plans))
    reglages, tuiles = {}, []
    for pl in plans:
        x = lire_image(a.rendu, (pl["debut"] + pl["fin"]) // 2)
        p = deriver(x, pl)
        p.update({"nom": pl["nom"], "stock": pl.get("stock", False)})
        reglages[str(pl["plan"])] = p
        tuiles += [vignette(x, "%02d av" % pl["plan"]), vignette(corr(x, p), "%02d ap" % pl["plan"])]
    json.dump(reglages, open(a.sortie, "w"), indent=1, ensure_ascii=False)
    if a.apercu:
        os.makedirs(a.apercu, exist_ok=True)
        rows = (len(tuiles) + 7) // 8
        planche = Image.new("RGB", (8 * 216, rows * 384), (20, 20, 20))
        for k, t in enumerate(tuiles):
            planche.paste(t, ((k % 8) * 216, (k // 8) * 384))
        planche.save(os.path.join(a.apercu, "planche-avant-apres.jpg"), quality=88)
    print("%d plans mesurés → %s" % (len(reglages), a.sortie))


def cmd_cuire(a):
    reglages = json.load(open(a.reglages))
    base = read_cube(a.look)
    ident = identity(base.shape[0])
    dossier = os.path.join(LUT_RESOLVE, a.sortie) if not os.path.isabs(a.sortie) else a.sortie
    os.makedirs(dossier, exist_ok=True)
    for k, p in sorted(reglages.items(), key=lambda kv: int(kv[0])):
        nom = "%s%02d" % (a.prefixe, int(k))
        write_cube(os.path.join(dossier, nom + ".cube"), nom, corr(ident if p.get("stock") else base, p))
    print("%d LUT dans %s (dans Resolve : project.RefreshLUTList(), puis Graph.SetLUT(1, chemin))"
          % (len(reglages), dossier))


def cmd_finition(a):
    plans = json.load(open(a.plans))

    def reglage_glow(f):
        for pl in plans:
            if pl["debut"] <= f < pl["fin"]:
                return dict(GLOW, **pl.get("glow", {}))
        return None

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r2 = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    bords = np.clip(1.15 - 0.35 * r2, 0.55, 1)[..., None]  # le glow s'éteint vers les coins
    pi, pc, pt = flux(a.images, "rgb48le", 6), flux(a.complet, "rgb48le", 6), flux(a.titres, "rgba", 4)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le",
                            "-s", "%dx%d" % (W, H), "-r", "25", "-i", "-",
                            "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                            a.sortie], stdin=subprocess.PIPE)
    f = 0
    while True:
        bi, bc, bt = pi.stdout.read(W * H * 6), pc.stdout.read(W * H * 6), pt.stdout.read(W * H * 4)
        if len(bi) < W * H * 6 or len(bc) < W * H * 6:
            break
        img = np.frombuffer(bi, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535
        out = np.frombuffer(bc, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535
        g = reglage_glow(f)
        if g:
            couche = glow_layer(img, g["amount"], g["threshold"], g["size"]) * bords
            if len(bt) == W * H * 4:
                alpha = np.frombuffer(bt, np.uint8).reshape(H, W, 4)[..., 3:4].astype(np.float32) / 255
                couche = couche * (1 - alpha)
            out = screen(out, couche)
        enc.stdin.write((np.clip(out, 0, 1) * 65535 + 0.5).astype(np.uint16).tobytes())
        f += 1
    enc.stdin.close()
    enc.wait()
    print("%d images → %s" % (f, a.sortie))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mesurer")
    m.add_argument("rendu"); m.add_argument("plans"); m.add_argument("sortie")
    m.add_argument("--apercu")
    c = sub.add_parser("cuire")
    c.add_argument("reglages"); c.add_argument("--look", required=True)
    c.add_argument("--sortie", required=True); c.add_argument("--prefixe", required=True)
    f = sub.add_parser("finition")
    for k in ("images", "complet", "titres", "plans", "sortie"):
        f.add_argument(k)
    a = ap.parse_args()
    {"mesurer": cmd_mesurer, "cuire": cmd_cuire, "finition": cmd_finition}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

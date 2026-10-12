#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pierre Huiban : reels et stories en ralenti à partir des rushes FX3 de Rome.

Deux gabarits, une seule chaîne :

- « reel » : le style que Maxime a donné en référence le 07/10/2026 (reel de
  @rundadlift, instagram.com/p/DeH2T6FOUuJ) : image en noir et blanc, ralenti,
  phrases courtes en jaune, police à empattements, posées en bas à gauche du
  tiers inférieur, qui apparaissent l'une après l'autre. Pas de logo, pas de
  carton : l'image et la phrase portent tout.
- « story » : le même ralenti, en couleur, sous le calque de la DA « trois
  vies » (dégradé, registre ATHLETE · FATHER · EXECUTIVE, phrase du jour),
  produit par `pierre-story-photo-v2.py - SPEC CLE calque.png`.

Les rushes sont en 4K 100p S-Log3 (S-Gamut3.Cine). Le ralenti est un vrai
ralenti : 100 images par seconde relues à 25, soit ×4, sans image inventée.
L'étalonnage passe par `slog3.cube` (S-Log3 → Rec.709, courbe filmique douce),
écrit par `--lut`. Toutes les sorties sont MUETTES (règle stories-sans-son,
étendue aux reels : Maxime pose la musique dans Instagram). Seule exception,
voulue par Maxime le 07/10/2026 : la voix d'enfant des reels « dialogue »
(clé `voix`), une voix de synthèse Artlist, jamais un clone de voix réelle.

Usage :
    python3 pierre-reel-ralenti.py --lut slog3.cube
    python3 pierre-reel-ralenti.py SPEC.json [--rushes DOSSIER] [--polices fonts]

SPEC :
{
  "gabarit": "reel" | "story",
  "sortie": "reel-2026-10-08.mp4",
  "ralenti": 4,
  "plans": [{"clip": "7374", "debut": 1.0, "duree": 1.5, "x": 0.5}, ...],
  "textes": [{"debut": 0.5, "fin": 4.0, "texte": "Station eight."}, ...],   # reel
  "calque": "calque-mer.png",                                              # story
  "voix": [{"fichier": "q1.mp3", "debut": 0.4}, ...]                       # reel, facultatif
}
`debut` et `duree` d'un plan sont en secondes du RUSH ; la durée à l'écran est
multipliée par `ralenti` (réglable plan par plan : ×2 pour un rush en 50p, ×1
pour un rush en 25p). `"slog3": false` sur un plan déjà en Rec.709 (téléphone,
rushes d'entraînement non log) saute la LUT. `clip` est un bout du nom de
fichier (« 7374 » trouve FX3POST20260926_7374.MP4 dans tout `--rushes`). Une
voix peut porter `"hauteur": 1.3` (rubberband) pour rajeunir la voix. `x` place le recadrage 9:16 dans la largeur (0 = bord
gauche, 1 = bord droit). Les temps des textes sont ceux de la vidéo finie.
"""
import argparse
import fnmatch
import glob
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 25
JAUNE = (244, 208, 63)


# ---------------------------------------------------------------- étalonnage

def ecrire_lut(chemin, exposition=0.9, n=33):
    """S-Log3 / S-Gamut3.Cine → Rec.709. Formules publiées par Sony, tonemap Narkowicz."""
    def lin(x):
        if x >= 171.2102946929 / 1023:
            return (10 ** ((x * 1023 - 420) / 261.5)) * 0.19 - 0.01
        return (x * 1023 - 95) * 0.01125 / (171.2102946929 - 95)
    m = [[1.6269474, -0.5401385, -0.0868089],
         [-0.1785155, 1.4179409, -0.2394254],
         [-0.0444361, -0.1959199, 1.2403560]]

    def tm(x):
        x = max(0.0, x * exposition)
        return min(1.0, (x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14))

    def enc(v):
        v = max(0.0, min(1.0, v))
        return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055

    with open(chemin, "w") as f:
        f.write(f"LUT_3D_SIZE {n}\n")
        for b in range(n):
            for g in range(n):
                for r in range(n):
                    c = [lin(r / (n - 1)), lin(g / (n - 1)), lin(b / (n - 1))]
                    o = [enc(tm(sum(m[i][j] * c[j] for j in range(3)))) for i in range(3)]
                    f.write("%.5f %.5f %.5f\n" % tuple(o))


# ---------------------------------------------------------------- textes

def carton_texte(texte, polices, chemin):
    """Une phrase du gabarit reel : jaune, empattements, tiers inférieur, ombre douce."""
    police = ImageFont.truetype(os.path.join(polices, "Fraunces-Regular.ttf"), 58)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x, y = int(W * 0.2), int(H * 0.705)
    lignes = texte.split("\n")
    pas = 70
    ombre = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    do = ImageDraw.Draw(ombre)
    for i, ligne in enumerate(lignes):
        do.text((x + 2, y + i * pas + 3), ligne, font=police, fill=(0, 0, 0, 170))
    ombre = ombre.filter(ImageFilter.GaussianBlur(4))
    img.alpha_composite(ombre)
    for i, ligne in enumerate(lignes):
        d.text((x, y + i * pas), ligne, font=police, fill=JAUNE + (255,))
    # une phrase trop longue sortirait du cadre : on refuse plutôt que de la couper
    for ligne in lignes:
        if x + d.textlength(ligne, font=police) > W - 60:
            raise SystemExit(f"ligne trop longue pour le cadre : « {ligne} »")
    img.save(chemin)


# ---------------------------------------------------------------- montage

def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def trouver_rush(dossier, clip):
    """« 7374 » → FX3POST20260926_7374.MP4, cherché dans tout le dossier (casse ignorée)."""
    for motif in (f"{clip}.mp4", f"*{clip}.mp4", f"*{clip}*.mp4", f"*{clip}*.mov"):
        for chemin in glob.glob(os.path.join(dossier, "**", "*"), recursive=True):
            if fnmatch.fnmatch(os.path.basename(chemin).lower(), motif):
                return chemin
    raise SystemExit(f"rush introuvable pour le clip {clip} dans {dossier}")


def plan(rush, debut, duree, x, ralenti, lut, nb, sortie, p_log=True):
    filtre = (f"setpts={ralenti}*PTS,"
              f"crop=ih*9/16:ih:(iw-ih*9/16)*{x}:0,"
              f"scale={W}:{H}:flags=lanczos,lut3d={lut}")
    if p_log is False:
        filtre = filtre.replace(f",lut3d={lut}", "")
    if nb:
        filtre += ",hue=s=0,eq=contrast=1.12:brightness=-0.02,noise=alls=5:allf=t"
    filtre += ",format=yuv420p"
    ffmpeg("-ss", str(debut), "-t", str(duree), "-i", rush, "-vf", filtre,
           "-r", str(FPS), "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", sortie)


def monter(spec, rushes, polices, lut):
    nb = spec.get("gabarit", "reel") == "reel"
    ralenti = spec.get("ralenti", 4)
    morceaux = []
    for i, p in enumerate(spec["plans"]):
        m = f"_plan{i}.mp4"
        plan(trouver_rush(rushes, p["clip"]), p["debut"], p["duree"], p.get("x", 0.5),
             p.get("ralenti", ralenti), lut, nb, m, p.get("slog3", True))
        morceaux.append(m)
    with open("_liste.txt", "w") as f:
        f.writelines(f"file '{m}'\n" for m in morceaux)
    ffmpeg("-f", "concat", "-safe", "0", "-i", "_liste.txt", "-c", "copy", "_base.mp4")
    total = sum(p["duree"] * p.get("ralenti", ralenti) for p in spec["plans"])

    entrees, filtres, courant = ["-i", "_base.mp4"], [], "[0:v]"
    if nb:
        for k, t in enumerate(spec.get("textes", [])):
            png = f"_texte{k}.png"
            carton_texte(t["texte"], polices, png)
            entrees += ["-loop", "1", "-t", f"{total:.2f}", "-i", png]
            a, b = t["debut"], min(t["fin"], total)
            filtres.append(f"[{k + 1}:v]format=rgba,fade=in:st={a}:d=0.35:alpha=1,"
                           f"fade=out:st={b - 0.35:.2f}:d=0.35:alpha=1[t{k}]")
            filtres.append(f"{courant}[t{k}]overlay=0:0:enable='between(t,{a},{b})'[v{k}]")
            courant = f"[v{k}]"
    else:
        entrees += ["-loop", "1", "-t", f"{total:.2f}", "-i", spec["calque"]]
        filtres.append(f"{courant}[1:v]overlay=0:0[v0]")
        courant = "[v0]"
    # voix off (reel seulement) : les répliques de l'enfant, posées à leur seconde ;
    # sans voix, la sortie reste muette
    son = []
    for v in spec.get("voix", []):
        entrees += ["-i", v["fichier"]]
        son.append(v)
    nb_video = 1 + (len(spec.get("textes", [])) if nb else 1)
    pistes = []
    for j, v in enumerate(son):
        ms = int(v["debut"] * 1000)
        filtres.append(f"[{nb_video + j}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                       + (f"rubberband=pitch={v['hauteur']}," if v.get("hauteur") else "")
                       + f"volume={v.get('volume', 1.0)},adelay={ms}|{ms}[a{j}]")
        pistes.append(f"[a{j}]")
    carte_son = []
    if pistes:
        filtres.append("".join(pistes) + f"amix=inputs={len(pistes)}:normalize=0,"
                       f"apad,atrim=0:{total:.2f}[son]")
        carte_son = ["-map", "[son]", "-c:a", "aac", "-b:a", "192k"]
    if filtres:
        ffmpeg(*entrees, "-filter_complex", ";".join(filtres), "-map", courant,
               *(carte_son or ["-an"]),
               "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
               "-r", str(FPS), "-t", f"{total:.2f}", "-movflags", "+faststart", spec["sortie"])
    else:
        os.replace("_base.mp4", spec["sortie"])
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--rushes", default=".")
    ap.add_argument("--polices", default="fonts")
    ap.add_argument("--lut", default="slog3.cube")
    args = ap.parse_args()
    if not args.spec:
        ecrire_lut(args.lut)
        print(args.lut)
        return
    if not os.path.exists(args.lut):
        ecrire_lut(args.lut)
    spec = json.load(open(args.spec, encoding="utf-8"))
    total = monter(spec, args.rushes, args.polices, args.lut)
    print(f"{spec['sortie']} {total:.1f} s, " + ("voix seule" if spec.get("voix") else "muet"))


if __name__ == "__main__":
    sys.exit(main())

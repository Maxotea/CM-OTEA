#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Effet « le logo se construit tout seul » sur la vraie photo d'un lieu.

Inspiration n° 4 de `.claude/skills/cm-metricool/references/inspirations-montage.md`
(reel DeD1VHeuHfb, @welamall, 18 s). La façade, la salle ou le stand du client est
une vraie photo, immobile ; seul le logo bouge : il est absent au départ, puis il
s'assemble (pièces, lettres, disque qui pivote, néon qui s'allume) et se pose
exactement à sa place. Trois plans de 6 s, coupe franche entre eux.

La méthode complète, ses pièges et son coût sont dans
`.claude/memories/effet-logo-qui-se-construit.md`. Ce script couvre les deux bouts
qui ne passent pas par le modèle :

    # 1. le prompt et les réglages Higgsfield d'un plan, prêts à coller
    python3 scripts/logo-reveal.py prompt --style pieces --logo "le logo rond vert"

    # 2. l'image de début : la même photo, logo effacé (zone = ellipse cx,cy,rx,ry)
    python3 scripts/logo-reveal.py effacer photo-916.jpg --zone 100,662,200,205 \\
        --sortie photo-sans-logo.jpg
    #    sur une moquette ou un tissu : masque du logo + rectangle de surface vide
    python3 scripts/logo-reveal.py effacer photo.jpg --masque logo.png \\
        --grain 1000,3950,2900,4880 --sortie photo-sans-logo.jpg

    # 3. le contrôle et le montage, une fois les plans i2v téléchargés
    python3 scripts/logo-reveal.py assembler \\
        plan1.mp4:facade.jpg plan2.mp4:enseigne.jpg plan3.mp4:logo.jpg \\
        --sortie o/otea-logo-reveal.mp4

Chaque plan est donné avec sa photo source (`video:photo`). Le script compare la
dernière image du plan à la photo : si l'écart dépasse le seuil, le modèle a dérivé
(logo mal orthographié, façade réinventée) et le plan est refusé. Sinon il est
recadré en 1080×1920 plein cadre et **finit sur la vraie photo** (fondu de 0,25 s
puis tenue) : la dernière image vue est toujours le vrai logo, jamais une
approximation du modèle. Sortie muette : la musique se pose dans Instagram
(`.claude/memories/reels-musique-instagram.md`).
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

W, H = 1080, 1920
FPS = 30
FONDU_PHOTO = 0.25          # fondu entre la fin du plan i2v et la vraie photo
TENUE_PHOTO = 0.6           # durée pendant laquelle la vraie photo reste à l'écran
SEUIL_ECART = 8.0           # au-delà, la dernière image ne ressemble plus à la photo
# Repères mesurés le 28/08/2026 (story-video-plein-cadre.md) : 4 à 6 sur un plan sain,
# 4 entre deux images d'une même vidéo, 58,8 quand le modèle réinvente le lieu.

# Les styles repérés dans le reel. Chaque phrase décrit le mouvement du logo, jamais
# celui du lieu : le reste de l'image ne doit pas bouger.
# Maxime, 08/11/2026, sur l'essai Gossip : « la texture est trop 3D ». Les styles plats
# (`trace`, `encre`) passent donc en premier ; `pieces`, `lettres` et `disque` donnent
# du volume et ne servent que si on le demande.
PLAT = ("Strictly flat 2D graphic animation, printed on the surface like paint or ink: "
        "no extrusion, no thickness, no volume, no 3D pieces, no flying parts, no bounce, "
        "no shadows cast by the logo, no glossy reflections")

STYLES = {
    "trace": (
        "a thin line traces the outline of the logo on the surface in one continuous, "
        "smooth stroke, then the shape fills in flat, and the lettering prints in from "
        "left to right in reading order. " + PLAT),
    "encre": (
        "the logo soaks into the surface like ink spreading into fabric, from the center "
        "outward, sharp edges forming last, then the lettering appears the same way. "
        + PLAT),
    "pieces": (
        "the logo appears with a creative advertising animation: it assembles "
        "smoothly piece by piece, each part flying in with physical motion, a light "
        "bounce and soft reflections, then locks into place"),
    "lettres": (
        "the letters of the sign arrive one by one, in reading order, each letter "
        "dropping into its slot with a small mechanical bounce, until the full word "
        "is spelled exactly as in the final frame"),
    "disque": (
        "a flat dark disc sits where the logo will be; it rotates on its vertical "
        "axis, and as it turns to face the camera the logo outline is drawn on it "
        "and lights up like a neon tube"),
    "neon": (
        "the logo lights up like a neon sign: a short flicker, then the tube fills "
        "from one end to the other and settles to a steady glow"),
}

BASE = (
    "Locked-off camera, tripod shot, no camera movement, no zoom, no parallax. "
    "Animate only {logo} as a premium commercial reveal. "
    "IMPORTANT: preserve the input image exactly. Do not redesign, replace, move or "
    "regenerate the background, the building, objects, people, composition, colors, "
    "textures or perspective. The original scene must remain visually identical and "
    "recognizable. Only the existing logo is animated. "
    "{debut} Then {style}. "
    "The logo ends in exactly the same position, size, colors and spelling as in "
    "the {cible}, and holds still for the last second. No text other than the "
    "existing logo, no added people, no camera shake.")

DEBUT = {
    "debut-fin": ("The first frame shows the place without the logo; the last frame "
                  "is the real photo with the logo."),
    "une-image": ("At the beginning the logo is absent or invisible while the rest "
                  "of the scene stays completely unchanged."),
}
CIBLE = {"debut-fin": "end frame", "une-image": "input image"}


def construire_prompt(style, logo, mode="debut-fin"):
    """Le prompt i2v d'un plan. Le texte part en anglais : les modèles vidéo le
    suivent mieux, et il ne sort jamais vers le client."""
    if style not in STYLES:
        raise ValueError(f"style inconnu « {style} » : choisis parmi {', '.join(STYLES)}")
    if mode not in DEBUT:
        raise ValueError(f"mode inconnu « {mode} » : choisis parmi {', '.join(DEBUT)}")
    return BASE.format(logo=logo, style=STYLES[style], debut=DEBUT[mode],
                       cible=CIBLE[mode])


def reglages_higgsfield(mode="debut-fin", duree=6):
    """Les paramètres de `generate_video`. Kling 3.0 est le seul des deux Kling à
    accepter une image de fin ; le mode une-image reste sur le Turbo validé le 28/08."""
    if mode == "debut-fin":
        return {"model": "kling3_0", "mode": "std", "sound": "off", "duration": duree,
                "aspect_ratio": "9:16", "use_unlim": False,
                "medias": [{"value": "<photo sans logo>", "role": "start_image"},
                           {"value": "<vraie photo>", "role": "end_image"}]}
    return {"model": "kling3_0_turbo", "duration": duree, "aspect_ratio": "9:16",
            "use_unlim": False,
            "medias": [{"value": "<vraie photo>", "role": "start_image"}]}


def _vignette(image):
    """Image réduite en niveaux de gris, recadrée au 9:16 : on compare la forme,
    pas le bruit de compression."""
    image = image.convert("L")
    w, h = image.size
    cible = 9 / 16
    if w / h > cible:
        nw = round(h * cible)
        image = image.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w / cible)
        image = image.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return image.resize((72, 128), Image.LANCZOS)


def ecart(image_a, image_b):
    """Écart moyen (0 à 255) entre deux images, même méthode que les stories."""
    diff = ImageChops.difference(_vignette(image_a), _vignette(image_b))
    return ImageStat.Stat(diff).mean[0]


def verdict(valeur, seuil=SEUIL_ECART):
    if valeur <= seuil:
        return True, f"écart {valeur:.1f}, le plan retombe bien sur la photo"
    return False, (f"écart {valeur:.1f} (seuil {seuil:.0f}) : la fin du plan ne "
                   "ressemble plus à la photo. Regarde la dernière image, puis relance "
                   "le plan avec la photo sans logo en image de début")


def lire_zone(texte):
    try:
        cx, cy, rx, ry = (int(v) for v in texte.split(","))
    except ValueError:
        raise ValueError(f"« {texte} » : donne la zone du logo sous la forme cx,cy,rx,ry "
                         "(centre et demi-largeurs en pixels, ex. 100,662,200,205)")
    return cx, cy, rx, ry


def lire_rectangle(texte):
    try:
        x0, y0, x1, y1 = (int(v) for v in texte.split(","))
    except ValueError:
        raise ValueError(f"« {texte} » : donne la zone de grain sous la forme x0,y0,x1,y1 "
                         "(un rectangle de surface vide, sans logo ni objet)")
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"« {texte} » : le coin bas droit doit être après le coin haut gauche")
    return x0, y0, x1, y1


def effacer_logo(source, sortie, zone=None, masque=None, grain=None):
    """Efface le logo : reconstruction de la surface autour (OpenCV), puis grain.

    - `zone` (ellipse cx,cy,rx,ry) ou `masque` (PNG blanc sur noir, même taille que la
      photo) dit où est le logo. Le masque sert dès que le logo n'est pas un rond :
      lettrage en biais, symbole au sol.
    - `grain` (rectangle x0,y0,x1,y1 de surface vide) recopie la texture réelle de cette
      zone, répétée en miroir et ajustée à la lumière locale. Indispensable sur une
      moquette, un tissu, un béton : sans lui, la zone effacée devient une tache floue.
      Sans `grain`, un grain fin uniforme suffit sur un mur peint.

    Testé le 07/11 sur le mur rose de Gossip (zone, sans grain) et le 08/11 sur la
    moquette de J Lawson Golf (masque, grain pris dans la moquette vide du bas). Sur
    une brique ou un bois à motif, passer par un remplissage génératif."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        sys.exit("Il manque OpenCV pour effacer le logo. Installe-le une fois avec "
                 "« pip install opencv-python-headless », puis relance.")
    im = cv2.imread(str(source))
    if im is None:
        sys.exit(f"Impossible de lire {source}. Vérifie le chemin et relance.")
    H, W = im.shape[:2]
    if masque is not None:
        m = cv2.imread(str(masque), 0)
        if m is None or m.shape != (H, W):
            sys.exit(f"Le masque {masque} est illisible ou n'a pas la taille de la photo "
                     f"({W}×{H}). Refais-le à la même taille et relance.")
        m = (m > 127).astype(np.uint8) * 255
    elif zone is not None:
        cx, cy, rx, ry = zone
        m = np.zeros((H, W), np.uint8)
        cv2.ellipse(m, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
        m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    else:
        sys.exit("Dis où est le logo : --zone cx,cy,rx,ry ou --masque fichier.png.")
    imf = im.astype(np.float32)
    echelle = 0.5 if grain is None else 0.25
    petit = cv2.inpaint(cv2.resize(im, None, fx=echelle, fy=echelle),
                        cv2.resize(m, None, fx=echelle, fy=echelle),
                        25 if grain is None else 15, cv2.INPAINT_TELEA)
    fond = cv2.GaussianBlur(cv2.resize(petit, (W, H), interpolation=cv2.INTER_CUBIC)
                            .astype(np.float32), (0, 0), 6 if grain is None else 12)
    if grain is None:
        bruit = np.random.default_rng(1).normal(0, 1.6, im.shape).astype(np.float32)
        rempli = np.clip(fond + bruit, 0, 255)
    else:
        x0, y0, x1, y1 = grain
        bloc = imf[y0:y1, x0:x1]
        if bloc.size == 0:
            sys.exit("La zone de grain sort de la photo. Choisis un rectangle à l'intérieur.")
        base = cv2.GaussianBlur(bloc, (0, 0), 6)
        relatif = (bloc - base) / np.maximum(base, 8)
        motif = np.concatenate([relatif, relatif[::-1]], 0)
        motif = np.concatenate([motif, motif[:, ::-1]], 1)
        tuile = np.tile(motif, (H // motif.shape[0] + 1, W // motif.shape[1] + 1, 1))[:H, :W]
        rempli = np.clip(fond * (1 + tuile), 0, 255)
    alpha = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0),
                             8 if grain is None else 10)[..., None]
    sortie_img = (rempli * alpha + imf * (1 - alpha)).astype(np.uint8)
    Path(sortie).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(sortie), sortie_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"Photo sans logo : {sortie}. Regarde-la : rien d'autre ne doit avoir changé.")


def lire_couple(texte):
    if ":" not in texte:
        raise ValueError(f"« {texte} » : donne chaque plan sous la forme video.mp4:photo.jpg")
    video, photo = texte.rsplit(":", 1)
    return Path(video), Path(photo)


# ---------------------------------------------------------------- ffmpeg

def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg a refusé le montage. Dernières lignes :\n"
                 + "\n".join(r.stderr.strip().splitlines()[-6:]))
    return r


def derniere_image(ffmpeg, video, dossier):
    sortie = Path(dossier) / f"{video.stem}-fin.png"
    _run([ffmpeg, "-v", "error", "-y", "-sseof", "-0.1", "-i", str(video),
          "-frames:v", "1", "-update", "1", str(sortie)])
    return Image.open(sortie)


def duree_video(ffprobe, video):
    r = _run([ffprobe, "-v", "error", "-show_entries", "format=duration",
              "-of", "default=nw=1:nk=1", str(video)])
    return float(r.stdout.strip())


CADRE = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
         f"setsar=1,fps={FPS},format=yuv420p")


def rendre_plan(ffmpeg, video, photo, duree, sortie, tenue=TENUE_PHOTO):
    """Le plan i2v plein cadre, qui se fond dans la vraie photo puis la tient."""
    queue = FONDU_PHOTO + tenue          # la photo entre pendant le fondu, puis reste
    filtre = (f"[0:v]{CADRE}[v];[1:v]{CADRE},trim=duration={queue:.3f}[p];"
              f"[v][p]xfade=transition=fade:duration={FONDU_PHOTO}:"
              f"offset={max(duree - FONDU_PHOTO, 0):.3f}[out]")
    _run([ffmpeg, "-v", "error", "-y", "-i", str(video),
          "-loop", "1", "-t", f"{queue:.3f}", "-i", str(photo),
          "-filter_complex", filtre, "-map", "[out]", "-an",
          "-c:v", "libx264", "-crf", "18", "-preset", "medium", str(sortie)])


def assembler(couples, sortie, ffmpeg, ffprobe, seuil, forcer=False):
    with tempfile.TemporaryDirectory() as tmp:
        plans, refus = [], []
        for i, (video, photo) in enumerate(couples, 1):
            for f in (video, photo):
                if not f.exists():
                    sys.exit(f"Fichier introuvable : {f}. Vérifie le chemin et relance.")
            ok, message = verdict(ecart(derniere_image(ffmpeg, video, tmp),
                                        Image.open(photo)), seuil)
            print(f"plan {i} ({video.name}) : {message}")
            if not ok:
                refus.append(video.name)
            plan = Path(tmp) / f"plan{i:02d}.mp4"
            rendre_plan(ffmpeg, video, photo, duree_video(ffprobe, video), plan)
            plans.append(plan)
        if refus and not forcer:
            sys.exit(f"{len(refus)} plan(s) refusé(s) : {', '.join(refus)}. Rien n'a été "
                     "monté. Relance-les, ou ajoute --forcer pour monter quand même.")
        liste = Path(tmp) / "plans.txt"
        liste.write_text("".join(f"file '{p}'\n" for p in plans))
        Path(sortie).parent.mkdir(parents=True, exist_ok=True)
        _run([ffmpeg, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
              str(liste), "-c", "copy", "-an", "-movflags", "+faststart", str(sortie)])
    print(f"Montage prêt, muet, 1080×1920 : {sortie}")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = p.add_subparsers(dest="commande", required=True)

    pp = sp.add_parser("prompt", help="prompt et réglages d'un plan i2v")
    pp.add_argument("--style", choices=sorted(STYLES), default="trace")
    pp.add_argument("--logo", default="the logo visible in the image",
                    help="ce qui doit s'animer, en anglais (ex. « the round green logo »)")
    pp.add_argument("--mode", choices=sorted(DEBUT), default="debut-fin")
    pp.add_argument("--duree", type=int, default=6)

    pe = sp.add_parser("effacer", help="la photo sans le logo, pour l'image de début")
    pe.add_argument("photo")
    pe.add_argument("--zone", help="ellipse du logo : cx,cy,rx,ry en pixels")
    pe.add_argument("--masque", help="ou un masque PNG (blanc = logo), à la taille de la photo")
    pe.add_argument("--grain", help="rectangle x0,y0,x1,y1 de surface vide dont copier la texture")
    pe.add_argument("--sortie", required=True)

    pa = sp.add_parser("assembler", help="contrôle et montage des plans i2v")
    pa.add_argument("plans", nargs="+", help="video.mp4:photo.jpg, dans l'ordre du montage")
    pa.add_argument("--sortie", required=True)
    pa.add_argument("--seuil", type=float, default=SEUIL_ECART)
    pa.add_argument("--forcer", action="store_true")
    pa.add_argument("--ffmpeg", default=shutil.which("ffmpeg") or "ffmpeg")

    args = p.parse_args()
    if args.commande == "prompt":
        import json
        print(construire_prompt(args.style, args.logo, args.mode))
        print()
        print(json.dumps(reglages_higgsfield(args.mode, args.duree), indent=2,
                         ensure_ascii=False))
        return
    if args.commande == "effacer":
        try:
            zone = lire_zone(args.zone) if args.zone else None
            grain = lire_rectangle(args.grain) if args.grain else None
        except ValueError as e:
            sys.exit(str(e))
        effacer_logo(args.photo, args.sortie, zone=zone, masque=args.masque, grain=grain)
        return
    ffprobe = str(Path(args.ffmpeg).with_name("ffprobe")) if "/" in args.ffmpeg else "ffprobe"
    try:
        couples = [lire_couple(t) for t in args.plans]
    except ValueError as e:
        sys.exit(str(e))
    assembler(couples, args.sortie, args.ffmpeg, ffprobe, args.seuil, args.forcer)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La Galerie Immobilière : vidéo d'annonce, un mandat = un reel.

Réponse maison à ce que vend diane.estate (voir
`offre/video-annonce-la-galerie.md`) : à partir de VRAIES photos du bien,
recadrées 9:16 et animées en i2v caméra verrouillée (la chaîne validée par
Maxime le 28/08/2026), on assemble une vidéo d'annonce d'une trentaine de
secondes :

    intro (médaillon, « à vendre », titre du bien, accroche)
    → N plans enchaînés en fondu, chacun avec un titre et la phrase de
      narration incrustés (lisible sans le son, comme un sous-titre)
    → outro (visite sur rendez-vous, contact, pied « puteaux · paris ouest »)

Bande son : musique en synthèse procédurale (aucun sample tiers, zéro droits),
et narration optionnelle, un fichier wav par plan, produite en amont avec
`generate_audio` (voix préréglée française, jamais la voix clonée de Sabrina).
La musique baisse sous la voix.

Ce que ce script ne fait PAS, et c'est voulu :
  - pas d'avatar, pas de visage généré (règle absolue du dépôt) ;
  - pas de vue drone ni de travelling inventés : le modèle ne doit rien
    montrer que la photo ne montre pas (Maxime a écarté le travelling avant
    le 28/08) ;
  - aucun chiffre du bien inventé : surface, prix, étage viennent de
    l'annonce publiée, ou restent entre crochets dans la spec.

Usage (sandbox Higgsfield, ou local avec ffmpeg) :
    python3 lg-video-annonce.py videos-annonces/la-galerie-immobiliere/pilote-vm383.json
    python3 lg-video-annonce.py spec.json --format 16x9      # version site / portails
    python3 lg-video-annonce.py spec.json --test             # clips synthétiques, sans réseau

Sortie : o/annonce-<slug>-<format>.mp4
"""
import importlib.util
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import urllib.request
import wave

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))

SABLE = (212, 187, 165)          # #D4BBA5, la couleur du compte
ENCRE = (41, 37, 39)             # #292527
SOMBRE = (178, 153, 124)         # #B2997C
PIED = "puteaux · paris ouest"

FD = "f"
SERIF = FD + "/playfair.ttf"
MONO = FD + "/mono.ttf"
LOGO = FD + "/lg-rond.png"
# Mêmes URLs que lg-story-video.py : ne pas les changer, sinon la typo saute
# d'un contenu à l'autre.
SERIF_URL = ("https://fonts.gstatic.com/s/playfairdisplay/v40/"
             "nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKeiukDQ.ttf")
MONO_URL = ("https://fonts.gstatic.com/s/spacemono/v14/"
            "i7dPIFZifjKcF5UAWdDRUEZ2RFq7AwU.ttf")
LOGO_URL = ("https://lagalerieimmobiliere.com/wp-content/uploads/2021/12/"
            "rond-logo3.webp.png")

FPS = 25
XF = 0.5                         # fondu enchaîné entre deux segments
D_INTRO, D_PLAN, D_OUTRO = 2.5, 5.0, 3.5
SR = 44100

FFMPEG = shutil.which("ffmpeg")
if not FFMPEG:
    try:
        import imageio_ffmpeg
        FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("ffmpeg introuvable")

TEST = "--test" in sys.argv
FORMAT = "16x9" if "--format" in sys.argv and \
    sys.argv[sys.argv.index("--format") + 1] == "16x9" else "9x16"

if FORMAT == "9x16":
    W, H = 1080, 1920
    ZONE_HAUT, ZONE_BAS = 250, 1670      # bande visible sous l'interface Instagram
    MARGE = 90
    LOGO_D = 190
    Y_VOILE0, Y_VOILE1 = 1060, 1240      # voile sable qui porte le texte
    Y_TITRE = 1270                       # la photo garde les 55 % du haut
    T_TITRE, T_TEXTE, T_PIED = 84, 40, 26
else:
    W, H = 1920, 1080
    ZONE_HAUT, ZONE_BAS = 0, H
    MARGE = 100
    LOGO_D = 150
    Y_VOILE0, Y_VOILE1 = 640, 760
    Y_TITRE = 780
    T_TITRE, T_TEXTE, T_PIED = 68, 34, 24
Y_PIED = ZONE_BAS - 34
LOGO_X, LOGO_Y = W - MARGE - LOGO_D, ZONE_HAUT + 50


# --- Ressources ---------------------------------------------------------------

def _get(url, chemin):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            open(chemin, "wb").write(r.read())
        return True
    except Exception as e:
        print("!! %s : %s" % (url.split("/")[-1], e))
        return False


def boot():
    os.makedirs(FD, exist_ok=True)
    os.makedirs("o", exist_ok=True)
    for chemin, url in ((SERIF, SERIF_URL), (MONO, MONO_URL), (LOGO, LOGO_URL)):
        if os.path.exists(chemin) or _get(url, chemin):
            continue
        if not TEST:
            sys.exit("ressource manquante, la DA ne serait pas la leur : " + chemin)
        # En test seulement : polices système et logo dessiné, pour valider
        # la mécanique sans réseau. Jamais pour une vidéo livrée.
        if chemin == LOGO:
            im = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.ellipse([0, 0, 399, 399], fill=(20, 20, 20, 255))
            d.text((200, 200), "LG", fill=(255, 255, 255), anchor="mm",
                   font=ImageFont.truetype(_sys_font("Serif"), 150))
            im.save(chemin)
        else:
            shutil.copy(_sys_font("Serif" if chemin == SERIF else "SansMono"),
                        chemin)


def _sys_font(nom):
    for base in ("/usr/share/fonts/truetype/dejavu/DejaVu%s.ttf" % nom,
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(base):
            return base
    sys.exit("aucune police système pour le mode test")


def sf(taille, graisse=430):
    f = ImageFont.truetype(SERIF, taille)
    try:
        f.set_variation_by_axes([graisse])       # Playfair : axe unique [Weight]
    except Exception:
        pass
    return f


def wrap(d, txt, font, maxw):
    out, cur = [], ""
    for mot in txt.split():
        essai = (cur + " " + mot).strip()
        if d.textlength(essai, font=font) <= maxw or not cur:
            cur = essai
        else:
            out.append(cur)
            cur = mot
    if cur:
        out.append(cur)
    return out


def verifier_glyphes(texte, font):
    """Le piège des accents : on vérifie que chaque caractère a un glyphe."""
    for c in texte:
        if c.strip() and font.getmask(c).getbbox() is None:
            sys.exit("glyphe manquant pour %r dans %s" % (c, font.path))


# --- Calques ------------------------------------------------------------------

def medaillon(im, cx, cy, diam):
    logo = Image.open(LOGO).convert("RGBA").resize((diam, diam), Image.LANCZOS)
    r = diam // 2
    anneau = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(anneau).ellipse(
        [cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=SABLE + (255,))
    im.alpha_composite(anneau)
    im.paste(logo, (cx - r, cy - r), logo)


def filet(d, x, y):
    """Filet tracé à main levée, la signature graphique du compte."""
    pts = [(x + 190 * (i / 34.0), y + 2.2 * math.sin((i / 34.0) * 7.5))
           for i in range(35)]
    d.line(pts, fill=ENCRE, width=3, joint="curve")


def pied(d):
    fp = ImageFont.truetype(MONO, T_PIED)
    x = MARGE
    for ch in PIED:
        d.text((x, Y_PIED), ch, font=fp, fill=SOMBRE)
        x += d.textlength(ch, font=fp) + 3


def titre_bloc(d, y, titre, texte, maxw):
    """Titre serif bas-de-casse, filet, phrase de narration. Renvoie le y final."""
    taille = T_TITRE
    ft = sf(taille)
    lignes = wrap(d, titre.lower(), ft, maxw)
    while len(lignes) > 2 and taille > 56:
        taille -= 6
        ft = sf(taille)
        lignes = wrap(d, titre.lower(), ft, maxw)
    verifier_glyphes(titre, ft)
    for ligne in lignes:
        d.text((MARGE, y), ligne, font=ft, fill=ENCRE)
        y += int(taille * 1.18)
    filet(d, MARGE, y + 22)
    y += 60
    if texte:
        ts = T_TEXTE
        fs = sf(ts, 400)
        lg = wrap(d, texte, fs, maxw)
        while len(lg) > 3 and ts > 28:
            ts -= 2
            fs = sf(ts, 400)
            lg = wrap(d, texte, fs, maxw)
        verifier_glyphes(texte, fs)
        for ligne in lg:
            d.text((MARGE, y), ligne, font=fs, fill=ENCRE)
            y += int(ts * 1.42)
    return y


def calque_plan(chemin, titre, texte):
    """Calque transparent posé sur un plan : voile sable en bas, titre,
    phrase de narration, pied, médaillon en haut à droite."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for y in range(Y_VOILE0, H):
        if y < Y_VOILE1:
            t = (y - Y_VOILE0) / float(Y_VOILE1 - Y_VOILE0)
            a = int(255 * t * t)
        else:
            a = 255
        d.line([(0, y), (W, y)], fill=SABLE + (a,))
    yfin = titre_bloc(d, Y_TITRE, titre, texte, W - 2 * MARGE)
    if yfin > Y_PIED - 10:
        print("!! texte trop long sur « %s » : il mord sur le pied" % titre)
    pied(d)
    medaillon(im, LOGO_X + LOGO_D // 2, LOGO_Y + LOGO_D // 2, LOGO_D)
    im.save(chemin)


def carte(chemin, surtitre, titre, texte):
    """Carte pleine (intro / outro) : fond sable, médaillon centré, textes."""
    im = Image.new("RGBA", (W, H), SABLE + (255,))
    d = ImageDraw.Draw(im)
    diam = int(LOGO_D * 1.5)
    cy = int(H * 0.36) if FORMAT == "9x16" else int(H * 0.30)
    medaillon(im, W // 2, cy, diam)
    fm = ImageFont.truetype(MONO, T_PIED + 2)
    verifier_glyphes(surtitre, fm)
    x = (W - d.textlength(surtitre, font=fm) - 3 * len(surtitre)) // 2
    for ch in surtitre:
        d.text((x, cy + diam // 2 + 60), ch, font=fm, fill=SOMBRE)
        x += d.textlength(ch, font=fm) + 3
    titre_bloc(d, cy + diam // 2 + 130, titre, texte, W - 2 * MARGE)
    pied(d)
    im.convert("RGB").save(chemin)


# --- Segments vidéo -----------------------------------------------------------

def ff(*args):
    subprocess.run([FFMPEG, "-loglevel", "error", "-y"] + list(args), check=True)


def seg_carte(png, duree, out):
    ff("-loop", "1", "-framerate", str(FPS), "-i", png, "-t", str(duree),
       "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
       "-crf", "20", out)


def seg_plan(src, png, out):
    if FORMAT == "9x16":
        # plan natif 720×1280 (kling 9:16) -> plein cadre 1080×1920
        fil = "[0:v]scale=%d:%d,fps=%d[p];[p][1:v]overlay=0:0,format=yuv420p[v]" \
              % (W, H, FPS)
    else:
        # plan paysage (i2v lancé sur la photo non recadrée) : on remplit la
        # hauteur, on complète la largeur en sable, jamais d'étirement.
        fil = ("[0:v]scale=-2:%d,pad=%d:%d:(ow-iw)/2:0:color=#D4BBA5,fps=%d[p];"
               "[p][1:v]overlay=0:0,format=yuv420p[v]" % (H, W, H, FPS))
    ff("-i", src, "-i", png, "-filter_complex", fil, "-map", "[v]", "-an",
       "-t", str(D_PLAN), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out)


def plan_source(p, plans_connus, cdn):
    """URL du plan i2v : clé de lg-story-video.py, ou URL explicite."""
    if TEST:
        src = "o/_test_%s_%s.mp4" % ((p.get("plan") or "u").replace("/", "_"), FORMAT)
        if not os.path.exists(src):
            taille = "720x1280" if FORMAT == "9x16" else "1176x784"
            ff("-f", "lavfi", "-i", "testsrc2=size=%s:rate=%d" % (taille, FPS),
               "-t", str(D_PLAN), "-pix_fmt", "yuv420p", src)
        return src
    url = p.get("url") or (cdn + plans_connus[p["plan"]] + ".mp4")
    src = "o/_" + os.path.basename(url)
    if not os.path.exists(src) and not _get(url, src):
        sys.exit("plan introuvable : " + url)
    return src


# --- Bande son ----------------------------------------------------------------

def musique(chemin, duree):
    """Arpège feutré type piano sur nappe basse, motif de 8 s en boucle,
    entrée et sortie en fondu. Oscillateurs purs : zéro droits."""
    import array
    n = int(SR * duree)
    motif = [(0.0, 261.63), (1.2, 329.63), (2.4, 392.00), (4.0, 493.88),
             (5.2, 587.33), (6.0, 392.00), (7.0, 329.63)]
    notes = [(k * 8.0 + t0, f) for k in range(int(duree // 8) + 1)
             for t0, f in motif]
    ech = array.array("d", [0.0] * n)
    for depart, f in notes:
        i0 = int(depart * SR)
        for i in range(i0, min(n, i0 + int(3.0 * SR))):
            dt = (i - i0) / SR
            ech[i] += (math.sin(2 * math.pi * f * dt)
                       + 0.25 * math.sin(2 * math.pi * 2 * f * dt)) \
                * min(1.0, dt / 0.006) * math.exp(-1.6 * dt) * 0.5
    pic = 0.0
    for i in range(n):
        t = i / SR
        nappe = (math.sin(2 * math.pi * 130.81 * t)
                 + 0.5 * math.sin(2 * math.pi * 196.0 * t)) \
            * min(1.0, t / 2.0) * 0.10
        v = 0.5 * ech[i] + nappe
        v *= min(1.0, t / 1.0) * min(1.0, max(0.0, (duree - t) / 1.5))
        ech[i] = v
        pic = max(pic, abs(v))
    gain = 0.45 / (pic or 1.0)
    with wave.open(chemin, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(
            struct.pack("<h", int(max(-1.0, min(1.0, x * gain)) * 32767))
            for x in ech))


# --- Assemblage ---------------------------------------------------------------

def assembler(spec):
    slug = spec["slug"]
    bien = spec["bien"]
    plans = spec["plans"]
    connus, cdn = {}, ""
    if not TEST:
        m = importlib.util.spec_from_file_location(
            "lgsv", os.path.join(ICI, "lg-story-video.py"))
        mod = importlib.util.module_from_spec(m)
        m.loader.exec_module(mod)
        connus, cdn = mod.PLANS, mod.CDN

    segs, durees = [], []
    carte("o/_intro.png", "à vendre · " + bien["ville"], bien["titre"], bien["accroche"])
    seg_carte("o/_intro.png", D_INTRO, "o/_s00.mp4")
    segs.append("o/_s00.mp4"); durees.append(D_INTRO)
    for i, p in enumerate(plans, 1):
        png = "o/_c%02d.png" % i
        calque_plan(png, p["titre"], p["texte"])
        out = "o/_s%02d.mp4" % i
        seg_plan(plan_source(p, connus, cdn), png, out)
        segs.append(out); durees.append(D_PLAN)
    outro = spec.get("outro", {})
    carte("o/_outro.png", "la galerie immobilière",
          outro.get("titre", "visite sur rendez-vous"),
          outro.get("texte", "Contactez l'agence, on vous accompagne."))
    seg_carte("o/_outro.png", D_OUTRO, "o/_s%02d.mp4" % (len(plans) + 1))
    segs.append("o/_s%02d.mp4" % (len(plans) + 1)); durees.append(D_OUTRO)

    # fondus enchaînés : le segment k démarre à sum(durées avant) - k*XF
    debut = [sum(durees[:k]) - k * XF for k in range(len(segs))]
    total = sum(durees) - (len(segs) - 1) * XF
    fil, prev = "", "[0:v]"
    for k in range(1, len(segs)):
        lab = "[v%d]" % k if k < len(segs) - 1 else "[v]"
        fil += "%s[%d:v]xfade=transition=fade:duration=%s:offset=%.3f%s;" % (
            prev, k, XF, debut[k] - XF, lab)
        prev = lab
    fil = fil.rstrip(";")

    # audio : musique + narration (un wav par plan, posé au début du plan)
    voix = [(debut[i], p["voix"]) for i, p in enumerate(plans, 1)
            if p.get("voix") and os.path.exists(p["voix"])]
    entrees = []
    for s in segs:
        entrees += ["-i", s]
    afil, amaps = "", []
    if spec.get("musique", True):
        musique("o/_musique.wav", total)
        entrees += ["-i", "o/_musique.wav"]
        vol = 0.28 if voix else 0.7      # la musique baisse sous la voix
        afil += "[%d:a]volume=%s[m];" % (len(segs), vol)
        amaps.append("[m]")
    for j, (t0, wav) in enumerate(voix):
        entrees += ["-i", wav]
        idx = len(segs) + (1 if spec.get("musique", True) else 0) + j
        afil += "[%d:a]adelay=%d|%d[n%d];" % (idx, int(t0 * 1000), int(t0 * 1000), j)
        amaps.append("[n%d]" % j)
    sortie = "o/annonce-%s-%s.mp4" % (slug, FORMAT)
    if amaps:
        afil += "%samix=inputs=%d:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]" % (
            "".join(amaps), len(amaps))
        ff(*entrees, "-filter_complex", fil + ";" + afil, "-map", "[v]", "-map", "[a]",
           "-t", "%.3f" % total, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "44100", "-b:a", "160k", sortie)
    else:
        ff(*entrees, "-filter_complex", fil, "-map", "[v]", "-an",
           "-t", "%.3f" % total, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", sortie)
    print("ok %s  %.1f s  %d plans  narration %d/%d" % (
        sortie, total, len(plans), len(voix), len(plans)))
    return sortie


if __name__ == "__main__":
    specs = [a for a in sys.argv[1:] if a.endswith(".json")]
    if not specs:
        sys.exit(__doc__)
    boot()
    for chemin in specs:
        with open(chemin, encoding="utf-8") as f:
            assembler(json.load(f))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La Galerie Immobilière — stories vidéo 1080×1920, muettes.

Répond aux deux reproches de Sabrina du 19/08/2026 :

  1. « les storys ne sont pas à leur couleur »  → fond sable #D4BBA5, titre
     serif bas-de-casse #292527, relevés sur leurs propres publications.
  2. « ce n'est pas comme les autres comptes avec des vidéos et juste un
     texte » → une **vraie photo de leurs biens** occupe la carte et bouge
     réellement, comme sur le compte Run On Invest.

## Méthode : i2v sur leurs vraies photos

Version du 21/08/2026. La première version animait la photo avec un simple
`zoompan` ffmpeg : Maxime avait **déjà refusé ce procédé le 01/08** (« pas des
images animées mais juste des zooms »). Le mouvement vient donc d'un vrai
image-to-video (`kling3_0_turbo`, 16:9, 5 s), lancé une fois par photo, et
dont le mp4 est récupéré ici puis habillé.

Ce qui est conforme à `.claude/memories/stories-vraies-photos-sans-ia.md` :
  - la **photo source est réelle** et appartient au client (mandats publiés
    sur lagalerieimmobiliere.com) ; le modèle ne fabrique pas le lieu, il ne
    fait que le mettre en mouvement ;
  - **aucune personne identifiable** dans le lot (intérieurs et extérieurs) ;
  - la **dernière frame est contrôlée** contre la photo source avant de
    brancher quoi que ce soit ;
  - le **texte n'entre jamais dans le modèle** : il est incrusté après coup,
    en ffmpeg, à partir d'un calque PNG.

⚠️ **Muet.** `-an` obligatoire (`.claude/memories/stories-sans-son.md`).

Usage (sandbox Higgsfield) :
    python3 lg-story-video.py visites rare adresse    # -> o/lg-<clé>.mp4
"""
import math
import os
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
SABLE = (212, 187, 165)          # #D4BBA5 — la couleur du compte
ENCRE = (41, 37, 39)             # #292527
SOMBRE = (178, 153, 124)         # #B2997C

# Fenêtre vidéo : 16:9, le format sorti par le modèle. Le reste de la hauteur
# est du sable, où vient le texte.
PX, PY, PW, PH = 70, 430, 940, 529
Y_TITRE = 1090
DUREE = 5.0

FD = "f"
SERIF = FD + "/playfair.ttf"
SERIF_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
             "playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf")
MONO = FD + "/mono.ttf"
MONO_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
            "spacemono/SpaceMono-Regular.ttf")

# Les deux lots i2v générés le 21/08/2026. La clé de SPEC porte le préfixe du
# lot (A ou B) suivi de l'identifiant du job.
LOTS = {
    "A": ("https://d8j0ntlcm91z4.cloudfront.net/"
          "user_2zae6klRfE97hlBWhyQP6j7d9cR/hf_20260821_093630_"),
    "B": ("https://d8j0ntlcm91z4.cloudfront.net/"
          "user_2zae6klRfE97hlBWhyQP6j7d9cR/hf_20260821_093655_"),
}


def boot():
    os.makedirs(FD, exist_ok=True)
    os.makedirs("o", exist_ok=True)
    for chemin, url in ((SERIF, SERIF_URL), (MONO, MONO_URL)):
        if not os.path.exists(chemin):
            urllib.request.urlretrieve(url, chemin)


def sf(taille, graisse=430):
    f = ImageFont.truetype(SERIF, taille)
    try:
        f.set_variation_by_axes([graisse])   # Playfair : axe unique [Weight]
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


def calque(chemin, titre, sous_titre):
    """Calque PNG transparent : cadre de la fenêtre, titre, filet, pied."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # filet fin autour de la fenêtre vidéo, pour l'asseoir sur le sable
    d.rectangle([PX - 1, PY - 1, PX + PW, PY + PH],
                outline=SOMBRE + (150,), width=2)

    marge = 90
    maxw = W - 2 * marge
    taille = 78
    ft = sf(taille)
    lignes = wrap(d, titre.lower(), ft, maxw)
    while len(lignes) > 2 and taille > 52:
        taille -= 6
        ft = sf(taille)
        lignes = wrap(d, titre.lower(), ft, maxw)

    y = Y_TITRE
    for ligne in lignes:
        d.text((marge, y), ligne, font=ft, fill=ENCRE)
        y += int(taille * 1.18)

    # filet tracé à main levée — la signature graphique du compte
    pts = [(marge + 190 * (i / 34.0),
            y + 26 + 2.2 * math.sin((i / 34.0) * 7.5)) for i in range(35)]
    d.line(pts, fill=ENCRE, width=3, joint="curve")

    if sous_titre:
        fs = sf(31, 400)
        yy = y + 78
        for ligne in wrap(d, sous_titre, fs, maxw):
            d.text((marge, yy), ligne, font=fs, fill=ENCRE)
            yy += 44

    fp = ImageFont.truetype(MONO, 23)
    x = marge
    for ch in "puteaux · paris ouest":
        d.text((x, H - 132), ch, font=fp, fill=SOMBRE)
        x += d.textlength(ch, font=fp) + 3

    im.save(chemin)


def build(cle, job, titre, sous_titre):
    src = "o/_%s.mp4" % cle
    if not os.path.exists(src):
        urllib.request.urlretrieve(LOTS[job[0]] + job[1:] + ".mp4", src)
    calque("o/_t.png", titre, sous_titre)
    fil = ("[0:v]scale=%d:%d,fps=25[p];"
           "color=c=0xD4BBA5:s=%dx%d:r=25[bg];"
           "[bg][p]overlay=%d:%d[b1];"
           "[b1][1:v]overlay=0:0[v]" % (PW, PH, W, H, PX, PY))
    subprocess.run([
        "ffmpeg", "-loglevel", "error", "-y",
        "-i", src,
        "-i", "o/_t.png",
        "-filter_complex", fil, "-map", "[v]",
        "-an",                       # muet : règle stories-sans-son
        "-t", str(DUREE),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "o/lg-%s.mp4" % cle,
    ], check=True)


# --- Les 20 stories : clé → (lot+job i2v, titre, sous-titre) ----------------
# Chaque job part d'une photo d'un bien réel du portefeuille, publiée sur leur
# site (Suresnes, Nanterre, Colombes). Jamais de banque d'images.
SPEC = {
 "visites":     ("A74a4573d-359a-4f46-8e0a-c0d7df7a12ca", "week-end de visites",    "Les portes s'ouvrent, on vous accompagne."),
 "rare":        ("Acfc2402f-2abe-4e48-a01e-eddcd3063a5a", "le bien rare",           "Il ne reste jamais longtemps."),
 "inspiration": ("A94f66fa3-bd7c-4914-9285-2e6b1c0b67d0", "inspiration",            "Ce qu'on aime chez nous."),
 "semaine":     ("Ad75f1f01-18f1-47b6-a709-2cc6ddcc30bb", "nouvelle semaine",       "On est là du lundi au samedi."),
 "valeur":      ("A8980943a-9a0f-4c39-8a19-294d296bae9b", "mise en valeur",         "Un bien bien présenté se vend mieux."),
 "adresse":     ("Abaaaef20-ab72-4619-b2a3-f0ad23448f9c", "l'adresse compte",       "Puteaux, Suresnes, Nanterre, Colombes."),
 "estimation":  ("A2602eb34-c85f-4c71-89f8-3ac9703dae59", "l'estimation",           "Le bon prix, dès le premier jour."),
 "avant":       ("A74569906-3b75-49c2-ae6b-289743f95466", "avant de visiter",       "Trois questions à se poser."),
 "ouest":       ("A8b273207-e9c6-4fe3-bb5a-02cc8cb35337", "paris ouest",            "Notre terrain de jeu depuis le début."),
 "douceur":     ("A2d6f0bbd-f598-40b1-ba16-e3728da74102", "douceur du dimanche",    "Prenez le temps. Nous aussi."),
 "belle":       ("A3f283d52-387d-4ce9-933a-8d7f6069290c", "belle semaine",          "À très vite à l'agence."),
 "rentree":     ("A00516aa6-5bec-4136-a442-7c273a9133b8", "bonne rentrée",          "L'agence est ouverte, comme toujours."),
 "taux":        ("B23939ee1-98c2-452b-a596-77d028ac0e63", "les taux ont bougé",     "Votre budget aussi. On refait le point."),
 "ancien":      ("B4a089bca-cfc4-474e-92a1-a39fb660c866", "le charme de l'ancien",  "Ce qui ne se refabrique pas."),
 "dpe":         ("B091eac2f-6d5a-4883-a7b1-31b031211a0e", "votre dpe, on le relit", "La classe a peut-être changé."),
 "patrimoine":  ("B7f653565-c3cb-4dbf-876a-17c621df3fb8", "journées du patrimoine", "Les portes s'ouvrent ce week-end."),
 "gratuite":    ("Bef2568e4-740a-4905-a1de-94c5898ea87b", "estimation gratuite",    "Sans engagement, évidemment."),
 "fetes":       ("Bb946c729-4e1a-4f4c-8fdd-f1b2e07a9697", "vendre avant les fêtes", "C'est maintenant que ça se joue."),
 "visites2":    ("B36fee8d3-27b0-4530-9215-8fc289c8bcb1", "week-end de visites",    "Deux jours pour se projeter."),
 "reperage":    ("A74a4573d-359a-4f46-8e0a-c0d7df7a12ca", "repérage de quartier",   "On vous dit tout, même les défauts."),
}

if __name__ == "__main__":
    boot()
    for cle in sys.argv[1:]:
        job, titre, sous_titre = SPEC[cle]
        build(cle, job, titre, sous_titre)
        print("ok", cle)

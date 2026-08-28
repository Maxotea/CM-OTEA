#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La Galerie Immobilière — stories vidéo 1080×1920 plein cadre, muettes.

Répond aux deux reproches de Sabrina du 19/08/2026 :

  1. « les storys ne sont pas à leur couleur »  → sable #D4BBA5, titre serif
     bas-de-casse #292527, filet à main levée, relevés sur leurs publications.
  2. « ce n'est pas comme les autres comptes avec des vidéos et juste un
     texte » → une **vraie photo de leurs biens, animée, occupe tout le cadre**,
     comme sur le compte Run On Invest.

## Ce que la version précédente ratait (mesuré le 21/08/2026)

La première mouture logeait la vidéo dans une fenêtre de 940×529, soit **24 %
de la surface**, sur une carte de texte. Mesures comparées à une story Run On
Invest :

| | Run On Invest | v1 La Galerie |
|---|---|---|
| lignes de l'image qui bougent | 100 % | 24 % |
| écart moyen entre la 1re et la dernière frame | 18,2 | 1,0 |

Ce n'était pas une vidéo, c'était une carte typo avec une vignette qui frémit.
En prime, le modèle sortait du 1176×784 (3:2) forcé dans une fenêtre 16:9 :
l'image était **étirée de 18 %**.

## La méthode, et le piège à ne pas refaire

⛔ **Ne jamais lancer l'i2v en 9:16 depuis une photo paysage.** Testé : le
modèle **réinvente la pièce**. Écart de 58,8 contre la vraie photo, et aucun
recadrage de l'original ne correspond. C'est exactement ce que William du Loft
a reproché le 21/08 (« des photos qui ne sont pas prises chez moi »).

✅ **Recadrer d'abord en 9:16 dans PIL, animer ensuite** (ce que prescrivait
déjà `.claude/memories/stories-vraies-photos-sans-ia.md`). Mesuré sur la même
photo : écart de 4,12 sur la première frame, 6,02 sur la dernière, contre 4,0
entre deux frames d'une même vidéo. C'est leur photo, elle bouge, rien n'est
inventé.

Le recadrage se fait avec `scripts/lg-crop-9-16.py`, l'animation en
`kling3_0_turbo` 9:16 5 s (7,5 crédits par plan), caméra verrouillée.

⚠️ **Muet.** `-an` obligatoire (`.claude/memories/stories-sans-son.md`).

Les photos viennent des **mandats publiés sur leur propre site**
(lagalerieimmobiliere.com/bien-immobilier/…) : leurs biens, leurs photos.

Usage (sandbox Higgsfield) :
    python3 lg-story-video.py visites rare adresse   # -> o/lg-<clé>.mp4
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

# Le voile sable qui porte le texte : transparent au-dessus de Y_VOILE0,
# opaque à partir de Y_VOILE1. L'image reste pleine largeur et visible sur
# les 60 % du haut.
Y_VOILE0, Y_VOILE1 = 980, 1200
ALPHA_VOILE = 255
Y_TITRE = 1260

# Le médaillon : leur logo rond, disque noir à lettrage blanc, relevé sur leur
# site. C'est la version la plus lisible sur photo : la variante beige a du
# blanc sur beige, illisible en petit (luminance moyenne mesurée 192 contre 36).
LOGO_URL = ("https://lagalerieimmobiliere.com/wp-content/uploads/2021/12/"
            "rond-logo3.webp.png")
LOGO = FD + "/lg-rond.png"
LOGO_D = 168                     # diamètre du médaillon
LOGO_Y = 108                     # marge haute
DUREE = 5.0

FD = "f"
SERIF = FD + "/playfair.ttf"
SERIF_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
             "playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf")
MONO = FD + "/mono.ttf"
MONO_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
            "spacemono/SpaceMono-Regular.ttf")

CDN = ("https://d8j0ntlcm91z4.cloudfront.net/"
       "user_2zae6klRfE97hlBWhyQP6j7d9cR/hf_20260821_")

# Photo du site (numérotée par lg-crop-9-16.py) -> plan i2v 9:16 correspondant.
PLANS = {
    "01": "161732_e126fa6e-2008-452e-9f7b-57f87b60b3a8",
    "02": "161732_d49f24ca-df96-44e6-9391-93e9a13295cc",
    "04": "161732_f1c081eb-eb94-4e14-a396-9f32018abfac",
    "06": "161732_14bd054d-0bda-4318-ab38-63b8afe81b55",
    "07": "161732_5dc1a48d-b7f8-422a-951d-01e70aeda6d6",
    "08": "161732_66768aff-6a84-4bc5-898a-b12d2ca2d3f9",
    "09": "161732_aa2d8c02-5670-472a-8f06-aa3a79e93961",
    "10": "161732_70c5ba27-20d1-4eb3-8297-904389a45f9b",
    "11": "161732_564f82a9-fa35-49c3-99d0-ad42a0ad3aec",
    "12": "142523_93b5998a-4acc-481d-99c0-e236590da8ce",
    "13": "161733_852ec55a-885d-4ef6-9170-0365e2c75400",
    "15": "161732_865a72e8-0159-4223-a3cc-e09532d69e43",
    "17": "161732_a1684a36-d00c-42dc-90dd-7beb1c0dc685",
    "18": "161754_e64055db-afcd-425b-9319-d2c3788e6f73",
    "20": "161754_455e0a26-f981-4967-862b-a3cb2c1f1de3",
    "24": "161754_6f0a451b-307a-4d5b-aaa6-81122c978bcf",
    "27": "161754_e1283828-a603-4f86-9d86-4a9a8a12aa14",
    "28": "161754_186d95af-24d1-4e9b-8739-76fdc02d4dbc",
    "30": "161754_4cd3b0cd-431a-47cd-b7e9-5cf5a50e7358",
}


def boot():
    os.makedirs(FD, exist_ok=True)
    os.makedirs("o", exist_ok=True)
    for chemin, url in ((SERIF, SERIF_URL), (MONO, MONO_URL), (LOGO, LOGO_URL)):
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


def medaillon(im):
    """Pose leur logo rond en haut, cerclé de sable.

    Le cercle sable n'est pas décoratif : le logo est un disque noir, il
    disparaîtrait sur une photo sombre sans ce liseré.
    """
    logo = Image.open(LOGO).convert("RGBA").resize((LOGO_D, LOGO_D),
                                                   Image.LANCZOS)
    cx, cy = W // 2, LOGO_Y + LOGO_D // 2
    r = LOGO_D // 2
    anneau = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(anneau).ellipse(
        [cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=SABLE + (255,))
    im.alpha_composite(anneau)
    im.paste(logo, (cx - r, cy - r), logo)


def calque(chemin, titre, sous_titre):
    """Calque PNG : médaillon, voile sable, titre, filet, sous-titre, pied."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    for y in range(Y_VOILE0, H):
        if y < Y_VOILE1:
            t = (y - Y_VOILE0) / float(Y_VOILE1 - Y_VOILE0)
            a = int(ALPHA_VOILE * t * t)      # montée douce, pas de ligne dure
        else:
            a = ALPHA_VOILE
        d.line([(0, y), (W, y)], fill=SABLE + (a,))

    marge = 90
    maxw = W - 2 * marge
    taille = 96
    ft = sf(taille)
    lignes = wrap(d, titre.lower(), ft, maxw)
    while len(lignes) > 2 and taille > 64:
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
        # le sous-titre rétrécit plutôt que de mordre sur le pied de page
        ts = 38
        fs = sf(ts, 400)
        lg = wrap(d, sous_titre, fs, maxw)
        while len(lg) > 3 and ts > 30:
            ts -= 2
            fs = sf(ts, 400)
            lg = wrap(d, sous_titre, fs, maxw)
        yy = y + 84
        for ligne in lg:
            d.text((marge, yy), ligne, font=fs, fill=ENCRE)
            yy += int(ts * 1.42)

    fp = ImageFont.truetype(MONO, 26)
    x = marge
    for ch in "puteaux · paris ouest":
        d.text((x, H - 132), ch, font=fp, fill=SOMBRE)
        x += d.textlength(ch, font=fp) + 3

    medaillon(im)
    im.save(chemin)


def build(cle, photo, titre, sous_titre):
    src = "o/_%s.mp4" % photo
    if not os.path.exists(src):
        urllib.request.urlretrieve(CDN + PLANS[photo] + ".mp4", src)
    calque("o/_t.png", titre, sous_titre)
    fil = ("[0:v]scale=%d:%d,fps=25[p];[p][1:v]overlay=0:0[v]" % (W, H))
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


# --- Les 20 stories : clé → (photo du site, titre, sous-titre) --------------
SPEC = {
 "visites":     ("12", "week-end de visites",    "Les portes s'ouvrent, on vous accompagne."),
 "rare":        ("13", "le bien rare",           "Il ne reste jamais longtemps."),
 "inspiration": ("15", "inspiration",            "Ce qu'on aime chez nous."),
 "semaine":     ("11", "nouvelle semaine",       "On est là du lundi au samedi."),
 "valeur":      ("27", "mise en valeur",         "Un bien bien présenté se vend mieux."),
 "adresse":     ("09", "l'adresse compte",       "Puteaux, Suresnes, Nanterre, Colombes."),
 "estimation":  ("28", "l'estimation",           "Le bon prix, dès le premier jour."),
 "avant":       ("24", "avant de visiter",       "Trois questions à se poser."),
 "ouest":       ("30", "paris ouest",            "Notre terrain de jeu depuis le début."),
 "douceur":     ("17", "douceur du dimanche",    "Prenez le temps. Nous aussi."),
 "belle":       ("20", "belle semaine",          "À très vite à l'agence."),
 "rentree":     ("01", "bonne rentrée",          "L'agence est ouverte, comme toujours."),
 "taux":        ("08", "les taux ont bougé",     "Votre budget aussi. On refait le point."),
 "ancien":      ("06", "le charme de l'ancien",  "Ce qui ne se refabrique pas."),
 "dpe":         ("02", "votre dpe, on le relit", "La classe a peut-être changé."),
 "patrimoine":  ("10", "journées du patrimoine", "Les portes s'ouvrent ce week-end."),
 "gratuite":    ("04", "estimation gratuite",    "Sans engagement, évidemment."),
 "reperage":    ("12", "repérage de quartier",   "On vous dit tout, même les défauts."),
 "fetes":       ("18", "vendre avant les fêtes", "C'est maintenant que ça se joue."),
 "visites2":    ("07", "week-end de visites",    "Deux jours pour se projeter."),

 # --- Vague du 24 au 30/08, deux stories par jour (10h et 16h) -------------
 # Elle remplace des cartes typo grises et des photos de banque qui avaient
 # été branchées à la place des biens de La Galerie. Chaque plan est distinct
 # des cinq déjà en ligne du 31/08 au 12/09, aucune photo ne repasse deux fois.
 "n24a": ("11", "dernière ligne droite",   "Septembre arrive, on prépare votre projet."),
 "n24b": ("09", "l'agence vous accueille", "Poussez la porte, on prend le temps."),
 "n25a": ("13", "le marché redémarre",     "Septembre concentre les acquéreurs sérieux."),
 "n25b": ("27", "votre projet s'étudie",   "On regarde les chiffres avec vous."),
 "n26a": ("28", "préparer son bien",       "Quelques gestes changent tout avant les visites."),
 "n26b": ("15", "le salon qui donne envie", "C'est la pièce qui décide, souvent."),
 "n27a": ("04", "estimation gratuite",     "Sans engagement, évidemment."),
 "n27b": ("02", "les clés de votre prochain chez-vous", "On vous accompagne jusqu'à la remise."),
 "n28a": ("24", "le charme de l'ancien",   "Ce qui ne se refabrique pas."),
 "n28b": ("30", "puteaux, votre quartier", "Notre terrain de jeu depuis le début."),
 "n29a": ("10", "puteaux en famille",      "Écoles, parcs, transports : on connaît."),
 "n29b": ("18", "le cœur de la maison",    "La cuisine, là où tout se passe."),
 "n30a": ("17", "le calme du dimanche",    "Prenez le temps. Nous aussi."),
 "n30b": ("12", "inspiration",             "La terrasse de fin d'été."),
}

if __name__ == "__main__":
    boot()
    for cle in sys.argv[1:]:
        photo, titre, sous_titre = SPEC[cle]
        build(cle, photo, titre, sous_titre)
        print("ok", cle)

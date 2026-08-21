#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La Galerie Immobilière — stories vidéo 1080×1920, muettes.

Répond aux deux reproches de Sabrina du 19/08/2026 :

  1. « les storys ne sont pas à leur couleur »  → fond sable #D4BBA5, titre
     serif bas-de-casse #292527, relevés sur leurs propres publications.
  2. « ce n'est pas comme les autres comptes avec des vidéos et juste un
     texte » → une **vraie photo de leurs biens** occupe la carte et bouge
     lentement, comme sur le compte Run On Invest.

⚠️ **Zéro IA.** Le mouvement est un travelling ffmpeg `zoompan` sur les pixels
   de la photo d'origine : aucun modèle génératif, donc la règle
   `.claude/memories/stories-vraies-photos-sans-ia.md` est respectée. Run On
   Invest reste la seule exception i2v du portefeuille.

⚠️ **Muet.** `-an` obligatoire (`.claude/memories/stories-sans-son.md`).

Les photos viennent des **mandats publiés sur leur propre site**
(lagalerieimmobiliere.com/bien-immobilier/…) : ce sont leurs biens, leurs
photos. Jamais de banque d'images, jamais de photo d'une autre agence.

Usage (sandbox Higgsfield) :
    python3 lgv.py projet visites rare      # -> o/lg-<clé>.mp4
"""
import os
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
SABLE = (212, 187, 165)          # #D4BBA5 — la couleur du compte
ENCRE = (41, 37, 39)             # #292527
SABLE_SOMBRE = (178, 153, 124)   # #B2997C

# fenêtre photo
PX, PY, PW, PH = 70, 240, 940, 900
Y_TITRE = 1290
DUREE = 5.0

FD = "f"
SERIF = FD + "/playfair.ttf"
SERIF_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
             "playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf")
MONO = FD + "/mono.ttf"
MONO_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
            "spacemono/SpaceMono-Regular.ttf")

CDN = "https://lagalerieimmobiliere.com/wp-content/uploads/"


ANNONCES = [
    "appartement-5-pieces-patio-20-m%c2%b2-clim-et-parking-a-suresnes-92150",
    "maison-5-chambres-et-terrain-arbore-de-800-m%c2%b2-a-nanterre-92000",
    "maison-loft-144m%c2%b2-terrasse-jardin-cave-et-parking-a-suresnes-92150",
]


def _photos():
    """Relève les photos des mandats en ligne et les numérote 01..30.

    On repart systématiquement du site : la numérotation est donc
    reproductible tant que les mêmes annonces sont publiées. Si un bien est
    vendu et retiré, il faut revérifier le mapping de SPEC à l'œil."""
    import re
    html = ""
    for a in ANNONCES:
        try:
            req = urllib.request.Request(
                "https://lagalerieimmobiliere.com/bien-immobilier/%s/" % a,
                headers={"User-Agent": "Mozilla/5.0"})
            html += urllib.request.urlopen(req, timeout=25).read().decode(
                "utf-8", "replace")
        except Exception as e:
            print("annonce injoignable:", a, e)
    urls = sorted(set(re.findall(
        r"https://lagalerieimmobiliere\.com/wp-content/uploads/"
        r"202[56]/\d+/\d+_V[AM]\d+_\d+_original\.jpg", html)))
    for i, u in enumerate(urls, 1):
        dst = "r/%02d.jpg" % i
        if not os.path.exists(dst):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with open(dst, "wb") as f:
                f.write(urllib.request.urlopen(req, timeout=25).read())
    print("photos:", len(urls))


def _bootstrap():
    os.makedirs(FD, exist_ok=True)
    os.makedirs("o", exist_ok=True)
    os.makedirs("r", exist_ok=True)
    for chemin, url in ((SERIF, SERIF_URL), (MONO, MONO_URL)):
        if not os.path.exists(chemin):
            urllib.request.urlretrieve(url, chemin)
    _photos()


def sf(taille, graisse=430):
    f = ImageFont.truetype(SERIF, taille)
    try:
        f.set_variation_by_axes([graisse])   # Playfair : axe unique [Weight]
    except Exception:
        pass
    return f


def mo(taille):
    return ImageFont.truetype(MONO, taille)


def ls_text(d, x, y, txt, font, fill, tracking=0.0):
    for ch in txt:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x


def ls_width(d, txt, font, tracking=0.0):
    return sum(d.textlength(c, font=font) for c in txt) + tracking * (len(txt) - 1)


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


def filet(d, x, y, longueur):
    """Filet tracé à main levée — la signature graphique du compte."""
    pts = []
    n = 34
    for i in range(n + 1):
        t = i / n
        pts.append((x + longueur * t, y + 2.2 * __import__("math").sin(t * 7.5)))
    d.line(pts, fill=ENCRE, width=3, joint="curve")


def calque(chemin, titre, sous_titre):
    """Calque PNG transparent : titre, filet, sous-titre, pied."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
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

    filet(d, marge, y + 26, 190)

    if sous_titre:
        fs = sf(31, 400)
        yy = y + 78
        for ligne in wrap(d, sous_titre, fs, maxw):
            d.text((marge, yy), ligne, font=fs, fill=ENCRE)
            yy += 44

    pied = "puteaux · paris ouest"
    fp = mo(23)
    ls_text(d, marge, H - 132, pied, fp, SABLE_SOMBRE, 3)

    im.save(chemin)


def cadre(chemin):
    """Filet fin autour de la fenêtre photo, pour asseoir l'image sur le sable."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([PX - 1, PY - 1, PX + PW, PY + PH],
                outline=SABLE_SOMBRE + (150,), width=2)
    im.save(chemin)


def video(photo, dst, titre, sous_titre):
    calque("o/_t.png", titre, sous_titre)
    cadre("o/_c.png")

    # Travelling lent sur les pixels d'origine. Aucun modèle génératif.
    zoom = ("zoompan=z='min(zoom+0.00035,1.09)':d=125:"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            "s=%dx%d:fps=25" % (PW, PH))
    filtre = (
        "[0:v]scale=%d:%d:force_original_aspect_ratio=increase,"
        "crop=%d:%d,%s[p];"
        "color=c=0xD4BBA5:s=%dx%d:r=25[bg];"
        "[bg][p]overlay=%d:%d[b1];"
        "[b1][1:v]overlay=0:0[b2];"
        "[b2][2:v]overlay=0:0[v]"
        % (PW * 2, PH * 2, PW * 2, PH * 2, zoom, W, H, PX, PY)
    )
    subprocess.run([
        "ffmpeg", "-loglevel", "error", "-y",
        "-loop", "1", "-i", photo,
        "-i", "o/_c.png",
        "-i", "o/_t.png",
        "-filter_complex", filtre,
        "-map", "[v]",
        "-an",                       # muet : règle stories-sans-son
        "-t", str(DUREE),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        dst,
    ], check=True)


# --- Les 21 stories : clé, photo source, titre, sous-titre ------------------
# La photo est un bien réel du portefeuille, publié sur leur site.
SPEC = {
 "projet":      ("14", "votre projet",            "On en parle quand vous voulez."),
 "visites":     ("12", "week-end de visites",     "Les portes s'ouvrent, on vous accompagne."),
 "rare":        ("13", "le bien rare",            "Il ne reste jamais longtemps."),
 "inspiration": ("15", "inspiration",             "Ce qu'on aime chez nous."),
 "semaine":     ("11", "nouvelle semaine",        "On est là du lundi au samedi."),
 "valeur":      ("27", "mise en valeur",          "Un bien bien présenté se vend mieux."),
 "adresse":     ("09", "l'adresse compte",        "Puteaux, Suresnes, Nanterre, Colombes."),
 "estimation":  ("28", "l'estimation",            "Le bon prix, dès le premier jour."),
 "avant":       ("24", "avant de visiter",        "Trois questions à se poser."),
 "ouest":       ("30", "paris ouest",             "Notre terrain de jeu depuis le début."),
 "douceur":     ("17", "douceur du dimanche",     "Prenez le temps. Nous aussi."),
 "belle":       ("20", "belle semaine",           "À très vite à l'agence."),
 "rentree":     ("01", "bonne rentrée",           "L'agence est ouverte, comme toujours."),
 "taux":        ("08", "les taux ont bougé",      "Votre budget aussi. On refait le point."),
 "ancien":      ("06", "le charme de l'ancien",   "Ce qui ne se refabrique pas."),
 "dpe":         ("02", "votre dpe, on le relit",  "La classe a peut-être changé."),
 "patrimoine":  ("10", "journées du patrimoine",  "Les portes s'ouvrent ce week-end."),
 "gratuite":    ("04", "estimation gratuite",     "Sans engagement, évidemment."),
 "reperage":    ("12", "repérage de quartier",    "On vous dit tout, même les défauts."),
 "fetes":       ("18", "vendre avant les fêtes",  "C'est maintenant que ça se joue."),
 "visites2":    ("07", "week-end de visites",     "Deux jours pour se projeter."),
}

if __name__ == "__main__":
    _bootstrap()
    for cle in sys.argv[1:]:
        photo, titre, sous_titre = SPEC[cle]
        video("r/%s.jpg" % photo, "o/lg-%s.mp4" % cle, titre, sous_titre)
        print("ok", cle)

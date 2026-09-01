#!/usr/bin/env python3
"""Carrousel « faux drama » pour Le Loft, sur ses VRAIES photos.

Reprise de la trend de @teamoperou14_ : une fausse accusation publique
(« il est parti sans payer ») sert de prétexte à dérouler la carte, puis la
chute révèle que le client n'a jamais existé. Ici la chute porte sur le
bien-être (head spa, soin visage), pas sur la coupe.

Les photos viennent des stories d'août déjà en ligne, elles-mêmes issues du
shooting pro du 15/07. Le texte des stories est incrusté en haut du cadre
9:16 : on recadre donc le BAS en 4:5, ce qui élimine ce texte. Vérification
OCR obligatoire avant de brancher.

    python3 loft-carrousel-trend.py            # écrit o/loft-01.png .. o/loft-07.png
"""

import math
import os
import subprocess
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350                 # 4:5, le format du feed
OR_SRC = 1920                     # hauteur de la story source
OR_TOP = OR_SRC - H               # on garde le bas : le texte story est en haut

DORE = (206, 170, 105)            # #CEAA69, la couleur du compte
CREME = (240, 230, 216)           # #F0E6D8
NOIR = (14, 14, 14)               # #0E0E0E

Y_VOILE0, Y_VOILE1 = 600, 830     # montée du voile
ALPHA_VOILE = 238
MARGE = 84

CDN = "https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/"

# Les 7 stories d'août, identifiées par le titre incrusté (OCR).
PLANS = {
    "equipe":  "366e521c-1c5e-4348-8bd4-45b42d5e49a6",  # équipe dans le salon
    "coupe":   "fb8eeaa1-6cb6-4268-b493-aa6ecee09585",  # barbier, geste précis
    "barbe":   "02bf2bcb-25df-48cf-bbaa-dd9b1b7f2ffe",  # taille de barbe
    "headspa": "48aa7e58-af62-4b87-b8ff-6fd214270aec",  # le bac, lumière bleue
    "visage":  "97e07089-d422-4598-bd27-b1f5adcbc738",  # soin visage, masque
    "sortie":  "692cb848-ba4b-49d8-a0b2-df414cfc3295",  # barbier face objectif
    "salle":   "1b2b8b1d-977a-4949-a8f1-42387d47b179",  # équipe assise, vue large
}

# (clé photo, titre, corps). Le bien-être tient le centre et la chute.
SPEC = [
    ("equipe", "il est parti sans payer",
     "On a attendu deux jours. On a appelé deux fois. Rien. "
     "Alors on va dire ici, publiquement, tout ce qu'il a pris."),
    ("coupe", "il a commencé par la coupe",
     "Dégradé net, contours au rasoir, serviette chaude sur la nuque. "
     "Jusque là, rien d'anormal."),
    ("barbe", "puis il a pris la barbe",
     "Taille, soin, contours dessinés. Il a même demandé le baume."),
    ("headspa", "et là, il a demandé le head spa",
     "Vingt minutes la tête posée dans le bac. Massage du cuir chevelu, "
     "de la nuque, des épaules. C'est là qu'on l'a perdu."),
    ("visage", "il a enchaîné sur le soin visage",
     "Nettoyage, vapeur, masque. À ce stade il ne parlait plus du tout."),
    ("sortie", "il est reparti comme ça",
     "Détendu. Beaucoup trop détendu, visiblement."),
    ("salle", "ce client n'a jamais existé",
     "On cherchait une excuse pour te montrer qu'ici on ne fait pas que "
     "couper les cheveux. Coupe, barbe, head spa, soin visage, manucure. "
     "Au même endroit, 7j/7 de 10h à 20h."),
]

F_TITRE = "f/PlayfairDisplay-Bold.ttf"
F_CORPS = "f/LibreBaskerville-Italic.ttf"


def police_titre(taille):
    """Playfair Display est une variable font : l'axe doit être posé à la main.

    Sans set_variation_by_axes le rendu retombe sur le Regular et le titre
    perd son contraste. Toujours interroger get_variation_axes avant de
    supposer un nom d'axe.
    """
    f = ImageFont.truetype(F_TITRE, taille)
    try:
        f.set_variation_by_axes([700])
    except Exception:
        pass
    return f


def lettres(d, xy, txt, font, fill, ecart):
    """Titre interlettré : la signature typo du compte."""
    x, y = xy
    for c in txt:
        d.text((x, y), c, font=font, fill=fill)
        x += d.textlength(c, font=font) + ecart
    return x


def largeur_lettree(d, txt, font, ecart):
    return sum(d.textlength(c, font=font) + ecart for c in txt) - ecart


def couper(d, txt, font, maxi):
    mots, lignes, cur = txt.split(), [], ""
    for m in mots:
        essai = (cur + " " + m).strip()
        if d.textlength(essai, font=font) <= maxi:
            cur = essai
        else:
            if cur:
                lignes.append(cur)
            cur = m
    if cur:
        lignes.append(cur)
    return lignes


def couper_lettree(d, txt, font, ecart, maxi):
    mots, lignes, cur = txt.split(), [], ""
    for m in mots:
        essai = (cur + " " + m).strip()
        if largeur_lettree(d, essai, font, ecart) <= maxi:
            cur = essai
        else:
            if cur:
                lignes.append(cur)
            cur = m
    if cur:
        lignes.append(cur)
    return lignes


def photo(cle):
    """Récupère la story et en tire le bas du cadre, sans le texte incrusté."""
    mp4 = "o/_%s.mp4" % cle
    png = "o/_%s.png" % cle
    if not os.path.exists(png):
        if not os.path.exists(mp4):
            urllib.request.urlretrieve(CDN + PLANS[cle] + ".mp4", mp4)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4,
                        "-frames:v", "1", png], check=True)
    im = Image.open(png).convert("RGB")
    if im.size != (W, OR_SRC):
        im = im.resize((W, OR_SRC), Image.LANCZOS)
    return im.crop((0, OR_TOP, W, OR_SRC))


def planche(idx, cle, titre, corps):
    im = photo(cle)
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)

    for y in range(Y_VOILE0, H):
        if y < Y_VOILE1:
            t = (y - Y_VOILE0) / float(Y_VOILE1 - Y_VOILE0)
            a = int(ALPHA_VOILE * t * t)      # montée douce, pas de ligne dure
        else:
            a = ALPHA_VOILE
        d.line([(0, y), (W, y)], fill=NOIR + (a,))

    ft = police_titre(76)
    fc = ImageFont.truetype(F_CORPS, 34)
    maxi = W - 2 * MARGE
    ecart = 3

    lt = couper_lettree(d, titre.upper(), ft, ecart, maxi)
    lc = couper(d, corps, fc, maxi)

    h_t = len(lt) * 92
    h_c = len(lc) * 52
    y = H - 96 - h_c - 40 - h_t
    for ligne in lt:
        lettres(d, (MARGE, y), ligne, ft, DORE, ecart)
        y += 92

    y += 8
    d.line([(MARGE, y), (MARGE + 108, y)], fill=DORE, width=3)
    y += 32

    for ligne in lc:
        d.text((MARGE, y), ligne, font=fc, fill=CREME)
        y += 52

    out = Image.alpha_composite(im.convert("RGBA"), calque).convert("RGB")
    out.save("o/loft-%02d.png" % idx)
    return "o/loft-%02d.png" % idx


def main():
    os.makedirs("o", exist_ok=True)
    for i, (cle, titre, corps) in enumerate(SPEC, start=1):
        print(planche(i, cle, titre, corps))


if __name__ == "__main__":
    main()

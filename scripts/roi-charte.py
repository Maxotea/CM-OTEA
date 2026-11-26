#!/usr/bin/env python3
"""Run on Investment (R.O.I.) : kit de marque de la charte V3.

Charte validée en réunion le 19/11/2026, logo déposé à l'INPI (marque figurative avec
« RUN ON INVESTMENT » sous les lettres, version du 23/11/2026). Elle remplace le kit V2.1
du 03/08/2026 : mêmes lettres, une seule typographie (Archivo), le Terracotta à la place
de l'orange Blaze, des photos en noir et blanc.

Tout part des deux fichiers officiels de `assets/run-on-invest/charte-v3/source/` :
  * `ROI_logo_3points_NB.svg` : le logo vectoriel (R, piste, I, trois points) ;
  * `ROI_logo_depose_INPI.jpg` : la version déposée, avec le nom déplié dessous.
On ne redessine jamais le logo à la main : on recolore ces deux sources.

    python3 scripts/roi-charte.py            # régénère tout le kit dans charte-v3/
    python3 scripts/roi-charte.py --verifier # contrôle seulement les sources

Sorties (dossier `assets/run-on-invest/charte-v3/`) :
  logos/      logo seul et logo déposé, en Encre, Craie et Terracotta (PNG transparents,
              et SVG pour le logo seul), plus le symbole de la piste
  avatars/    photo de profil Instagram et LinkedIn (le symbole dans un rond)
  bannieres/  LinkedIn page entreprise et profil personnel
  gabarits/   Instagram feed 4:5 et story 9:16, LinkedIn post 4:5 et carré, couvertures des
              stories à la une ; les trois familles de la charte (Terracotta, Encre, photo voilée)
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

RACINE = Path(__file__).resolve().parent.parent
KIT = RACINE / "assets" / "run-on-invest" / "charte-v3"
SRC = KIT / "source"
POLICES = RACINE / "fonts" / "archivo"

# Couleurs de la charte V3 (section 03). Le Terracotta clair ne sert que sur fond Encre ou
# sur photo voilée. Jamais de texte Encre sur Terracotta.
TERRACOTTA = (181, 65, 43)        # #B5412B · 50 %
TERRACOTTA_CLAIR = (217, 87, 60)  # #D9573C
ENCRE = (17, 17, 17)              # #111111 · 30 %
CRAIE = (239, 237, 232)           # #EFEDE8 · 15 %
BETON = (140, 135, 126)           # #8C877E · 5 %
COULEURS = {"encre": ENCRE, "craie": CRAIE, "terracotta": TERRACOTTA}

# Une seule typographie : Archivo (section 04).
TITRE = POLICES / "Archivo_Expanded-Black.ttf"   # titres, capitales, interlettrage -3,5 %
TEXTE = POLICES / "Archivo-Medium.ttf"           # texte, 400 et 500
REPERE = POLICES / "Archivo-SemiBold.ttf"        # repères, 600, petites capitales espacées

VIEWBOX_W, VIEWBOX_H = 2823, 688   # boîte du dessin dans le SVG officiel (sans la marge)


# ---------------------------------------------------------------- le logo officiel

def _chemin(d, echelle, n=24):
    """Polygones d'un attribut d du SVG (commandes M, H, V, L, Q, Z) à l'échelle voulue."""
    jetons = re.findall(r"[MHVLQZ]|-?\d+(?:\.\d+)?", d)
    polys, cour, x, y, i = [], [], 0.0, 0.0, 0
    while i < len(jetons):
        c = jetons[i]
        i += 1
        if c == "M":
            if cour:
                polys.append(cour)
            x, y = float(jetons[i]), float(jetons[i + 1])
            i += 2
            cour = [(x, y)]
        elif c == "H":
            x = float(jetons[i]); i += 1; cour.append((x, y))
        elif c == "V":
            y = float(jetons[i]); i += 1; cour.append((x, y))
        elif c == "L":
            x, y = float(jetons[i]), float(jetons[i + 1]); i += 2; cour.append((x, y))
        elif c == "Q":
            cx, cy, ex, ey = (float(v) for v in jetons[i:i + 4])
            i += 4
            for k in range(1, n + 1):
                t = k / n
                cour.append(((1 - t) ** 2 * x + 2 * (1 - t) * t * cx + t * t * ex,
                             (1 - t) ** 2 * y + 2 * (1 - t) * t * cy + t * t * ey))
            x, y = ex, ey
        elif c == "Z":
            if cour:
                polys.append(cour)
            cour = []
    if cour:
        polys.append(cour)
    return [[(px * echelle, py * echelle) for px, py in p] for p in polys]


def masque_logo(hauteur):
    """Masque (mode L) du logo officiel, hauteur des capitales = hauteur px."""
    svg = (SRC / "ROI_logo_3points_NB.svg").read_text()
    sur = 4  # suréchantillonnage pour des bords nets
    e = hauteur * sur / VIEWBOX_H
    m = Image.new("L", (round(VIEWBOX_W * e) + 2, round(VIEWBOX_H * e) + 2), 0)
    d = ImageDraw.Draw(m)
    for attr in re.findall(r'<path d="([^"]+)"', svg):
        for k, poly in enumerate(_chemin(attr, e)):
            d.polygon(poly, fill=255 if k == 0 else 0)   # 2e sous-chemin : le creux du R
    for cx, cy, r in re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', svg):
        cx, cy, r = float(cx) * e, float(cy) * e, float(r) * e
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    for x, y, w, h, rx, sw in re.findall(
            r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="([\d.]+)"'
            r' fill="none" stroke="#000" stroke-width="([\d.]+)"', svg):
        x, y, w, h, rx, sw = (float(v) * e for v in (x, y, w, h, rx, sw))
        # Le trait SVG est centré sur le bord : on élargit la boîte d'un demi-trait.
        d.rounded_rectangle((x - sw / 2, y - sw / 2, x + w + sw / 2, y + h + sw / 2),
                            radius=rx + sw / 2, outline=255, width=round(sw))
    return m.resize((m.width // sur, m.height // sur), Image.LANCZOS)


def masque_piste(hauteur, pleine=False):
    """Le symbole : la piste seule. Sous 120 px de large, elle devient pleine (version réduite)."""
    m = masque_logo(hauteur)
    e = hauteur / VIEWBOX_H
    x0, x1 = round((1121.2 - 33.2) * e), round((1121.2 + 993.7 + 33.2) * e)
    p = m.crop((x0, 0, x1 + 1, m.height))
    if pleine or p.width < 120:
        d = ImageDraw.Draw(p)
        d.rounded_rectangle((0, 0, p.width - 1, p.height - 1), radius=p.height / 2, fill=255)
    return p


def masque_depose(largeur):
    """Masque de la version déposée à l'INPI (logo + RUN ON INVESTMENT), recadrée au plus juste."""
    im = ImageOps.grayscale(Image.open(SRC / "ROI_logo_depose_INPI.jpg"))
    m = ImageOps.invert(im).point(lambda v: 0 if v < 40 else (255 if v > 215 else v))
    m = m.crop(m.getbbox())
    return m.resize((largeur, round(m.height * largeur / m.width)), Image.LANCZOS)


def colorer(masque, couleur):
    img = Image.new("RGBA", masque.size, couleur + (0,))
    img.putalpha(masque)
    return img


def svg_colore(couleur_hex, fond=None):
    """Le SVG officiel recoloré, fond transparent (ou plein si fond donné)."""
    svg = (SRC / "ROI_logo_3points_NB.svg").read_text()
    svg = svg.replace('fill="#fff"', f'fill="{fond}"' if fond else 'fill="none"')
    return svg.replace("#000", couleur_hex)


# ---------------------------------------------------------------- typographie

def police(chemin, taille):
    return ImageFont.truetype(str(chemin), int(taille))


def largeur(txt, f, track):
    return sum(f.getlength(c) for c in txt) + track * (len(txt) - 1)


def ecrire(d, x, y, txt, f, fill, track=0.0, ancre="l"):
    """Texte lettre à lettre (interlettrage), y = ligne de base."""
    w = largeur(txt, f, track)
    if ancre == "c":
        x -= w / 2
    elif ancre == "r":
        x -= w
    for c in txt:
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += f.getlength(c) + track
    return w


def titre(d, lignes, x, y_haut, maxw, maxtaille, fill, ancre="l"):
    """Titres : Archivo Expanded Black, capitales, interlettrage -3,5 %. Renvoie le bas du bloc."""
    t = maxtaille
    while t > 20 and max(largeur(l, police(TITRE, t), -0.035 * t) for l in lignes) > maxw:
        t -= 2
    f = police(TITRE, t)
    y = y_haut + t * 0.72
    for l in lignes:
        ecrire(d, x, y, l, f, fill, -0.035 * t, ancre)
        y += t * 0.98
    return y - t * 0.98


def repere(d, x, y, txt, fill, taille, ancre="l"):
    """Repères : Archivo 600, capitales espacées (horaires, distances, lieux)."""
    return ecrire(d, x, y, txt.upper(), police(REPERE, taille), fill, 0.22 * taille, ancre)


def texte(d, x, y, txt, fill, taille, ancre="l"):
    return ecrire(d, x, y, txt, police(TEXTE, taille), fill, 0, ancre)


def grain(img, force=18):
    """Grain de la charte : bruit gaussien léger, le même sur les trois canaux."""
    from PIL import ImageChops
    bruit = Image.effect_noise(img.size, force).convert("L")
    base = img.convert("RGB")
    return Image.merge("RGB", [ImageChops.add(c, bruit, 1, -128) for c in base.split()])


def photo_nb(chemin, w, h):
    """Photo en noir et blanc contrasté, recadrée plein cadre (section 05 : la photo)."""
    im = ImageOps.fit(ImageOps.grayscale(Image.open(chemin)), (w, h), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=1)
    courbe = [round(255 * (3 * (i / 255) ** 2 - 2 * (i / 255) ** 3)) for i in range(256)]
    return im.point(courbe).convert("RGB")


def voile(img, force=0.5):
    return Image.blend(img, Image.new("RGB", img.size, ENCRE), force)


def couloir(w, h, n=1):
    """Masque des couloirs (section 05) : formes de la piste debout, côte à côte."""
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    gap = w * 0.03
    cw = (w - (n - 1) * gap) / n
    for k in range(n):
        x = k * (cw + gap)
        d.rounded_rectangle((x, 0, x + cw, h), radius=cw / 2, fill=255)
    return m


# ---------------------------------------------------------------- éléments communs

def coin(img, couleur, marge, cap=34, haut=None):
    """Constantes : logo haut-gauche, repère haut-droite (haut : sous la zone libre des stories)."""
    y = marge if haut is None else haut
    lg = colorer(masque_logo(cap), couleur)
    img.alpha_composite(lg, (round(marge), round(y)))
    d = ImageDraw.Draw(img)
    repere(d, img.width - marge, y + cap * 0.86, "LA DÉFENSE · 48.89° N", couleur,
           cap * 0.5, "r")


def pied(img, couleur, marge, txt="WE RUN. WE TALK. WE INVEST."):
    d = ImageDraw.Draw(img)
    repere(d, marge, img.height - marge, txt, couleur, 22)


# ---------------------------------------------------------------- le kit

def kit(sortie=KIT):
    faits = []

    def sauver(img, chemin, **kw):
        chemin = sortie / chemin
        chemin.parent.mkdir(parents=True, exist_ok=True)
        if chemin.suffix == ".jpg":
            img.convert("RGB").save(chemin, quality=92, **kw)
        else:
            img.save(chemin, **kw)
        faits.append(chemin.relative_to(sortie))

    # 1. Logos
    for nom, coul in COULEURS.items():
        sauver(colorer(masque_logo(600), coul), Path("logos") / f"ROI-logo-{nom}.png")
        sauver(colorer(masque_depose(2400), coul), Path("logos") / f"ROI-logo-depose-{nom}.png")
        sauver(colorer(masque_piste(600), coul), Path("logos") / f"ROI-symbole-piste-{nom}.png")
        (sortie / "logos" / f"ROI-logo-{nom}.svg").write_text(
            svg_colore("#%02X%02X%02X" % coul))
        faits.append(Path("logos") / f"ROI-logo-{nom}.svg")

    # 2. Avatars (rond Instagram et LinkedIn) : la piste seule, Craie sur Terracotta, et Terracotta clair sur Encre
    for nom, fond, coul in (("terracotta", TERRACOTTA, CRAIE), ("encre", ENCRE, TERRACOTTA_CLAIR)):
        for cote in (1080, 400):
            img = Image.new("RGBA", (cote, cote), fond + (255,))
            p = colorer(masque_piste(round(cote * 0.34)), coul)
            img.alpha_composite(p, ((cote - p.width) // 2, (cote - p.height) // 2))
            sauver(img.convert("RGB"), Path("avatars") / f"ROI-avatar-{nom}-{cote}.jpg")

    # 3. Bannières LinkedIn
    for nom, (w, h) in (("page-entreprise", (1128, 191)), ("profil", (1584, 396))):
        img = Image.new("RGBA", (w, h), TERRACOTTA + (255,))
        ph = photo_nb(SRC / "photo-defense-peloton-16x9.jpg", round(w * 0.42), h)
        m = couloir(ph.width, h, 3)
        img.paste(voile(ph, 0.2), (w - ph.width, 0), m)
        # La photo de profil LinkedIn recouvre le bas à gauche : le logo part au tiers et
        # s'arrête avant les couloirs.
        x = round(w * 0.30)
        place = (w - ph.width) - x - round(w * 0.04)
        lg = colorer(masque_depose(min(round(h * 1.4), place)), CRAIE)
        img.alpha_composite(lg, (x, round((h - lg.height) / 2)))
        sauver(img.convert("RGB"), Path("bannieres") / f"ROI-linkedin-{nom}-{w}x{h}.jpg")

    # 4. Gabarits de posts : trois familles jamais mélangées
    formats = {"instagram-feed-1080x1350": (1080, 1350), "instagram-story-1080x1920": (1080, 1920),
               "linkedin-post-1080x1350": (1080, 1350), "linkedin-post-1200x1200": (1200, 1200)}
    for fmt, (w, h) in formats.items():
        story = h == 1920
        marge = 0.065 * w
        zone = 200 if story else 0  # stories : zone libre en haut et en bas
        for famille in ("terracotta", "encre", "photo"):
            if famille == "terracotta":
                img = Image.new("RGBA", (w, h), TERRACOTTA + (255,)); txt, acc = CRAIE, CRAIE
            elif famille == "encre":
                img = Image.new("RGBA", (w, h), ENCRE + (255,)); txt, acc = CRAIE, TERRACOTTA_CLAIR
            else:
                src = SRC / ("photo-defense-arche-9x16.jpg" if h > w else "photo-defense-peloton-16x9.jpg")
                img = voile(photo_nb(src, w, h), 0.45).convert("RGBA"); txt, acc = CRAIE, TERRACOTTA_CLAIR
            coin(img, txt, marge, cap=30 if w < 1100 else 34, haut=zone if story else None)
            d = ImageDraw.Draw(img)
            y = h * 0.40
            repere(d, marge, y - 30, "ZÉRO PITCH", acc, 26)
            bas = titre(d, ["PUIS ON", "SE POSE."], marge, y, w - 2 * marge, 160, txt)
            texte(d, marge, bas + 110, "5 ou 10 km à La Défense, puis un vrai temps d'échange.", txt, 36)
            repere(d, marge, h - marge - zone, "08:30 · 5 OU 10 KM · LA DÉFENSE", txt, 22)
            sauver(grain(img), Path("gabarits") / fmt / f"{famille}.jpg")

    # 5. Couvertures des stories à la une
    for mot in ("COURSE", "ÉCHANGES", "INVEST", "INFOS", "ÉD. 01"):
        img = Image.new("RGBA", (1080, 1920), TERRACOTTA + (255,))
        p = colorer(masque_piste(260), CRAIE)
        img.alpha_composite(p, ((1080 - p.width) // 2, 960 - p.height // 2 - 60))
        d = ImageDraw.Draw(img)
        repere(d, 540, 960 + 150, mot, CRAIE, 44, "c")
        nom = mot.replace("É", "E").replace(". ", "").replace(" ", "-").lower()
        sauver(img.convert("RGB"), Path("gabarits") / "instagram-a-la-une" / f"{nom}.jpg")
    return faits


def verifier():
    m = masque_logo(200)
    assert m.getbbox(), "le logo officiel est vide"
    assert masque_depose(800).getbbox(), "la version déposée est vide"
    return True


if __name__ == "__main__":
    if "--verifier" in sys.argv:
        print("sources OK" if verifier() else "sources en défaut")
    else:
        for f in kit():
            print(f)

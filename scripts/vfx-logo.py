#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logo qui se dessine en néon puis se remplit, incrusté sur une surface du plan.

L'effet de l'inspiration n° 4 (`inspirations-montage.md`, carrousel @pedroleaumvfx,
vue 5 « Vivo ») : le logo du client apparaît sur un mur, une façade, une
banderole, comme s'il y avait toujours été. Trois temps :

1. **tracé** : le contour s'allume en trait néon, lettre après lettre dans le
   sens de lecture ; chaque lettre se dessine en tournant autour d'elle-même,
   avec une tête plus brillante qui avance (0,8 s par défaut) ;
2. **remplissage** : l'intérieur se remplit (0,5 s), le néon redescend et ne
   laisse qu'une lueur ;
3. **tenue** : le logo reste incrusté jusqu'à la fin du plan.

Le logo est posé en perspective sur un quadrilatère (les 4 coins de la zone où
il doit s'inscrire) et suit le mouvement de caméra : soit par suivi automatique
de points du plan, soit par des coins donnés à la main à plusieurs instants.

## Usage

    # 1. sortir l'image de repérage (grille graduée en pixels) à la seconde voulue
    python3 scripts/vfx-logo.py plan.mp4 logo.png --debut 0.4 --reperes o/reperes.png

    # 2. lire sur la grille les 4 coins de la zone, dans l'ordre :
    #    haut-gauche, haut-droite, bas-droite, bas-gauche (du logo tel qu'il se lit)
    python3 scripts/vfx-logo.py plan.mp4 logo.png --debut 0.4 \\
        --coins "212,80 610,140 590,330 190,300" --sortie o/plan-vfx.mp4

    # vérifier une seule image avant de tout rendre
    python3 scripts/vfx-logo.py ... --apercu 1.2 --sortie o/apercu.png

Le logo : un PNG détouré (fond transparent) ou un SVG, de préférence la version
vectorielle fournie par le client. Les couleurs se règlent avec `--neon` et
`--remplissage`.

## Le suivi

- `--suivi auto` (défaut) : les points sont suivis image par image à partir de
  `--debut`, et le logo épouse leur mouvement (homographie). Par défaut on suit
  les 4 coins, et l'outil ajoute de lui-même des repères marquants autour du
  logo (un repère qui glisse est recalé, un repère qui sort du cadre est
  remplacé) ; si la zone est un aplat sans détail (mur uni), donner avec
  `--points` 4 points ou plus **bien contrastés et sur le même plan** (angle de
  fenêtre, vis, joint, lettre déjà peinte). Le script s'arrête avec un message
  clair si un point se perd.
- `--suivi fixe` : plan sur pied, aucun suivi.
- `--cles cles.json` : coins donnés à la main à plusieurs instants, interpolés
  entre eux. Le secours quand le suivi automatique décroche :

      [{"t": 0.4, "coins": [[212,80],[610,140],[590,330],[190,300]]},
       {"t": 2.0, "coins": [[260,40],[650,120],[620,320],[230,280]]}]

Le son du plan est recopié tel quel. Tout le calcul (masques, animation,
homographie, suivi) est testé sans ffmpeg : `tests/test_vfx_logo.py`.
"""
import argparse
import itertools
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

LARGEUR_LOGO = 900        # largeur de travail du logo, en pixels
MARGE = 0.18              # marge autour du logo pour la lueur, en part de sa largeur


# ---------------------------------------------------------------- outils ---

def log(msg):
    print(msg, flush=True)


def hex_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


def clamp(x):
    return np.clip(x, 0.0, 1.0)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lire_coins(texte):
    """« x,y x,y x,y x,y » -> tableau 4x2. Message clair si la saisie est fausse."""
    try:
        pts = [[float(v) for v in p.split(",")] for p in texte.split()]
    except ValueError:
        sys.exit("✗ coins illisibles : écris-les comme « 212,80 610,140 590,330 190,300 »")
    if len(pts) < 4 or any(len(p) != 2 for p in pts):
        sys.exit("✗ il faut au moins 4 points « x,y » séparés par des espaces")
    return np.array(pts, np.float64)


# ----------------------------------------------------------- géométrie ---

def _normaliser(pts):
    """Centre et met à l'échelle les points : la résolution reste stable en pixels."""
    c = pts.mean(0)
    d = np.sqrt(((pts - c) ** 2).sum(1)).mean() or 1.0
    k = math.sqrt(2) / d
    return np.array([[k, 0, -k * c[0]], [0, k, -k * c[1]], [0, 0, 1]])


def homographie(src, dst):
    """Matrice 3x3 qui envoie src sur dst (4 points ou plus, moindres carrés)."""
    src = np.asarray(src, np.float64)
    dst = np.asarray(dst, np.float64)
    ns, nd = _normaliser(src), _normaliser(dst)
    a = appliquer(ns, src)
    b = appliquer(nd, dst)
    lignes = []
    for (x, y), (u, v) in zip(a, b):
        lignes.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        lignes.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    _, _, vt = np.linalg.svd(np.array(lignes))
    h = np.linalg.inv(nd) @ vt[-1].reshape(3, 3) @ ns
    return h / h[2, 2]


def homographie_robuste(src, dst, tolerance=3.0):
    """Homographie qui ignore les points aberrants (un repère qui a glissé).

    On essaie les quadruplets de points, on garde celui avec lequel le plus de
    points sont d'accord à `tolerance` pixels près, puis on recalcule sur ceux-là.
    Renvoie (matrice, masque des points fiables).
    """
    src = np.asarray(src, np.float64)
    dst = np.asarray(dst, np.float64)
    n = len(src)
    if n == 4:
        return homographie(src, dst), np.ones(4, bool)
    quads = list(itertools.combinations(range(n), 4))
    if len(quads) > 300:
        alea = np.random.default_rng(0)
        quads = [quads[i] for i in alea.choice(len(quads), 300, replace=False)]
    meilleur, fiables = -1, np.ones(n, bool)
    for q in quads:
        q = list(q)
        try:
            with np.errstate(all="ignore"):
                h = homographie(src[q], dst[q])
                err = np.sqrt(((appliquer(h, src) - dst) ** 2).sum(1))
        except np.linalg.LinAlgError:
            continue
        err = np.where(np.isfinite(err), err, np.inf)
        ok = err < tolerance
        score = ok.sum() - err[ok].sum() / (tolerance * n * 10)
        if score > meilleur:
            meilleur, fiables = score, ok
    if fiables.sum() < 4:
        return homographie(src, dst), np.ones(n, bool)
    return homographie(src[fiables], dst[fiables]), fiables


def appliquer(h, pts):
    pts = np.asarray(pts, np.float64)
    p = np.c_[pts, np.ones(len(pts))] @ h.T
    return p[:, :2] / p[:, 2:3]


def interpoler_cles(cles, t):
    """Coins à l'instant t, entre deux clés (linéaire), tenus avant et après."""
    cles = sorted(cles, key=lambda c: c["t"])
    if t <= cles[0]["t"]:
        return np.array(cles[0]["coins"], np.float64)
    for a, b in zip(cles, cles[1:]):
        if t <= b["t"]:
            k = (t - a["t"]) / max(b["t"] - a["t"], 1e-9)
            return (1 - k) * np.array(a["coins"], np.float64) + k * np.array(b["coins"], np.float64)
    return np.array(cles[-1]["coins"], np.float64)


# --------------------------------------------------------------- suivi ---

def _sommes(img, h, w):
    """Somme de img sur chaque fenêtre h x w (image intégrale)."""
    s = np.pad(img, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    return s[h:, w:] - s[:-h, w:] - s[h:, :-w] + s[:-h, :-w]


def correlation(zone, modele):
    """Corrélation croisée normalisée du modèle sur chaque position de la zone."""
    h, w = modele.shape
    m = modele - modele.mean()
    norme_m = math.sqrt(float((m * m).sum())) or 1e-9
    H, W = zone.shape
    fh, fw = H + h, W + w
    num = np.fft.irfft2(np.fft.rfft2(zone, (fh, fw)) * np.conj(np.fft.rfft2(m, (fh, fw))), (fh, fw))
    num = num[:H - h + 1, :W - w + 1]
    n = h * w
    s1 = _sommes(zone, h, w)
    s2 = _sommes(zone * zone, h, w)
    var = np.maximum(s2 - s1 * s1 / n, 1e-6)
    return num / (np.sqrt(var) * norme_m)


def _sous_pixel(c, i, j):
    """Affinage parabolique du pic de corrélation."""
    def dec(a, b, cc):
        d = a - 2 * b + cc
        return 0.0 if abs(d) < 1e-12 else 0.5 * (a - cc) / d
    dy = dec(c[i - 1, j], c[i, j], c[i + 1, j]) if 0 < i < c.shape[0] - 1 else 0.0
    dx = dec(c[i, j - 1], c[i, j], c[i, j + 1]) if 0 < j < c.shape[1] - 1 else 0.0
    return dx, dy


def coins_marquants(gris, r):
    """Carte « ce point se suit bien » : plus petite valeur propre du tenseur de
    structure (Shi-Tomasi), forte sur un coin, faible sur un aplat ou une ligne."""
    gy, gx = np.gradient(gris.astype(np.float64))
    k = 2 * r + 1
    sxx = np.pad(_sommes(gx * gx, k, k), r)
    syy = np.pad(_sommes(gy * gy, k, k), r)
    sxy = np.pad(_sommes(gx * gy, k, k), r)
    tr, det = sxx + syy, sxx * syy - sxy * sxy
    return tr / 2 - np.sqrt(np.maximum(tr * tr / 4 - det, 0))


def dans_polygone(x, y, poly):
    """Masque des points (x, y) à l'intérieur du polygone convexe `poly`."""
    signe = None
    dedans = np.ones(np.shape(x), bool)
    for (x1, y1), (x2, y2) in zip(poly, np.roll(poly, -1, axis=0)):
        c = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if signe is None:
            signe = np.sign(np.sum(c)) or 1
        dedans &= c * signe >= 0
    return dedans


class Suivi:
    """Suit le plan de la surface d'image en image.

    Des repères sont suivis par corrélation (modèle rafraîchi à chaque image).
    À chaque image on calcule le mouvement du plan sur lequel la majorité des
    repères sont d'accord ; un repère qui a glissé est recalé, un repère sorti du
    cadre est abandonné, et de nouveaux repères sont pris dans l'image autour du
    logo pour que le suivi continue même quand la caméra s'éloigne des premiers.

    `rayon` : demi-côté du carré suivi ; `recherche` : déplacement maximal par image.
    """

    CIBLE = 10            # nombre de repères qu'on cherche à garder

    def __init__(self, gris, points, coins, rayon=20, recherche=36, seuil=0.45, auto=True):
        self.r, self.s, self.seuil, self.auto = rayon, recherche, seuil, auto
        self.coins = np.asarray(coins, np.float64)
        self.ref = np.asarray(points, np.float64).copy()   # position dans l'image de départ
        self.pts = self.ref.copy()                         # position dans l'image courante
        self.vit = np.zeros_like(self.pts)
        self.actifs = np.ones(len(self.pts), bool)
        self.modeles = [self._patch(gris, p, self.r) for p in self.pts]
        # chaque repère garde l'image où il est né, pour être recalé sur son
        # apparence d'origine : c'est ce qui empêche le suivi de dériver
        self.naissances = [(np.asarray(gris, np.float32), np.eye(3))]
        self.ne = [0] * len(self.pts)
        self.h = np.eye(3)
        if auto:
            self._ajouter(gris)

    @staticmethod
    def _patch(gris, p, r):
        x, y = int(round(p[0])), int(round(p[1]))
        g = np.pad(gris, r + 64, mode="edge")
        x, y = x + r + 64, y + r + 64
        return g[y - r:y + r + 1, x - r:x + r + 1].astype(np.float64)

    def _dans_cadre(self, gris, p):
        h, w = gris.shape
        m = self.r + 2
        return bool(np.isfinite(p).all() and m <= p[0] < w - m and m <= p[1] < h - m)

    def _avancer_points(self, gris):
        for k, p in enumerate(self.pts):
            if not self.actifs[k]:
                continue
            prevu = p + self.vit[k]
            if not self._dans_cadre(gris, prevu):
                self.actifs[k] = False        # sorti du cadre
                continue
            zone = self._patch(gris, prevu, self.r + self.s)
            c = correlation(zone, self.modeles[k])
            i, j = np.unravel_index(np.argmax(c), c.shape)
            if c[i, j] < self.seuil:
                self.actifs[k] = False        # caché ou méconnaissable
                continue
            dx, dy = _sous_pixel(c, i, j)
            nouveau = np.array([round(prevu[0]) - self.s + j + dx,
                                round(prevu[1]) - self.s + i + dy])
            self.vit[k] = 0.5 * self.vit[k] + 0.5 * (nouveau - p)
            self.pts[k] = nouveau
            self.modeles[k] = self._patch(gris, nouveau, self.r)

    def _ajouter(self, gris):
        """Prend de nouveaux repères marquants autour du logo, sur le même plan."""
        manque = self.CIBLE - int(self.actifs.sum())
        if manque <= 0:
            return
        quad = appliquer(self.h, self.coins)
        centre = quad.mean(0)
        zone = centre + (quad - centre) * 1.6
        carte = coins_marquants(gris, max(3, self.r // 3))
        H, W = gris.shape
        pas = max(4, self.r // 2)
        yy, xx = np.mgrid[self.r + 2:H - self.r - 2:pas, self.r + 2:W - self.r - 2:pas]
        sel = dans_polygone(xx, yy, zone)
        if not sel.any():
            return
        cand = np.c_[xx[sel], yy[sel]].astype(np.float64)
        score = carte[cand[:, 1].astype(int), cand[:, 0].astype(int)]
        seuil = max(float(np.percentile(carte, 90)), 1e-4)
        ordre = np.argsort(-score)
        pris = [p for p, a in zip(self.pts, self.actifs) if a]
        inv = np.linalg.inv(self.h)
        naissance = None
        for i in ordre:
            if manque <= 0 or score[i] < seuil:
                break
            p = cand[i]
            if any(np.hypot(*(p - q)) < 2.5 * self.r for q in pris):
                continue
            pris.append(p)
            self.pts = np.vstack([self.pts, p])
            self.ref = np.vstack([self.ref, appliquer(inv, p[None])[0]])
            self.vit = np.vstack([self.vit, np.zeros(2)])
            self.actifs = np.append(self.actifs, True)
            self.modeles.append(self._patch(gris, p, self.r))
            if naissance is None:
                self.naissances.append((np.asarray(gris, np.float32), self.h.copy()))
                naissance = len(self.naissances) - 1
            self.ne.append(naissance)
            manque -= 1

    def _apparence(self, k, h, centre):
        """Le repère k tel qu'il devrait apparaître, centré sur `centre`, si le
        mouvement du plan est h : son image de naissance déformée."""
        image, h_ne = self.naissances[self.ne[k]]
        m = h_ne @ np.linalg.inv(h)                     # image courante -> naissance
        x0, y0 = centre[0] - self.r, centre[1] - self.r
        m = m @ np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]], np.float64)
        m = m / m[2, 2]
        cote = 2 * self.r + 1
        img = Image.fromarray(image, "F").transform((cote, cote), Image.PERSPECTIVE,
                                                    tuple(m.flatten()[:8]), Image.BILINEAR)
        return np.asarray(img, np.float64)

    def _recaler_sur_origine(self, gris, h, act, jeu=4):
        """Corrige chaque repère en le cherchant, à quelques pixels près de la
        position prévue, sous son apparence d'origine."""
        for k in act:
            p = appliquer(h, self.ref[k:k + 1])[0]
            if not self._dans_cadre(gris, p):
                continue
            c0 = np.round(p)
            modele = self._apparence(k, h, c0)
            if modele.std() < 1e-3:
                continue
            c = correlation(self._patch(gris, c0, self.r + jeu), modele)
            i, j = np.unravel_index(np.argmax(c), c.shape)
            if c[i, j] < self.seuil:
                continue
            dx, dy = _sous_pixel(c, i, j)
            self.pts[k] = c0 + [j - jeu + dx, i - jeu + dy]

    def avancer(self, gris):
        """Passe à l'image suivante. Renvoie la matrice départ -> image courante,
        ou None s'il ne reste pas assez de repères pour suivre le plan."""
        self._avancer_points(gris)
        act = np.flatnonzero(self.actifs)
        if len(act) < 4:
            return None
        h, _ = homographie_robuste(self.ref[act], self.pts[act])
        self._recaler_sur_origine(gris, h, act)
        h, fiables = homographie_robuste(self.ref[act], self.pts[act])
        self.h = h
        for k in act[~fiables]:
            p = appliquer(h, self.ref[k:k + 1])[0]
            if self._dans_cadre(gris, p):
                self.pts[k], self.vit[k] = p, 0.0
                self.modeles[k] = self._patch(gris, p, self.r)
            else:
                self.actifs[k] = False
        if self.auto:
            self._ajouter(gris)
        return h


# ---------------------------------------------------------- le logo ---

def charger_logo(chemin, ffmpeg=None):
    """PNG ou SVG -> RGBA à la largeur de travail."""
    if chemin.lower().endswith(".svg"):
        if not ffmpeg:
            sys.exit("✗ pour un SVG il faut ffmpeg ; sinon donne un PNG détouré")
        tmp = tempfile.mkdtemp()
        png = os.path.join(tmp, "logo.png")
        r = subprocess.run([ffmpeg, "-v", "error", "-y", "-width", str(LARGEUR_LOGO),
                            "-i", chemin, png], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("✗ SVG illisible (%s). Exporte le logo en PNG détouré et relance." % chemin)
        chemin = png
    img = Image.open(chemin).convert("RGBA")
    a = np.asarray(img)[:, :, 3]
    if a.min() > 250:
        sys.exit("✗ le logo n'a pas de fond transparent : il faut un PNG détouré "
                 "(ou le SVG du client), sinon c'est un rectangle qui va se dessiner")
    boite = img.getbbox()
    img = img.crop(boite)
    h = max(1, round(img.height * LARGEUR_LOGO / img.width))
    return img.resize((LARGEUR_LOGO, h), Image.LANCZOS)


def etiqueter(masque):
    """Composantes connexes (4-voisinage) d'un masque booléen, sans scipy."""
    h, w = masque.shape
    lab = np.where(masque, np.arange(1, h * w + 1).reshape(h, w), 0)
    grand = h * w + 10
    while True:
        l = np.where(lab > 0, lab, grand)
        p = np.pad(l, 1, constant_values=grand)
        voisins = np.minimum.reduce([p[1:-1, 1:-1], p[:-2, 1:-1], p[2:, 1:-1],
                                     p[1:-1, :-2], p[1:-1, 2:]])
        nouveau = np.where(masque, voisins, 0)
        if np.array_equal(nouveau, lab):
            break
        lab = nouveau
    _, inv = np.unique(lab, return_inverse=True)
    return inv.reshape(h, w)          # 0 = fond, 1..n = lettres


class Logo:
    """Les masques du logo dans son propre repère, avec la marge pour la lueur."""

    def __init__(self, img, epaisseur=None):
        self.w0, self.h0 = img.size
        m = round(self.w0 * MARGE)
        self.marge = m
        self.W, self.H = self.w0 + 2 * m, self.h0 + 2 * m
        toile = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        toile.alpha_composite(img, (m, m))
        self.alpha = np.asarray(toile)[:, :, 3].astype(np.float32) / 255.0

        # contour : bande de part et d'autre du bord du logo
        k = epaisseur or max(3, (self.w0 // 160) | 1)
        a8 = toile.getchannel("A")
        ext = np.asarray(a8.filter(ImageFilter.MaxFilter(k)), np.float32) / 255.0
        inte = np.asarray(a8.filter(ImageFilter.MinFilter(k)), np.float32) / 255.0
        self.contour = clamp(ext - inte)

        # lettres : composantes du logo (sur une version réduite, plus rapide)
        f = max(1, self.W // 320)
        petit = np.asarray(a8.resize((self.W // f, self.H // f), Image.BILINEAR)) > 100
        petit = np.asarray(Image.fromarray(petit.astype(np.uint8) * 255)
                           .filter(ImageFilter.MaxFilter(3))) > 0
        lab = etiqueter(petit)
        lab = np.asarray(Image.fromarray(lab.astype(np.int32)).resize((self.W, self.H), Image.NEAREST))
        # un pixel du contour hors lettre prend la lettre la plus proche (dilatation)
        for _ in range(4):
            vide = lab == 0
            if not (vide & (self.contour > 0)).any():
                break
            d = np.asarray(Image.fromarray(lab.astype(np.int32)).filter(ImageFilter.MaxFilter(5)))
            lab = np.where(vide, d, lab)
        n = int(lab.max())
        # ordre de lecture : de gauche à droite (centre de chaque lettre)
        yy, xx = np.mgrid[0:self.H, 0:self.W]
        centres = []
        for i in range(1, n + 1):
            sel = lab == i
            if sel.any():
                centres.append((i, xx[sel].mean(), yy[sel].mean()))
        centres.sort(key=lambda c: c[1])
        self.n = len(centres)
        self.rang = np.zeros((self.H, self.W), np.int32) - 1
        self.angle = np.zeros((self.H, self.W), np.float32)
        for rang, (i, cx, cy) in enumerate(centres):
            sel = lab == i
            self.rang[sel] = rang
            # angle autour du centre de la lettre : 0 en haut, sens des aiguilles d'une montre
            self.angle[sel] = (np.arctan2(xx[sel] - cx, -(yy[sel] - cy)) / (2 * np.pi)) % 1.0

    def coins(self):
        """Coins du logo (sans la marge) dans le repère de la toile."""
        m = self.marge
        return np.array([[m, m], [m + self.w0, m], [m + self.w0, m + self.h0], [m, m + self.h0]],
                        np.float64)


def avancement_lettres(n, t, duree):
    """Avancement 0..1 du tracé de chaque lettre à l'instant t (t=0 début du tracé).

    Chaque lettre dure la moitié du tracé total ; elles démarrent en cascade.
    """
    if n <= 0:
        return np.zeros(0)
    d = duree * (0.5 if n > 1 else 1.0)
    pas = (duree - d) / max(n - 1, 1)
    return ease_in_out((t - np.arange(n) * pas) / d)


def calques(logo, t, reg):
    """Les deux calques du logo à l'instant t (t=0 début de l'effet), dans son repère.

    Renvoie (dessus, lueur) : `dessus` en RGBA prémultiplié (posé par-dessus),
    `lueur` en RGB (ajoutée en lumière, mode écran).
    """
    trace, remp = reg["duree_trace"], reg["duree_remplissage"]
    neon, fond = reg["neon"], reg["remplissage"]
    av = avancement_lettres(logo.n, t, trace)
    av_px = np.where(logo.rang >= 0, av[np.clip(logo.rang, 0, None)] if logo.n else 0, 0)
    adoucir = 0.035
    revele = clamp((av_px * (1 + adoucir) - logo.angle) / adoucir)
    revele = np.where(av_px >= 0.999, 1.0, revele)
    # tête du trait : plus brillante là où le tracé avance
    tete = np.exp(-((av_px - logo.angle) / 0.03) ** 2) * (av_px < 0.999) * (av_px > 0.001)

    f = ease_out((t - trace * 0.85) / remp) if remp > 0 else float(t >= trace)
    # le néon redescend pendant le remplissage et ne laisse qu'une lueur
    intensite_neon = 1.0 - (1.0 - reg["lueur_finale"]) * f
    trait = logo.contour * clamp(revele + tete * 0.6) * intensite_neon
    if reg["scintillement"] and trace <= t < trace + 0.16:
        trait = trait * (0.55 if int((t - trace) * 25) % 2 == 0 else 1.0)

    a_fond = logo.alpha * f * reg["opacite"]
    a_trait = clamp(trait)
    a = clamp(a_fond + a_trait * (1 - a_fond))
    rgb = fond[None, None, :] * a_fond[..., None] + neon[None, None, :] * (a_trait * (1 - a_fond))[..., None]
    dessus = np.dstack([rgb, a]).astype(np.float32)

    # lueur : le trait flouté à deux rayons, plus un halo léger du remplissage
    base = Image.fromarray((clamp(trait + tete * logo.contour) * 255).astype(np.uint8))
    r = logo.w0 / 120
    l1 = np.asarray(base.filter(ImageFilter.GaussianBlur(r)), np.float32) / 255
    l2 = np.asarray(base.filter(ImageFilter.GaussianBlur(r * 4)), np.float32) / 255
    halo = np.asarray(Image.fromarray((a_fond * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(r * 3)), np.float32) / 255
    lueur = (neon[None, None, :] * (1.2 * l1 + 0.9 * l2)[..., None]
             + fond[None, None, :] * (0.18 * halo)[..., None]) * reg["force_lueur"]
    return dessus, clamp(lueur).astype(np.float32)


# ---------------------------------------------------------- incrustation ---

def _deformer(tab, coeffs, boite, mode=Image.BILINEAR):
    """Déforme un tableau HxWxC (0..1) vers la boîte (x0, y0, x1, y1) de l'image."""
    x0, y0, x1, y1 = boite
    img = Image.fromarray((clamp(tab) * 255).astype(np.uint8))
    out = img.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, coeffs, mode)
    return np.asarray(out, np.float32) / 255.0


def incruster(image, logo, coins, t, reg):
    """Pose le logo à l'instant t sur l'image (HxWx3, 0..1) dans le quadrilatère `coins`."""
    if t < 0:
        return image
    H_img, W_img = image.shape[:2]
    h = homographie(logo.coins(), coins)            # logo -> image
    toile = np.array([[0, 0], [logo.W, 0], [logo.W, logo.H], [0, logo.H]], np.float64)
    bord = appliquer(h, toile)
    x0, y0 = np.floor(bord.min(0)).astype(int)
    x1, y1 = np.ceil(bord.max(0)).astype(int)
    x0, y0 = max(x0, 0), max(y0, 0)
    x1, y1 = min(x1, W_img), min(y1, H_img)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return image
    # PIL veut l'inverse : pour chaque pixel de la boîte, où lire dans le logo
    decal = np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]], np.float64)
    inv = np.linalg.inv(h) @ decal
    inv = inv / inv[2, 2]
    coeffs = tuple(inv.flatten()[:8])

    dessus, lueur = calques(logo, t, reg)
    d = _deformer(dessus, coeffs, (x0, y0, x1, y1))
    l = _deformer(lueur, coeffs, (x0, y0, x1, y1))
    if reg["flou"] > 0:
        # même douceur que le plan : un logo trop net se voit tout de suite
        d = np.dstack([np.asarray(Image.fromarray((d[..., c] * 255).astype(np.uint8))
                                  .filter(ImageFilter.GaussianBlur(reg["flou"])), np.float32) / 255
                       for c in range(4)])
    zone = image[y0:y1, x0:x1].copy()
    a = d[..., 3:4]
    rgb = d[..., :3]
    if reg["eclairage"] > 0 and a.max() > 0:
        # le logo prend la lumière du support : plus sombre là où le mur l'est
        lum = zone.mean(axis=2, keepdims=True)
        ref = float((lum * a).sum() / max(a.sum(), 1e-6)) or 1e-3
        e = reg["eclairage"]
        rgb = rgb * clamp((1 - e) + e * lum / ref)
    zone = zone * (1 - a) + rgb
    zone = 1 - (1 - zone) * (1 - l)
    out = image.copy()
    out[y0:y1, x0:x1] = clamp(zone)
    return out


# ------------------------------------------------------------ la vidéo ---

def trouver_ffmpeg():
    p = shutil.which("ffmpeg")
    if not p:
        sys.exit("✗ ffmpeg introuvable : installe-le (brew install ffmpeg) puis relance")
    return p


def infos(ffmpeg, video):
    """Largeur, hauteur (après rotation), images par seconde, présence de son."""
    ffprobe = shutil.which("ffprobe") or ffmpeg.replace("ffmpeg", "ffprobe")
    r = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                        "stream=codec_type,r_frame_rate", "-of", "json", video],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("✗ vidéo illisible : %s" % video)
    flux = json.loads(r.stdout)["streams"]
    v = next((s for s in flux if s["codec_type"] == "video"), None)
    if not v:
        sys.exit("✗ pas d'image dans %s" % video)
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    img = extraire(ffmpeg, video, 0.0)
    return img.width, img.height, num / den, any(s["codec_type"] == "audio" for s in flux)


def extraire(ffmpeg, video, t):
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, "f.png")
    subprocess.run([ffmpeg, "-v", "error", "-y", "-ss", "%.3f" % t, "-i", video,
                    "-frames:v", "1", png], check=True)
    return Image.open(png).convert("RGB")


def reperes(img, chemin):
    """Grille graduée pour lire les coordonnées des coins à l'œil."""
    img = img.copy()
    d = ImageDraw.Draw(img)
    pas = 50 if max(img.size) <= 1200 else 100
    for x in range(0, img.width, pas):
        d.line([(x, 0), (x, img.height)], fill=(255, 255, 0) if x % (pas * 2) == 0 else (120, 120, 0))
        if x % (pas * 2) == 0:
            d.text((x + 2, 2), str(x), fill=(255, 255, 0))
    for y in range(0, img.height, pas):
        d.line([(0, y), (img.width, y)], fill=(0, 255, 255) if y % (pas * 2) == 0 else (0, 120, 120))
        if y % (pas * 2) == 0:
            d.text((2, y + 2), str(y), fill=(0, 255, 255))
    img.save(chemin)
    log("✓ repérage : %s (x en jaune, y en cyan)" % chemin)


def fin_suivi_ok(coins, W, H):
    """Le suivi peut s'arrêter sans dommage si le logo est déjà sorti du cadre."""
    if coins is None:
        return False
    x0, y0 = coins.min(0)
    x1, y1 = coins.max(0)
    return x1 < 0 or y1 < 0 or x0 > W or y0 > H


def gris(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def rendre(args, reg):
    ffmpeg = trouver_ffmpeg()
    W, H, fps, son = infos(ffmpeg, args.video)
    logo = Logo(charger_logo(args.logo, ffmpeg))
    log("· logo : %d lettre(s) repérée(s)" % logo.n)

    cles = None
    if args.cles:
        with open(args.cles, encoding="utf-8") as f:
            cles = json.load(f)
    elif not args.coins:
        sys.exit("✗ donne les 4 coins (--coins) ou un fichier de clés (--cles). "
                 "Pour les lire : --reperes o/reperes.png")
    coins0 = lire_coins(args.coins)[:4] if args.coins else interpoler_cles(cles, args.debut)
    points0 = lire_coins(args.points) if args.points else coins0

    if args.apercu is not None and args.suivi != "auto":
        img = np.asarray(extraire(ffmpeg, args.video, args.apercu), np.float32) / 255
        c = interpoler_cles(cles, args.apercu) if cles else coins0
        out = incruster(img, logo, c, args.apercu - args.debut, reg)
        Image.fromarray((out * 255).astype(np.uint8)).save(args.sortie)
        log("✓ aperçu : %s" % args.sortie)
        return

    lecture = subprocess.Popen([ffmpeg, "-v", "error", "-i", args.video, "-f", "rawvideo",
                                "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    ecriture = None
    if args.apercu is None:
        cmd = [ffmpeg, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", "%dx%d" % (W, H), "-r", "%.6f" % fps, "-i", "-"]
        if son:
            cmd += ["-i", args.video, "-map", "0:v", "-map", "1:a", "-c:a", "copy", "-shortest"]
        cmd += ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", args.sortie]
        ecriture = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    taille = W * H * 3
    suivi, h_suivi, dernier, i = None, None, None, 0
    while True:
        brut = lecture.stdout.read(taille)
        if len(brut) < taille:
            break
        t = i / fps
        img = np.frombuffer(brut, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        coins = None
        if t + 0.5 / fps >= args.debut:
            if cles:
                coins = interpoler_cles(cles, t)
            elif args.suivi == "fixe":
                coins = coins0
            else:
                g = gris(img)
                if suivi is None:
                    suivi = Suivi(g, points0, coins0, rayon=args.rayon, recherche=args.recherche,
                                  auto=not args.points_fixes)
                    h_suivi = np.eye(3)
                elif h_suivi is not None:
                    h_suivi = suivi.avancer(g)
                    if h_suivi is None:
                        log("· à %.2f s plus assez de repères : le logo n'est plus suivi" % t)
                if h_suivi is None:
                    coins = None
                    if not fin_suivi_ok(dernier, W, H):
                        lecture.kill()
                        if ecriture:
                            ecriture.stdin.close()
                        sys.exit("✗ à %.2f s le suivi a décroché alors que le logo est encore à "
                                 "l'image : la zone est trop unie ou le plan bouge trop vite. "
                                 "Donne avec --points des repères contrastés sur le même plan, "
                                 "augmente --recherche, ou passe en coins à la main avec --cles." % t)
                else:
                    coins = appliquer(h_suivi, coins0)
                    dernier = coins
        if coins is not None:
            img = incruster(img, logo, coins, t - args.debut, reg)
        if args.apercu is not None and t + 0.5 / fps >= args.apercu:
            Image.fromarray((img * 255).astype(np.uint8)).save(args.sortie)
            lecture.kill()
            log("✓ aperçu : %s" % args.sortie)
            return
        if ecriture:
            ecriture.stdin.write((img * 255 + 0.5).astype(np.uint8).tobytes())
        i += 1
    if ecriture:
        ecriture.stdin.close()
        ecriture.wait()
        log("✓ %s (%d images)" % (args.sortie, i))


def main():
    p = argparse.ArgumentParser(description="Logo qui se dessine en néon puis se remplit, "
                                            "incrusté et suivi sur une surface du plan.")
    p.add_argument("video")
    p.add_argument("logo", help="PNG détouré ou SVG")
    p.add_argument("--debut", type=float, default=0.0, help="seconde où le tracé commence")
    p.add_argument("--coins", help="4 coins « x,y » à --debut : haut-gauche, haut-droite, "
                                   "bas-droite, bas-gauche")
    p.add_argument("--cles", help="fichier JSON de coins à plusieurs instants (sans suivi)")
    p.add_argument("--suivi", choices=["auto", "fixe"], default="auto")
    p.add_argument("--points", help="points à suivre (4 ou plus), par défaut les coins")
    p.add_argument("--points-fixes", action="store_true",
                   help="ne suivre que les points donnés, sans en ajouter")
    p.add_argument("--rayon", type=int, default=20, help="taille du repère suivi, en pixels")
    p.add_argument("--recherche", type=int, default=36, help="déplacement max par image, en pixels")
    p.add_argument("--duree-trace", type=float, default=0.8)
    p.add_argument("--duree-remplissage", type=float, default=0.5)
    p.add_argument("--neon", default="#C9A2FF", help="couleur du trait")
    p.add_argument("--remplissage", default="#EDE4FF", help="couleur du logo rempli")
    p.add_argument("--opacite", type=float, default=0.9, help="opacité du logo rempli")
    p.add_argument("--lueur-finale", type=float, default=0.35, help="néon restant après remplissage")
    p.add_argument("--force-lueur", type=float, default=0.8)
    p.add_argument("--flou", type=float, default=0.6, help="douceur du logo, en pixels")
    p.add_argument("--eclairage", type=float, default=0.35, help="0 à 1 : le logo prend la lumière du mur")
    p.add_argument("--sans-scintillement", action="store_true")
    p.add_argument("--reperes", help="sortir l'image de --debut avec une grille, puis s'arrêter")
    p.add_argument("--apercu", type=float, help="ne sortir qu'une image PNG à cette seconde")
    p.add_argument("--sortie", default="vfx-logo.mp4")
    args = p.parse_args()

    if args.reperes:
        reperes(extraire(trouver_ffmpeg(), args.video, args.debut), args.reperes)
        return
    reg = {"duree_trace": args.duree_trace, "duree_remplissage": args.duree_remplissage,
           "neon": hex_rgb(args.neon), "remplissage": hex_rgb(args.remplissage),
           "opacite": args.opacite, "lueur_finale": args.lueur_finale,
           "force_lueur": args.force_lueur, "flou": args.flou, "eclairage": args.eclairage,
           "scintillement": not args.sans_scintillement}
    rendre(args, reg)


if __name__ == "__main__":
    main()

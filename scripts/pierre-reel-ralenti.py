#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pierre Huiban : reels et stories en ralenti à partir des rushes FX3 de Rome.

Trois gabarits, une seule chaîne :

- « reel » : le style que Maxime a donné en référence le 07/10/2026 (reel de
  @rundadlift, instagram.com/p/DeH2T6FOUuJ) : image en noir et blanc, ralenti,
  phrases courtes en jaune, police à empattements, posées en bas à gauche du
  tiers inférieur, qui apparaissent l'une après l'autre. Pas de logo, pas de
  carton : l'image et la phrase portent tout.
- « story » : le même ralenti, en couleur, sous le calque de la DA « trois
  vies » (dégradé, registre ATHLETE · FATHER · EXECUTIVE, phrase du jour),
  produit par `pierre-story-photo-v2.py - SPEC CLE calque.png`.
- « monologue » : la référence du 13/10/2026 (reel de @rundadlift,
  instagram.com/reel/DeHgY1RxPfB) : le monologue intérieur d'un père qui court,
  en phrases très courtes. Noir et blanc sombre et contrasté, léger grain, flou
  de bougé facultatif. Sous-titres CENTRÉS, bloc centré à 0,75 H, une ou deux
  lignes, Fraunces SemiBold statique (fonts/fraunces/, opsz 100), 64 px,
  approche -0,045 em (encre, largeur et hauteur de la couverture à 1 % près),
  mots allumés un à un à leur place définitive (chaque ligne est
  centrée sur son texte complet, les mots ne bougent jamais), fondu court,
  blanc cassé, et les « mots_jaunes » en jaune #F2D124. Contour noir doux
  (60 %, 3 px, flou 0,8) pour la lisibilité sur fond clair ; le contraste est
  MESURÉ sous le texte sur chaque image du rendu (cible 4,5 au pire pixel) et
  un voile local léger s'ajoute derrière le bloc si la cible n'est pas tenue.
  Mesures de la référence : REFERENCE.md du chantier, résumées dans
  projets/pierre-huiban/reels-dialogue/README.md, section « Gabarit monologue ».

Les rushes sont en 4K 100p S-Log3 (S-Gamut3.Cine). Le ralenti est un vrai
ralenti : 100 images par seconde relues à 25, soit ×4, sans image inventée.
L'étalonnage passe par `slog3.cube` (S-Log3 → Rec.709, courbe filmique douce),
écrit par `--lut`. Toutes les sorties sont MUETTES (règle stories-sans-son,
étendue aux reels : Maxime pose la musique dans Instagram). Seule exception,
voulue par Maxime le 07/10/2026 : la voix d'enfant des reels « dialogue »
(clé `voix`), une voix de synthèse Artlist, jamais un clone de voix réelle. Le
gabarit monologue refuse toute clé `voix` : on ne synthétise jamais la voix de
Pierre.

Usage :
    python3 pierre-reel-ralenti.py --lut slog3.cube
    python3 pierre-reel-ralenti.py SPEC.json [--rushes DOSSIER] [--polices fonts]
                                   [--drive-index rushes-drive.json] [--sans-relais]

SPEC :
{
  "gabarit": "reel" | "story" | "monologue",
  "sortie": "reel-2026-10-08.mp4",
  "ralenti": 4,
  "plans": [{"clip": "7374", "debut": 1.0, "duree": 1.5, "x": 0.5}, ...],
  "textes": [{"debut": 0.5, "fin": 4.0, "texte": "Station eight."}, ...],   # reel
  "calque": "calque-mer.png",                                              # story
  "voix": [{"fichier": "q1.mp3", "debut": 0.4}, ...],                      # reel, facultatif
  "sous_titres": [{"t": 0.4, "fin": 3.8,                                   # monologue
                   "lignes": ["He won't remember", "Rome, or 53:34."],
                   "mots_jaunes": ["53:34"]}, ...]
}
`debut` et `duree` d'un plan sont en secondes du RUSH ; la durée à l'écran est
multipliée par `ralenti` (réglable plan par plan : ×2 pour un rush en 50p, ×1
pour un rush en 25p). `"slog3": false` sur un plan déjà en Rec.709 (téléphone,
rushes d'entraînement non log) saute la LUT. `clip` est un bout du nom de
fichier (« 7374 » trouve FX3POST20260926_7374.MP4 dans tout `--rushes`). Une
voix peut porter `"hauteur": 1.3` (rubberband) pour rajeunir la voix. `x` place le recadrage 9:16 dans la largeur (0 = bord
gauche, 1 = bord droit). Les temps des textes sont ceux de la vidéo finie.

Carton (tous gabarits) : un plan `{"clip": "CARTON NOIR", "duree": 0.88}` (ou
`"carton": "noir"`) est un fond noir sans rush, pour un temps qui n'a aucune
image (reel des splits de Rome, D1-R8). Il dure `duree` × `ralenti` du plan, et 1
par défaut (pas le `ralenti` global) ; il reçoit le même étalonnage que les
autres plans, grain compris, et ne lit rien sur Drive.

Rushes à distance (tous gabarits) : `clip` peut être une URL http(s) ; avec
`--drive-index` (JSON {"clips": [{"clip": "FX3POST20260926_7345.MP4", "id":
"…"}]}, une liste de ces objets, ou {nom: id}), le clip est cherché dans
l'index et lu sur Drive par plages HTTP, sans téléchargement complet
(drive.usercontent.google.com/download?id=ID&export=download&confirm=t), à
travers le proxy de l'environnement (HTTPS_PROXY). Drive répond « Quota
exceeded » aux plages OUVERTES que demande ffmpeg (13/10/2026) : par défaut un
relais local (classe Relais) les découpe en plages bornées de 4 Mo, gardées dans
`_cache_rushes/`. `--sans-relais` passe l'URL telle quelle à ffmpeg avec
`-http_proxy`. Sans index ni URL, le rush est cherché dans `--rushes` comme avant.

Gabarit monologue, clés propres (toutes facultatives sauf `sous_titres`) :
- `sous_titres[]` : `t` et `fin` en secondes de la vidéo finie ; `lignes` (1
  ou 2) ; `mots_jaunes` (mots ou suites de mots du bloc, ponctuation et casse
  ignorées ; "*" = tout le bloc en jaune, comme sur la couverture mesurée) ;
  `horodatages` (un instant par mot, sinon interpolés) ; `tenue` (secondes où
  le bloc reste complet avant `fin`, 0 par défaut) ; `mot_en_cours` (karaoké :
  le dernier mot allumé est jaune jusqu'au suivant).
- Allumage : chaque mot apparaît à t + (fin - tenue - t) × (lettres des mots
  qui le précèdent / lettres du bloc), donc proportionnellement à la longueur
  des mots ; fondu d'entrée `fondu` (0,16 s, 4 images), sortie du bloc en
  `fondu_sortie` (0,16 s ; 0 = coupe sèche).
- Image : `exposition` (LUT S-Log3 réécrite à cette exposition, globale ou par
  plan ; sans elle, la LUT de `--lut`), `courbe` (courbe en S de `curves`, voir
  COURBE_NB ; "" = sans), `contraste`, `luminosite`, `gamma` (retouche `eq`,
  absente par défaut), `grain` (6, luminance seule), `flou_bouge` (nombre
  d'images de rush mélangées, 0 = sans ; global ou par plan). Contrôle :
  mesure_etalonnage.py du chantier sur une image extraite du rendu.
- Texte : `taille` (64), `approche` (-0,045 em), `graisse` ("semibold") et
  `graisse_jaune` (comme `graisse`), "regular" ou "semibold" ; l'instance du
  dépôt passe avant une Fraunces posée à plat dans `--polices` ;
  `ombre` {opacite, epaisseur, flou},
  `contraste_cible` (4,5), `voile_max` (0,45).
- Refus : plus de deux lignes, ligne plus large que 0,9 W, bloc qui chevauche
  le suivant, tiret cadratin, demi-cadratin ou double tiret, clé `voix`.
- Les specs du chantier écrites au format `textes` (`debut`, `fin`, `texte`
  avec \\n, `jaunes`, `mots[{mot, t}]`) sont acceptées telles quelles en
  gabarit monologue, ou en gabarit reel avec `"texte_mode": "centre_mot_a_mot"`.
"""
import argparse
import fnmatch
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 25
JAUNE = (244, 208, 63)
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def lut_exposee(lut, exposition):
    """La LUT de `--lut`, ou sa variante à une autre exposition (écrite une fois, à côté)."""
    if exposition is None:
        return lut
    base, ext = os.path.splitext(lut)
    chemin = f"{base}-e{float(exposition):g}{ext or '.cube'}"
    if not os.path.exists(chemin):
        ecrire_lut(chemin, exposition=float(exposition))
    return chemin


# ---------------------------------------------------------------- règles de texte

# Règle du dépôt : aucun tiret cadratin, demi-cadratin ni double tiret dans un
# texte publié ou rendu. Le trait d'union simple (« 35-39 ») reste permis.
TIRETS_INTERDITS = {
    "\u2012": "tiret numérique", "\u2013": "tiret demi-cadratin", "\u2014": "tiret cadratin",
    "\u2015": "barre horizontale", "\u2e3a": "tiret double cadratin",
    "\u2e3b": "tiret triple cadratin", "\ufe31": "tiret cadratin vertical",
    "\ufe32": "tiret demi-cadratin vertical", "\ufe58": "petit tiret cadratin",
}


def verifier_tirets(texte, ou="texte"):
    for c, nom in TIRETS_INTERDITS.items():
        if c in texte:
            raise SystemExit(f"{nom} interdit dans {ou} : « {texte} » (règle du dépôt : "
                             "aucun tiret cadratin, demi-cadratin ni double tiret)")
    if "--" in texte:
        raise SystemExit(f"double tiret interdit dans {ou} : « {texte} »")


# ---------------------------------------------------------------- polices

def fichier_police(polices, nom, depot_d_abord=False):
    """`polices/nom`, puis `polices/fraunces/nom`, puis `fonts/fraunces/nom` du dépôt.
    `depot_d_abord` (gabarit monologue, calé sur l'instance opsz 100 du dépôt) : un
    Fraunces quelconque posé à plat dans `--polices` (souvent la coupe opsz 9, un tiers
    plus large) ne passe qu'en dernier."""
    dossiers = [polices, os.path.join(polices, "fraunces"), os.path.join(RACINE, "fonts", "fraunces")]
    if depot_d_abord:
        dossiers = dossiers[1:] + dossiers[:1]
    for d in dossiers:
        chemin = os.path.join(d, nom)
        if os.path.exists(chemin):
            return chemin
    raise SystemExit(f"police introuvable : {nom} (cherchée dans {polices}, {polices}/fraunces "
                     "et fonts/fraunces du dépôt)")


# ---------------------------------------------------------------- textes (gabarit reel)

def carton_texte(texte, polices, chemin):
    """Une phrase du gabarit reel : jaune, empattements, tiers inférieur, ombre douce."""
    verifier_tirets(texte, "un texte du reel")
    police = ImageFont.truetype(fichier_police(polices, "Fraunces-Regular.ttf"), 58)
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


# ---------------------------------------------------------------- sous-titres (gabarit monologue)

# Mesures de la référence DeHgY1RxPfB (REFERENCE.md, section 3), repli Fraunces.
JAUNE_MONO = (242, 209, 36)        # #F2D124, médiane mesurée du jaune de la référence
BLANC_CASSE = (245, 241, 230)      # #F5F1E6, mots allumés hors « mots_jaunes »
TAILLE_MONO = 64                   # px : Fraunces SemiBold opsz 100, encre et largeurs mesurées
APPROCHE_MONO = -0.045             # em, entre les lettres d'un même mot seulement
BASE_1_LIGNE = 0.7588              # ligne de base d'un bloc d'une ligne, en H
DEMI_INTERLIGNE = 0.0176           # remontée de la 1re base par ligne en plus, en H
INTERLIGNE = 0.0352                # base à base, en H (67,6 px)
LIGNES_MAX = 2
LARGEUR_MAX = 0.90                 # au-delà : refus (la ligne frôle les bords)
LARGEUR_CONSEILLEE = 0.60          # plafond proposé par la fiche : avertissement
OMBRE = {"opacite": 0.60, "epaisseur": 3, "flou": 0.8}
FONDU = 0.16                       # 4 images à 25 i/s
CONTRASTE_CIBLE = 4.5
VOILE_MAX = 0.45
BANDE = (1180, 1680)               # tranche de l'image où vivent les sous-titres (y0, y1)
GRAISSES = {"regular": "Fraunces-Regular.ttf", "semibold": "Fraunces-SemiBold.ttf"}

_MESURE = ImageDraw.Draw(Image.new("L", (1, 1)))
_AVERTIES = set()


def _norm(mot):
    """« Boy. » → « boy », « 53:34. » → « 53:34 » : casse et ponctuation de bord ignorées."""
    mot = mot.casefold().replace("\u2019", "'")
    return re.sub(r"^\W+|\W+$", "", mot)


def decouper(lignes):
    """[(ligne, mot)] dans l'ordre de lecture. Les mots sont séparés par des blancs."""
    if isinstance(lignes, str):
        lignes = [lignes]
    if not lignes or len(lignes) > LIGNES_MAX:
        raise SystemExit(f"un sous-titre a une ou deux lignes, pas {len(lignes)} : {lignes}")
    mots = []
    for i, ligne in enumerate(lignes):
        if not isinstance(ligne, str) or not ligne.strip():
            raise SystemExit(f"ligne vide dans un sous-titre : {lignes}")
        verifier_tirets(ligne, "un sous-titre")
        mots += [(i, m) for m in ligne.split()]
    return mots


def horodater(mots, t, fin, tenue=0.0):
    """Instant d'apparition de chaque mot, interpolé entre `t` et `fin - tenue`
    au prorata de la longueur des mots : un mot long « dure » plus longtemps."""
    duree = fin - tenue - t
    if duree <= 0:
        raise SystemExit(f"sous-titre trop court : t={t}, fin={fin}, tenue={tenue}")
    poids = [max(1, len(m)) for m in mots]
    total, cumul, instants = sum(poids), 0, []
    for p in poids:
        instants.append(round(t + duree * cumul / total, 4))
        cumul += p
    return instants


def marquer_jaunes(mots, mots_jaunes):
    """Un booléen par mot. Chaque entrée est un mot ou une suite de mots du bloc
    (casse et ponctuation de bord ignorées) ; "*" passe tout le bloc en jaune.
    Une entrée introuvable est une faute de frappe : refus."""
    if mots_jaunes in ("*", ["*"]):
        return [True] * len(mots)
    if isinstance(mots_jaunes, str):
        mots_jaunes = [mots_jaunes]
    normes = [_norm(m) for m in mots]
    jaunes = [False] * len(mots)
    for entree in mots_jaunes or []:
        verifier_tirets(entree, "mots_jaunes")
        cible = [_norm(m) for m in entree.split() if _norm(m)]
        trouve = False
        for i in range(len(normes) - len(cible) + 1):
            if cible and normes[i:i + len(cible)] == cible:
                jaunes[i:i + len(cible)] = [True] * len(cible)
                trouve = True
        if not trouve:
            raise SystemExit(f"mot jaune introuvable dans le sous-titre : « {entree} » "
                             f"(mots : {' '.join(mots)})")
    return jaunes


def bases_lignes(n):
    """Lignes de base (px) d'un bloc de n lignes : bloc centré à 0,75 H."""
    return [H * (BASE_1_LIGNE - DEMI_INTERLIGNE * (n - 1) + INTERLIGNE * i) for i in range(n)]


def avances(mot, police, approche_px):
    """Abscisse de chaque lettre depuis l'origine du mot (crénage conservé, approche
    ajoutée entre les lettres) et chasse totale du mot."""
    xs = [_MESURE.textlength(mot[:k + 1], font=police) - _MESURE.textlength(mot[k], font=police)
          + k * approche_px for k in range(len(mot))]
    return xs, _MESURE.textlength(mot, font=police) + (len(mot) - 1) * approche_px


class Mot:
    def __init__(self, texte, ligne, t, jaune):
        self.texte, self.ligne, self.t, self.jaune = texte, ligne, t, jaune
        self.x = self.base = self.largeur = 0.0
        self.xs, self.police = [], None
        self.couche = None      # (y0, x0, glyphe, halo) en coordonnées de la bande


class Bloc:
    def __init__(self, t, fin, lignes, mots, mot_en_cours=False, fondu=FONDU, fondu_sortie=FONDU):
        self.t, self.fin, self.lignes, self.mots = t, fin, lignes, mots
        self.mot_en_cours, self.fondu, self.fondu_sortie = mot_en_cours, fondu, fondu_sortie
        self.voile, self.contraste = 0.0, None
        self.masque_voile = None   # (y0, x0, masque) en coordonnées de la bande
        self.taille, self.voile_max, self.cible = TAILLE_MONO, VOILE_MAX, CONTRASTE_CIBLE

    def couleur(self, k, t):
        m = self.mots[k]
        if m.jaune:
            return JAUNE_MONO
        if self.mot_en_cours:
            suivant = self.mots[k + 1].t if k + 1 < len(self.mots) else self.fin
            if t < suivant:
                return JAUNE_MONO
        return BLANC_CASSE

    def couleurs_possibles(self):
        cs = {JAUNE_MONO if m.jaune else BLANC_CASSE for m in self.mots}
        if self.mot_en_cours:
            cs.add(JAUNE_MONO)
        return cs


def _rampe(dt, duree):
    if dt < 0:
        return 0.0
    return 1.0 if duree <= 0 else min(1.0, dt / duree)


def _couche(img, y0, x0):
    """Rogne une couche (y0, x0, tableau) à la bande ; None si elle en sort."""
    import numpy as np
    a = np.asarray(img, dtype=np.float32) / 255.0
    hb = BANDE[1] - BANDE[0]
    y, x = y0 - BANDE[0], x0
    t, l = max(0, -y), max(0, -x)
    b, r = min(a.shape[0], hb - y), min(a.shape[1], W - x)
    if b <= t or r <= l:
        return None
    return y + t, x + l, a[t:b, l:r]


def preparer_bloc(st, polices, opts=None):
    """Un sous-titre de la spec → Bloc mis en page : position figée de chaque mot,
    couches glyphe et halo prêtes à composer. Aucune dépendance à ffmpeg."""
    opts = opts or {}
    t, fin = float(st["t"]), float(st["fin"])
    if fin <= t:
        raise SystemExit(f"sous-titre avec fin <= t : {st}")
    lignes = st["lignes"] if isinstance(st["lignes"], list) else [st["lignes"]]
    paires = decouper(lignes)
    textes = [m for _, m in paires]
    jaunes = marquer_jaunes(textes, st.get("mots_jaunes", []))
    if st.get("horodatages") is not None:
        inst = [float(x) for x in st["horodatages"]]
        if len(inst) != len(textes):
            raise SystemExit(f"{len(inst)} horodatages pour {len(textes)} mots : {lignes}")
        if any(b < a for a, b in zip(inst, inst[1:])) or inst[0] < t or inst[-1] >= fin:
            raise SystemExit(f"horodatages hors de [t, fin[ ou dans le désordre : {inst}")
    else:
        inst = horodater(textes, t, fin, float(st.get("tenue", opts.get("tenue", 0.0))))
    mots = [Mot(m, i, ti, j) for (i, m), ti, j in zip(paires, inst, jaunes)]

    taille = int(opts.get("taille", TAILLE_MONO))
    approche = float(opts.get("approche", APPROCHE_MONO)) * taille
    graisse = opts.get("graisse", "semibold")
    graisse_j = opts.get("graisse_jaune", graisse)
    for g in (graisse, graisse_j):
        if g not in GRAISSES:
            raise SystemExit(f"graisse inconnue : {g} (au choix : {', '.join(GRAISSES)})")
    p_norm = ImageFont.truetype(fichier_police(polices, GRAISSES[graisse], True), taille)
    p_jaune = ImageFont.truetype(fichier_police(polices, GRAISSES[graisse_j], True), taille)
    espace = _MESURE.textlength(" ", font=p_norm)
    ombre = dict(OMBRE, **(opts.get("ombre") or {}))

    # mise en page : chaque ligne centrée sur son texte COMPLET, positions figées
    bases = bases_lignes(len(lignes))
    for i in range(len(lignes)):
        de_la_ligne = [m for m in mots if m.ligne == i]
        for m in de_la_ligne:
            m.police = p_jaune if m.jaune else p_norm
            m.xs, m.largeur = avances(m.texte, m.police, approche)
        largeur = sum(m.largeur for m in de_la_ligne) + espace * (len(de_la_ligne) - 1)
        if largeur > LARGEUR_MAX * W:
            raise SystemExit(f"ligne trop large pour le cadre ({largeur / W:.2f} W > {LARGEUR_MAX} W) : "
                             f"« {lignes[i]} »")
        if largeur > LARGEUR_CONSEILLEE * W and lignes[i] not in _AVERTIES:
            _AVERTIES.add(lignes[i])
            print(f"  attention : « {lignes[i]} » fait {largeur / W:.2f} W "
                  f"(la référence plafonne vers {LARGEUR_CONSEILLEE} W)", file=sys.stderr)
        x = (W - largeur) / 2
        for m in de_la_ligne:
            m.x, m.base = x, bases[i]
            x += m.largeur + espace

    # couches : glyphe (alpha) et halo noir doux (alpha), rognées autour du mot
    ep, flou, opa = int(ombre["epaisseur"]), float(ombre["flou"]), float(ombre["opacite"])
    for m in mots:
        asc, desc = m.police.getmetrics()
        marge = ep + int(math.ceil(3 * flou)) + int(0.2 * taille) + 2
        x0 = int(math.floor(m.x)) - marge
        y0 = int(math.floor(m.base)) - asc - marge
        img = Image.new("L", (int(math.ceil(m.largeur)) + 2 * marge + 1, asc + desc + 2 * marge + 1), 0)
        d = ImageDraw.Draw(img)
        for c, xk in zip(m.texte, m.xs):
            d.text((m.x - x0 + xk, m.base - y0), c, font=m.police, fill=255, anchor="ls")
        # le contour part du glyphe renforcé (×2) : anneau régulier, déliés compris
        halo = img.point(lambda v: min(255, 2 * v))
        halo = halo.filter(ImageFilter.MaxFilter(2 * ep + 1)) if ep > 0 else halo
        halo = halo.filter(ImageFilter.GaussianBlur(flou)) if flou > 0 else halo
        g, h = _couche(img, y0, x0), _couche(halo, y0, x0)
        m.couche = (g[0], g[1], g[2], h[2] * opa) if g else None

    b = Bloc(t, fin, lignes, mots, bool(st.get("mot_en_cours", opts.get("mot_en_cours", False))),
             float(opts.get("fondu", FONDU)), float(opts.get("fondu_sortie", FONDU)))
    b.taille = taille
    b.voile_max = float(opts.get("voile_max", VOILE_MAX))
    b.cible = float(opts.get("contraste_cible", CONTRASTE_CIBLE))
    _preparer_voile(b)
    return b


def _encre(b):
    """Boîte (y0, x0, y1, x1) de l'encre du bloc complet, en coordonnées de la bande."""
    import numpy as np
    y0 = x0 = 10 ** 9
    y1 = x1 = -1
    for m in b.mots:
        if m.couche is None:
            continue
        cy, cx, g, _ = m.couche
        ys, xs = np.nonzero(g > 0.1)
        if len(ys):
            y0, y1 = min(y0, cy + ys.min()), max(y1, cy + ys.max())
            x0, x1 = min(x0, cx + xs.min()), max(x1, cx + xs.max())
    return y0, x0, y1, x1


def _preparer_voile(b):
    """Voile local : rectangle adouci derrière le bloc complet (sert si besoin)."""
    import numpy as np
    y0, x0, y1, x1 = _encre(b)
    pad, sigma = int(0.8 * b.taille), 0.35 * b.taille
    hb = BANDE[1] - BANDE[0]
    img = Image.new("L", (W, hb), 0)
    ImageDraw.Draw(img).rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), fill=255)
    img = img.filter(ImageFilter.GaussianBlur(sigma))
    a = np.asarray(img, dtype=np.float32) / 255.0
    ys, xs = np.nonzero(a > 0.002)
    b.masque_voile = (ys.min(), xs.min(), a[ys.min():ys.max() + 1, xs.min():xs.max() + 1])


def _luminance(rgb):
    """Luminance relative WCAG d'un tableau (..., 3) en 0..255."""
    import numpy as np
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def _zone_et_halo(b):
    """Zone de mesure (glyphes dilatés de 2 px) et halo cumulé, sur toute la bande."""
    import numpy as np
    if getattr(b, "_zone_halo", None) is not None:
        return b._zone_halo
    hb = BANDE[1] - BANDE[0]
    glyphes = np.zeros((hb, W), np.uint8)
    reste = np.ones((hb, W), np.float32)
    for m in b.mots:
        if m.couche is None:
            continue
        y, x, g, h = m.couche
        sl = (slice(y, y + g.shape[0]), slice(x, x + g.shape[1]))
        glyphes[sl] = np.maximum(glyphes[sl], (g > 0.5).astype(np.uint8) * 255)
        reste[sl] *= 1.0 - h
    zone = np.asarray(Image.fromarray(glyphes).filter(ImageFilter.MaxFilter(5))) > 0
    b._zone_halo = (zone, 1.0 - reste)
    return b._zone_halo


def mesurer_contraste(b, fond_bande, voile=None):
    """Contraste WCAG au pire pixel entre la couleur la plus sombre du texte et le
    fond tel qu'il est vu sous le texte (fond assombri par le voile et le halo).
    `fond_bande` : image (hauteur de BANDE, W, 3), le maximum des images du bloc."""
    import numpy as np
    voile = b.voile if voile is None else voile
    zone, halo = _zone_et_halo(b)
    v = np.zeros_like(halo)
    y, x, mv = b.masque_voile
    v[y:y + mv.shape[0], x:x + mv.shape[1]] = mv
    fond = np.asarray(fond_bande, dtype=np.float64)[zone]
    facteur = ((1.0 - voile * v[zone]) * (1.0 - halo[zone]))[:, None]
    lf = _luminance(fond * facteur)
    lt = min(float(_luminance(np.array(c))) for c in b.couleurs_possibles())
    clair, sombre = np.maximum(lf, lt), np.minimum(lf, lt)
    return float(((clair + 0.05) / (sombre + 0.05)).min())


def regler_voile(b, fond_bande):
    """Plus petit voile (pas de 0,01, plafond `voile_max`) qui tient la cible."""
    v = 0.0
    while True:
        c = mesurer_contraste(b, fond_bande, v)
        if c >= b.cible or v >= b.voile_max - 1e-9:
            b.voile, b.contraste = round(v, 2), c
            return b.voile, c
        v = min(b.voile_max, v + 0.01)


def etat(blocs, t):
    """Ce qui est visible à l'instant t ; deux images au même état sont identiques."""
    cle = []
    for i, b in enumerate(blocs):
        if not (b.t <= t < b.fin):
            continue
        g = 1.0 if b.fondu_sortie <= 0 else min(1.0, (b.fin - t) / b.fondu_sortie)
        mots = tuple((k, round(g * _rampe(t - m.t, b.fondu), 4), b.couleur(k, t))
                     for k, m in enumerate(b.mots) if t >= m.t)
        cle.append((i, round(g * _rampe(t - b.t, b.fondu), 4), mots))
    return tuple(cle)


def composer(blocs, t):
    """Calque RGBA (alpha droit) de la bande des sous-titres à l'instant t."""
    import numpy as np
    hb = BANDE[1] - BANDE[0]
    A = np.zeros((hb, W), np.float32)
    P = np.zeros((hb, W, 3), np.float32)
    for i, fv, mots in etat(blocs, t):
        b = blocs[i]
        if b.voile > 0 and fv > 0:
            y, x, mv = b.masque_voile
            a = fv * b.voile * mv
            sl = (slice(y, y + mv.shape[0]), slice(x, x + mv.shape[1]))
            P[sl] *= (1.0 - a)[..., None]
            A[sl] = a + A[sl] * (1.0 - a)
        for k, f, couleur in mots:
            if f <= 0 or b.mots[k].couche is None:
                continue
            y, x, g, h = b.mots[k].couche
            sl = (slice(y, y + g.shape[0]), slice(x, x + g.shape[1]))
            aw = f * (g + h * (1.0 - g))
            pw = (f * g)[..., None] * (np.array(couleur, np.float32) / 255.0)
            P[sl] = pw + P[sl] * (1.0 - aw)[..., None]
            A[sl] = aw + A[sl] * (1.0 - aw)
    out = np.zeros((hb, W, 4), np.uint8)
    nz = A > 1e-6
    out[..., :3][nz] = np.clip(P[nz] / A[nz][:, None] * 255.0 + 0.5, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(A * 255.0 + 0.5, 0, 255).astype(np.uint8)
    return out


def apercu(blocs, t, fond):
    """Image 1080×1920 : `fond` (PIL) avec les sous-titres de l'instant t. Pour les
    contrôles et les tests ; le rendu vidéo compose la même bande dans ffmpeg."""
    img = fond.convert("RGBA").resize((W, H)) if fond.size != (W, H) else fond.convert("RGBA")
    img.alpha_composite(Image.fromarray(composer(blocs, t), "RGBA"), (0, BANDE[0]))
    return img


def sous_titres_de(spec):
    """Les sous-titres de la spec ; le format `textes` du chantier est accepté."""
    if "sous_titres" in spec:
        return spec["sous_titres"]
    sts = []
    for tx in spec.get("textes", []):
        st = {"t": tx["debut"], "fin": tx["fin"], "lignes": tx["texte"].split("\n"),
              "mots_jaunes": tx.get("mots_jaunes", tx.get("jaunes", []))}
        if tx.get("mots"):
            st["horodatages"] = [m["t"] for m in tx["mots"]]
        sts.append(st)
    if not sts:
        raise SystemExit("gabarit monologue sans « sous_titres »")
    return sts


def preparer_sous_titres(spec, polices, total=None):
    """Tous les blocs de la spec, contrôlés : ordre, chevauchement, tirets, légende."""
    if spec.get("voix"):
        raise SystemExit("le gabarit monologue est muet : pas de clé « voix » (on ne synthétise "
                         "jamais la voix de Pierre ; s'il s'enregistre lui-même, sa voix se pose "
                         "au montage final)")
    if isinstance(spec.get("legende"), str):
        verifier_tirets(spec["legende"], "la légende")
    blocs = []
    for st in sous_titres_de(spec):
        st = dict(st)
        if total is not None:
            if float(st["t"]) >= total:
                raise SystemExit(f"sous-titre après la fin de la vidéo ({total:.2f} s) : {st}")
            st["fin"] = min(float(st["fin"]), total)
        blocs.append(preparer_bloc(st, polices, spec))
    for a, b in zip(blocs, blocs[1:]):
        if b.t < a.fin - 1e-6:
            raise SystemExit(f"sous-titres qui se chevauchent : « {' / '.join(a.lignes)} » finit à "
                             f"{a.fin} s, « {' / '.join(b.lignes)} » commence à {b.t} s")
    return blocs


# ---------------------------------------------------------------- montage

def binaire_ffmpeg():
    """$FFMPEG, sinon ffmpeg du PATH (Homebrew sur le Mac), sinon celui d'imageio-ffmpeg."""
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    trouve = shutil.which("ffmpeg")
    if trouve:
        return trouve
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def ffmpeg(*args):
    subprocess.run([binaire_ffmpeg(), "-v", "error", "-y", *args], check=True)


def trouver_rush(dossier, clip):
    """« 7374 » → FX3POST20260926_7374.MP4, cherché dans tout le dossier (casse ignorée)."""
    for motif in (f"{clip}.mp4", f"*{clip}.mp4", f"*{clip}*.mp4", f"*{clip}*.mov"):
        for chemin in glob.glob(os.path.join(dossier, "**", "*"), recursive=True):
            if fnmatch.fnmatch(os.path.basename(chemin).lower(), motif):
                return chemin
    raise SystemExit(f"rush introuvable pour le clip {clip} dans {dossier}")


URL_DRIVE = "https://drive.usercontent.google.com/download?id={id}&export=download&confirm=t"


def charger_index_drive(chemin):
    """{nom de fichier: id Drive} depuis {"clips": [...]}, une liste, ou {nom: id}."""
    with open(chemin, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("clips"), list):
        items = data["clips"]
    elif isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = [{"clip": k, "id": v.get("id") if isinstance(v, dict) else v}
                 for k, v in data.items() if not k.startswith("_") and isinstance(v, (str, dict))]
    else:
        items = []
    index = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        nom = it.get("clip") or it.get("name") or it.get("title") or it.get("nom")
        if nom and it.get("id"):
            index[str(nom)] = str(it["id"])
    return index


def trouver_dans_index(index, clip):
    for motif in (f"{clip}.mp4", f"*{clip}.mp4", f"*{clip}*.mp4", f"*{clip}*.mov"):
        for nom, fid in index.items():
            if fnmatch.fnmatch(os.path.basename(nom).lower(), motif.lower()):
                return fid
    return None


def source_rush(clip, rushes, index=None):
    """(chemin ou URL, options d'entrée ffmpeg). Une URL est lue par plages HTTP,
    à travers le proxy de l'environnement s'il y en a un."""
    clip = str(clip)
    if re.match(r"https?://", clip):
        url = clip
    else:
        fid = trouver_dans_index(index, clip) if index else None
        if not fid:
            return trouver_rush(rushes, clip), []
        url = URL_DRIVE.format(id=fid)
    proxy = next((os.environ[k] for k in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy")
                  if os.environ.get(k)), None)
    return url, (["-http_proxy", proxy] if proxy else [])


# ---------------------------------------------------------------- relais HTTP (rushes à distance)

BLOC_HTTP = 4 * 1024 * 1024


def telecharger_plage(url, a, b):
    """(octets a..b de l'URL, taille totale), en UNE requête bornée. Le proxy et les
    certificats sont ceux de l'environnement (HTTPS_PROXY, SSL_CERT_FILE)."""
    import urllib.request
    req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}", "User-Agent": "curl/8"})
    with urllib.request.urlopen(req, timeout=120) as r:
        if r.status != 206 or "text/html" in r.headers.get("Content-Type", ""):
            raise IOError(f"plage {a}-{b} refusée (HTTP {r.status}, {r.headers.get('Content-Type')}) : "
                          "quota Drive dépassé ou fichier non partagé")
        total = int(r.headers.get("Content-Range", "/0").rsplit("/", 1)[1])
        return r.read(), total


class Relais:
    """Serveur local entre ffmpeg et Drive. ffmpeg demande des plages OUVERTES
    (bytes=N-) ; Drive les compte comme un téléchargement complet et répond
    « Quota exceeded » (constaté le 13/10/2026). Le relais les découpe en blocs
    bornés de 4 Mo, gardés sur disque : un clip monté trois fois n'est lu qu'une fois."""

    def __init__(self, cache="_cache_rushes", telecharger=None, bloc=BLOC_HTTP):
        import http.server
        import threading
        self.cache, self.bloc_octets = cache, bloc
        self.telecharger = telecharger or telecharger_plage
        self.urls, self.tailles, self.erreur = {}, {}, None
        self.verrou = threading.Lock()
        self.stats = {"blocs": 0, "octets": 0}
        relais = self

        class Gestion(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *a):
                pass

            def do_HEAD(self):
                self._servir(corps=False)

            def do_GET(self):
                self._servir(corps=True)

            def _servir(self, corps):
                cle = self.path.strip("/").split("?")[0]
                try:
                    total = relais.taille(cle)
                except Exception as e:      # noqa: BLE001 (on rend la main à ffmpeg)
                    relais.erreur = str(e)
                    self.send_error(503 if cle in relais.urls else 404)
                    return
                m = re.match(r"bytes=(\d+)-(\d*)", self.headers.get("Range", ""))
                a = int(m.group(1)) if m else 0
                b = min(int(m.group(2)) if m and m.group(2) else total - 1, total - 1)
                if a >= total:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{total}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                self.send_response(206 if m else 200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Accept-Ranges", "bytes")
                if m:
                    self.send_header("Content-Range", f"bytes {a}-{b}/{total}")
                self.send_header("Content-Length", str(b - a + 1))
                self.send_header("Connection", "close")
                self.end_headers()
                if not corps:
                    return
                pos = a
                try:
                    while pos <= b:
                        k = pos // relais.bloc_octets
                        d = relais.bloc(cle, k)
                        seg = d[pos - k * relais.bloc_octets:b + 1 - k * relais.bloc_octets]
                        self.wfile.write(seg)
                        pos += len(seg)
                except (BrokenPipeError, ConnectionResetError):
                    pass                     # ffmpeg a fermé pour sauter ailleurs : normal
                except Exception as e:      # noqa: BLE001
                    relais.erreur = str(e)

        self.serveur = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Gestion)
        self.serveur.daemon_threads = True
        threading.Thread(target=self.serveur.serve_forever, daemon=True).start()

    def adresse(self, url):
        cle = str(len(self.urls))
        for c, u in self.urls.items():
            if u == url:
                cle = c
        self.urls[cle] = url
        return f"http://127.0.0.1:{self.serveur.server_address[1]}/{cle}"

    def taille(self, cle):
        if cle not in self.tailles:
            _, self.tailles[cle] = self.telecharger(self.urls[cle], 0, 0)
        return self.tailles[cle]

    def bloc(self, cle, k):
        chemin = None
        if self.cache:
            os.makedirs(self.cache, exist_ok=True)
            nom = re.sub(r"[^A-Za-z0-9_-]", "_", self.urls[cle])[-120:]
            chemin = os.path.join(self.cache, f"{nom}.{self.bloc_octets}.{k}")
        with self.verrou:
            if chemin and os.path.exists(chemin):
                with open(chemin, "rb") as f:
                    return f.read()
            a = k * self.bloc_octets
            b = min(a + self.bloc_octets, self.taille(cle)) - 1
            d, _ = self.telecharger(self.urls[cle], a, b)
            self.stats["blocs"] += 1
            self.stats["octets"] += len(d)
            if chemin:
                with open(chemin + ".part", "wb") as f:
                    f.write(d)
                os.replace(chemin + ".part", chemin)
        return d

    def fermer(self):
        self.serveur.shutdown()
        self.serveur.server_close()


class Sources:
    """Résout le `clip` d'un plan : fichier local, ou URL lue à travers le relais
    (par défaut) ou en direct avec -http_proxy (`relais=False`)."""

    def __init__(self, rushes=".", index=None, relais=True, cache="_cache_rushes"):
        self.rushes, self.index, self.avec_relais, self.cache = rushes, index, relais, cache
        self.relais = None

    def __call__(self, clip):
        chemin, entree = source_rush(clip, self.rushes, self.index)
        if not re.match(r"https?://", chemin) or not self.avec_relais:
            return chemin, entree
        if self.relais is None:
            self.relais = Relais(self.cache)
        return self.relais.adresse(chemin), []

    def fermer(self):
        if self.relais is not None:
            self.relais.fermer()
            self.relais = None


# Courbe en S du noir et blanc « monologue », calée le 13/10/2026 sur trois images du
# clip 7351 (sled pull, LUT exposition 0,9) contre les cibles mesurées sur la
# référence : p1 2 à 4, p5 6 à 8, médiane 51 à 86, p95 183 à 184 (cibles : p1 <= 5,
# p5 5 à 26, médiane 50 à 90, p95 160 à 255). Avec `eq=contrast=1.3`, p5 tombait à 0
# et la médiane montait à 96 à 129.
COURBE_NB = "0/0 0.18/0.07 0.5/0.31 0.78/0.72 1/1"


def filtre_nb_monologue(courbe=COURBE_NB, contraste=None, luminosite=None, gamma=None, grain=6):
    """Noir et blanc sombre et contrasté : courbe en S, retouche `eq` seulement si
    demandée, grain sur la luminance seule, chroma nulle (passage en gris)."""
    f = "hue=s=0"
    if courbe:
        f += f",curves=master='{courbe}'"
    if contraste is not None or luminosite is not None or gamma is not None:
        f += (f",eq=contrast={1.0 if contraste is None else contraste}"
              f":brightness={0.0 if luminosite is None else luminosite}"
              f":gamma={1.0 if gamma is None else gamma}")
    if grain:
        f += f",noise=c0s={grain}:c0f=t"
    return f + ",format=gray"


def plan(rush, debut, duree, x, ralenti, lut, nb, sortie, p_log=True, entree=(), grade=None,
         flou_bouge=0):
    filtre = (f"setpts={ralenti}*PTS,"
              f"crop=ih*9/16:ih:(iw-ih*9/16)*{x}:0,"
              f"scale={W}:{H}:flags=lanczos,setsar=1,lut3d={lut}")
    if p_log is False:
        filtre = filtre.replace(f",lut3d={lut}", "")
    if flou_bouge and int(flou_bouge) > 1:
        filtre += f",tmix=frames={int(flou_bouge)}"
    if grade:
        filtre += "," + grade
    elif nb:
        filtre += ",hue=s=0,eq=contrast=1.12:brightness=-0.02,noise=alls=5:allf=t"
    # les rushes FX3 sont en plage PLEINE (yuv422p10le pc) : sans conversion le plan sortait
    # en yuvj420p, la concaténation en copie gardait ce drapeau pour toute la base et les
    # cartons noirs (plage limitée) sortaient gris foncé, 17/255 au lieu de 0 (vérification
    # du 13/10/2026 sur 7351 suivi d'un CARTON NOIR). Tous les morceaux sortent en plage limitée.
    filtre += ",scale=out_range=tv,format=yuv420p"
    # nombre d'images imposé : en ralenti ×2 d'un rush 100p, la conversion à 25 i/s ajoutait
    # une image de trop par plan (1,56 s au lieu de 1,52), et les coupes dérivaient sous les
    # sous-titres (constaté le 13/10/2026 sur D1-R8, 0,24 s de décalage en fin de reel)
    ffmpeg(*entree, "-ss", str(debut), "-t", str(duree), "-i", rush, "-vf", filtre,
           "-r", str(FPS), "-frames:v", str(max(1, int(round(duree * ralenti * FPS)))),
           "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-color_range", "tv", sortie)


COULEURS_CARTON = {"noir": "black"}


def carton_du_plan(p):
    """Couleur du carton (« noir ») si le plan n'a pas de rush : clé `carton`, ou
    `clip` écrit « CARTON NOIR » comme dans les scripts du chantier ; sinon None."""
    if p.get("carton"):
        couleur = str(p["carton"]).strip().lower()
    else:
        clip = str(p.get("clip", "")).strip().lower()
        if not clip.startswith("carton"):
            return None
        couleur = clip[len("carton"):].strip() or "noir"
    if couleur not in COULEURS_CARTON:
        raise SystemExit(f"carton inconnu : {couleur} (au choix : {', '.join(COULEURS_CARTON)})")
    return couleur


def duree_ecran(p, spec):
    """Durée d'un plan dans la vidéo finie : rush × ralenti ; carton × ralenti du plan, 1 par défaut."""
    if carton_du_plan(p):
        return p["duree"] * p.get("ralenti", 1)
    return p["duree"] * p.get("ralenti", spec.get("ralenti", 4))


def plan_carton(couleur, duree, sortie, nb, grade=None):
    """Fond uni 1080×1920 à 25 i/s, étalonné comme les plans (grain du N&B compris)."""
    filtre = "setsar=1"
    if grade:
        filtre += "," + grade
    elif nb:
        filtre += ",hue=s=0,eq=contrast=1.12:brightness=-0.02,noise=alls=5:allf=t"
    filtre += ",format=yuv420p"
    ffmpeg("-f", "lavfi", "-i", f"color=c={COULEURS_CARTON[couleur]}:s={W}x{H}:r={FPS}",
           "-vf", filtre, "-r", str(FPS), "-frames:v", str(max(1, int(round(duree * FPS)))),
           "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-color_range", "tv", sortie)


def _base_plans(spec, sources, lut, nb, grade=None):
    """Les plans recadrés, ralentis, étalonnés, mis bout à bout dans _base.mp4."""
    ralenti = spec.get("ralenti", 4)
    morceaux = []
    for i, p in enumerate(spec["plans"]):
        m = f"_plan{i}.mp4"
        couleur = carton_du_plan(p)
        if couleur:
            plan_carton(couleur, duree_ecran(p, spec), m, nb, grade)
            morceaux.append(m)
            continue
        rush, entree = sources(p["clip"])
        expo = p.get("exposition", spec.get("exposition"))
        try:
            plan(rush, p["debut"], p["duree"], p.get("x", 0.5), p.get("ralenti", ralenti),
                 lut_exposee(lut, expo) if grade else lut, nb, m, p.get("slog3", True),
                 entree=entree, grade=grade,
                 flou_bouge=p.get("flou_bouge", spec.get("flou_bouge", 0)) if grade else 0)
        except subprocess.CalledProcessError:
            relais = getattr(sources, "relais", None)
            if relais is not None and relais.erreur:
                raise SystemExit(f"plan {i} (clip {p['clip']}) illisible à distance : {relais.erreur}")
            raise
        morceaux.append(m)
    with open("_liste.txt", "w") as f:
        f.writelines(f"file '{m}'\n" for m in morceaux)
    ffmpeg("-f", "concat", "-safe", "0", "-i", "_liste.txt", "-c", "copy", "_base.mp4")
    return sum(duree_ecran(p, spec) for p in spec["plans"])


def fonds_par_bloc(base, blocs):
    """Pour chaque bloc, le maximum pixel à pixel de la bande des sous-titres sur
    TOUTES les images où il est affiché : le pire fond qu'il aura sous lui."""
    import numpy as np
    hb = BANDE[1] - BANDE[0]
    taille = W * hb * 3
    proc = subprocess.Popen([binaire_ffmpeg(), "-v", "error", "-i", base, "-vf",
                             f"crop={W}:{hb}:0:{BANDE[0]}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                            stdout=subprocess.PIPE)
    maxi, n = [None] * len(blocs), 0
    while True:
        buf = proc.stdout.read(taille)
        if len(buf) < taille:
            break
        t = n / FPS
        img = None
        for i, b in enumerate(blocs):
            if b.t <= t < b.fin:
                if img is None:
                    img = np.frombuffer(buf, np.uint8).reshape(hb, W, 3)
                maxi[i] = img.copy() if maxi[i] is None else np.maximum(maxi[i], img)
        n += 1
    proc.stdout.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg n'a pas pu relire la base pour mesurer le contraste")
    return maxi


def incruster(base, blocs, total, sortie):
    """Compose la bande des sous-titres image par image et l'incruste, sortie muette."""
    hb = BANDE[1] - BANDE[0]
    cmd = [binaire_ffmpeg(), "-v", "error", "-y", "-i", base,
           "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{hb}", "-framerate", str(FPS), "-i", "-",
           "-filter_complex", f"[0:v][1:v]overlay=0:{BANDE[0]}:format=yuv444,format=yuv420p[v]",
           "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-t", f"{total:.2f}", "-movflags", "+faststart", sortie]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    precedent, image = None, None
    try:
        for n in range(int(round(total * FPS))):
            t = n / FPS
            cle = etat(blocs, t)
            if cle != precedent:
                precedent, image = cle, composer(blocs, t).tobytes()
            proc.stdin.write(image)
    except BrokenPipeError:
        pass
    finally:
        try:
            proc.stdin.close()
        except BrokenPipeError:
            pass
    if proc.wait() != 0:
        raise SystemExit("ffmpeg a échoué à l'incrustation des sous-titres")


def monter_monologue(spec, sources, polices, lut):
    # contrôle des textes AVANT de lire le moindre rush : une faute coûte zéro seconde
    preparer_sous_titres(spec, polices)
    grade = filtre_nb_monologue(spec.get("courbe", COURBE_NB), spec.get("contraste"),
                                spec.get("luminosite"), spec.get("gamma"), spec.get("grain", 6))
    total = _base_plans(spec, sources, lut, True, grade)
    blocs = preparer_sous_titres(spec, polices, total)
    for b, fond in zip(blocs, fonds_par_bloc("_base.mp4", blocs)):
        if fond is not None:
            regler_voile(b, fond)
    incruster("_base.mp4", blocs, total, spec["sortie"])
    for k, b in enumerate(blocs, 1):
        if b.contraste is None:
            continue
        ok = b.contraste >= b.cible
        print(f"  bloc {k} « {' / '.join(b.lignes)} » : contraste {b.contraste:.1f} au pire pixel, "
              f"voile {b.voile:.2f}" + ("" if ok else
              f"  ATTENTION sous la cible {b.cible} malgré le voile maximal : décaler le plan, "
              "baisser l'exposition ou changer le `x`"))
    return total


def monter(spec, rushes, polices, lut, index=None, relais=True):
    """`rushes` : dossier local ; `index` : {nom: id Drive} ; `relais` : lecture des
    URL par le relais à plages bornées (False = URL directe avec -http_proxy)."""
    sources = Sources(rushes, index, relais)
    try:
        # « texte_mode": "centre_mot_a_mot » : nom provisoire du gabarit dans les specs
        # écrites avant lui (chantier du 13/10/2026)
        if spec.get("gabarit", "reel") == "monologue" or spec.get("texte_mode") == "centre_mot_a_mot":
            return monter_monologue(spec, sources, polices, lut)
        return _monter_reel_story(spec, sources, polices, lut)
    finally:
        sources.fermer()


def _monter_reel_story(spec, sources, polices, lut):
    gabarit = spec.get("gabarit", "reel")
    if gabarit not in ("reel", "story"):
        raise SystemExit(f"gabarit inconnu : {gabarit} (reel, story ou monologue)")
    nb = gabarit == "reel"
    ralenti = spec.get("ralenti", 4)
    if nb:
        for t in spec.get("textes", []):
            verifier_tirets(t["texte"], "un texte du reel")
    total = _base_plans(spec, sources, lut, nb)

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
    ap.add_argument("--drive-index", default=None,
                    help="JSON des MP4 du dossier Drive (nom → id) : rushes lus par plages HTTP")
    ap.add_argument("--sans-relais", action="store_true",
                    help="URL passée telle quelle à ffmpeg avec -http_proxy (plages ouvertes : "
                         "Drive peut répondre « Quota exceeded »)")
    args = ap.parse_args()
    if not args.spec:
        ecrire_lut(args.lut)
        print(args.lut)
        return
    if not os.path.exists(args.lut):
        ecrire_lut(args.lut)
    spec = json.load(open(args.spec, encoding="utf-8"))
    index = charger_index_drive(args.drive_index) if args.drive_index else None
    total = monter(spec, args.rushes, args.polices, args.lut, index, relais=not args.sans_relais)
    print(f"{spec['sortie']} {total:.1f} s, " + ("voix seule" if spec.get("voix") else "muet"))


if __name__ == "__main__":
    sys.exit(main())

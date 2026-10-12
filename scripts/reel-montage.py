#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reel vertical (1080×1920) monté depuis les rushs d'un tournage, avec choix
de la meilleure prise, son stéréo garanti et étalonnage sur tout le montage.

Grand frère de `aftermovie.py` (dont il réutilise le sondage des rushs et les
cartons), mais pensé pour un **reel client** de 1 min 30 : plusieurs prises
d'une même scène ont été tournées, il faut n'en garder qu'une, le son a
parfois été enregistré en mono, et l'image doit être homogène d'un plan à
l'autre.

## Ce que fait le script

1. **Dérushage par scène.** Les rushs sont triés par date de tournage. Deux
   rushs consécutifs qui se ressemblent (même cadre : trois images de l'un
   comparées à trois images de l'autre, même répartition de luminosité,
   durées comparables, tournés à moins de 20 min d'écart) sont considérés
   comme deux prises de la même scène. Si les fichiers sont nommés `scene-03-prise-2.mov`, `sc03_t2.mp4`,
   etc., c'est le nom qui fait foi.
2. **Choix de la prise.** Chaque prise est notée : netteté de l'image,
   exposition, longueur (la prise complète est en général la plus longue),
   niveau et propreté du son (pas de saturation), et un léger bonus pour la
   dernière prise (celle qu'on garde généralement sur le plateau). La
   meilleure part au montage ; les autres sont listées dans le rapport.
3. **Grille de montage.** Accroche de 2,5 s, plans de 3 s qui se
   resserrent jusqu'à 1,6 s, plan final posé de 3 s, carton de fin en option,
   pour tomber exactement sur la durée demandée (90 s). Les scènes défilent
   dans l'ordre du tournage. Quand il y a plus de plans que de scènes, les
   scènes les plus longues fournissent plusieurs plans, à des moments
   différents de la prise retenue.
4. **Son stéréo, toujours.** Chaque rush est analysé canal par canal :
   - pas de piste → silence stéréo ;
   - piste mono → dupliquée gauche/droite ;
   - piste stéréo avec un canal mort (micro-cravate branché d'un seul côté :
     un canal à −60 dB ou 12 dB sous l'autre) → le bon canal est copié sur
     les deux ;
   - vraie stéréo → conservée.
   Les niveaux sont ensuite rapprochés plan par plan (±12 dB max), puis le
   mix final est normalisé à −14 LUFS. Le fichier de sortie est vérifié :
   deux canaux, tous les deux avec du signal.
5. **Étalonnage.** En deux temps : (a) chaque plan est ramené vers une
   exposition et un contraste communs (correction plafonnée pour ne pas
   dénaturer) ; un plan **surexposé** (tons moyens trop hauts, 90e centile
   au blanc ou pixels brûlés) passe par une voie dédiée, bien plus ferme :
   courbe maître qui écrase les hautes lumières, redescend les tons moyens
   et ramène le blanc pur à 95 % ; (b) un « look » unique est appliqué sur tout le montage
   assemblé : `ramen` par défaut (chaud, contrasté, saturé, léger vignettage,
   pour la cuisine et la vapeur), `neutre`, `froid`, ou ton propre `--lut
   fichier.cube`.

⚠️ Aucune image n'est générée : ce sont les rushs du client et rien d'autre.
Ce n'est pas une story, le reel garde son son.

## Usage

    # V1 complète depuis le disque vert
    python3 scripts/reel-montage.py "/Volumes/VERT/Nina Ramen" \\
        --titre "NINA RAMEN" --duree 90 --sortie o/nina-ramen-reel-v1.mp4

    # changer une prise ou un plan dans o/nina-ramen-reel-v1.montage.json, puis
    python3 scripts/reel-montage.py --edl o/nina-ramen-reel-v1.montage.json

    # reprendre l'étalonnage d'une V1 déjà montée (plans surexposés compris)
    python3 scripts/reel-montage.py --edl o/nina-ramen-reel-v1.montage.json --reetalonner

    # projet DaVinci Resolve déjà ouvert : juste la timeline, sans rendu mp4
    python3 scripts/reel-montage.py "/Volumes/VERT/Nina Ramen" --titre "NINA RAMEN" \
        --sortie o/nina-ramen-reel-v1.mp4 --sans-rendu
    # puis Fichier > Importer > Timeline > o/nina-ramen-reel-v1.fcpxml
    # (ou : python3 projets/nina-ramen/davinci-import.py o/nina-ramen-reel-v1.fcpxml)

    # V2 après retours client : blancs coupés entre les phrases, carton d'appel
    # à l'action aux couleurs de la charte (puis sous-titres dans Submagic)
    python3 scripts/reel-montage.py "/Volumes/VERT/Nina Ramen" --titre "NINA RAMEN" \
        --couper-blancs --carton-fin "Réservez votre table\nninaramen.fr" \
        --cta-fond "#F3E9D2" --cta-texte "#1F1F1F" --cta-police charte/Police.otf \
        --cta-logo charte/logo.png --sortie o/nina-ramen-reel-v2.mp4

Chaque lancement écrit aussi `<sortie>.fcpxml`, la même timeline pour DaVinci
Resolve : prises, points d'entrée, durées, fondus, titre en V2, carton de fin,
gain par plan, et un marqueur sur chaque plan mono ou surexposé.

ffmpeg et ffprobe doivent être dans le PATH (sur le Mac : `~/.local/node/bin`)
ou donnés par `--ffmpeg`. Dépendances Python : pillow, numpy.
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aftermovie as am  # noqa: E402  (sondage des rushs, cartons, binaires)

W, H = 1080, 1920
FPS = 30
TRANSITION = 0.2              # fondu très court : un reel se coupe sec
MARGE_RUSH = 0.06             # part ignorée au début et à la fin d'une prise
DUREE_ACCROCHE = 2.5
DUREE_FINALE = 3.0
DUREE_CARTON = 2.5
PLAN_MAX, PLAN_MIN = 3.0, 1.6

# --- prises
SEUIL_EMPREINTE = 14.0        # écart moyen (0-255) sous lequel deux images se ressemblent
SEUIL_HISTO = 0.7             # distance L1 entre histogrammes de luminosité 8 classes (0-2)
RATIO_DUREE = (0.4, 2.5)      # deux prises d'une scène ont des durées comparables
ECART_TOURNAGE_MAX = 20 * 60  # au-delà (s) entre deux rushs, c'est une autre scène
BONUS_DERNIERE_PRISE = 0.15

# --- son
CANAL_MORT_DB = -60.0         # sous ce RMS, un canal est considéré vide
ECART_CANAUX_DB = 12.0        # au-delà de cet écart, on ne garde que le bon canal
RMS_CIBLE_DB = -20.0          # niveau visé plan par plan avant le mix
GAIN_MAX_DB = 12.0

# --- blancs entre les phrases (--couper-blancs)
SILENCE_DB = -35.0            # sous ce niveau, c'est un blanc
SILENCE_MIN = 0.4             # un blanc plus court est une respiration, on le garde
SILENCE_GARDE = 0.12          # ce qu'on laisse de chaque côté d'une coupe (s)
SEGMENT_MIN = 0.35            # un bout de parole plus court n'est pas gardé seul

# --- image
LUMA_CIBLE = 118.0            # luminosité moyenne visée (0-255)
SPREAD_CIBLE = 140.0          # écart 10 % / 90 % visé
CORR_PART = 0.5               # on ne corrige que la moitié de l'écart mesuré
CORR_LUMA_MAX = 0.08          # brightness eq, borné
CORR_CONTRASTE = (0.9, 1.15)
# --- plans surexposés : voie dédiée, bien plus ferme que la correction douce
# Les mesures signalstats (YAVG, YLOW, YHIGH) sont en plage limitée : le blanc
# vidéo est à 235, pas 255. Les seuils ci-dessous sont dans cette échelle.
SUREXPO_YAVG = 160.0          # tons moyens au-dessus desquels le plan est surexposé…
SUREXPO_YAVG_HAUTES = 222.0   # …si en plus le 90e centile approche le blanc
SUREXPO_YHIGH = 232.0         # 90e centile qui touche le blanc (235) : surexposé
SUREXPO_CLIP = 0.03           # part de pixels brûlés (>= 233) qui suffit à déclencher
SUREXPO_TIRAGE_MAX = 0.28     # descente maximale des tons moyens (échelle 0-1)
SUREXPO_HAUTES = 0.82         # où retombe le 90e centile (échelle 0-1)
BLANC_MAX = 0.95              # le blanc pur est ramené à 95 % : le cramé redevient une haute lumière

LOOKS = {
    # chaud, contrasté, saturé : bouillon, vapeur, bois, néons
    "ramen": ("colortemperature=temperature=5600:mix=0.4,"
              "eq=contrast=1.07:saturation=1.18:gamma=1.02,"
              "curves=master='0/0.02 0.25/0.22 0.5/0.52 0.75/0.79 1/0.985',"
              "colorbalance=rs=0.03:bs=-0.04:rh=0.02:bh=-0.02,"
              "unsharp=5:5:0.6:5:5:0,vignette=angle=PI/5"),
    # juste de la tenue : un peu de contraste et de saturation
    "neutre": ("eq=contrast=1.05:saturation=1.08,"
               "curves=master='0/0.01 0.5/0.5 1/0.99',unsharp=5:5:0.5:5:5:0"),
    # froid, désaturé, propre (déco, archi)
    "froid": ("colortemperature=temperature=7400:mix=0.4,"
              "eq=contrast=1.06:saturation=0.92,"
              "curves=master='0/0.03 0.5/0.5 1/0.98',unsharp=5:5:0.5:5:5:0"),
    "aucun": "",
}

log, run = am.log, am.run


# --------------------------------------------------------------- outils ---

def echapper(chemin):
    """Échappe un chemin pour l'option file= d'un filtre ffmpeg."""
    return chemin.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def db(x):
    return -120.0 if x <= 0 else 20 * math.log10(x)


def image_gris(ffmpeg, fichier, t, largeur, hauteur):
    """Une image en niveaux de gris (tableau float) prise à l'instant t."""
    r = subprocess.run(
        [ffmpeg, "-hide_banner", "-ss", "%.3f" % t, "-i", fichier,
         "-frames:v", "1", "-vf", "scale=%d:%d" % (largeur, hauteur),
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    n = largeur * hauteur
    if len(r.stdout) < n:
        return None
    return np.frombuffer(r.stdout[:n], np.uint8).astype(float).reshape(hauteur, largeur)


def stats_image(ffmpeg, fichier, t):
    """YAVG, YLOW, YHIGH (signalstats, plage limitée) sur 3 images autour de
    t, et CLIP, la part de pixels brûlés (luma >= 233) sur une image réduite."""
    r = subprocess.run(
        [ffmpeg, "-hide_banner", "-ss", "%.3f" % max(0, t - 0.2), "-i", fichier,
         "-frames:v", "3", "-vf", "scale=240:-2,signalstats,metadata=print",
         "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    vals = {}
    for cle in ("YAVG", "YLOW", "YHIGH"):
        m = re.findall(r"lavfi\.signalstats\.%s=(\d+\.?\d*)" % cle, r.stderr)
        vals[cle] = sum(map(float, m)) / len(m) if m else None
    if vals["YAVG"] is None:
        return dict(YAVG=128.0, YLOW=40.0, YHIGH=215.0, CLIP=0.0)
    y = plan_luma(ffmpeg, fichier, t, 160, 90)
    vals["CLIP"] = float((y >= 233).mean()) if y is not None else 0.0
    return vals


def plan_luma(ffmpeg, fichier, t, largeur, hauteur):
    """Le plan Y brut (plage limitée, 16-235) d'une image prise à l'instant t,
    à la même échelle que signalstats, contrairement à image_gris qui sort
    du gris en plage pleine."""
    r = subprocess.run(
        [ffmpeg, "-hide_banner", "-ss", "%.3f" % t, "-i", fichier,
         "-frames:v", "1", "-vf", "scale=%d:%d" % (largeur, hauteur),
         "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    n = largeur * hauteur
    if len(r.stdout) < n:
        return None
    return np.frombuffer(r.stdout[:n], np.uint8).astype(float).reshape(hauteur, largeur)


def nettete(im):
    """Variance du laplacien : plus c'est haut, plus l'image est nette."""
    if im is None:
        return 0.0
    lap = (-4 * im[1:-1, 1:-1] + im[:-2, 1:-1] + im[2:, 1:-1]
           + im[1:-1, :-2] + im[1:-1, 2:])
    return float(lap.var())


# ----------------------------------------------------------------- son ---

def analyser_audio(ffmpeg, rush):
    """RMS et crête par canal, mesurés sur jusqu'à 60 s au cœur du rush."""
    if not rush["audio"]:
        return dict(canaux=0, rms=[], crete=[])
    debut = rush["duree"] * 0.1
    duree = min(60.0, rush["duree"] * 0.8)
    r = subprocess.run(
        [ffmpeg, "-hide_banner", "-ss", "%.3f" % debut, "-t", "%.3f" % duree,
         "-i", rush["fichier"], "-vn",
         "-af", "astats=measure_perchannel=RMS_level+Peak_level:measure_overall=none",
         "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    rms, crete = [], []
    for bloc in re.split(r"Channel: \d+", r.stderr)[1:]:
        m1 = re.search(r"RMS level dB: (-?[\d.]+|-inf)", bloc)
        m2 = re.search(r"Peak level dB: (-?[\d.]+|-inf)", bloc)
        rms.append(float(m1[1]) if m1 and m1[1] != "-inf" else -120.0)
        crete.append(float(m2[1]) if m2 and m2[1] != "-inf" else -120.0)
    return dict(canaux=len(rms), rms=rms, crete=crete)


def decision_stereo(son):
    """(diagnostic, filtre pan) pour sortir une vraie stéréo."""
    if son["canaux"] == 0:
        return "aucune piste → silence stéréo", None
    if son["canaux"] == 1:
        return "mono → dupliqué gauche/droite", "pan=stereo|c0=c0|c1=c0"
    rms = son["rms"]
    meilleur = int(np.argmax(rms))
    autres = [v for i, v in enumerate(rms) if i != meilleur]
    if rms[meilleur] <= CANAL_MORT_DB:
        return "piste muette → silence stéréo", "pan=stereo|c0=c0|c1=c0"
    if max(autres) <= CANAL_MORT_DB or rms[meilleur] - max(autres) > ECART_CANAUX_DB:
        cote = "gauche" if meilleur == 0 else ("droit" if meilleur == 1 else "canal %d" % (meilleur + 1))
        return ("mono sur le canal %s → copié sur les deux" % cote,
                "pan=stereo|c0=c%d|c1=c%d" % (meilleur, meilleur))
    if son["canaux"] > 2:
        return "%d canaux → mixés en stéréo" % son["canaux"], None
    return "stéréo → conservée", None


def gain_plan(son):
    """Gain (dB) pour rapprocher le plan de RMS_CIBLE_DB, borné à ±GAIN_MAX_DB."""
    if son["canaux"] == 0:
        return 0.0
    niveau = max(son["rms"])
    if niveau <= CANAL_MORT_DB:
        return 0.0
    g = RMS_CIBLE_DB - niveau
    # jamais au-delà de la crête : on ne sature pas
    marge = -1.0 - max(son["crete"])
    return round(max(-GAIN_MAX_DB, min(GAIN_MAX_DB, g, marge)), 1)


# ---------------------------------------------------------------- prises ---

RE_SCENE = re.compile(r"(?:sc[eè]ne?|sc|plan|shot)[ _-]?(\d+)", re.I)
RE_PRISE = re.compile(r"(?:prise|take|tk|t)[ _-]?(\d+)", re.I)


def scene_par_nom(fichier):
    nom = os.path.splitext(os.path.basename(fichier))[0]
    m = RE_SCENE.search(nom)
    if not m:
        return None
    p = RE_PRISE.search(nom[m.end():])
    return int(m[1]), (int(p[1]) if p else None)


def empreintes(ffmpeg, rush):
    """Trois images (25 %, 50 %, 75 %) : forme 48×27 centrée + histogramme."""
    out = []
    for frac in (0.25, 0.5, 0.75):
        im = image_gris(ffmpeg, rush["fichier"], rush["duree"] * frac, 48, 27)
        if im is None:
            continue
        histo, _ = np.histogram(im, bins=8, range=(0, 256))
        out.append((im - im.mean(), histo / histo.sum()))
    return out


def date_secondes(rush):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})", rush.get("date") or "")
    if not m:
        return None
    a, mo, j, h, mi, sec = map(int, m.groups())
    return ((a * 366 + mo * 31 + j) * 24 + h) * 3600 + mi * 60 + sec


def meme_scene(ref, r):
    """Deux rushs consécutifs sont-ils deux prises de la même scène ?"""
    ratio = r["duree"] / max(ref["duree"], 0.1)
    if not (RATIO_DUREE[0] <= ratio <= RATIO_DUREE[1]):
        return False
    t1, t2 = date_secondes(ref), date_secondes(r)
    if t1 is not None and t2 is not None and abs(t2 - t1) > ECART_TOURNAGE_MAX:
        return False
    if not ref["_empreintes"] or not r["_empreintes"]:
        return False
    # la plus petite distance entre une image de l'un et une image de l'autre
    forme = min(np.abs(a[0] - b[0]).mean() for a in ref["_empreintes"] for b in r["_empreintes"])
    histo = min(np.abs(a[1] - b[1]).sum() for a in ref["_empreintes"] for b in r["_empreintes"])
    r["_distance"] = (round(forme, 1), round(histo, 2))
    return forme < SEUIL_EMPREINTE and histo < SEUIL_HISTO


def grouper_scenes(ffmpeg, rushs):
    """Liste de scènes ; chaque scène est une liste de prises (rushs)."""
    if all(scene_par_nom(r["fichier"]) for r in rushs):
        groupes = {}
        for r in rushs:
            s, p = scene_par_nom(r["fichier"])
            r["prise_nom"] = p
            groupes.setdefault(s, []).append(r)
        scenes = [sorted(groupes[s], key=lambda r: (r.get("prise_nom") or 0, r["date"], r["fichier"]))
                  for s in sorted(groupes)]
        log("• scènes lues dans les noms de fichiers : %d" % len(scenes))
        return scenes, "noms de fichiers"

    # sinon : ressemblance visuelle entre rushs consécutifs
    for r in rushs:
        r["_empreintes"] = empreintes(ffmpeg, r)
    scenes = []
    for r in rushs:
        if scenes and meme_scene(scenes[-1][0], r):
            scenes[-1].append(r)
            continue
        scenes.append([r])
    log("• scènes détectées par ressemblance : %d (sur %d rushs)" % (len(scenes), len(rushs)))
    return scenes, "ressemblance visuelle"


def noter_prises(ffmpeg, scene):
    """Ajoute à chaque prise ses mesures et sa note ; renvoie l'index retenu."""
    for r in scene:
        t = r["duree"] / 2
        im = image_gris(ffmpeg, r["fichier"], t, 320, 180)
        r["nettete"] = nettete(im)
        r["stats"] = stats_image(ffmpeg, r["fichier"], t)
        r["son"] = analyser_audio(ffmpeg, r)
    max_net = max(r["nettete"] for r in scene) or 1.0
    max_dur = max(r["duree"] for r in scene) or 1.0
    for i, r in enumerate(scene):
        s_net = r["nettete"] / max_net
        y = r["stats"]["YAVG"]
        s_expo = 1.0 - min(1.0, abs(y - 120) / 120)
        s_dur = r["duree"] / max_dur
        son = r["son"]
        if son["canaux"] == 0:
            s_son = 0.3
        else:
            niveau = max(son["rms"])
            s_son = 1.0 if -35 <= niveau <= -8 else (0.5 if niveau > CANAL_MORT_DB else 0.1)
            if max(son["crete"]) > -0.5:
                s_son *= 0.6          # ça sature
        s_fin = BONUS_DERNIERE_PRISE if i == len(scene) - 1 and len(scene) > 1 else 0.0
        r["note"] = round(0.35 * s_net + 0.2 * s_expo + 0.2 * s_dur + 0.25 * s_son + s_fin, 3)
        r["detail_note"] = dict(nettete=round(s_net, 2), exposition=round(s_expo, 2),
                                duree=round(s_dur, 2), son=round(s_son, 2),
                                derniere=s_fin)
    return max(range(len(scene)), key=lambda i: scene[i]["note"])


# ---------------------------------------------------------------- grille ---

def grille_durees(total, avec_carton):
    """Accroche, plans qui se resserrent, plan final, carton : somme = total."""
    fixes = [DUREE_ACCROCHE, DUREE_FINALE] + ([DUREE_CARTON] if avec_carton else [])
    budget = total - sum(fixes) + (len(fixes) - 1) * TRANSITION
    if budget < PLAN_MIN:
        sys.exit("✗ durée trop courte pour un reel (%.0f s)" % total)
    milieu, cumul = [], 0.0
    while True:
        d = PLAN_MAX - (PLAN_MAX - PLAN_MIN) * (cumul / budget) ** 0.9
        if cumul + d - TRANSITION > budget:
            break
        milieu.append(round(d, 2))
        cumul += d - TRANSITION
    durees = [DUREE_ACCROCHE] + milieu + [DUREE_FINALE]
    if avec_carton:
        durees.append(DUREE_CARTON)
    i_final = -2 if avec_carton else -1
    somme = sum(durees) - (len(durees) - 1) * TRANSITION
    durees[i_final] = round(durees[i_final] + total - somme, 3)
    return durees


def repartir_plans(scenes, retenues, durees, accroche=None):
    """Associe à chaque durée de plan une prise et un point d'entrée."""
    n = len(durees)
    ordre = list(range(len(scenes)))
    if accroche is not None and 1 <= accroche <= len(scenes):
        ordre.remove(accroche - 1)
        ordre.insert(0, accroche - 1)
    prises = [scenes[i][retenues[i]] for i in ordre]
    # combien de plans par scène : au moins 1 chacune si possible, le surplus
    # aux prises les plus longues ; sinon on sous-échantillonne les scènes
    if len(prises) >= n:
        if len(prises) == n:
            choix = list(range(len(prises)))
        else:
            choix = sorted({round(k * (len(prises) - 1) / (n - 1)) for k in range(n)})
            while len(choix) < n:   # arrondis qui se chevauchent
                manquant = next(i for i in range(len(prises)) if i not in choix)
                choix.append(manquant)
                choix.sort()
        quotas = {i: (1 if i in choix else 0) for i in range(len(prises))}
    else:
        quotas = {i: 1 for i in range(len(prises))}
        reste = n - len(prises)
        for _ in range(reste):
            # la prise avec le plus de matière par plan déjà pris
            i = max(range(len(prises)),
                    key=lambda j: prises[j]["duree"] / (quotas[j] + 1))
            quotas[i] += 1
    plans, k = [], 0
    for i, p in enumerate(prises):
        q = quotas[i]
        if q == 0:
            continue
        marge = p["duree"] * MARGE_RUSH
        deb, fin = marge, p["duree"] - marge
        for j in range(q):
            duree = durees[k]
            k += 1
            if q == 1:
                debut = deb + max(0.0, (fin - deb - duree) / 2)
            else:
                # moments répartis dans la prise, du début vers la fin
                frac = (j + 0.5) / q
                debut = deb + (fin - deb) * frac - duree / 2
            debut = max(deb, min(debut, max(deb, fin - duree)))
            plans.append(dict(fichier=p["fichier"], debut=round(debut, 3),
                              duree=duree, scene=ordre[i] + 1))
    return plans


# ------------------------------------------------------- blancs coupés ---

def detecter_silences(ffmpeg, fichier, duree):
    """[(debut, fin)] des blancs d'une prise, mesurés par silencedetect."""
    r = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", fichier, "-vn",
         "-af", "silencedetect=noise=%ddB:d=%.2f" % (SILENCE_DB, SILENCE_MIN),
         "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    silences, debut = [], None
    for m in re.finditer(r"silence_(start|end): (-?[\d.]+)", r.stderr):
        if m[1] == "start":
            debut = max(0.0, float(m[2]))
        elif debut is not None:
            silences.append((debut, min(duree, float(m[2]))))
            debut = None
    if debut is not None:
        silences.append((debut, duree))
    return silences


def plages_parole(silences, duree, garde=SILENCE_GARDE, minimum=SEGMENT_MIN):
    """Ce qu'on garde d'une prise : tout sauf les blancs, en laissant `garde`
    secondes de respiration après chaque phrase et avant la suivante."""
    plages, cur = [], 0.0
    for s0, s1 in sorted(silences):
        fin = min(duree, s0 + garde)
        if fin - cur >= minimum:
            plages.append((round(cur, 3), round(fin, 3)))
        cur = max(cur, s1 - garde)
    if duree - cur >= minimum:
        plages.append((round(cur, 3), round(duree, 3)))
    return plages


def appliquer_coupes(plan, plages):
    """Remplace la fenêtre [debut, debut+duree] d'un plan par les bouts de
    parole qui se suivent à partir de debut, jusqu'à remplir la même durée :
    le plan garde sa place dans la grille, mais il contient plus de phrases
    et plus de blancs. Retourne (segments [(debut, duree)], blanc sauté en s),
    ou None si la prise n'a pas assez de parole après debut."""
    reste, t, segs, saute, fin_prec = plan["duree"], plan["debut"], [], 0.0, None
    for p0, p1 in plages:
        if p1 <= t:
            continue
        d0 = max(p0, t)
        d = min(p1 - d0, reste)
        if d < SEGMENT_MIN and d < reste - 1e-6:
            continue                      # miette de phrase, on passe
        if fin_prec is not None:
            saute += d0 - fin_prec
        segs.append((round(d0, 3), round(d, 3)))
        reste -= d
        fin_prec = d0 + d
        if reste <= 1e-6:
            break
    if reste > 0.05 or len(segs) < 2:
        return None
    return segs, round(saute, 3)


# ------------------------------------------------------------ étalonnage ---

def surexpose(stats):
    """Un plan est surexposé si les tons moyens sont trop hauts, si le 90e
    centile touche le blanc, ou si une part visible de l'image est brûlée."""
    yhigh = stats.get("YHIGH") or 0
    # une scène claire mais tenue (hautes lumières sous 222) n'est pas surexposée
    return ((stats["YAVG"] > SUREXPO_YAVG and yhigh >= SUREXPO_YAVG_HAUTES)
            or yhigh >= SUREXPO_YHIGH
            or (stats.get("CLIP") or 0.0) > SUREXPO_CLIP)


def courbe_surexpo(stats):
    """Points (x/y, échelle 0-1) d'une courbe maître qui ramène un plan
    surexposé : les ombres bougent à peine, les tons moyens redescendent
    vers la cible (plein chemin, borné), le 90e centile retombe à
    SUREXPO_HAUTES et le blanc pur à BLANC_MAX. Les points sont gardés
    strictement croissants, ce qu'exige le filtre curves.

    curves travaille en plage pleine (0-1 = 0-255) alors que les mesures
    sont en plage limitée (16-235) : chaque valeur est convertie."""
    def pleine(v):
        return max(0.0, min(1.0, (v - 16.0) / 219.0))
    y = pleine(stats["YAVG"])
    ylow = pleine(stats.get("YLOW") or 40)
    yhigh = pleine(stats.get("YHIGH") or 215)
    cible = pleine(LUMA_CIBLE)
    ym = max(y - SUREXPO_TIRAGE_MAX, cible + (y - cible) * 0.3)
    candidats = [(ylow, ylow * 0.95), (y, ym), (yhigh, min(SUREXPO_HAUTES, yhigh))]
    points = [(0.0, 0.0)]
    for x, v in candidats:
        if x <= points[-1][0] + 0.02 or x >= 0.98:
            continue                      # trop proche du point précédent ou du blanc
        v = max(v, points[-1][1] + 0.02)  # jamais en dessous du point précédent
        points.append((round(x, 3), round(min(v, 0.93), 3)))
    # Blanc pur : un cran au-dessus du dernier point, sans dépasser BLANC_MAX.
    # Plan entièrement brûlé (aucun point intermédiaire retenu) : on descend
    # le blanc jusqu'aux tons moyens visés, jamais en dessous.
    fin = min(BLANC_MAX, max(points[-1][1] + 0.2, ym))
    points.append((1.0, round(max(fin, points[-1][1] + 0.02), 3)))
    return points


def correction_plan(stats):
    """Filtre vidéo qui rapproche le plan de l'exposition commune.

    Plan normal : eq doux, la moitié du chemin vers LUMA_CIBLE / SPREAD_CIBLE,
    dans des bornes serrées (on rapproche, on n'uniformise pas).
    Plan surexposé : courbe maître ferme (voir courbe_surexpo), qui écrase les
    hautes lumières et redescend les tons moyens, avant le look global."""
    y = stats["YAVG"]
    spread = max(1.0, (stats.get("YHIGH") or 215) - (stats.get("YLOW") or 40))
    if surexpose(stats):
        points = courbe_surexpo(stats)
        courbe = " ".join("%g/%g" % (x, v) for x, v in points)
        return "curves=master='%s',eq=saturation=1.04" % courbe, \
            dict(YAVG=round(y, 1), spread=round(spread, 1),
                 clip=round(stats.get("CLIP") or 0.0, 3), surexpose=True,
                 courbe=courbe)
    contraste = 1 + (SPREAD_CIBLE / spread - 1) * CORR_PART
    contraste = max(CORR_CONTRASTE[0], min(CORR_CONTRASTE[1], contraste))
    # eq applique le contraste autour de 128 puis la luminosité
    y_apres = 128 + (y - 128) * contraste
    lum = (LUMA_CIBLE - y_apres) / 255 * CORR_PART
    lum = max(-CORR_LUMA_MAX, min(CORR_LUMA_MAX, lum))
    return "eq=contrast=%.3f:brightness=%.3f" % (contraste, lum), \
        dict(YAVG=round(y, 1), spread=round(spread, 1), contraste=round(contraste, 3),
             brightness=round(lum, 3), surexpose=False)


# ----------------------------------------------------------------- rendu ---

def rendre_plan(ffmpeg, plan, sortie):
    """Un plan aux dimensions, cadence et son uniformes, corrigé, en stéréo."""
    video = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
             "setsar=1,fps=%d,%s,format=yuv420p"
             % (W, H, W, H, FPS, plan.get("correction", "null")))
    segs = plan.get("segments") or [(plan["debut"], plan["duree"])]
    premier, dernier = segs[0][0], max(d0 + d for d0, d in segs)
    cmd = [ffmpeg, "-hide_banner", "-y", "-ss", "%.3f" % premier,
           "-t", "%.3f" % (dernier - premier), "-i", plan["fichier"],
           "-f", "lavfi", "-t", "%.3f" % plan["duree"],
           "-i", "anullsrc=r=48000:cl=stereo"]
    avec_son = plan.get("audio", True) and plan.get("pan") != "silence"
    f = []
    if len(segs) > 1:
        # blancs coupés : chaque bout est découpé puis les bouts sont mis bout à bout
        for i, (d0, d) in enumerate(segs):
            a, b = d0 - premier, d0 - premier + d
            f.append("[0:v]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS[v%d]" % (a, b, i))
            if avec_son:
                f.append("[0:a]atrim=start=%.3f:end=%.3f,asetpts=PTS-STARTPTS[a%d]" % (a, b, i))
        f.append("".join("[v%d]" % i for i in range(len(segs)))
                 + "concat=n=%d:v=1:a=0[vc]" % len(segs))
        src_v = "[vc]"
        if avec_son:
            f.append("".join("[a%d]" % i for i in range(len(segs)))
                     + "concat=n=%d:v=0:a=1[ac]" % len(segs))
        src_a = "[ac]"
    else:
        src_v, src_a = "[0:v]", "[0:a]"
    if avec_son:
        etapes = ["aresample=48000"]
        if plan.get("pan"):
            etapes.append(plan["pan"])
        etapes.append("aformat=channel_layouts=stereo")
        if plan.get("gain_db"):
            etapes.append("volume=%.1fdB" % plan["gain_db"])
        audio = "%s%s[a]" % (src_a, ",".join(etapes))
    else:
        audio = "[1:a]anull[a]"
    f.append("%s%s[v]" % (src_v, video))
    f.append(audio)
    cmd += ["-filter_complex", ";".join(f),
            "-map", "[v]", "-map", "[a]", "-t", "%.3f" % plan["duree"],
            "-c:v", "libx264", "-preset", "fast", "-crf", "16",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", sortie]
    run(cmd)


def rendre_carton_clip(ffmpeg, png, sortie, duree):
    run([ffmpeg, "-hide_banner", "-y", "-loop", "1", "-t", "%.3f" % duree,
         "-i", png, "-f", "lavfi", "-t", "%.3f" % duree,
         "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", "scale=%d:%d,setsar=1,fps=%d,format=yuv420p" % (W, H, FPS),
         "-c:v", "libx264", "-preset", "fast", "-crf", "16",
         "-c:a", "pcm_s16le", "-shortest", sortie])


def assembler(ffmpeg, clips, durees, titre_png, duree_titre, look, musique, sortie):
    """Fondus courts, look global sur toute la timeline, titre, musique."""
    n = len(clips)
    cmd = [ffmpeg, "-hide_banner", "-y"]
    for c in clips:
        cmd += ["-i", c]
    i_titre = n
    cmd += ["-loop", "1", "-t", "%.3f" % duree_titre, "-i", titre_png]
    i_musique = None
    if musique:
        i_musique = n + 1
        cmd += ["-i", musique]
    total = sum(durees) - (n - 1) * TRANSITION
    f = []
    prev, decalage = "[0:v]", 0.0
    for k in range(1, n):
        decalage += durees[k - 1] - TRANSITION
        out = "[v%d]" % k if k < n - 1 else "[vx]"
        f.append("%s[%d:v]xfade=transition=fade:duration=%.3f:offset=%.3f%s"
                 % (prev, k, TRANSITION, decalage, out))
        prev = out
    if n == 1:
        f.append("[0:v]null[vx]")
    # --- l'étalonnage global, une seule fois, sur la timeline entière
    f.append("[vx]%s[vg]" % (look or "null"))
    f.append("[%d:v]format=rgba,fade=in:st=0.4:d=0.6:alpha=1,"
             "fade=out:st=%.3f:d=0.5:alpha=1[t]" % (i_titre, duree_titre - 0.8))
    f.append("[vg][t]overlay=0:0:eof_action=pass,"
             "fade=in:st=0:d=0.5,fade=out:st=%.3f:d=0.6,format=yuv420p[vout]"
             % (total - 0.6))
    prev = "[0:a]"
    for k in range(1, n):
        out = "[a%d]" % k if k < n - 1 else "[ax]"
        f.append("%s[%d:a]acrossfade=d=%.3f:c1=tri:c2=tri%s" % (prev, k, TRANSITION, out))
        prev = out
    if n == 1:
        f.append("[0:a]anull[ax]")
    if musique:
        f.append("[ax]volume=-14dB[amb]")
        f.append("[%d:a]atrim=0:%.3f,asetpts=PTS-STARTPTS,aresample=48000,"
                 "aformat=channel_layouts=stereo,afade=in:st=0:d=0.8,"
                 "afade=out:st=%.3f:d=2[mus]" % (i_musique, total, total - 2))
        f.append("[amb][mus]amix=inputs=2:duration=first:normalize=0,"
                 "loudnorm=I=-14:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[aout]")
    else:
        f.append("[ax]afade=out:st=%.3f:d=1,loudnorm=I=-14:TP=-1.5:LRA=11,"
                 "aformat=channel_layouts=stereo[aout]" % (total - 1))
    cmd += ["-filter_complex", ";".join(f), "-map", "[vout]", "-map", "[aout]",
            "-t", "%.3f" % total, "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
            "-movflags", "+faststart", sortie]
    run(cmd)
    return total


def verifier_sortie(ffmpeg, ffprobe, sortie):
    info = am.sonder(ffprobe, ffmpeg, sortie)
    son = analyser_audio(ffmpeg, dict(fichier=sortie, duree=info["duree"], audio=True))
    ok = son["canaux"] == 2 and all(v > CANAL_MORT_DB for v in son["rms"]) \
        and abs(son["rms"][0] - son["rms"][1]) < 6
    return info, son, ok


# ------------------------------------------------------------ carton CTA ---

def couleur(hexa, defaut):
    """'#F1E4C8' -> (241, 228, 200) ; None -> defaut."""
    if not hexa:
        return defaut
    h = hexa.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def carton_cta(chemin, texte, W, H, fond=None, encre=None, police_chemin=None, logo=None):
    """Carton de fin aux couleurs du client : fond et encre de la charte, sa
    police, son logo au-dessus du texte. Première ligne en grand (l'appel à
    l'action), les suivantes en petit (adresse, site, compte)."""
    from PIL import Image, ImageDraw, ImageFont
    fond, encre = couleur(fond, am.ENCRE), couleur(encre, am.BLANC)
    im = Image.new("RGB", (W, H), fond)
    d = ImageDraw.Draw(im)

    def fonte(taille):
        if police_chemin and os.path.exists(police_chemin):
            try:
                return ImageFont.truetype(police_chemin, taille)
            except OSError:
                pass
        return am.police(taille)

    lignes = [l for l in re.split(r"\\n|\n", texte) if l.strip()]
    blocs, largeur_max = [], int(W * 0.86)
    for i, l in enumerate(lignes):
        taille = int(H * (0.055 if i == 0 else 0.028))
        while True:                       # la ligne tient dans la largeur, quitte à rapetisser
            fo = fonte(taille)
            b = d.textbbox((0, 0), l, font=fo)
            if b[2] - b[0] <= largeur_max or taille <= int(H * 0.02):
                break
            taille = int(taille * 0.92)
        blocs.append((l, fo, b[2] - b[0], b[3] - b[1]))
    inter = int(H * 0.022)
    h_texte = sum(h for *_, h in blocs) + inter * (len(blocs) - 1)
    im_logo = None
    if logo and os.path.exists(logo):
        im_logo = Image.open(logo).convert("RGBA")
        larg = int(W * 0.42)
        im_logo = im_logo.resize((larg, max(1, int(im_logo.height * larg / im_logo.width))))
    h_logo = (im_logo.height + int(H * 0.05)) if im_logo else 0
    y = (H - h_texte - h_logo) // 2
    if im_logo:
        im.paste(im_logo, ((W - im_logo.width) // 2, y), im_logo)
        y += h_logo
    for l, fo, w, h in blocs:
        d.text(((W - w) // 2, y), l, font=fo, fill=encre)
        y += h + inter
    im.save(chemin)


# ------------------------------------------------------- timeline DaVinci ---

FONDU_UID = "FxPlug:4731E73A-8DAC-4113-9A30-AE85B1761265"   # Cross Dissolve


def frames(secondes):
    return int(round(secondes * FPS))


def temps(n):
    """Valeur de temps FCPXML, alignée sur la grille de la timeline (30 i/s)."""
    return "%d/%ds" % (n, FPS)


def url_fichier(chemin):
    return "file://" + urllib.request.pathname2url(os.path.abspath(chemin))


def notes_plan(pl):
    """Ce qu'il faut savoir sur ce plan une fois dans Resolve : ce que le rendu
    ffmpeg faisait tout seul et qu'une timeline ne transporte pas. Chaque note
    devient un marqueur sur le plan."""
    notes = []
    pan = pl.get("pan")
    if pan == "silence":
        notes.append("Son : aucune piste, poser une ambiance")
    elif pan:
        notes.append("Son : %s. Dupliquer le bon canal sur G et D." % (pl.get("diag_son") or "mono"))
    m = pl.get("mesure_image") or {}
    if m.get("surexpose"):
        notes.append("Image : surexposé (YAVG %s, %.0f %% brûlé). Courbe : descendre les "
                     "hautes lumières, garder les ombres." % (m.get("YAVG", "?"),
                                                              100 * (m.get("clip") or 0)))
    return notes


def ecrire_fcpxml(chemin, nom, plans, titre_png=None, carton_png=None, evenement="Reel"):
    """Timeline importable dans DaVinci Resolve (Fichier > Importer > Timeline),
    identique au rendu ffmpeg : mêmes prises, mêmes points d'entrée, mêmes
    durées, fondus de 0,2 s centrés sur chaque coupe, titre en V2 sur
    l'accroche, carton de fin. Les rushs sont référencés à leur emplacement
    d'origine (chemins absolus), rien n'est copié.

    Ce qu'une timeline ne transporte pas (mise en stéréo, étalonnage) est posé
    en marqueur sur chaque plan concerné, et le gain par plan en volume du clip.
    Retourne la durée de la timeline en images."""
    t2 = frames(TRANSITION) // 2                 # demi-fondu, de chaque côté de la coupe
    root = ET.Element("fcpxml", version="1.8")
    res = ET.SubElement(root, "resources")
    ET.SubElement(res, "format", id="r1", name="FFVideoFormatRateUndefined",
                  frameDuration="100/%ds" % (FPS * 100), width=str(W), height=str(H))
    ET.SubElement(res, "effect", id="r2", name="Cross Dissolve", uid=FONDU_UID)
    ids = {}

    def ressource(fichier, duree=None, image=False, audio=True):
        if fichier in ids:
            return ids[fichier]
        rid = "r%d" % (len(ids) + 3)
        attrs = dict(id=rid, name=os.path.basename(fichier), src=url_fichier(fichier),
                     start="0s", hasVideo="1")
        if image:
            attrs["duration"] = "0s"
        else:
            if audio:
                attrs["hasAudio"] = "1"
            if duree:
                attrs["duration"] = temps(frames(duree))
        ET.SubElement(res, "asset", **attrs)
        ids[fichier] = rid
        return rid

    lib = ET.SubElement(root, "library")
    ev = ET.SubElement(lib, "event", name=evenement)
    proj = ET.SubElement(ev, "project", name=nom)
    seq = ET.SubElement(proj, "sequence", format="r1", tcStart="0s", tcFormat="NDF",
                        audioLayout="stereo", audioRate="48k")
    spine = ET.SubElement(seq, "spine")

    items = [dict(pl, carton=False) for pl in plans]
    if carton_png:
        items.append(dict(fichier=carton_png, debut=0.0, duree=DUREE_CARTON, carton=True))
    total = 0
    for k, pl in enumerate(items):
        premier, dernier = k == 0, k == len(items) - 1
        # les plans se suivent bord à bord, chaque fondu mord t2 images de part
        # et d'autre de la coupe : on rend ces images au plan (poignées) pour
        # que la timeline dure exactement ce que dure le rendu
        duree = frames(pl["duree"]) - (0 if premier else t2) - (0 if dernier else t2)
        if pl["carton"]:
            rid = ressource(pl["fichier"], image=True)
            morceaux = [(0, duree)]
            nom_clip = "Carton de fin"
        else:
            rid = ressource(pl["fichier"], pl.get("duree_rush"), audio=pl.get("audio", True))
            nom_clip = "%02d sc%02d %s" % (k + 1, pl.get("scene", 0), os.path.basename(pl["fichier"]))
            segs = pl.get("segments") or [(pl["debut"], pl["duree"])]
            # blancs coupés : un clip par bout de parole, coupes franches entre
            # eux ; les poignées du fondu sont prises sur le premier et le dernier
            morceaux = [(frames(d0), frames(d)) for d0, d in segs]
            if not premier:
                morceaux[0] = (morceaux[0][0] + t2, morceaux[0][1] - t2)
            if not dernier:
                morceaux[-1] = (morceaux[-1][0], morceaux[-1][1] - t2)
            ecart = duree - sum(d for _, d in morceaux)   # arrondis image par image
            morceaux[-1] = (morceaux[-1][0], morceaux[-1][1] + ecart)
        if not premier:
            tr = ET.SubElement(spine, "transition", name="Cross Dissolve",
                               offset=temps(total - t2), duration=temps(2 * t2))
            ET.SubElement(tr, "filter-video", ref="r2", name="Cross Dissolve")
        for j, (start, d) in enumerate(morceaux):
            nom = nom_clip if len(morceaux) == 1 else "%s (%d/%d)" % (nom_clip, j + 1, len(morceaux))
            clip = ET.SubElement(spine, "asset-clip", ref=rid, name=nom, offset=temps(total),
                                 start=temps(start), duration=temps(d), format="r1", tcFormat="NDF")
            if not pl["carton"] and pl.get("audio", True):
                clip.set("audioRole", "dialogue")
            if pl.get("gain_db"):
                ET.SubElement(clip, "adjust-volume", amount="%+.1fdB" % pl["gain_db"])
            if j == 0 and premier and titre_png:
                rid_t = ressource(titre_png, image=True)
                ET.SubElement(clip, "asset-clip", ref=rid_t, lane="1", name="Titre",
                              offset=temps(start), start="0s",
                              duration=temps(min(frames(DUREE_ACCROCHE), d)), format="r1")
            if j == 0 and not pl["carton"]:
                for note in notes_plan(pl):
                    ET.SubElement(clip, "marker", start=temps(start), duration=temps(1), value=note)
            total += d
    seq.set("duration", temps(total))

    if hasattr(ET, "indent"):
        ET.indent(root, space="  ")
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n')
        fh.write(ET.tostring(root, encoding="unicode") + "\n")
    return total


# ------------------------------------------------------------------ main ---

def ecrire_rapport(chemin, a, scenes, retenues, methode, plans, verif):
    L = ["# Rapport de montage : %s" % os.path.basename(a.sortie), ""]
    if verif:
        info, son, ok = verif
        L.append("- Durée : %.1f s, %dx%d, %d i/s" % (info["duree"], info["largeur"], info["hauteur"], FPS))
        L.append("- Son de sortie : %d canaux, RMS G %.1f dB / D %.1f dB → %s"
                 % (son["canaux"], son["rms"][0] if son["rms"] else -120,
                    son["rms"][1] if len(son["rms"]) > 1 else -120,
                    "stéréo OK" if ok else "⚠ À VÉRIFIER"))
        L.append("- Look : %s" % (("LUT " + a.lut) if a.lut else a.look))
    else:
        L.append("- Rendu ffmpeg non effectué (`--sans-rendu`) : le montage vit dans la timeline DaVinci")
    L.append("- Timeline DaVinci Resolve : `%s` (Fichier > Importer > Timeline). Les plans mono ou "
             "surexposés portent un marqueur qui dit quoi faire." % a.fcpxml_chemin)
    L.append("- Scènes : %d (%s), plans : %d" % (len(scenes), methode, len(plans)))
    coupes = [p for p in plans if len(p.get("segments") or []) > 1]
    if coupes:
        L.append("- Blancs coupés entre les phrases : %d coupes sur %d plans, %.1f s de silence retirés"
                 % (sum(len(p["segments"]) - 1 for p in coupes), len(coupes),
                    sum(p.get("blancs_coupes", 0) for p in coupes)))
    n_sur = sum(1 for p in plans if p.get("mesure_image", {}).get("surexpose"))
    if n_sur:
        L.append("- Plans surexposés : %d (courbe au rendu ffmpeg, marqueur dans la timeline DaVinci)" % n_sur)
    L += ["", "## Prises", ""]
    for i, sc in enumerate(scenes):
        L.append("### Scène %d, %d prise%s" % (i + 1, len(sc), "s" if len(sc) > 1 else ""))
        for j, r in enumerate(sc):
            diag, _ = decision_stereo(r["son"])
            L.append("- %s `%s` %.1f s, note %.2f (%s), son : %s"
                     % ("✅" if j == retenues[i] else "▫️", os.path.basename(r["fichier"]),
                        r["duree"], r["note"],
                        ", ".join("%s %s" % (k, v) for k, v in r["detail_note"].items()),
                        diag))
        L.append("")
    L += ["## Plans montés", "", "| # | scène | fichier | entrée | durée | son | image |", "|---|---|---|---|---|---|---|"]
    for k, p in enumerate(plans):
        n_seg = len(p.get("segments") or [])
        L.append("| %d | %d | %s | %.2f | %.2f%s | %s%s | %s |" % (
            k + 1, p.get("scene", 0), os.path.basename(p["fichier"]), p["debut"], p["duree"],
            (" (%d bouts, %.1f s de blanc sautés)" % (n_seg, p.get("blancs_coupes", 0))) if n_seg > 1 else "",
            p.get("diag_son", ""), (" (%+.1f dB)" % p["gain_db"]) if p.get("gain_db") else "",
            ("⚠ surexposé, ramené (YAVG %s, %.0f %% brûlé)" % (
                p.get("mesure_image", {}).get("YAVG", "?"),
                100 * (p.get("mesure_image", {}).get("clip") or 0)))
            if p.get("mesure_image", {}).get("surexpose") else p.get("correction", "")))
    L += ["", "Pour changer un plan ou une prise : éditer `%s` puis relancer avec `--edl`." % a.edl_chemin]
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


def couper_blancs(ffmpeg, plans, par_fichier):
    """Applique la coupe des blancs à chaque plan qui a du son. Une prise n'est
    analysée qu'une fois. Les plans qui n'ont pas assez de parole gardent leur
    fenêtre d'origine."""
    plages = {}
    n_coupes, gagne = 0, 0.0
    for pl in plans:
        r = par_fichier.get(pl["fichier"])
        if not r or not r.get("audio", True) or pl.get("pan") == "silence":
            continue
        if pl["fichier"] not in plages:
            sil = detecter_silences(ffmpeg, pl["fichier"], r["duree"])
            plages[pl["fichier"]] = plages_parole(sil, r["duree"])
        res = appliquer_coupes(pl, plages[pl["fichier"]])
        if not res:
            continue
        segs, saute = res
        pl["segments"] = segs
        pl["blancs_coupes"] = saute
        pl["debut"] = segs[0][0]
        n_coupes += len(segs) - 1
        gagne += saute
    log("• blancs coupés : %d coupes, %.1f s de silence sautés" % (n_coupes, gagne))


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("dossier", nargs="?", help="dossier des rushs (récursif)")
    p.add_argument("--edl", help="re-rendre depuis un montage.json existant")
    p.add_argument("--reetalonner", action="store_true",
                   help="avec --edl : remesurer chaque plan et recalculer sa correction "
                        "d'exposition (plans surexposés compris) avant le rendu")
    p.add_argument("--titre", default="", help="titre incrusté sur l'accroche")
    p.add_argument("--sous-titre", default="", dest="sous_titre")
    p.add_argument("--carton-fin", default="", dest="carton_fin",
                   help="texte du carton de fin ; \\n pour une 2e ligne")
    p.add_argument("--cta-fond", default=None, dest="cta_fond",
                   help="couleur de fond du carton de fin (#hex, charte du client)")
    p.add_argument("--cta-texte", default=None, dest="cta_texte",
                   help="couleur du texte du carton de fin (#hex)")
    p.add_argument("--cta-police", default=None, dest="cta_police",
                   help="police .ttf/.otf du carton de fin (charte du client)")
    p.add_argument("--cta-logo", default=None, dest="cta_logo",
                   help="logo .png (fond transparent) posé au-dessus du texte du carton")
    p.add_argument("--couper-blancs", action="store_true", dest="couper_blancs",
                   help="couper les blancs entre les phrases dans chaque plan (silences "
                        "de plus de %.1f s, %.2f s de respiration gardés de chaque côté)"
                        % (SILENCE_MIN, SILENCE_GARDE))
    p.add_argument("--duree", type=float, default=90.0, help="durée totale (s), 90 par défaut")
    p.add_argument("--musique", help="fichier audio de fond (optionnel)")
    p.add_argument("--look", default="ramen", choices=sorted(LOOKS),
                   help="étalonnage global : ramen (défaut), neutre, froid, aucun")
    p.add_argument("--lut", help="fichier .cube appliqué à la place du look")
    p.add_argument("--accroche", type=int, help="numéro de la scène à mettre en ouverture")
    p.add_argument("--sortie", help="fichier mp4 de sortie")
    p.add_argument("--ffmpeg", help="chemin de ffmpeg (ffprobe cherché à côté)")
    p.add_argument("--garder", action="store_true", help="garder les clips intermédiaires")
    p.add_argument("--sans-rendu", action="store_true", dest="sans_rendu",
                   help="écrire l'EDL, la timeline DaVinci (.fcpxml) et le rapport "
                        "sans rendre le mp4")
    a = p.parse_args()

    ffmpeg = am.trouver_binaire("ffmpeg", a.ffmpeg)
    ffprobe = shutil.which("ffprobe") or (
        os.path.join(os.path.dirname(ffmpeg), "ffprobe")
        if os.path.exists(os.path.join(os.path.dirname(ffmpeg), "ffprobe")) else None)
    if a.lut and not os.path.exists(a.lut):
        sys.exit("✗ LUT introuvable : %s" % a.lut)
    look = ("lut3d=file='%s'" % echapper(a.lut)) if a.lut else LOOKS[a.look]

    if a.edl:
        edl = json.load(open(a.edl, encoding="utf-8"))
        for cle in ("titre", "sous_titre", "carton_fin", "musique", "sortie", "lut",
                    "cta_fond", "cta_texte", "cta_police", "cta_logo"):
            if getattr(a, cle) in ("", None) and edl.get(cle):
                setattr(a, cle, edl[cle])
        if edl.get("look") and a.look == "ramen":
            a.look = edl["look"]
        if a.lut:
            look = "lut3d=file='%s'" % echapper(a.lut)
        elif a.look in LOOKS:
            look = LOOKS[a.look]
        plans = [pl for pl in edl["plans"] if pl.get("fichier") != "__carton__"]
        durees = [pl["duree"] for pl in plans]
        if a.carton_fin:
            durees.append(DUREE_CARTON)
        scenes, retenues, methode = [], [], "EDL"
        log("↻ EDL relue : %d plans" % len(plans))
        if a.couper_blancs and not any(pl.get("segments") for pl in plans):
            infos = {}
            for pl in plans:
                if pl["fichier"] not in infos:
                    i = am.sonder(ffprobe, ffmpeg, pl["fichier"])
                    infos[pl["fichier"]] = dict(duree=i["duree"], audio=i["audio"]) if i else None
            couper_blancs(ffmpeg, plans, {k: v for k, v in infos.items() if v})
        if a.reetalonner:
            n_sur = 0
            for pl in plans:
                st = stats_image(ffmpeg, pl["fichier"], pl["debut"] + pl["duree"] / 2)
                pl["correction"], pl["mesure_image"] = correction_plan(st)
                n_sur += int(pl["mesure_image"].get("surexpose", False))
            log("↻ étalonnage recalculé : %d plans, dont %d surexposés" % (len(plans), n_sur))
    else:
        if not a.dossier:
            p.error("donne un dossier de rushs, ou --edl montage.json")
        fichiers = am.lister_rushs(a.dossier)
        if not fichiers:
            sys.exit("✗ aucun rush dans %s" % a.dossier)
        log("• %d fichiers vidéo trouvés" % len(fichiers))
        rushs = []
        for fch in fichiers:
            info = am.sonder(ffprobe, ffmpeg, fch)
            if info and info["duree"] >= PLAN_MIN * 2:
                rushs.append(info)
            else:
                log("  – ignoré (illisible ou < 3 s) : %s" % os.path.basename(fch))
        if not rushs:
            sys.exit("✗ aucun rush exploitable")
        if all(r["date"] for r in rushs):
            rushs.sort(key=lambda r: r["date"])
        log("• %d rushs exploitables, %d min %02d s de matière"
            % (len(rushs), sum(r["duree"] for r in rushs) // 60,
               sum(r["duree"] for r in rushs) % 60))

        scenes, methode = grouper_scenes(ffmpeg, rushs)
        retenues = []
        for i, sc in enumerate(scenes):
            best = noter_prises(ffmpeg, sc)
            retenues.append(best)
            if len(sc) > 1:
                log("  ▸ scène %02d : %d prises, retenue %s (note %.2f)"
                    % (i + 1, len(sc), os.path.basename(sc[best]["fichier"]), sc[best]["note"]))
        durees = grille_durees(a.duree, bool(a.carton_fin))
        durees_rushs = durees[:-1] if a.carton_fin else durees
        log("• %d plans à monter sur %d scènes" % (len(durees_rushs), len(scenes)))
        plans = repartir_plans(scenes, retenues, durees_rushs, a.accroche)
        par_fichier = {r["fichier"]: r for sc in scenes for r in sc}
        for pl in plans:
            r = par_fichier[pl["fichier"]]
            pl["audio"] = r["audio"]
            pl["duree_rush"] = round(r["duree"], 3)
            diag, pan = decision_stereo(r["son"])
            pl["diag_son"] = diag
            pl["pan"] = pan or ("silence" if r["son"]["canaux"] == 0 else None)
            pl["gain_db"] = gain_plan(r["son"])
            pl["correction"], pl["mesure_image"] = correction_plan(r["stats"])
        if a.couper_blancs:
            couper_blancs(ffmpeg, plans, par_fichier)

    a.sortie = a.sortie or os.path.join("o", "reel.mp4")
    os.makedirs(os.path.dirname(a.sortie) or ".", exist_ok=True)
    a.edl_chemin = os.path.splitext(a.sortie)[0] + ".montage.json"
    with open(a.edl_chemin, "w", encoding="utf-8") as fh:
        json.dump(dict(titre=a.titre, sous_titre=a.sous_titre, carton_fin=a.carton_fin,
                       cta_fond=a.cta_fond, cta_texte=a.cta_texte, cta_police=a.cta_police,
                       cta_logo=a.cta_logo, couper_blancs=a.couper_blancs,
                       musique=a.musique, look=a.look, lut=a.lut, sortie=a.sortie,
                       duree=a.duree, plans=plans), fh, ensure_ascii=False, indent=2)
    log("• EDL écrite : %s" % a.edl_chemin)

    # cartons écrits à côté de la sortie : le rendu et la timeline DaVinci
    # utilisent les mêmes fichiers
    base = os.path.splitext(a.sortie)[0]
    titre_png = base + "-titre.png"
    am.carton_titre(titre_png, a.titre, a.sous_titre, W, H)
    carton_png = None
    if a.carton_fin:
        carton_png = base + "-carton-fin.png"
        if a.cta_fond or a.cta_texte or a.cta_police or a.cta_logo:
            carton_cta(carton_png, a.carton_fin, W, H, a.cta_fond, a.cta_texte,
                       a.cta_police, a.cta_logo)
        else:
            am.carton_fin(carton_png, a.carton_fin, W, H)
    a.fcpxml_chemin = base + ".fcpxml"
    n_images = ecrire_fcpxml(a.fcpxml_chemin, os.path.basename(base), plans,
                             titre_png if a.titre else None, carton_png,
                             evenement=a.titre or "Reel")
    log("• timeline DaVinci : %s (%.1f s, %d plans)" % (a.fcpxml_chemin, n_images / FPS, len(plans)))
    if a.sans_rendu:
        rapport = base + ".rapport.md"
        ecrire_rapport(rapport, a, scenes, retenues, methode, plans, None)
        log("• rapport : %s (pas de rendu mp4, --sans-rendu)" % rapport)
        return

    tmp = tempfile.mkdtemp(prefix="reel-")
    try:
        clips = []
        for k, pl in enumerate(plans):
            c = os.path.join(tmp, "plan-%02d.mov" % k)
            log("  ▸ plan %02d  sc%02d %-30s %7.2f s +%.2f s  %s" % (
                k + 1, pl.get("scene", 0), os.path.basename(pl["fichier"])[:30],
                pl["debut"], pl["duree"], pl.get("diag_son", "")))
            rendre_plan(ffmpeg, pl, c)
            clips.append(c)
        if carton_png:
            c = os.path.join(tmp, "carton-fin.mov")
            rendre_carton_clip(ffmpeg, carton_png, c, DUREE_CARTON)
            clips.append(c)
        log("• assemblage + étalonnage (%s)…" % (("LUT " + a.lut) if a.lut else a.look))
        total = assembler(ffmpeg, clips, durees, titre_png, min(DUREE_ACCROCHE, durees[0]),
                          look, a.musique, a.sortie)
        if a.garder:
            garde = os.path.splitext(a.sortie)[0] + "-plans"
            shutil.copytree(tmp, garde, dirs_exist_ok=True)
            log("• clips intermédiaires : %s" % garde)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    verif = verifier_sortie(ffmpeg, ffprobe, a.sortie)
    info, son, ok = verif
    rapport = os.path.splitext(a.sortie)[0] + ".rapport.md"
    ecrire_rapport(rapport, a, scenes, retenues, methode, plans, verif)
    log("✓ %s — %.1f s attendues, %.1f s mesurées, %dx%d, son %s (G %.1f dB / D %.1f dB)" % (
        a.sortie, total, info["duree"], info["largeur"], info["hauteur"],
        "stéréo OK" if ok else "⚠ À VÉRIFIER",
        son["rms"][0] if son["rms"] else -120, son["rms"][1] if len(son["rms"]) > 1 else -120))
    log("• rapport : %s" % rapport)


if __name__ == "__main__":
    main()

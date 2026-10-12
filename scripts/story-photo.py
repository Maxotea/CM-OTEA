#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 1080x1920 sur VRAIE photo plein cadre, pilotée par scripts/themes.json.

Moteur unique des stories photo d'OTEA Production, d'Otea Filmakers et de Run On Invest
(cadrage du 12/10/2026, §1.1). Construction de Pierre Huiban (scripts/pierre-story-photo-v2.py) :
photo plein cadre, voile sombre en haut (nom, registre) et en bas (kicker, UNE phrase, pied
sous filet), milieu net entre y=480 et y=880 où se trouve la personne. La charte vient du thème :

    theme["fond"]   texte, muted, accent, voile (les clés que lit carrousel.py)
    theme["story"]  nom, logo, mention, registre, pied, polices, casse, tailles, grain, barre,
                    cache (originaux des stories), photos_ia_autorisees

Usage :
    python3 scripts/story-photo.py CLIENT SPEC.json CLE PHOTO SORTIE.jpg [options]
    python3 scripts/story-photo.py --verifier-carrousel carrousels/<client>/<spec>.json

    PHOTO  fichier local, URL, ou clé du manifeste photos/<client>.json (l'original est lu
           dans story.cache, jamais un fond 4:5 préparé)
    --fond F.jpg        écrit aussi le recadrage 9:16 sans texte (l'entrée de l'i2v)
    --calque C.png      écrit aussi le calque transparent à poser sur la vidéo i2v ; son voile
                        reprend le palier calculé sur cette photo plus 0,04
    --controle IMG ...  frames 1080x1920 de la vidéo i2v AVANT pose du calque (0, milieu, fin) :
                        chacune reçoit le voile du calque, contraste mesuré sous les masques
    --decalage 0..1     position horizontale du recadrage (défaut : celle du manifeste, ou 0,5)
    --visage x0,y0,x1,y1  boîte d'un visage dans le cadre 1080x1920 (répétable), pour une
                        photo hors manifeste ; --sans-visage si elle n'en montre aucun
    --voile-bas A       plancher du voile du bas (jamais en dessous du besoin mesuré)
    --basse-definition  accepte une source dont le recadrage 9:16 fait moins de 1280 px de haut

Garde-fous, tous bloquants :
  - lisibilité MESURÉE sur les pixels (métrologie de carrousel.py, seule du dépôt) : phrase
    7:1 ; nom, mention, registre (élément allumé compris) et pied 4,5:1 ; kicker, mots
    accentués et barre 3:1. Le voile de chaque zone est la plus petite opacité qui tient ces
    cibles, plafonnée à 0,96. Le grain est posé AVANT la mesure. Si l'accent ne peut pas
    tenir 4,5:1 sur le registre, l'élément allumé passe en couleur de texte, souligné de 3 px ;
  - rampes du voile en smoothstep (aucune cassure visible au raccord) ;
  - aucun tiret cadratin, demi-cadratin ni double tiret, aucun « [ » de placeholder, dans
    aucun champ affiché (jour, phrase, registre, nom, mention, pied) ;
  - aucun visage sous l'encre ni dans les 150 px de rampe : boîtes visage_916 du manifeste
    (visage_45 pour les carrousels, via --verifier-carrousel) ;
  - polices strictes : un nom absent de la liste du thème est une erreur, jamais un repli ;
  - photo IA refusée sauf sur un thème qui l'autorise (Run On Invest), personne identifiable
    toujours refusée.

Aucune image générée, aucune retouche de visage : recadrage, voile, texte. Sortie muette par
construction. Brouillon côté Metricool (règle permanente du CM).
"""
import argparse
import importlib.util
import json
import os
import sys
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

ICI = Path(__file__).resolve().parent
ROOT = ICI.parent
POLICES_DEPOT = ROOT / "fonts"

# La métrologie de carrousel.py, réutilisée sans copie (le fichier n'est jamais modifié ici).
_spec = importlib.util.spec_from_file_location("carrousel_metrologie", ICI / "carrousel.py")
carrousel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(carrousel)

W, H = 1080, 1920
Y_REGISTRE = 250                       # nom du compte, sous la barre de progression Instagram
Y_PIED = H - 330                       # filet du pied : 1590
BAS_BLOC = Y_PIED - 70                 # le bloc kicker + phrase se termine ici : 1520
HAUT_PLEIN, HAUT_FIN = 320, 480        # voile du haut : plein jusqu'à 320, nul à 480
BAS_DEBUT, BAS_PLEIN = 880, 1080       # voile du bas : nul jusqu'à 880, plein à 1080
RAMPE_VISAGE = 150                     # aucun visage à moins de 150 px de l'encre
VOILE_MAX = 0.96
MARGE_CALQUE = 0.04
CIBLE_PHRASE, CIBLE_PETIT, CIBLE_LARGE = 7.0, 4.5, 3.0
HAUTEUR_SOURCE_MIN = 1280              # un 9:16 pris dans un aperçu 1440x960 ne fait que 960
TIRETS = ("—", "–", "--")    # cadratin, demi-cadratin, double tiret

# élément tracé -> (zone du voile, rôle de couleur, cible de contraste ; None = décor non mesuré)
ELEMENTS = {
    "nom": ("haut", "texte", CIBLE_PETIT),
    "mention": ("haut", "texte", CIBLE_PETIT),
    "registre": ("haut", "muted", CIBLE_PETIT),
    "registre_actif": ("haut", "accent", CIBLE_PETIT),
    "souligne": ("haut", "accent", CIBLE_LARGE),
    "kicker": ("bas", "accent", CIBLE_LARGE),
    "phrase": ("bas", "texte", CIBLE_PHRASE),
    "phrase_accent": ("bas", "accent", CIBLE_LARGE),
    "barre": ("bas", "accent", CIBLE_LARGE),
    "pied": ("bas", "muted", CIBLE_PETIT),
    "filet": ("bas", "regle", None),
}


class PoliceIntrouvable(LookupError):
    """Une police demandée par le thème n'est installée nulle part : on ne rend pas."""


# ---------------------------------------------------------------- polices

def _index(extra):
    dossiers = ([Path(extra)] if extra else []) + [POLICES_DEPOT] + list(carrousel.FONT_DIRS)
    idx = []
    for d in dossiers:
        if d.is_dir():
            for p in sorted(d.rglob("*")):
                if p.suffix.lower() in (".ttf", ".otf"):
                    idx.append((carrousel._norm(p.stem), p))
    return dossiers, idx


def police(noms, taille, extra=None):
    """Première police de la liste du thème trouvée sur la machine, sinon PoliceIntrouvable.

    Nom complet attendu (« Inter Display Bold » pour InterDisplay-Bold.ttf). Pas de repli
    caché : la liste du thème EST la déclaration, et le fichier réellement chargé est tracé
    dans police.utilisees pour être affiché à chaque rendu."""
    if isinstance(noms, str):
        noms = [noms]
    cache = police.__dict__.setdefault("cache", {})
    cle = (tuple(noms), taille, extra)
    if cle in cache:
        return cache[cle]
    index = police.__dict__.setdefault("index", {})
    if extra not in index:
        index[extra] = _index(extra)
    dossiers, idx = index[extra]
    for nom in noms:
        n = carrousel._norm(nom)
        for stem, chemin in idx:
            if stem == n or stem == n + "regular" or (n.endswith("regular") and stem == n[:-7]):
                f = ImageFont.truetype(str(chemin), taille)
                police.__dict__.setdefault("utilisees", {})[nom] = chemin.name
                cache[cle] = f
                return f
    raise PoliceIntrouvable(
        f"police introuvable : {' / '.join(noms)}. Cherchée dans {', '.join(str(d) for d in dossiers)}. "
        f"Installer le fichier (voir fonts/README.md) : aucun repli n'est pris.")


# ---------------------------------------------------------------- texte

def espace(d, xy, texte, f, fill, track=0.0):
    x, y = xy
    for c in texte:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return x


def largeur_espacee(d, texte, f, track):
    return sum(d.textlength(c, font=f) + track for c in texte) - track


def lignes_phrase(d, texte, f, largeur, track):
    """Avec « \\n » : les lignes imposées (cartes du kit R.O.I.), jamais recoupées ; une ligne
    trop large fait rétrécir le corps. Sans « \\n » : coupure gloutonne."""
    if "\n" not in texte:
        return _lignes_gloutonnes(d, texte, f, largeur, track)
    out = []
    for morceau in texte.split("\n"):
        out.extend(_lignes_gloutonnes(d, morceau.strip(), f, 10 ** 6, track))
    return out


def _lignes_gloutonnes(d, texte, f, largeur, track):
    """Mots (texte, accentué, collé) ; un morceau collé à une balise ** reste soudé au mot
    précédent, sinon la ponctuation se détache (même règle que carrousel.tokeniser)."""
    mots, fin_espace = [], True
    for i, segment in enumerate(texte.split("**")):
        fort = i % 2 == 1
        debut_espace = segment[:1].isspace() if segment else True
        parts = segment.split()
        for j, m in enumerate(parts):
            colle = bool(mots) and j == 0 and not (fin_espace or debut_espace)
            mots.append((m, fort, colle))
        if parts:
            fin_espace = segment[-1:].isspace()
    esp = d.textlength(" ", font=f)
    lignes, ligne, lx = [], [], 0
    for m, fort, colle in mots:
        w = largeur_espacee(d, m, f, track)
        supp = w if (not ligne or colle) else esp + w
        if ligne and lx + supp > largeur and not colle:
            lignes.append(ligne)
            ligne, lx = [(m, fort, False)], w
        else:
            ligne.append((m, fort, colle))
            lx += supp
    if ligne:
        lignes.append(ligne)
    return lignes


def largeur_ligne(d, ligne, f, track):
    esp = d.textlength(" ", font=f)
    tot = 0
    for i, (m, _fort, colle) in enumerate(ligne):
        if i and not colle:
            tot += esp
        tot += largeur_espacee(d, m, f, track)
    return tot


def poser_phrase(d, xy, lignes, f, fill, accent, interligne, track):
    x0, y = xy
    esp = d.textlength(" ", font=f)
    for ligne in lignes:
        x = x0
        for i, (m, fort, colle) in enumerate(ligne):
            if i and not colle:
                x += esp
            x = espace(d, (x, y), m, f, accent if fort else fill, track)
        y += interligne
    return y


def verifier_textes(theme, carte):
    """Refuse tout texte affiché qui porte un tiret interdit ou un placeholder."""
    st = theme["story"]
    champs = {f"carte.{k}": carte.get(k) for k in ("jour", "phrase", "registre")}
    champs.update({f"story.{k}": st.get(k) for k in ("nom", "mention", "pied")})
    champs.update({f"story.registre[{i}]": r for i, r in enumerate(st.get("registre", []))})
    fautes = []
    for champ, texte in champs.items():
        if not isinstance(texte, str):
            continue
        fautes += [f"{champ} : « {t} » dans « {texte} »" for t in TIRETS if t in texte]
        if "[" in texte:
            fautes.append(f"{champ} : placeholder « [ » dans « {texte} »")
    if fautes:
        raise ValueError("texte refusé (tiret cadratin, demi-cadratin, double tiret ou placeholder "
                         "dans un texte affiché) :\n  - " + "\n  - ".join(fautes))
    for k in ("jour", "phrase"):
        if not (carte.get(k) or "").strip():
            raise ValueError(f"carte {carte.get('cle')} : champ « {k} » vide")
    if carte["phrase"].count("**") % 2:
        raise ValueError(f"carte {carte.get('cle')} : balise ** non refermée dans la phrase")
    actif = carte.get("registre") or ""
    if actif and actif not in st.get("registre", []):
        raise ValueError(f"carte {carte.get('cle')} : registre « {actif} » absent de la liste du "
                         f"thème {st.get('registre')} (jamais de valeur inventée)")


# ---------------------------------------------------------------- image

def cadrer(photo, decalage=0.5, basse_definition=False):
    """Recadrage 9:16 plein cadre, sans déformation ; refuse une source trop petite."""
    im = ImageOps.exif_transpose(photo).convert("RGB")
    haut_utile = min(im.height, im.width * H / W)
    if haut_utile < HAUTEUR_SOURCE_MIN and not basse_definition:
        raise ValueError(
            f"source trop petite pour une story plein cadre : le recadrage 9:16 ne fait que "
            f"{haut_utile:.0f} px de haut (minimum {HAUTEUR_SOURCE_MIN}). Partir de l'original "
            f"(story.cache), pas d'un aperçu ; --basse-definition pour passer outre en connaissance de cause.")
    return ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(decalage, 0.45))


def _lisse(t):
    """Rampe smoothstep : dérivée nulle aux deux bouts, donc aucune cassure là où le voile
    rejoint son plat (la rampe quadratique laissait une crête nette, POC du 12/10/2026)."""
    return t * t * (3 - 2 * t)


def voile(a_haut, a_bas):
    """Masque L : plein en haut, nul au milieu, plein en bas ; rampes smoothstep."""
    v = Image.new("L", (1, H))
    for y in range(H):
        if y < HAUT_PLEIN:
            a = a_haut
        elif y < HAUT_FIN:
            a = a_haut * (1 - _lisse((y - HAUT_PLEIN) / (HAUT_FIN - HAUT_PLEIN)))
        elif y < BAS_DEBUT:
            a = 0
        elif y < BAS_PLEIN:
            a = a_bas * _lisse((y - BAS_DEBUT) / (BAS_PLEIN - BAS_DEBUT))
        else:
            a = a_bas
        v.putpixel((0, y), int(round(min(1.0, a) * 255)))
    return v.resize((W, H))


def grain(im, bruit):
    """Ajoute un bruit centré sur 128, tiré UNE fois par rendu : la mesure et l'image livrée
    voient exactement le même grain."""
    return ImageChops.add(im, bruit, 1, -128)


def _boites(valeur):
    if not valeur:
        return []
    if isinstance(valeur[0], (int, float)):
        valeur = [valeur]
    return [tuple(float(v) for v in b) for b in valeur]


# ---------------------------------------------------------------- habillage

def charger_logo(st):
    """Logotype du thème, mis à la hauteur demandée. Absent : secours SIGNALÉ sur le nom saisi."""
    conf = st.get("logo")
    if not conf:
        return None, None
    chemin = ROOT / conf["fichier"]
    if not chemin.exists():
        alerte = (f"SECOURS : logotype absent ({conf['fichier']}), nom saisi « {st['nom']} » à la place. "
                  f"Le déposer depuis le Drive ({conf.get('drive_id', 'id non renseigné')}) avant un rendu final.")
        print(alerte, file=sys.stderr)
        return None, alerte
    im = Image.open(chemin).convert("RGBA")
    h = int(conf.get("hauteur", 40))
    return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS), None


def couleur_logo(logo):
    """Couleur moyenne des pixels opaques du logo : c'est elle qu'on mesure contre le fond."""
    if logo is None:
        return None
    alpha = logo.getchannel("A").point(lambda v: 255 if v > 200 else 0)
    if alpha.getbbox() is None:
        return None
    rgb = logo.convert("RGB")
    return tuple(int(round(sum(rgb.getchannel(i).histogram(alpha)[v] * v for v in range(256))
                           / max(1, sum(rgb.getchannel(i).histogram(alpha)))))
                 for i in range(3))


def habiller(img, theme, carte, extra, couleur, opts):
    """Trace tout l'habillage ; couleur(élément) donne le remplissage de chaque élément."""
    d = ImageDraw.Draw(img)
    st = theme["story"]
    M = st.get("marge", 96)
    P = lambda k, t: police(st["polices"][k], t, extra)
    tr_label = 3.4

    # --- tête : nom (logotype ou nom saisi), mention, registre --------------------
    logo = opts.get("logo")
    if logo is not None:
        fill = couleur("nom")
        if isinstance(fill, int):
            img.paste(Image.new(img.mode, logo.size, fill), (M, Y_REGISTRE), logo.getchannel("A"))
        else:
            img.paste(logo, (M, Y_REGISTRE), logo)
        x_fin, base = M + logo.width, Y_REGISTRE + logo.height
    else:
        f_nom = P("nom", 24) if "nom" in st["polices"] else P("label", 24)
        x_fin = espace(d, (M, Y_REGISTRE), st["nom"], f_nom, couleur("nom"), st.get("tracking_nom", tr_label))
        base = Y_REGISTRE + f_nom.getmetrics()[0]
    if st.get("mention"):
        # même ligne de base que le nom (deux polices, deux jambages)
        d.text((W - M, base), st["mention"], font=P("mono", 22), fill=couleur("mention"), anchor="rs")
    actif = carte.get("registre") or ""
    mots = []
    for i, r in enumerate(st.get("registre", [])):
        mots.append((r, r == actif))
        if i < len(st["registre"]) - 1:
            mots.append(("·", False))
    if mots:
        fl, tr = P("label", 22), 2.6
        larg = sum(largeur_espacee(d, m, fl, tr) for m, _ in mots) + 14 * (len(mots) - 1)
        if not st.get("mention") and x_fin + 40 + larg <= W - M:
            x, y = W - M - larg, Y_REGISTRE + 2          # même ligne, à droite (cas de Pierre)
        else:                                            # deuxième ligne, à gauche, taille adaptée
            for taille, tr in ((20, 2.4), (18, 2.0), (16, 1.8)):
                fl = P("label", taille)
                larg = sum(largeur_espacee(d, m, fl, tr) for m, _ in mots) + 14 * (len(mots) - 1)
                if larg <= W - 2 * M:
                    break
            else:
                raise ValueError(f"registre trop long pour la zone utile : {larg:.0f} px")
            x, y = M, max(Y_REGISTRE + 44, base + 14)
        for m, on in mots:
            x0 = x
            x = espace(d, (x, y), m, fl, couleur("registre_actif" if on else "registre"), tr)
            if on and opts.get("souligne"):
                y_ul = y + fl.getmetrics()[0] + 5
                d.rectangle([x0, y_ul, x - tr, y_ul + 2], fill=couleur("souligne"))
            x += 14

    # --- bloc bas : kicker, phrase, barre ----------------------------------------
    t0, t1 = st["taille_phrase"]
    phrase = carte["phrase"].upper() if st.get("casse_phrase", "upper") == "upper" else carte["phrase"]
    taille = t0
    h_barre = 46 if st.get("barre_accent") else 0
    while True:   # rétrécit par pas de 4 px : 4 lignes au plus, bloc entier sur le voile plein
        f = P("titre", taille)
        trp = st.get("tracking_phrase", 0.0) * taille
        lignes = lignes_phrase(d, phrase, f, W - 2 * M, trp)
        larg_phrase = max(largeur_ligne(d, l, f, trp) for l in lignes)
        il = int(taille * st.get("interligne_phrase", 1.14))
        h_bloc = 30 + 84 + il * len(lignes) + h_barre
        y = BAS_BLOC - h_bloc
        if (len(lignes) <= 4 and y >= BAS_PLEIN - 40 and larg_phrase <= W - 2 * M) or taille - 4 < t1:
            break
        taille -= 4
    if y < BAS_PLEIN - 40:
        raise ValueError(f"phrase trop longue même à {taille} px : le bloc commence à y={y}, "
                         f"au-dessus du voile plein ({BAS_PLEIN}). Raccourcir la phrase.")
    if larg_phrase > W - 2 * M:
        raise ValueError(f"un mot de la phrase dépasse la largeur utile même à {taille} px "
                         f"({larg_phrase:.0f} px pour {W - 2 * M}) : couper le mot ou raccourcir.")
    fk = P("label", 30)
    if largeur_espacee(d, carte["jour"].upper(), fk, tr_label) > W - 2 * M:
        raise ValueError("kicker trop large pour la zone utile : " + carte["jour"])
    espace(d, (M, y), carte["jour"].upper(), fk, couleur("kicker"), tr_label)
    y = poser_phrase(d, (M, y + 84), lignes, f, couleur("phrase"), couleur("phrase_accent"), il, trp)
    if st.get("barre_accent"):
        y += 30
        d.rectangle([M, y, M + int(W * 0.20), y + 6], fill=couleur("barre"))

    # --- pied ----------------------------------------------------------------------
    d.line([(M, Y_PIED), (W - M, Y_PIED)], fill=couleur("filet"), width=2)
    fp = P("label", 22)
    if largeur_espacee(d, st["pied"], fp, 2.8) > W - 2 * M:
        raise ValueError("pied trop large pour la zone utile : " + st["pied"])
    espace(d, (M, Y_PIED + 30), st["pied"], fp, couleur("pied"), 2.8)
    return {"taille_phrase": taille, "lignes": len(lignes), "y_bloc": BAS_BLOC - h_bloc}


def couleurs(theme, opts):
    fd = theme["fond"]
    base = {k: carrousel._hex_rgb(fd[k]) for k in ("texte", "muted", "accent", "voile")}
    base["regle"] = tuple(int(a * 0.55 + b * 0.45) for a, b in zip(base["muted"], base["voile"]))
    col = {el: base[role] for el, (_z, role, _c) in ELEMENTS.items()}
    if theme.get("story", {}).get("filet_accent"):
        col["filet"] = base["accent"]
    if opts.get("souligne"):
        col["registre_actif"] = base["texte"]
    if opts.get("logo_couleur"):
        col["nom"] = opts["logo_couleur"]
    return base, col


def masques(theme, carte, extra, opts):
    """Un masque L par élément : blanc là où son encre tombe."""
    out = {}
    for el in ELEMENTS:
        m = Image.new("L", (W, H), 0)
        habiller(m, theme, carte, extra, lambda e, el=el: 255 if e == el else 0, opts)
        if m.getbbox():
            out[el] = m
    return out


def sous_encre(img, masque, marge=12):
    """carrousel._fond_sous_encre restreint à la boîte du masque élargie de 12 px : même
    résultat (dilatation de 3 px et flou de 1 px tiennent dans la marge), vingt fois plus vite."""
    x0, y0, x1, y1 = masque.getbbox()
    boite = (max(0, x0 - marge), max(0, y0 - marge), min(W, x1 + marge), min(H, y1 + marge))
    return carrousel._fond_sous_encre(img.crop(boite), masque.crop(boite))


def mesurer(img, col, masq):
    """Contraste réel sous l'encre de chaque élément mesuré : {élément: (contraste, cible)}."""
    rgb = img.convert("RGB")
    return {el: (round(carrousel._contraste(sous_encre(rgb, m), col[el]), 2), ELEMENTS[el][2])
            for el, m in masq.items() if ELEMENTS[el][2] is not None}


def manques(mes):
    return {el: v for el, (v, cible) in mes.items() if v < cible}


def bande_nette(masq):
    """Bande verticale où un visage peut se trouver : hors de l'encre, de ses 150 px de rampe
    et des voiles."""
    hauts = [masq[e].getbbox()[3] for e in masq if ELEMENTS[e][0] == "haut"]
    bas = [masq[e].getbbox()[1] for e in masq if ELEMENTS[e][0] == "bas"]
    y0 = max([HAUT_FIN] + [y + RAMPE_VISAGE for y in hauts])
    y1 = min([BAS_DEBUT] + [y - RAMPE_VISAGE for y in bas])
    return y0, y1


def controler_visages(masq, visages):
    if visages is None:
        raise ValueError("boîtes visage non fournies : visage_916 au manifeste, --visage, ou "
                         "--sans-visage (liste vide) si la photo ne montre aucun visage")
    y0, y1 = bande_nette(masq)
    coupes = [b for b in _boites(visages) if b[1] < y0 or b[3] > y1]
    if coupes:
        raise ValueError(
            f"visage sous l'encre ou dans la rampe : {coupes} sort de la bande nette y={y0} à {y1}. "
            f"Décaler le recadrage, raccourcir le texte ou choisir une autre photo.")
    return y0, y1


# ---------------------------------------------------------------- composition

def _voiler(fond, col, masq, voile_rgb, bruit, voile_bas):
    """Plus petit voile (par zone) qui tient toutes les cibles, mesuré APRÈS le grain."""
    besoin = {"haut": 0.0, "bas": 0.0}
    for el, m in masq.items():
        zone, _role, cible = ELEMENTS[el]
        if cible:
            pire = sous_encre(fond, m)
            besoin[zone] = max(besoin[zone], carrousel._alpha_requis(pire, col[el], voile_rgb, cible))
    a_haut = min(VOILE_MAX, max(0.35, besoin["haut"] + 0.02))
    a_bas = min(VOILE_MAX, max(0.55, besoin["bas"] + 0.02, voile_bas or 0.0))
    aplat = Image.new("RGB", (W, H), voile_rgb)
    for _ in range(40):   # composition, grain, PUIS mesure ; on renforce par pas de 0,02
        img = Image.composite(aplat, fond, voile(a_haut, a_bas))
        if bruit is not None:
            img = grain(img, bruit)
        mes = mesurer(img, col, masq)
        manque = manques(mes)
        h = any(ELEMENTS[e][0] == "haut" for e in manque) and a_haut < VOILE_MAX
        b = any(ELEMENTS[e][0] == "bas" for e in manque) and a_bas < VOILE_MAX
        if not (h or b):
            break
        a_haut = min(VOILE_MAX, a_haut + 0.02) if h else a_haut
        a_bas = min(VOILE_MAX, a_bas + 0.02) if b else a_bas
    return img, a_haut, a_bas, mes, manque


def composer(photo, theme, carte, extra=None, decalage=0.5, visages=None, voile_bas=None,
             calque=False, basse_definition=False):
    """Compose la story. Renvoie {image, calque, voile, voile_calque, mesures, mesures_calque,
    info, ...}. Lève ValueError (ou PoliceIntrouvable) au lieu de livrer une image fautive."""
    verifier_textes(theme, carte)
    st = theme["story"]
    logo, secours = charger_logo(st)
    opts = {"logo": logo, "souligne": bool(st.get("registre_souligne")), "logo_couleur": couleur_logo(logo)}
    fond = cadrer(photo, decalage, basse_definition)
    base, col = couleurs(theme, opts)
    masq = masques(theme, carte, extra, opts)
    bande = controler_visages(masq, visages)
    g = st.get("grain", 0)
    bruit = Image.effect_noise((W, H), g).convert("RGB") if g else None

    img, a_haut, a_bas, mes, manque = _voiler(fond, col, masq, base["voile"], bruit, voile_bas)
    # registre allumé à 4,5:1 : si l'accent n'y arrive pas même sous le voile maximal (grain
    # compris), il passe en couleur de texte, souligné de 3 px dans la couleur d'accent
    if set(manque) == {"registre_actif"} and not opts["souligne"]:
        opts["souligne"] = True
        base, col = couleurs(theme, opts)
        masq = masques(theme, carte, extra, opts)
        bande = controler_visages(masq, visages)
        img, a_haut, a_bas, mes, manque = _voiler(fond, col, masq, base["voile"], bruit, voile_bas)
    if manque:
        raise ValueError(
            f"photo trop claire sous le texte au voile maximal (haut={a_haut:.2f}, bas={a_bas:.2f}) : "
            f"{manque}. Cibles : phrase {CIBLE_PHRASE}:1 ; nom, registre et pied {CIBLE_PETIT}:1 ; "
            f"kicker et accents {CIBLE_LARGE}:1. Décaler le recadrage ou choisir une autre photo.")
    info = habiller(img, theme, carte, extra, lambda e: col[e], opts)
    info.update(registre_souligne=opts["souligne"], bande_nette=bande,
                nom="logotype" if logo is not None else ("nom saisi (SECOURS)" if secours else "nom saisi"),
                polices=dict(police.__dict__.get("utilisees", {})))
    rendu = {"image": img, "voile": (round(a_haut, 2), round(a_bas, 2)), "mesures": mes, "info": info,
             "secours": secours, "masques": masq, "couleurs": col, "voile_rgb": base["voile"],
             "calque": None, "voile_calque": None, "mesures_calque": None}

    if calque:
        # voile du calque = palier calculé sur cette photo + 0,04. Contrôle sur la frame 0
        # (le recadrage sans texte, sans grain : la vidéo a le sien), voile seul sous l'encre.
        ch, cb = min(1.0, a_haut + MARGE_CALQUE), min(1.0, a_bas + MARGE_CALQUE)
        cq = Image.new("RGBA", (W, H), base["voile"] + (0,))
        cq.putalpha(voile(ch, cb))
        habiller(cq, theme, carte, extra, lambda e: col[e] + (255,), opts)
        rendu.update(calque=cq, voile_calque=(round(ch, 2), round(cb, 2)))
        rendu["mesures_calque"] = controler_images([fond], rendu)["frame 1"]["mesures"]
        if manques(rendu["mesures_calque"]):
            raise ValueError(f"calque sous les cibles sur la frame 0 : {manques(rendu['mesures_calque'])}")
    return rendu


def controler_images(frames, rendu):
    """Mesure des frames de la vidéo i2v AVANT pose du calque (sans texte) : chaque frame reçoit
    le voile du calque (ou celui de l'image fixe) et le contraste est relevé sous les masques.
    Les frames déjà habillées ne se mesurent pas ainsi : l'encre y masquerait le fond."""
    a_haut, a_bas = rendu["voile_calque"] or rendu["voile"]
    masque_voile = voile(a_haut, a_bas)
    aplat = Image.new("RGB", (W, H), rendu["voile_rgb"])
    bilan = {}
    for i, frame in enumerate(frames, 1):
        nom = str(frame) if not isinstance(frame, Image.Image) else f"frame {i}"
        im = (frame if isinstance(frame, Image.Image) else Image.open(frame)).convert("RGB")
        if im.size != (W, H):
            raise ValueError(f"{nom} : {im.size[0]}x{im.size[1]}, attendu {W}x{H}")
        mes = mesurer(Image.composite(aplat, im, masque_voile), rendu["couleurs"], rendu["masques"])
        bilan[nom] = {"mesures": mes, "manques": manques(mes)}
    return bilan


# ---------------------------------------------------------------- entrées

def _octets(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def charger_photo(valeur, theme):
    """(image, entrée du manifeste ou None). Une clé du manifeste se lit dans story.cache
    (originaux) et jamais dans fond.cache (fonds 4:5 préparés, voile déjà posé)."""
    if valeur.startswith(("http://", "https://")):
        return Image.open(BytesIO(_octets(valeur))), None
    if os.path.exists(valeur):
        return Image.open(valeur), None
    fonds = carrousel.charger_manifeste(theme) or {}
    if valeur not in fonds:
        raise ValueError(f"photo introuvable : « {valeur} » n'est ni un fichier, ni une URL, "
                         f"ni une clé de {theme.get('fond', {}).get('manifeste')}")
    p = fonds[valeur]
    st = theme["story"]
    if p.get("matiere") is False:
        raise ValueError(f"« {valeur} » est une carte déjà composée (matiere: false), jamais un fond")
    if p.get("personne_identifiable"):
        raise ValueError(f"« {valeur} » montre une personne identifiable générée : interdit sur tout compte")
    if p.get("provenance") == "ia" and not st.get("photos_ia_autorisees"):
        raise ValueError(f"« {valeur} » est une image IA : interdite sur ce compte, qui a de vraies photos")
    if not st.get("cache"):
        raise ValueError("clé story.cache absente du thème : une story ne part jamais d'un fond 4:5 préparé")
    fichier = ROOT / st["cache"] / (p["cle"] + ".jpg")
    if not fichier.exists():
        if not p.get("url_originale"):
            raise ValueError(f"« {valeur} » : aucun original (url_originale absente du manifeste, rien dans "
                             f"{st['cache']}/). Une story ne part jamais du fond 4:5 de {theme['fond']['cache']}.")
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_bytes(_octets(p["url_originale"]))
    return Image.open(fichier), p


def verifier_carrousel(spec, theme):
    """Refuse un carrousel dont le voile (encre et 150 px de rampe) couvre une boîte visage_45.

    carrousel.py n'est pas modifié : on lit la boîte de voile qu'il calcule en interceptant
    poser_voile, comme da/sweep-carrousel.py."""
    fonds = carrousel.charger_manifeste(theme) or {}
    slides, fautes = spec["slides"], []
    origine = carrousel.poser_voile
    for i, s in enumerate(slides, 1):
        p = fonds.get(s.get("photo"))
        if not p:
            continue
        if "visage_45" not in p:
            fautes.append(f"slide {i} : boîte visage_45 absente du manifeste pour « {p['cle']} » "
                          f"(liste vide si aucun visage)")
            continue
        vu = {}

        def espion(img, boite, alpha, v, vu=vu):
            vu["boite"] = boite
            return origine(img, boite, alpha, v)
        carrousel.poser_voile = espion
        try:
            carrousel.render_slide(s, theme, i, len(slides), spec.get("slug", "?"), fonds)
        finally:
            carrousel.poser_voile = origine
        y_voile = vu["boite"][1] - carrousel.RAMPE_VOILE
        fautes += [f"slide {i} : visage {b} sous le voile (qui commence à y={y_voile}, photo « {p['cle']} »)"
                   for b in _boites(p["visage_45"]) if b[3] > y_voile]
    if fautes:
        raise ValueError("carrousel refusé :\n  - " + "\n  - ".join(fautes))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Story sur vraie photo, DA par thème.")
    ap.add_argument("args", nargs="*", help="CLIENT SPEC CLE PHOTO SORTIE")
    ap.add_argument("--verifier-carrousel", metavar="SPEC")
    ap.add_argument("--decalage", type=float, default=None)
    ap.add_argument("--fond", help="écrit aussi le recadrage 9:16 sans texte (entrée i2v)")
    ap.add_argument("--calque", help="écrit aussi le calque PNG (voile calculé + 0,04)")
    ap.add_argument("--controle", nargs="+", default=[], help="frames i2v sans texte à mesurer sous le voile du calque")
    ap.add_argument("--visage", action="append", default=[], help="x0,y0,x1,y1 dans le cadre 1080x1920")
    ap.add_argument("--sans-visage", action="store_true")
    ap.add_argument("--voile-bas", type=float, default=None)
    ap.add_argument("--basse-definition", action="store_true")
    ap.add_argument("--themes", default=str(ROOT / "scripts" / "themes.json"))
    ap.add_argument("--polices", default=None, help="dossier de polices supplémentaire")
    a = ap.parse_args(argv)

    themes = json.loads(Path(a.themes).read_text(encoding="utf-8"))
    if a.verifier_carrousel:
        spec = json.loads(Path(a.verifier_carrousel).read_text(encoding="utf-8"))
        verifier_carrousel(spec, themes[spec["client"]])
        print(f"{a.verifier_carrousel} : aucun visage sous le voile")
        return 0
    if len(a.args) != 5:
        ap.error("arguments attendus : CLIENT SPEC CLE PHOTO SORTIE")
    client, spec_path, cle, photo_arg, sortie = a.args
    theme = themes[client]
    if "fond" not in theme or "story" not in theme:
        raise SystemExit(f"{client} : blocs fond et story requis dans themes.json")
    cartes = {c["cle"]: c for c in json.loads(Path(spec_path).read_text(encoding="utf-8"))["cartes"]}
    if cle not in cartes:
        raise SystemExit(f"carte « {cle} » absente de {spec_path} ({', '.join(cartes)})")
    if photo_arg == "-":
        raise SystemExit("le calque se calcule sur la photo : passer la photo et --calque SORTIE.png")

    photo, entree = charger_photo(photo_arg, theme)
    if entree is not None:
        if "visage_916" not in entree:
            raise SystemExit(f"« {photo_arg} » : boîte visage_916 absente du manifeste (liste vide si aucun visage)")
        visages = entree["visage_916"]
        attendu = float(entree.get("decalage_916", 0.5))
        if a.decalage is not None and abs(a.decalage - attendu) > 1e-6:
            raise SystemExit(f"--decalage {a.decalage} : les boîtes visage_916 ont été relevées pour "
                             f"{attendu} ; relever les boîtes pour ce recadrage d'abord")
        decalage = attendu
    else:
        visages = [] if a.sans_visage else ([[float(v) for v in b.split(",")] for b in a.visage] or None)
        decalage = 0.5 if a.decalage is None else a.decalage
    try:
        rendu = composer(photo, theme, cartes[cle], a.polices, decalage, visages, a.voile_bas,
                         calque=bool(a.calque), basse_definition=a.basse_definition)
    except (ValueError, PoliceIntrouvable) as exc:
        raise SystemExit(f"✗ {client} {cle} : {exc}")
    if a.fond:
        cadrer(photo, decalage, a.basse_definition).save(a.fond, quality=95, subsampling=0)
        print(f"{a.fond} : recadrage 9:16 sans texte (entrée i2v)")
    rendu["image"].save(sortie, quality=92, subsampling=0)
    print(f"{sortie} : voile (haut, bas) = {rendu['voile']}")
    print("  contrastes : " + ", ".join(f"{e} {v}:1 (cible {c})" for e, (v, c) in rendu["mesures"].items()))
    info = {k: v for k, v in rendu["info"].items() if k != "polices"}
    print("  " + json.dumps(info, ensure_ascii=False))
    print("  polices : " + json.dumps(rendu["info"]["polices"], ensure_ascii=False))
    if rendu["secours"]:
        print("  " + rendu["secours"])
    if a.calque:
        rendu["calque"].save(a.calque)
        print(f"{a.calque} : calque, voile {rendu['voile_calque']}")
    if a.controle:
        bilan = controler_images(a.controle, rendu)
        for chemin, r in bilan.items():
            print(f"  contrôle {chemin} : {'OK' if not r['manques'] else 'SOUS LES CIBLES ' + str(r['manques'])}")
        if any(r["manques"] for r in bilan.values()):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

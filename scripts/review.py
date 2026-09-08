#!/usr/bin/env python3
"""La review hebdo client : un fichier Excel par compte, en aller-retour avec Metricool.

    python3 scripts/review.py generer   [--semaine 2026-08-10] [--client le-loft] [--dry-run]
    python3 scripts/review.py appliquer [--client le-loft] [--dry-run]

Le circuit complet est décrit dans .claude/skills/cm-metricool/references/review-hebdo.md.
En résumé : `generer` lit les brouillons de la semaine dans Metricool et écrit un fichier
Excel par client dans reviews/a-envoyer/ ; la session Claude du lundi le dépose dans le
Drive du client (converti en Google Sheet) et note son identifiant dans reviews/config.json ;
le client coche ✅ / ✏️ / ⛔ ligne par ligne, corrige les légendes ; `appliquer`, plusieurs
fois par jour, relit le fichier par son export public, pousse les modifications dans
Metricool et passe les lignes ✅ en publication automatique.

Même partage des rôles que le reste du dépôt : ce script tourne dans GitHub Actions — la
politique réseau des sessions Claude bloque app.metricool.com et les exports Drive — et la
session fait la moitié authentifiée (dépôt du fichier, récap). Aucune clé Google, comme
drive_sync.py : la lecture des retours passe par l'export public du fichier partagé.

Garde-fous, dans l'ordre où ils ont été décidés :
  - jamais de suppression automatique : un ⛔ reste en brouillon, Maxime tranche ;
  - un post déjà validé dans Metricool (autoPublish) n'est JAMAIS retouché ;
  - un ✅ sur un texte à placeholders ([VAINQUEUR]…) ou sans média est bloqué et signalé,
    pas publié — publier un trou de texte fait plus de dégâts qu'un retard ;
  - idempotence par reviews/etat/<client>.json : une décision déjà appliquée à l'identique
    n'est pas rejouée, une décision changée est rejouée.

Secrets attendus : METRICOOL_USER_ID, METRICOOL_TOKEN. Dépendance : openpyxl.
"""

import argparse
import hashlib
import io
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publier import metricool  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "reviews"
A_ENVOYER = REVIEWS / "a-envoyer"
RETOURS = REVIEWS / "retours"
ETAT = REVIEWS / "etat"

# Les trois décisions offertes au client. Le vide est la quatrième : « pas encore décidé »,
# et un post sans décision ne part jamais.
DECISION_OK = "✅ OK pour publier"
DECISION_CORRIGER = "✏️ À corriger (voir commentaire)"
DECISION_NON = "⛔ Ne pas publier"

# La case « j'ai fini », en haut du tableau. Le client la bascule quand il a terminé sa
# relecture : c'est CE basculement qui prévient Maxime qu'il peut reprendre la main. Elle
# ne conditionne rien — les décisions déjà posées sont appliquées au fil de l'eau, la case
# dit « j'ai fini de relire », pas « vous pouvez commencer à lire ».
FINI_NON = "🕐 Je n'ai pas fini"
FINI_OUI = "✅ J'ai terminé mes retours"
FINI_ETIQUETTE = "Quand vous avez tout relu, dites-le nous ici →"
FINI_CELLULE = "H1"

JOURS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
RESEAUX = {"instagram": "IG", "facebook": "FB", "tiktok": "TikTok", "linkedin": "LinkedIn",
           "youtube": "YT", "twitter": "X", "pinterest": "Pinterest", "threads": "Threads",
           "gmb": "GMB"}
PLACEHOLDER = re.compile(r"\[[A-ZÀ-Ü0-9][A-ZÀ-Ü0-9 +/'-]*\]")


# ---------------------------------------------------------------- lecture Metricool

def semaine_lundi(texte=None):
    """Le lundi de la semaine visée. Sans argument : la semaine en cours."""
    if texte:
        d = date.fromisoformat(texte)
        if d.weekday() != 0:
            d -= timedelta(days=d.weekday())
            print(f"(la date donnée n'est pas un lundi — semaine du {d} retenue)")
        return d
    aujourd_hui = date.today()
    return aujourd_hui - timedelta(days=aujourd_hui.weekday())


def posts_semaine(blog_id, lundi):
    dimanche = lundi + timedelta(days=6)
    posts = metricool("/scheduler/posts", blogId=blog_id,
                      start=f"{lundi}T00:00:00", end=f"{dimanche}T23:59:59").get("data", [])
    return sorted(posts, key=lambda p: p.get("publicationDate", {}).get("dateTime", ""))


def type_du(post):
    """Le format lisible par le client. La donnée vit dans instagramData/facebookData/…"""
    if len(post.get("media") or []) > 1:
        return f"Carrousel ({len(post['media'])} visuels)"
    for cle, val in post.items():
        if cle.endswith("Data") and isinstance(val, dict) and val.get("type"):
            return {"POST": "Post", "REEL": "Reel", "STORY": "Story"}.get(val["type"], val["type"].title())
    return "Post"


def reseaux_du(post):
    abbr = [RESEAUX.get(pr.get("network"), pr.get("network", "?")) for pr in post.get("providers", [])]
    return " + ".join(abbr) or "?"


# ---------------------------------------------------------------- écriture du fichier

ENTETES = ["Réf", "Jour", "Heure", "Format", "Réseaux", "Visuel",
           "Légende", "Votre décision", "Votre commentaire"]
# Colonnes que le client édite. Tout le reste est verrouillé — le verrou tient dans Excel,
# Google Sheets l'ignore : c'est un garde-fou contre la fausse manœuvre, pas une serrure.
EDITABLES = {"C", "G", "H", "I"}
LARGEURS = {"A": 9, "B": 11, "C": 9, "D": 12, "E": 13, "F": 15, "G": 78, "H": 27, "I": 34}

NOIR = "FF111827"
GRIS_FOND = "FFF5F6F8"
JAUNE_EDIT = "FFFFF7DB"
VERT_OK = "FFE3F4E8"
ORANGE_CORRIGER = "FFFDEBD3"
ROUGE_NON = "FFFADBD8"
BORD = Border(*[Side(style="thin", color="FFD9DDE3")] * 4)


def _mode_demploi(wb, compte, lundi):
    ws = wb.active
    ws.title = "Mode d'emploi"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 100
    lignes = [
        (f"Vos publications — semaine du {lundi:%d/%m} au {lundi + timedelta(days=6):%d/%m}", "titre"),
        (compte["nom"], "sous-titre"),
        ("", None),
        ("Trois minutes suffisent :", "gras"),
        ("1.  Ouvrez l'onglet « Semaine du … » : chaque ligne est une publication prévue.", None),
        ("2.  Les colonnes JAUNES sont à vous : corrigez la légende directement dans la case,", None),
        ("     ajustez l'heure si besoin, et laissez-nous un commentaire si utile.", None),
        ("3.  Choisissez votre décision dans le menu de la colonne « Votre décision » :", None),
        (f"      {DECISION_OK} — la publication part automatiquement, plus rien à faire.", None),
        (f"      {DECISION_CORRIGER} — on la retravaille avec votre commentaire et on vous la représente.", None),
        (f"      {DECISION_NON} — elle est retirée de la semaine.", None),
        ("", None),
        (f"4.  Quand vous avez tout relu, basculez la case en haut du tableau sur", "gras"),
        (f"      « {FINI_OUI} ». C'est elle qui nous prévient.", "gras"),
        ("", None),
        ("Vos décisions sont relevées plusieurs fois par jour et prises en compte sous quelques", None),
        ("heures. Une ligne laissée sans décision reste en attente : elle ne sera pas publiée.", None),
        ("Les lignes « ⚠️ visuel à venir » reçoivent leur photo/vidéo avant publication.", None),
        ("Pas besoin d'attendre d'avoir fini pour valider : chaque décision part de son côté.", None),
        ("", None),
        ("Merci de ne pas toucher aux colonnes grises ni à la colonne Réf : elles servent au suivi.", "petit"),
    ]
    for i, (texte, style) in enumerate(lignes, start=2):
        cellule = ws.cell(row=i, column=2, value=texte)
        if style == "titre":
            cellule.font = Font(bold=True, size=16, color=NOIR)
        elif style == "sous-titre":
            cellule.font = Font(bold=True, size=12, color="FF6B7280")
        elif style == "gras":
            cellule.font = Font(bold=True)
        elif style == "petit":
            cellule.font = Font(size=9, color="FF6B7280", italic=True)
    ws.protection.sheet = True
    return ws


# Bornes de hauteur de ligne. Elles ne sont pas décoratives.
# Le PLANCHER : une story porte un simple libellé d'une ligne (« Story lundi —
# Nouvelle semaine »). Sans plancher sa ligne tombait à 21 points, une lamelle
# coincée entre deux pavés de 210, et le tableau prenait l'air cassé. C'est le
# reproche de Maxime du 02/09 : « la présentation n'est pas jolie ». Mesuré sur
# la semaine du 31/08 : cinq fichiers sur six avaient un écart de 189 points
# entre leur plus petite et leur plus grande ligne ; le seul qui passait pour
# beau, Otea Filmakers, avait un écart de 15.
# Le PLAFOND : au-delà, une seule légende mange l'écran et le client perd la
# vue d'ensemble de sa semaine.
HAUTEUR_MIN = 42
HAUTEUR_MAX = 150
# Caractères tenant sur une ligne de la colonne Légende. Dérivé de sa largeur,
# et non écrit en dur : une valeur figée à 58 pendant que la colonne passait à
# 78 aurait remis le tableau de travers sans que personne ne le voie.
CARS_PAR_LIGNE = LARGEURS["G"] - 4


def _hauteur(texte):
    """Une hauteur de ligne qui laisse la légende lisible sans dérouler."""
    lignes = sum(max(1, len(l) // CARS_PAR_LIGNE + 1)
                 for l in (texte or "").splitlines()) or 1
    return max(HAUTEUR_MIN, min(15 * lignes + 6, HAUTEUR_MAX))


def ecrire_fichier(compte, lundi, brouillons, chemin):
    wb = openpyxl.Workbook()
    _mode_demploi(wb, compte, lundi)

    ws = wb.create_sheet(f"Semaine du {lundi:%d-%m}")
    ws.freeze_panes = "A3"
    for col, largeur in LARGEURS.items():
        ws.column_dimensions[col].width = largeur

    # Ligne 1 : la case « j'ai fini ». Au-dessus de l'entête pour être vue en premier et
    # rester visible au défilement (les deux premières lignes sont figées).
    ws.merge_cells("A1:G1")
    etiquette = ws.cell(row=1, column=1, value=FINI_ETIQUETTE)
    etiquette.font = Font(bold=True, color=NOIR)
    etiquette.alignment = Alignment(vertical="center", horizontal="right")
    case = ws.cell(row=1, column=8, value=FINI_NON)
    case.fill = PatternFill("solid", fgColor=JAUNE_EDIT)
    case.font = Font(bold=True)
    case.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
    case.border = BORD
    case.protection = Protection(locked=False)
    ws.row_dimensions[1].height = 30

    for c, entete in enumerate(ENTETES, start=1):
        cellule = ws.cell(row=2, column=c, value=entete)
        cellule.font = Font(bold=True, color="FFFFFFFF")
        cellule.fill = PatternFill("solid", fgColor=NOIR)
        cellule.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[2].height = 22

    tech = wb.create_sheet("_tech")
    tech["A1"], tech["B1"] = "client", compte["slug"]
    tech["A2"], tech["B2"] = "semaine", lundi.isoformat()
    tech["A3"], tech["B3"] = "genere", datetime.now().isoformat(timespec="seconds")
    # L'adresse de la case « j'ai fini » voyage avec le fichier : la relève la lit ici
    # plutôt que de la supposer, et un fichier d'une autre version reste lisible.
    tech["A4"], tech["B4"] = "case_fini", FINI_CELLULE
    for c, entete in enumerate(["ref", "post_id", "blog_id", "date_time", "texte_original"], start=1):
        tech.cell(row=5, column=c, value=entete)

    for i, post in enumerate(brouillons, start=1):
        r = i + 2
        dt = datetime.fromisoformat(post["publicationDate"]["dateTime"])
        ref = f"{compte['prefixe']}-{i:02d}"
        media = post.get("media") or []
        valeurs = [ref, f"{JOURS[dt.weekday()]} {dt:%d/%m}", f"{dt:%H:%M}", type_du(post),
                   reseaux_du(post), "", post.get("text", ""), "", ""]
        for c, valeur in enumerate(valeurs, start=1):
            cellule = ws.cell(row=r, column=c, value=valeur)
            colonne = cellule.column_letter
            cellule.border = BORD
            cellule.alignment = Alignment(vertical="top",
                                          wrap_text=colonne in ("G", "I"),
                                          horizontal="center" if colonne in "ABCDEF" else "left")
            if colonne in EDITABLES:
                cellule.fill = PatternFill("solid", fgColor=JAUNE_EDIT)
                cellule.protection = Protection(locked=False)
            else:
                cellule.fill = PatternFill("solid", fgColor=GRIS_FOND)
        visuel = ws.cell(row=r, column=6)
        if media:
            visuel.value = "voir le visuel"
            visuel.hyperlink = media[0]
            visuel.font = Font(color="FF1155CC", underline="single")
        else:
            visuel.value = "⚠️ visuel à venir"
        ws.row_dimensions[r].height = _hauteur(post.get("text", ""))

        for c, valeur in enumerate([ref, post.get("id"), compte["blog_id"],
                                    post["publicationDate"]["dateTime"], post.get("text", "")], start=1):
            tech.cell(row=5 + i, column=c, value=valeur)

    fin = len(brouillons) + 2
    decisions = DataValidation(
        type="list", formula1=f'"{DECISION_OK},{DECISION_CORRIGER},{DECISION_NON}"',
        allow_blank=True, showErrorMessage=True, errorTitle="Choisir dans la liste",
        error="Choisissez une des trois décisions du menu, ou laissez la case vide.")
    ws.add_data_validation(decisions)
    decisions.add(f"H3:H{fin}")
    for fond, decision in ((VERT_OK, DECISION_OK), (ORANGE_CORRIGER, DECISION_CORRIGER),
                           (ROUGE_NON, DECISION_NON)):
        ws.conditional_formatting.add(
            f"A3:I{fin}",
            FormulaRule(formula=[f'$H3="{decision}"'],
                        fill=PatternFill("solid", bgColor=fond), stopIfTrue=True))

    fini = DataValidation(
        type="list", formula1=f'"{FINI_NON},{FINI_OUI}"', allow_blank=True,
        showErrorMessage=True, errorTitle="Choisir dans la liste",
        error="Deux choix : pas encore fini, ou terminé.")
    ws.add_data_validation(fini)
    fini.add(FINI_CELLULE)
    ws.conditional_formatting.add(
        FINI_CELLULE,
        FormulaRule(formula=[f'${FINI_CELLULE[0]}${FINI_CELLULE[1:]}="{FINI_OUI}"'],
                    fill=PatternFill("solid", bgColor=VERT_OK)))

    ws.protection.sheet = True
    tech.sheet_state = "hidden"
    tech.protection.sheet = True

    chemin.parent.mkdir(parents=True, exist_ok=True)
    wb.save(chemin)


def generer_compte(compte, lundi, dry_run=False):
    """Écrit le fichier de review d'un compte. Retourne le nombre de brouillons couverts."""
    posts = posts_semaine(compte["blog_id"], lundi)
    brouillons = [p for p in posts if p.get("draft")]
    if not brouillons:
        print(f"= {compte['slug']} : aucun brouillon du {lundi} au {lundi + timedelta(days=6)} — pas de fichier")
        return 0

    a_completer = [p for p in brouillons if PLACEHOLDER.search(p.get("text", ""))]
    sans_media = [p for p in brouillons if not p.get("media")]
    if dry_run:
        print(f"[dry-run] {compte['slug']} : {len(brouillons)} brouillon(s), "
              f"{len(a_completer)} placeholder(s), {len(sans_media)} sans média")
        for p in brouillons:
            print(f"           └ {p['publicationDate']['dateTime']} {type_du(p)} : {p.get('text', '')[:60]}…")
        return len(brouillons)

    chemin = A_ENVOYER / f"{compte['slug']}-{lundi}.xlsx"
    ecrire_fichier(compte, lundi, brouillons, chemin)
    print(f"✓ {compte['slug']} : {len(brouillons)} brouillon(s) → {chemin.relative_to(ROOT)}")
    if a_completer:
        print(f"  ⚠ {len(a_completer)} texte(s) à placeholders — à compléter AVANT que le client valide")
    if sans_media:
        print(f"  ⚠ {len(sans_media)} post(s) sans média — un ✅ restera bloqué tant que le visuel manque")
    return len(brouillons)


# ---------------------------------------------------------------- lecture des retours

def telecharger_review(drive_id):
    """L'export public du fichier de review, sans identifiant Google.

    Deux formes possibles selon ce que le connecteur a créé au dépôt : un Google Sheet
    (conversion par défaut) s'exporte en xlsx via docs.google.com, un .xlsx resté brut se
    télécharge par le lien direct. On tente dans cet ordre. Un xlsx est un zip : la
    signature PK distingue un vrai fichier d'une page HTML « demande d'accès ».
    """
    urls = [f"https://docs.google.com/spreadsheets/d/{drive_id}/export?format=xlsx",
            f"https://drive.google.com/uc?export=download&id={drive_id}"]
    for url in urls:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                octets = r.read()
        except urllib.error.HTTPError:
            continue
        if octets[:2] == b"PK":
            return octets
    raise RuntimeError("export impossible — le fichier n'est probablement plus partagé "
                       "« tous les utilisateurs disposant du lien »")


def _iso(valeur):
    """Une date de _tech telle qu'écrite. La conversion en Google Sheet retype parfois nos
    chaînes ISO en vraies dates : au retour, on re-normalise plutôt que de planter."""
    if isinstance(valeur, datetime):
        return valeur.strftime("%Y-%m-%dT%H:%M:%S")
    return str(valeur)


def lire_review(source):
    """Extrait (meta, lignes) d'un fichier de review, quel que soit son canal de retour."""
    contenu = io.BytesIO(source) if isinstance(source, bytes) else source
    wb = openpyxl.load_workbook(contenu, data_only=True)
    if "_tech" not in wb.sheetnames:
        raise RuntimeError("onglet _tech absent — ce fichier n'a pas été généré par review.py")
    tech = wb["_tech"]
    meta = {"client": tech["B1"].value, "semaine": _iso(tech["B2"].value)[:10]}
    originaux = {}
    for ligne in tech.iter_rows(min_row=6, max_col=5, values_only=True):
        if ligne[0]:
            originaux[str(ligne[0])] = {"post_id": ligne[1], "blog_id": ligne[2],
                                        "date_time": _iso(ligne[3]), "texte": ligne[4] or ""}
    feuille = next((ws for ws in wb.worksheets if ws.title.startswith("Semaine")), None)
    if feuille is None:
        raise RuntimeError("onglet « Semaine du … » introuvable")

    # L'entête n'est plus forcément en ligne 1 : depuis la case « j'ai fini » elle est en
    # ligne 2. On la cherche au lieu de la supposer, ce qui garde lisibles les fichiers
    # déjà entre les mains des clients.
    ligne_entete = next((r for r in range(1, 6)
                         if str(feuille.cell(row=r, column=1).value or "").strip() == ENTETES[0]), 1)

    # La case « j'ai fini », à l'adresse que le fichier déclare lui-même. Absente des
    # fichiers d'avant : meta["fini"] vaut alors None, et la veille ne signale rien.
    meta["fini"] = None
    if str(tech["A4"].value or "").strip() == "case_fini" and tech["B4"].value:
        meta["fini"] = feuille[str(tech["B4"].value).strip()].value

    lignes = []
    for valeurs in feuille.iter_rows(min_row=ligne_entete + 1, max_col=9, values_only=True):
        ref = str(valeurs[0]).strip() if valeurs[0] else None
        if not ref:
            continue
        lignes.append({"ref": ref, "heure": valeurs[2], "legende": valeurs[6],
                       "decision": valeurs[7], "commentaire": valeurs[8],
                       "original": originaux.get(ref)})
    return meta, lignes


def normaliser_texte(texte):
    return "\n".join(l.rstrip() for l in str(texte or "").replace("\r\n", "\n").split("\n")).strip()


def normaliser_heure(cellule):
    """« 18:00 », 18h, 18 h 30, « 18 » nu, une heure Excel ou un sériel Sheets → « HH:MM ».

    Une heure illisible ou impossible (25h…) vaut None = « heure inchangée » : on garde le
    créneau d'origine plutôt que d'inventer, l'écart se voit dans le fichier au pire.
    """
    if cellule is None or str(cellule).strip() == "":
        return None
    if isinstance(cellule, datetime):
        return cellule.strftime("%H:%M")
    if isinstance(cellule, dtime):
        return cellule.strftime("%H:%M")
    if isinstance(cellule, (int, float)) and not isinstance(cellule, bool):
        valeur = float(cellule)
        if 0 <= valeur < 1:  # sériel : fraction de jour
            minutes = round(valeur * 24 * 60)
            return f"{minutes // 60:02d}:{minutes % 60:02d}"
        if valeur.is_integer() and 0 <= valeur < 24:  # « 18 » tapé nu, devenu nombre
            return f"{int(valeur):02d}:00"
        return None
    texte = str(cellule)
    m = re.search(r"(\d{1,2})\s*[hH:.]\s*(\d{1,2})?", texte)
    if not m:
        m = re.fullmatch(r"\s*(\d{1,2})\s*", texte)
        if m and int(m.group(1)) < 24:
            return f"{int(m.group(1)):02d}:00"
        return None
    heures, minutes = int(m.group(1)), int(m.group(2) or 0)
    if heures > 23 or minutes > 59:
        return None
    return f"{heures:02d}:{minutes:02d}"


def lire_decision(cellule):
    """Décision d'une ligne, tolérante aux clients qui tapent au lieu de choisir dans le menu.

    L'ordre des tests compte : « ne pas publier » contient « publier », le refus se teste
    donc avant l'accord. Tout ce qui n'est pas reconnu devient INCONNU : signalé à Maxime,
    jamais interprété — on ne publie pas sur une devinette.
    """
    if cellule is None or str(cellule).strip() == "":
        return None
    brut = str(cellule)
    plat = unicodedata.normalize("NFKD", brut.strip().lower())
    plat = "".join(c for c in plat if not unicodedata.combining(c))
    if "⛔" in brut or "pas publier" in plat or plat in {"non", "refuse", "no", "stop"}:
        return "NON"
    if "✅" in brut or "ok" in plat or "valid" in plat or "publier" in plat or plat in {"oui", "go", "yes"}:
        return "OK"
    if "✏" in brut or "corrig" in plat or "modif" in plat or "revoir" in plat or "retravail" in plat:
        return "CORRIGER"
    return "INCONNU"


# ---------------------------------------------------------------- application Metricool

def corps_de(post, texte, date_time, publier_auto):
    """Le corps d'écriture d'un post, à partir de sa version lue dans Metricool.

    Même socle que publier.py (text, publicationDate, draft, autoPublish, media, providers)
    plus les blocs *Data : c'est là que vit le type POST/REEL/STORY, le perdre transforme
    un reel en post feed.
    """
    corps = {
        "text": texte,
        "publicationDate": {"dateTime": date_time,
                            "timezone": post.get("publicationDate", {}).get("timezone", "Europe/Paris")},
        "draft": not publier_auto,
        "autoPublish": publier_auto,
        "media": post.get("media") or [],
        "providers": [{"network": pr["network"]} for pr in post.get("providers", []) if pr.get("network")],
    }
    for cle, valeur in post.items():
        if cle.endswith("Data") and isinstance(valeur, dict):
            corps[cle] = valeur
    if post.get("firstCommentText"):
        corps["firstCommentText"] = post["firstCommentText"]
    return corps


def passer_en_publication(blog_id, post, texte, date_time):
    """Applique texte/horaire et sort le post du brouillon. Retourne (résultat, post_id).

    ⚠️ Constaté au premier test réel (post 355355797 → 359735766, OTEA, 08/08/2026) : le
    PUT de l'API ne modifie PAS l'entrée existante — il crée une NOUVELLE entrée de
    planning (nouvel id, même uuid) avec les nouvelles valeurs, et laisse l'ancien
    brouillon en place. D'où la marche en trois temps, chacun vérifié sur l'état réel :

      1. la version publiable existe-t-elle déjà ? (un run précédent a pu la poser sans
         finir son ménage) — si oui, ne PAS ré-écrire : un second PUT publierait en double ;
      2. sinon PUT, puis relire le jour pour trouver la version réellement en place ;
      3. ménage : retirer l'ancien id s'il est resté en brouillon, et les éventuels
         doublons publiables identiques. Seul cas de suppression automatique du système,
         strictement borné : l'entrée périmée d'un post que le client vient de valider —
         sans ce ménage, la review suivante re-proposerait un post déjà validé.

    Si l'API refuse le PUT : suppression puis recréation. L'ordre (inverse de publier.py)
    est voulu : ici le post recréé part en publication automatique, un doublon publierait
    DEUX fois chez le client. Mieux vaut un trou signalé qu'un doublon publié.
    """
    ancien_id = post["id"]
    jour = date_time[:10]

    def etat_du_jour():
        posts_jour = metricool("/scheduler/posts", blogId=blog_id,
                               start=f"{jour}T00:00:00", end=f"{jour}T23:59:59").get("data", [])
        publiables = [p for p in posts_jour
                      if p.get("autoPublish") and not p.get("draft")
                      and p.get("publicationDate", {}).get("dateTime") == date_time
                      and normaliser_texte(p.get("text")) == normaliser_texte(texte)]
        reste = any(p.get("id") == ancien_id and p.get("draft") for p in posts_jour)
        return publiables, reste

    publiables, reste = etat_du_jour()
    if not publiables:
        try:
            metricool(f"/scheduler/posts/{ancien_id}", "PUT",
                      corps_de(post, texte, date_time, True), blogId=blog_id)
        except RuntimeError as exc:
            print(f"    (mise à jour refusée — {exc} — suppression puis recréation)")
            metricool(f"/scheduler/posts/{ancien_id}", "DELETE", blogId=blog_id)
            cree = metricool("/scheduler/posts", "POST",
                             corps_de(post, texte, date_time, True), blogId=blog_id)
            nouveau = cree.get("data", {}).get("id")
            return f"publication programmée (recréé, nouvel id {nouveau})", nouveau
        publiables, reste = etat_du_jour()
    if not publiables:
        raise RuntimeError(f"aucune version publiable en place après la mise à jour du "
                           f"post {ancien_id} — vérifier dans Metricool")

    version = publiables[0]
    for doublon in publiables[1:]:
        metricool(f"/scheduler/posts/{doublon['id']}", "DELETE", blogId=blog_id)
    if reste and version["id"] != ancien_id:
        metricool(f"/scheduler/posts/{ancien_id}", "DELETE", blogId=blog_id)
        return (f"publication programmée (version {version['id']}, ancien brouillon "
                f"{ancien_id} retiré)"), version["id"]
    return f"publication programmée (version {version['id']})", version["id"]


def retrouver_post(posts, original):
    """Le brouillon visé, par id d'abord, par créneau horaire sinon.

    Le repêchage par horaire n'est pas un luxe : les ids changent quand un brouillon est
    recréé (correction d'horaire, --remplacer de publier.py). Même clé que
    carrousels_existants : le créneau, pas le texte.
    """
    for p in posts:
        if p.get("id") == original["post_id"]:
            return p
    candidats = [p for p in posts
                 if p.get("publicationDate", {}).get("dateTime") == original["date_time"]
                 and p.get("draft")]
    return candidats[0] if len(candidats) == 1 else None


def charger_etat(slug):
    chemin = ETAT / f"{slug}.json"
    if chemin.exists():
        return json.loads(chemin.read_text(encoding="utf-8"))
    return {"_doc": "Journal des décisions client appliquées par scripts/review.py — écrit par "
                    "le workflow « Review hebdo client », ne pas éditer à la main. Sert "
                    "d'idempotence (une décision déjà appliquée à l'identique n'est pas rejouée) "
                    "et de matière au récap du lundi. Le bloc « veille » mémorise, par semaine, "
                    "l'état de la relecture du client (signature, nombre de décisions, case "
                    "« j'ai fini ») : c'est lui qui permet de dire ce qui a bougé depuis la "
                    "relève précédente sans re-signaler deux fois la même chose.",
            "semaines": {}, "veille": {}}


def signature_relecture(lignes):
    """Ce que le client a écrit, tout compris : décisions, commentaires, légendes.

    Sert à répondre à une seule question — « a-t-il touché au tableau depuis la dernière
    relève ? » — sans dépendre du journal des décisions, qui lui n'enregistre que les
    lignes actionnables. Une légende corrigée sans décision compte comme un retour.
    """
    brut = "\n".join(
        f"{l['ref']}|{normaliser_texte(l['decision'])}"
        f"|{normaliser_texte(l['commentaire'])}|{normaliser_texte(l['legende'])}"
        for l in lignes)
    return hashlib.sha256(brut.encode()).hexdigest()[:16]


def veiller(compte, meta, lignes, etat, evenements):
    """Compare la relecture du client à ce qu'on en savait, et note ce qui a bougé.

    Trois signaux, du plus faible au plus fort : il a commencé, il a continué, il a
    terminé. Le dernier est celui qui compte — c'est la main qui repasse à Maxime.
    """
    semaine = str(meta["semaine"])
    veille = etat.setdefault("veille", {})
    avant = veille.get(semaine, {})
    signature = signature_relecture(lignes)
    posees = sum(1 for l in lignes if str(l["decision"] or "").strip())
    fini = str(meta.get("fini") or "").strip() == FINI_OUI
    lien = (f"https://docs.google.com/spreadsheets/d/{compte['drive_fichier']}/edit"
            if compte.get("drive_fichier") else None)

    def signaler(type_, titre, detail):
        evenements.append({
            "quand": datetime.now().isoformat(timespec="seconds"),
            "client": compte["slug"], "nom": compte["nom"], "semaine": semaine,
            "type": type_, "titre": titre, "detail": detail, "lien": lien})

    if fini and not avant.get("fini"):
        signaler("termine",
                 f"{compte['nom']} a terminé ses retours — semaine du {semaine}",
                 f"{posees} ligne(s) sur {len(lignes)} décidées. À toi de jouer : "
                 f"les ✏️ sont à retravailler, les ⛔ à retirer du calendrier.")
    elif signature != avant.get("signature"):
        if not avant.get("signature") or avant.get("posees", 0) == 0:
            signaler("premiers_retours",
                     f"{compte['nom']} a commencé à répondre — semaine du {semaine}",
                     f"{posees} ligne(s) sur {len(lignes)} décidées pour l'instant.")
        else:
            avance = posees - avant.get("posees", 0)
            signaler("nouveaux_retours",
                     f"{compte['nom']} a modifié ses retours — semaine du {semaine}",
                     (f"{avance:+d} décision(s) depuis le dernier passage, "
                      f"{posees} sur {len(lignes)} au total."
                      if avance else
                      f"Une légende ou un commentaire a changé. Toujours {posees} "
                      f"décision(s) sur {len(lignes)}."))

    veille[semaine] = {"signature": signature, "posees": posees, "lignes": len(lignes),
                       "fini": fini, "vu": datetime.now().isoformat(timespec="seconds")}
    return signature != avant.get("signature") or fini != bool(avant.get("fini"))


def empiler_notifications(evenements):
    """Dépose les signaux dans une file que scripts/notifier.py vide ensuite.

    Deux étages volontairement séparés : la relève sait ce qui a bougé (elle a le fichier
    sous les yeux), l'envoi sait comment joindre Maxime (il a les secrets). Si l'envoi
    tombe, rien n'est perdu — la file attend le passage suivant.
    """
    chemin = ETAT / "notifications.json"
    file = {"_doc": "File des signaux de veille de la review client — écrite par "
                    "scripts/review.py, vidée par scripts/notifier.py. « en_attente » = pas "
                    "encore notifié, « envoyes » = les 50 derniers, pour ne pas re-signaler.",
            "en_attente": [], "envoyes": [], "fils": {}}
    if chemin.exists():
        file.update(json.loads(chemin.read_text(encoding="utf-8")))
    file["en_attente"].extend(evenements)
    ETAT.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(file, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def empreinte(decision, legende, heure):
    brut = f"{decision}|{normaliser_texte(legende)}|{heure or ''}"
    return hashlib.sha256(brut.encode()).hexdigest()[:16]


def appliquer_compte(compte, dry_run=False, evenements=None):
    """Traite toutes les sources de retour d'un compte. Retourne les compteurs."""
    slug = compte["slug"]
    sources = []
    if compte.get("drive_fichier"):
        try:
            sources.append(("Drive", telecharger_review(compte["drive_fichier"])))
        except Exception as exc:
            print(f"✗ {slug} : export Drive impossible — {exc}", file=sys.stderr)
            return {"erreurs": 1}
    for chemin in sorted(RETOURS.glob(f"{slug}*.xlsx")):
        sources.append((chemin.name, chemin))
    if not sources:
        print(f"= {slug} : aucun fichier de review à lire (drive_fichier vide, aucun retour déposé)")
        return {}

    etat = charger_etat(slug)
    compteurs = {"publies": 0, "a_corriger": 0, "refuses": 0, "erreurs": 0,
                 "sans_decision": 0, "en_attente": 0}
    posts_cache = {}
    touches = False

    for nom_source, source in sources:
        try:
            meta, lignes = lire_review(source)
        except Exception as exc:
            print(f"✗ {slug} : {nom_source} illisible — {exc}", file=sys.stderr)
            compteurs["erreurs"] += 1
            continue
        if meta["client"] != slug:
            print(f"! {slug} : {nom_source} appartient à « {meta['client']} », ignoré")
            continue
        semaine = str(meta["semaine"])
        journal = etat["semaines"].setdefault(semaine, {})
        print(f"{compte['nom']} — semaine du {semaine} (source : {nom_source})")

        # La veille tourne avant l'application : même si aucune décision n'est actionnable,
        # un tableau touché doit se voir. Un retour Drive fait foi ; un fichier revenu par
        # mail est un doublon de la même semaine et ne redéclenche pas de signal.
        if evenements is not None and nom_source == "Drive" and not dry_run:
            if veiller(compte, meta, lignes, etat, evenements):
                touches = True

        for ligne in lignes:
            ref, original = ligne["ref"], ligne["original"]
            decision = lire_decision(ligne["decision"])
            legende = normaliser_texte(ligne["legende"])
            heure = normaliser_heure(ligne["heure"])
            commentaire = str(ligne["commentaire"]).strip() if ligne["commentaire"] else None

            if original is None:
                print(f"  ! {ref} : référence inconnue de l'onglet _tech — ligne ignorée")
                compteurs["erreurs"] += 1
                continue

            legende_modifiee = legende != normaliser_texte(original["texte"])
            heure_originale = original["date_time"][11:16]
            heure_modifiee = heure is not None and heure != heure_originale

            if decision is None:
                if legende_modifiee or commentaire:
                    compteurs["sans_decision"] += 1
                    print(f"  ℹ {ref} : ligne retouchée mais AUCUNE décision — rien fait, à trancher")
                continue

            cle = empreinte(decision, legende, heure)
            deja = journal.get(ref, {})
            if deja.get("hash") == cle and not deja.get("en_attente"):
                continue  # déjà appliqué à l'identique — sauf ✅ retenu, qui se retente

            entree = {"decision": decision, "hash": cle,
                      "quand": datetime.now().isoformat(timespec="seconds"),
                      "commentaire": commentaire, "legende_modifiee": legende_modifiee,
                      "heure": heure if heure_modifiee else None,
                      "post_id": original["post_id"], "resultat": None}

            if decision == "INCONNU":
                entree["resultat"] = f"décision illisible : « {ligne['decision']} » — à clarifier"
                print(f"  ? {ref} : {entree['resultat']}")
                # Silencieux côté client : sa case est remplie, il croit avoir décidé, et
                # rien ne partira. Ça mérite un signal, pas seulement une ligne de journal.
                if evenements is not None:
                    evenements.append({
                        "quand": datetime.now().isoformat(timespec="seconds"),
                        "client": slug, "nom": compte["nom"], "semaine": semaine,
                        "type": "decision_illisible",
                        "titre": f"{compte['nom']} — décision illisible sur {ref}",
                        "detail": f"La case « Votre décision » contient « {ligne['decision']} », "
                                  f"qui n'est aucun des trois choix. La ligne ne partira pas "
                                  f"tant que ce n'est pas clarifié.",
                        "lien": (f"https://docs.google.com/spreadsheets/d/"
                                 f"{compte['drive_fichier']}/edit"
                                 if compte.get("drive_fichier") else None)})
            elif decision == "NON":
                entree["resultat"] = "refusé — laissé en brouillon, à retirer à la main"
                compteurs["refuses"] += 1
                print(f"  ⛔ {ref} : refusé" + (f" — « {commentaire} »" if commentaire else ""))
            elif decision == "CORRIGER":
                entree["resultat"] = "à corriger puis re-proposer"
                compteurs["a_corriger"] += 1
                print(f"  ✏️ {ref} : à corriger — « {commentaire or 'sans commentaire'} »")
            else:  # OK
                if compte["blog_id"] not in posts_cache:
                    lundi = date.fromisoformat(semaine)
                    posts_cache[compte["blog_id"]] = posts_semaine(compte["blog_id"], lundi)
                post = retrouver_post(posts_cache[compte["blog_id"]], original)
                nouvelle_date = f"{original['date_time'][:11]}{heure}:00" if heure_modifiee \
                    else original["date_time"]
                # Une case légende vidée est presque toujours une fausse manœuvre : on garde
                # le texte d'origine plutôt que de publier une légende vide.
                texte_final = legende if (legende_modifiee and legende) else original["texte"]

                if post is None:
                    entree["resultat"] = "post introuvable dans Metricool (supprimé ou déplacé hors semaine)"
                    compteurs["erreurs"] += 1
                    print(f"  ✗ {ref} : {entree['resultat']}")
                elif not post.get("draft"):
                    entree["resultat"] = "déjà validé directement dans Metricool — rien à faire"
                    print(f"  = {ref} : {entree['resultat']}")
                elif PLACEHOLDER.search(texte_final):
                    # ✅ retenu, pas refusé : l'accord du client reste acquis, la relève
                    # retente à chaque passage et publie dès que le texte est complété.
                    entree["resultat"] = ("✅ retenu — texte à placeholders, publication en attente : "
                                          "compléter le texte et la relève suivante publiera")
                    entree["en_attente"] = True
                    compteurs["en_attente"] += 1
                    print(f"  ⏳ {ref} : {entree['resultat']}")
                elif not post.get("media"):
                    entree["resultat"] = ("✅ retenu — aucun média attaché, publication en attente : "
                                          "ajouter le visuel dans Metricool et la relève suivante publiera")
                    entree["en_attente"] = True
                    compteurs["en_attente"] += 1
                    print(f"  ⏳ {ref} : {entree['resultat']}")
                elif dry_run:
                    detail = [d for d, actif in (("légende", legende_modifiee),
                                                 (f"heure → {heure}", heure_modifiee)) if actif]
                    print(f"  [dry-run] {ref} : passerait en publication auto"
                          + (f" ({', '.join(detail)})" if detail else ""))
                    continue
                else:
                    try:
                        resultat, post_id = passer_en_publication(
                            compte["blog_id"], post, texte_final, nouvelle_date)
                        entree["resultat"], entree["post_id"] = resultat, post_id
                        compteurs["publies"] += 1
                        detail = " — légende du client" if legende_modifiee else ""
                        print(f"  ✓ {ref} : {resultat}{detail}")
                        posts_cache.pop(compte["blog_id"], None)  # cache invalide après écriture
                    except Exception as exc:
                        entree["resultat"] = f"échec Metricool : {exc}"
                        compteurs["erreurs"] += 1
                        print(f"  ✗ {ref} : {exc}", file=sys.stderr)

            if not dry_run:
                journal[ref] = entree
                touches = True

    if touches:
        ETAT.mkdir(parents=True, exist_ok=True)
        (ETAT / f"{slug}.json").write_text(
            json.dumps(etat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return compteurs


# ---------------------------------------------------------------- orchestration

def charger_comptes(filtre=None):
    config = json.loads((REVIEWS / "config.json").read_text(encoding="utf-8"))
    comptes = [c for c in config["comptes"] if c.get("actif")]
    if filtre:
        comptes = [c for c in comptes if c["slug"] == filtre]
        if not comptes:
            raise SystemExit(f"client inconnu ou inactif : {filtre}")
    return comptes


def main():
    ap = argparse.ArgumentParser(description="Review hebdo client — fichier Excel ↔ Metricool.")
    sous = ap.add_subparsers(dest="commande", required=True)
    g = sous.add_parser("generer", help="écrit le fichier Excel de la semaine par client")
    g.add_argument("--semaine", help="lundi visé (YYYY-MM-DD). Vide = semaine en cours")
    a = sous.add_parser("appliquer", help="lit les retours clients et pousse dans Metricool")
    for p in (g, a):
        p.add_argument("--client", help="ne traiter qu'un compte, ex. le-loft")
        p.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    absents = [v for v in ("METRICOOL_USER_ID", "METRICOOL_TOKEN") if not os.environ.get(v)]
    if absents:
        raise SystemExit(f"secrets manquants : {', '.join(absents)}")

    comptes = charger_comptes(args.client)
    if args.commande == "generer":
        lundi = semaine_lundi(args.semaine)
        print(f"Review de la semaine du {lundi} au {lundi + timedelta(days=6)} — {len(comptes)} compte(s)\n")
        total = sum(generer_compte(c, lundi, args.dry_run) for c in comptes)
        verbe = "couverts (rien n'a été écrit)" if args.dry_run else "couverts par les fichiers générés"
        print(f"\n{total} brouillon(s) {verbe}.")
        return 0

    totaux, evenements = {}, []
    for compte in comptes:
        for cle, valeur in appliquer_compte(compte, args.dry_run, evenements).items():
            totaux[cle] = totaux.get(cle, 0) + valeur
    if evenements and not args.dry_run:
        empiler_notifications(evenements)
        print(f"\n{len(evenements)} signal(aux) de veille en file — scripts/notifier.py les envoie.")
    for e in evenements:
        print(f"  🔔 {e['titre']}")
    print(f"\nBilan : {totaux.get('publies', 0)} publié(s), {totaux.get('a_corriger', 0)} à corriger, "
          f"{totaux.get('refuses', 0)} refusé(s), {totaux.get('en_attente', 0)} ✅ en attente "
          f"(média/placeholders), {totaux.get('sans_decision', 0)} sans décision, "
          f"{totaux.get('erreurs', 0)} erreur(s)."
          + ("" if args.dry_run else " Détail durable : reviews/etat/."))
    return 1 if totaux.get("erreurs") else 0


if __name__ == "__main__":
    sys.exit(main())

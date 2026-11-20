#!/usr/bin/env python3
"""Style « educatif » des carrousels : la DA stylisée des séries pédagogiques d'Otea Filmakers.

Appelé par scripts/carrousel.py dès qu'un spec porte `"style": "educatif"`. Même entrée (un
spec JSON dans carrousels/<client>/), mêmes sorties (slides PNG numérotées, caption.txt,
manifest.json), même planification par scripts/publier.py. Ce qui change, c'est la mise en
page : au lieu d'un bloc de texte centré sur aplat ou sur photo, chaque slide est posée
comme l'écran d'une caméra.

    - les quatre coins portent les repères d'un viseur, « REC » s'allume sur la couverture ;
    - une mention technique en Space Mono en haut (série à gauche, compte ou matériel à
      droite), une barre de progression et le compteur « 03 / 08 » en bas ;
    - un gabarit par slide : couverture, chapitre (numéro géant en filigrane), chiffre (une
      valeur en très grand), liste (index mono), duel (deux colonnes), cta (fond inversé) ;
    - un grain film léger (celui des stories Filmakers), posé en dernier.

Typographique par construction : aucune photo, aucune image générée. Les images de
compétition restent pour les reels et les stories, où elles bougent. Les règles de la
doctrine (8 slides, 40 mots, deux accents, aucun crochet, aucun tiret cadratin) s'appliquent
à l'identique, et le script refuse un texte qui déborde plutôt que de livrer une slide
illisible.
"""

from PIL import Image, ImageChops, ImageDraw

from carrousel import CONTENT_W, H, MARGIN, MAX_SLIDES, W, block, draw_lines, font, tracked

GABARITS = ("couverture", "chapitre", "chiffre", "liste", "duel", "cta")

# Zones communes : au-dessus du chrome du haut, en dessous de la barre de progression.
Y_HAUT = 170
Y_BAS = H - 150

SZ_COUV = (112, 68)
SZ_TITRE = (66, 48)
SZ_TITRE_CTA = (84, 56)
SZ_CORPS = (48, 44)
SZ_ITEM = (44, 40)
SZ_COLONNE = (40, 36)
SZ_LEGENDE = 28
SZ_LABEL = 24
SZ_CHIFFRE_MAX = 300


def _palette(theme, conf, inverse):
    """Les couleurs d'une slide : la DA du compte, retournée sur la slide CTA."""
    if inverse:
        return {
            "bg": theme["cta_bg"], "texte": theme["cta_fg"], "accent": theme["cta_fg"],
            "label": theme["cta_fg"], "trait": conf.get("trait_inverse", "#CDD3D2"),
            "ghost": conf.get("ghost_inverse", "#E2E6E5"),
        }
    return {
        "bg": theme["bg"], "texte": theme["fg"], "accent": theme["accent"],
        "label": conf["sauge"], "trait": conf["graphite"], "ghost": conf["graphite"],
    }


def _mono(conf, size, bold=False):
    return font(conf.get("mono_family", ["Space Mono", "DejaVu Sans Mono"]), size, bold)


def _mots(texte):
    return len(str(texte).replace("**", " ").split())


def _texte_slide(slide):
    """Tout le texte publié d'une slide, pour les comptes de mots et d'accents."""
    morceaux = [slide.get("kicker", ""), slide.get("title", ""), slide.get("body", ""),
                slide.get("chiffre", ""), slide.get("legende", "")]
    morceaux += list(slide.get("items") or [])
    for col in ("gauche", "droite"):
        if slide.get(col):
            morceaux += [slide[col].get("label", ""), slide[col].get("texte", "")]
    return " ".join(str(m) for m in morceaux if m)


# ---------------------------------------------------------------- validation

def valider(spec, themes):
    """Les erreurs d'un spec « educatif ». Liste vide quand tout est bon."""
    errs = []
    theme = themes.get(spec.get("client")) or {}
    conf = theme.get("educatif")
    if not conf:
        errs.append(f"client « {spec.get('client')} » : pas de bloc « educatif » dans scripts/themes.json")
    for field in ("client", "slug", "archetype", "pilier", "date_time", "cible", "slides", "caption"):
        if not spec.get(field):
            errs.append(f"champ obligatoire manquant : {field}")
    slides = spec.get("slides") or []
    if len(slides) > MAX_SLIDES:
        errs.append(f"{len(slides)} slides, le maximum est {MAX_SLIDES}")
    if len(slides) < 4:
        errs.append(f"{len(slides)} slides, un carrousel en dessous de 4 slides n'en est pas un")
    for i, s in enumerate(slides, 1):
        gabarit = s.get("gabarit")
        if gabarit not in GABARITS:
            errs.append(f"slide {i} : gabarit « {gabarit} » inconnu (attendu : {', '.join(GABARITS)})")
            continue
        if i == 1 and gabarit != "couverture":
            errs.append("slide 1 : la première slide est la couverture")
        if i == len(slides) and gabarit != "cta":
            errs.append(f"slide {i} : la dernière slide est le cta")
        if gabarit not in ("chiffre",) and not s.get("title"):
            errs.append(f"slide {i} : titre manquant")
        if gabarit == "chiffre" and not s.get("chiffre"):
            errs.append(f"slide {i} : gabarit chiffre sans « chiffre »")
        if gabarit == "liste":
            items = s.get("items") or []
            if not 2 <= len(items) <= 5:
                errs.append(f"slide {i} : une liste porte 2 à 5 items, pas {len(items)}")
        if gabarit == "duel":
            for col in ("gauche", "droite"):
                if not (s.get(col) or {}).get("texte"):
                    errs.append(f"slide {i} : colonne « {col} » sans texte")
        brut = _texte_slide(s)
        if brut.count("**") % 2:
            errs.append(f"slide {i} : balise ** non refermée")
        groupes = brut.count("**") // 2
        if groupes > 2:
            errs.append(f"slide {i} : {groupes} groupes accentués, maximum 2")
        mots = _mots(brut)
        if mots > 40:
            errs.append(f"slide {i} : {mots} mots (maximum 40)")
        if "[" in brut:
            errs.append(f"slide {i} : placeholder « [ » restant dans un texte publié")
        if any(t in brut for t in ("—", "–")):
            errs.append(f"slide {i} : tiret cadratin dans un texte publié")
    legende = spec.get("caption", "")
    if "[" in legende:
        errs.append("placeholder « [ » restant dans la légende")
    if any(t in legende for t in ("—", "–")):
        errs.append("tiret cadratin dans la légende")
    return errs


# ---------------------------------------------------------------- chrome

def _coins(d, pal):
    """Les repères de viseur dans les quatre coins."""
    inset, bras, ep = 44, 60, 3
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        x = inset if sx > 0 else W - inset
        y = inset if sy > 0 else H - inset
        d.rectangle([min(x, x + sx * bras), y - ep // 2, max(x, x + sx * bras), y + ep // 2], fill=pal["trait"])
        d.rectangle([x - ep // 2, min(y, y + sy * bras), x + ep // 2, max(y, y + sy * bras)], fill=pal["trait"])


def _chrome(d, spec, slide, theme, conf, pal, index, total):
    _coins(d, pal)
    f_label = _mono(conf, SZ_LABEL, bold=True)
    serie = (spec.get("serie") or conf.get("serie") or "").upper()
    if serie:
        tracked(d, serie, MARGIN, 64, f_label, pal["label"], tracking=3)
    if index == 1:
        rec = "REC"
        largeur = d.textlength(rec, font=f_label) + 3 * (len(rec) - 1)
        x = W - MARGIN - largeur
        d.ellipse([x - 30, 71, x - 14, 87], fill=pal["accent"])
        tracked(d, rec, x, 64, f_label, pal["accent"], tracking=3)
    else:
        mention = (slide.get("mention") or spec.get("mention") or conf.get("mention") or "").upper()
        if mention:
            largeur = d.textlength(mention, font=f_label) + 3 * (len(mention) - 1)
            tracked(d, mention, W - MARGIN - largeur, 64, f_label, pal["label"], tracking=3)

    # Barre de progression : la part du carrousel déjà lue.
    y_barre = H - 84
    d.rectangle([MARGIN, y_barre, W - MARGIN, y_barre + 2], fill=pal["trait"])
    fait = MARGIN + int(CONTENT_W * index / total)
    d.rectangle([MARGIN, y_barre - 1, fait, y_barre + 3], fill=pal["accent"])

    f_pied = _mono(conf, 22)
    pied = (conf.get("pied") or "").upper()
    if pied:
        d.text((MARGIN, H - 70), pied, font=f_pied, fill=pal["label"])
    if index == 1:
        cue = "SWIPE →"
        f_cue = _mono(conf, 22, bold=True)
        d.text((W - MARGIN - d.textlength(cue, font=f_cue), H - 70), cue, font=f_cue, fill=pal["accent"])
    else:
        compteur = f"{index:02d} / {total:02d}"
        d.text((W - MARGIN - d.textlength(compteur, font=f_pied), H - 70), compteur,
               font=f_pied, fill=pal["label"])


def _grain(img, force):
    if not force:
        return img
    bruit = Image.effect_noise(img.size, force).convert("RGB")
    return ImageChops.add(img, bruit, 1, -128)


def _deborde(slug, index, y_fin, plafond=Y_BAS):
    if y_fin > plafond:
        raise ValueError(
            f"{slug} · slide {index} : le texte déborde même à la taille minimale. "
            f"Raccourcir le titre, le corps ou la liste.")


def _kicker(d, slide, conf, pal, x, y):
    kicker = (slide.get("kicker") or "").upper()
    if not kicker:
        return y
    tracked(d, kicker, x, y, _mono(conf, 28, bold=True), pal["label"], tracking=4)
    d.rectangle([x, y + 52, x + 96, y + 55], fill=pal["accent"])
    return y + 96


# ---------------------------------------------------------------- gabarits

def _couverture(d, slide, fam, conf, pal, slug, index):
    tf, tl, tlh = block(d, slide["title"], fam, SZ_COUV, CONTENT_W, bold=True, leading=1.04)
    corps = slide.get("body", "")
    bf, bl, blh = block(d, corps, fam, SZ_CORPS, CONTENT_W) if corps else (None, [], 0)
    h_kicker = 96 if slide.get("kicker") else 0
    total = h_kicker + len(tl) * tlh + (36 + len(bl) * blh if bl else 0)
    y = Y_BAS - 40 - total
    if y < Y_HAUT:
        _deborde(slug, index, Y_HAUT + total, Y_BAS - 40)
    y = _kicker(d, slide, conf, pal, MARGIN, y)
    y = draw_lines(d, tl, MARGIN, y, tf, tlh, pal["texte"], pal["accent"])
    if bl:
        draw_lines(d, bl, MARGIN, y + 36, bf, blh, pal["texte"], pal["accent"])


def _chapitre(d, slide, fam, conf, pal, slug, index):
    numero = str(slide.get("numero") or f"{index - 1:02d}")
    f_ghost = font(fam, 560, bold=True)
    largeur = d.textlength(numero, font=f_ghost)
    d.text((W - largeur + 40, 60), numero, font=f_ghost, fill=pal["ghost"])
    y = _kicker(d, slide, conf, pal, MARGIN, 330)
    tf, tl, tlh = block(d, slide["title"], fam, SZ_TITRE, CONTENT_W, bold=True, leading=1.12)
    y = draw_lines(d, tl, MARGIN, y, tf, tlh, pal["texte"], pal["accent"])
    corps = slide.get("body", "")
    if corps:
        bf, bl, blh = block(d, corps, fam, SZ_CORPS, CONTENT_W)
        y = draw_lines(d, bl, MARGIN, y + 40, bf, blh, pal["texte"], pal["accent"])
    _deborde(slug, index, y)


def _chiffre(d, slide, fam, conf, pal, slug, index):
    valeur = str(slide["chiffre"])
    taille = SZ_CHIFFRE_MAX
    while taille > 120:
        f_val = font(fam, taille, bold=True)
        if d.textlength(valeur, font=f_val) <= CONTENT_W:
            break
        taille -= 10
    y = 250
    d.text((MARGIN - 8, y), valeur, font=f_val, fill=pal["accent"])
    y += int(taille * 1.18)
    legende = (slide.get("legende") or "").upper()
    if legende:
        tracked(d, legende, MARGIN, y, _mono(conf, SZ_LEGENDE, bold=True), pal["label"], tracking=3)
        y += 70
    d.rectangle([MARGIN, y, MARGIN + 96, y + 3], fill=pal["accent"])
    y += 44
    if slide.get("title"):
        tf, tl, tlh = block(d, slide["title"], fam, (56, 44), CONTENT_W, bold=True, leading=1.12)
        y = draw_lines(d, tl, MARGIN, y, tf, tlh, pal["texte"], pal["accent"])
    corps = slide.get("body", "")
    if corps:
        bf, bl, blh = block(d, corps, fam, SZ_CORPS, CONTENT_W)
        y = draw_lines(d, bl, MARGIN, y + 32, bf, blh, pal["texte"], pal["accent"])
    _deborde(slug, index, y)


def _liste(d, slide, fam, conf, pal, slug, index):
    y = _kicker(d, slide, conf, pal, MARGIN, 230)
    tf, tl, tlh = block(d, slide["title"], fam, (60, 46), CONTENT_W, bold=True, leading=1.1)
    y = draw_lines(d, tl, MARGIN, y, tf, tlh, pal["texte"], pal["accent"]) + 36
    f_idx = _mono(conf, 30, bold=True)
    x_txt = MARGIN + 110
    for n, item in enumerate(slide["items"], 1):
        d.rectangle([MARGIN, y, W - MARGIN, y + 1], fill=pal["trait"])
        y += 26
        d.text((MARGIN, y + 6), f"{n:02d}", font=f_idx, fill=pal["label"])
        bf, bl, blh = block(d, item, fam, SZ_ITEM, CONTENT_W - 110, leading=1.2)
        y = draw_lines(d, bl, x_txt, y, bf, blh, pal["texte"], pal["accent"]) + 26
    d.rectangle([MARGIN, y, W - MARGIN, y + 1], fill=pal["trait"])
    _deborde(slug, index, y + 1)


def _duel(d, slide, fam, conf, pal, slug, index):
    y = _kicker(d, slide, conf, pal, MARGIN, 230)
    tf, tl, tlh = block(d, slide["title"], fam, (60, 46), CONTENT_W, bold=True, leading=1.1)
    y = draw_lines(d, tl, MARGIN, y, tf, tlh, pal["texte"], pal["accent"]) + 56
    gouttiere = 60
    larg = (CONTENT_W - gouttiere) // 2
    d.rectangle([W // 2 - 1, y, W // 2 + 1, Y_BAS], fill=pal["trait"])
    bas = y
    for col, x in (("gauche", MARGIN), ("droite", MARGIN + larg + gouttiere)):
        donnees = slide[col]
        yy = y
        label = (donnees.get("label") or "").upper()
        if label:
            tracked(d, label, x, yy, _mono(conf, SZ_LABEL, bold=True), pal["label"], tracking=3)
            yy += 60
        bf, bl, blh = block(d, donnees["texte"], fam, SZ_COLONNE, larg, leading=1.24)
        yy = draw_lines(d, bl, x, yy, bf, blh, pal["texte"], pal["accent"])
        bas = max(bas, yy)
    _deborde(slug, index, bas)


def _cta(d, slide, fam, conf, pal, slug, index):
    tf, tl, tlh = block(d, slide["title"], fam, SZ_TITRE_CTA, CONTENT_W, bold=True, leading=1.06)
    corps = slide.get("body", "")
    bf, bl, blh = block(d, corps, fam, SZ_CORPS, CONTENT_W) if corps else (None, [], 0)
    h_kicker = 96 if slide.get("kicker") else 0
    total = h_kicker + len(tl) * tlh + (40 + len(bl) * blh if bl else 0)
    y = max(Y_HAUT + 40, (H - total) // 2)
    _deborde(slug, index, y + total)
    y = _kicker(d, slide, conf, pal, MARGIN, y)
    # Sur fond inversé, l'accent se fait au gras seul : la couleur d'accent est le fond.
    y = draw_lines(d, tl, MARGIN, y, tf, tlh, pal["texte"], pal["texte"])
    if bl:
        draw_lines(d, bl, MARGIN, y + 40, bf, blh, pal["texte"], pal["texte"])


RENDUS = {"couverture": _couverture, "chapitre": _chapitre, "chiffre": _chiffre,
          "liste": _liste, "duel": _duel, "cta": _cta}


def rendre_slide(spec, slide, theme, index, total):
    conf = theme["educatif"]
    gabarit = slide["gabarit"]
    pal = _palette(theme, conf, inverse=(gabarit == "cta"))
    fam = theme.get("font_family", ["DejaVu Sans"])
    img = Image.new("RGB", (W, H), pal["bg"])
    d = ImageDraw.Draw(img)
    RENDUS[gabarit](d, slide, fam, conf, pal, spec["slug"], index)
    _chrome(d, spec, slide, theme, conf, pal, index, total)
    return _grain(img, conf.get("grain", 0))

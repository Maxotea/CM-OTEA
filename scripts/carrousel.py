#!/usr/bin/env python3
"""Rend les slides d'un carrousel hebdomadaire à partir d'un spec JSON.

    python3 scripts/carrousel.py carrousels/le-loft/2026-08-12-erreurs-barbe.json
    python3 scripts/carrousel.py carrousels/le-loft/          # tout le dossier
    python3 scripts/carrousel.py carrousels/ --check          # valide sans écrire

Sortie : medias/<client>/carrousels/<slug>/slide-01.png … + caption.txt + manifest.json
Le manifest donne les slides DANS L'ORDRE : c'est lui qui alimente media01…media0N de
`schedule_post`. Voir .claude/skills/cm-metricool/references/carrousels-hebdo.md.

Le script échoue plutôt que de livrer une slide illisible : un texte qui déborde à la taille
minimale se corrige à l'écriture, pas à la publication.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import urllib.request

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    sys.exit("Pillow manquant : pip install pillow")

ROOT = Path(__file__).resolve().parent.parent
THEMES_PATH = ROOT / "scripts" / "themes.json"

W, H = 1080, 1350          # 4:5, le ratio qui occupe le plus de surface dans le fil
MARGIN = 90                # marge de sécurité : Instagram rogne les coins sur certains appareils
CONTENT_W = W - 2 * MARGIN
MAX_SLIDES = 8             # l'API accepte 10 médias ; on garde 2 de marge de correction

# (taille de départ, taille plancher) — le plancher vient des règles de lisibilité de la doctrine
SZ_KICKER = (34, 30)
SZ_COVER_TITLE = (100, 62)
SZ_TITLE = (66, 48)
SZ_BODY = (48, 44)
SZ_NUM = (28, 28)

# Contraste : on ne juge pas un fond photo à l'œil, on le mesure. Rapport WCAG
# entre la couleur du texte et le fond réellement composité sous ce texte.
# Une photo d'ambiance sous licence libre habille un propos général. Elle ne
# doit JAMAIS illustrer un texte qui désigne un bien précis : le lecteur
# comprendrait qu'on lui montre un mandat de l'agence. C'est exactement le
# reproche qui a coûté le compte Le Loft le 31/08/2026.
DESIGNE_UN_BIEN = (
    "ce bien", "cet appartement", "cette maison", "ce logement", "ce studio",
    "notre mandat", "nos mandats", "à vendre", "a vendre", "en exclusivité",
    "en exclusivite", "ce duplex", "cet immeuble", "visitez", "coup de coeur",
    "coup de cœur", "nouveauté", "nouveaute", "vendu", "disponible",
)

CONTRASTE_TITRE = 7.0      # AAA — un titre doit tenir même au soleil
CONTRASTE_CORPS = 4.5      # AA
VOILE_MAX = 0.94           # au-delà, le fond photo ne sert plus à rien
RAMPE_VOILE = 150          # dégradé au-dessus du bloc de texte, en pixels

FONT_DIRS = [
    Path("/System/Library/Fonts"), Path("/Library/Fonts"), Path.home() / "Library/Fonts",
    Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts",
]
# Suffixes tolérés après le nom de famille : tout le reste (mono, narrow, italic…) est une
# AUTRE famille et ne doit jamais être substitué silencieusement.
REGULAR_TOKENS = {"", "regular", "book", "roman", "medium", "text", "display", "displayregular"}
BOLD_TOKENS = {"bold", "heavy", "black", "demibold", "semibold", "displaybold"}


# ---------------------------------------------------------------- polices

def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _font_index():
    if not hasattr(_font_index, "cache"):
        idx = []
        for d in FONT_DIRS:
            if not d.is_dir():
                continue
            for p in d.rglob("*"):
                if p.suffix.lower() in (".ttf", ".otf"):
                    idx.append((_norm(p.stem), p))
        _font_index.cache = idx
    return _font_index.cache


def _find_file(families, bold):
    for fam in families:
        f = _norm(fam)
        for stem, path in _font_index():
            if not stem.startswith(f):
                continue
            rest = stem[len(f):]
            if bold and rest in BOLD_TOKENS:
                return path
            if not bold and rest in REGULAR_TOKENS:
                return path
    return None


def font(families, size, bold=False):
    """Charge la première police disponible de la liste, avec repli sur les polices système."""
    key = (tuple(families), size, bold)
    cache = font.__dict__.setdefault("cache", {})
    if key in cache:
        return cache[key]
    path = _find_file(families, bold) or _find_file(
        ["DejaVu Sans", "Liberation Sans", "Helvetica Neue", "Arial"], bold)
    f = ImageFont.truetype(str(path), size) if path else ImageFont.load_default(size)
    cache[key] = f
    return f


# ---------------------------------------------------------------- fond photo

def _luminance(rgb):
    """Luminance relative WCAG d'un triplet 0-255."""
    canaux = []
    for v in rgb[:3]:
        v /= 255.0
        canaux.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    r, v, b = canaux
    return 0.2126 * r + 0.7152 * v + 0.0722 * b


def _contraste(c1, c2):
    l1, l2 = _luminance(c1), _luminance(c2)
    if l2 > l1:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _fond_sous_encre(img, masque, halo=3):
    """Pixel le plus clair du fond RÉELLEMENT recouvert par le texte.

    Deux erreurs ont été commises ici et corrigées le 02/09/2026, après
    reproduction sur le vrai chemin de code :

    1. On mesurait sur toute la boîte, marges comprises. Les grandes zones
       sombres où aucun texte ne passe diluaient la mesure.
    2. On prenait le 97e centile. Sur une boîte de 894 000 px, 3 % font un
       carré de 163 px : une fenêtre surexposée plus petite que ça était
       jetée par le centile, c'est-à-dire exactement ce qu'on cherchait.
       Mesuré : une fenêtre de 200×100 recevait un voile de 0 %, le script
       annonçait 13,94:1 et le contraste réel était de 1,08:1.

    On prend donc le MAXIMUM, et seulement sous l'encre. L'encre est dilatée
    de quelques pixels : un glyphe est antialiasé, ses bords empruntent la
    couleur du fond, et l'œil lit le contraste sur cette frange. Un flou léger
    sur le fond écarte le pixel isolé sans effacer une zone brûlée.
    """
    if masque.getbbox() is None:
        return (0, 0, 0)
    encre = masque.filter(ImageFilter.MaxFilter(2 * halo + 1))
    encre = encre.point(lambda v: 255 if v > 32 else 0)
    gris = img.convert("L").filter(ImageFilter.GaussianBlur(1.0))
    sous = Image.composite(gris, Image.new("L", gris.size, 0), encre)
    haut = sous.getextrema()[1]
    return (haut, haut, haut)


def _alpha_requis(fond, texte, voile, cible):
    """Plus petite opacité de voile qui amène le contraste à la cible."""
    if _contraste(fond, texte) >= cible:
        return 0.0
    bas, haut = 0.0, 1.0
    for _ in range(24):                       # dichotomie, 24 tours = 1e-7
        milieu = (bas + haut) / 2
        melange = tuple(f * (1 - milieu) + v * milieu for f, v in zip(fond, voile))
        if _contraste(melange, texte) >= cible:
            haut = milieu
        else:
            bas = milieu
    return haut


def charger_fond(conf, photo, slug):
    """Récupère la photo du client, la met en cache, la recadre en 4:5."""
    cache = ROOT / conf["cache"]
    cache.mkdir(parents=True, exist_ok=True)
    fichier = cache / (photo["cle"] + ".jpg")
    if not fichier.exists():
        requete = urllib.request.Request(photo["url"],
                                         headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(requete, timeout=45) as flux:
                fichier.write_bytes(flux.read())
        except Exception as exc:
            raise ValueError(
                f"{slug} : photo de fond « {photo['cle']} » introuvable ({exc}). "
                f"Vérifier {photo['url']}")
    img = Image.open(fichier).convert("RGB")
    lw, lh = img.size
    if lw / lh > W / H:
        cw = int(lh * W / H)
        img = img.crop(((lw - cw) // 2, 0, (lw - cw) // 2 + cw, lh))
    else:
        ch = int(lw * H / W)
        img = img.crop((0, (lh - ch) // 2, lw, (lh - ch) // 2 + ch))
    return img.resize((W, H), Image.LANCZOS)


def poser_voile(img, boite, alpha, voile):
    """Voile dégradé : nul en haut de la rampe, plein sur le bloc de texte.

    La photo reste lisible au-dessus du texte ; en dessous, le voile ne se lève
    pas, sinon la fin d'une phrase retomberait sur une zone claire.
    """
    y0 = max(0, boite[1] - RAMPE_VOILE)
    calque = Image.new("RGBA", (W, H), voile + (0,))
    dessin = ImageDraw.Draw(calque)
    for y in range(y0, H):
        if y < boite[1]:
            t = (y - y0) / float(max(1, boite[1] - y0))
            a = alpha * t * t
        else:
            a = alpha
        dessin.line([(0, y), (W, y)], fill=voile + (int(round(a * 255)),))
    return Image.alpha_composite(img.convert("RGBA"), calque).convert("RGB")


# ---------------------------------------------------------------- texte

def tokeniser(text):
    """Découpe un texte balisé `**ainsi**` en mots, chacun marqué accentué ou non.

    L'accentuation est ce qui permet de lire une slide en diagonale : l'œil accroche le
    chiffre et le mot décisif avant de lire la phrase. Sans elle, une slide se lit
    entièrement ou pas du tout.
    """
    tokens, fin_espace = [], True
    for i, segment in enumerate(text.split("**")):
        emph = i % 2 == 1
        debut_espace = segment[:1].isspace() if segment else True
        mots = segment.split()
        for j, mot in enumerate(mots):
            # Un mot qui suit immédiatement une balise, sans espace, lui reste collé :
            # sinon la ponctuation se détache — « séchant , et » au lieu de « séchant, et ».
            colle = bool(tokens) and j == 0 and not (fin_espace or debut_espace)
            tokens.append((mot, emph, colle))
        if mots:
            fin_espace = segment[-1:].isspace()
    return tokens


def wrap_tokens(draw, tokens, f_norm, f_emph, max_w):
    lignes, ligne, largeur = [], [], 0
    espace = draw.textlength(" ", font=f_norm)
    for mot, emph, colle in tokens:
        w = draw.textlength(mot, font=f_emph if emph else f_norm)
        supp = w if (not ligne or colle) else w + espace
        # Un mot collé ne peut pas ouvrir une ligne : il partirait de sa ponctuation.
        if largeur + supp > max_w and ligne and not colle:
            lignes.append(ligne)
            ligne, largeur = [(mot, emph, False)], w
        else:
            ligne.append((mot, emph, colle))
            largeur += supp
    if ligne:
        lignes.append(ligne)
    return lignes


def block(draw, text, families, sizes, max_w, bold=False, leading=1.24):
    """Rend un bloc à la plus grande taille qui tient, sans jamais passer sous le plancher."""
    start, floor = sizes
    tokens = tokeniser(text)
    size = start
    while True:
        f_norm = font(families, size, bold)
        f_emph = font(families, size, True)          # l'accent passe en gras s'il ne l'est pas déjà
        lignes = wrap_tokens(draw, tokens, f_norm, f_emph, max_w)
        if size <= floor:
            return (f_norm, f_emph), lignes, int(size * leading)
        # 4 lignes max pour un titre, 6 pour un corps : au-delà, la slide dit deux choses
        if len(lignes) <= (4 if bold else 6):
            return (f_norm, f_emph), lignes, int(size * leading)
        size -= 2


def draw_lines(draw, lignes, x, y, fonts, lh, fill, fill_emph):
    f_norm, f_emph = fonts
    espace = draw.textlength(" ", font=f_norm)
    for ligne in lignes:
        cx = x
        for i, (mot, emph, colle) in enumerate(ligne):
            if i and not colle:
                cx += espace
            f = f_emph if emph else f_norm
            draw.text((cx, y), mot, font=f, fill=fill_emph if emph else fill)
            cx += draw.textlength(mot, font=f)
        y += lh
    return y


def tracked(draw, text, x, y, fnt, fill, tracking=6):
    """Texte lettré espacé — réservé aux kickers, qui doivent se lire comme une étiquette."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


# ---------------------------------------------------------------- rendu d'une slide

def render_slide(slide, theme, index, total, slug, fonds=None):
    is_cta = slide.get("cta") or index == total
    is_cover = slide.get("cover") or index == 1

    bg = theme["cta_bg"] if is_cta else theme["bg"]
    fg = theme["cta_fg"] if is_cta else theme["fg"]
    accent = theme["cta_fg"] if is_cta else theme["accent"]
    muted = theme["cta_fg"] if is_cta else theme["muted"]

    # Fond photo : les couleurs de texte changent, le calcul du voile vient plus
    # bas, une fois la boîte du texte connue.
    conf_fond = theme.get("fond")
    photo = fonds.get(slide["photo"]) if (conf_fond and fonds and slide.get("photo")) else None
    if photo:
        fg = conf_fond["texte"]
        muted = conf_fond["muted"]
        accent = conf_fond["accent"]

    fam = theme.get("font_family", ["DejaVu Sans"])
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    title = slide.get("title", "")
    if theme.get("uppercase_titles"):
        title = title.upper()
    body = slide.get("body", "")
    kicker = (slide.get("kicker") or "").upper()

    # Sur la slide CTA le fond EST la couleur d'accent : y colorer un mot le rendrait
    # invisible. L'accentuation s'y fait au gras seul.
    fill_emph = fg if is_cta else accent

    sizes = SZ_COVER_TITLE if is_cover else SZ_TITLE
    tf, tlines, tlh = block(d, title, fam, sizes, CONTENT_W, bold=True, leading=1.12)
    bf, blines, blh = (None, [], 0)
    if body:
        bf, blines, blh = block(d, body, fam, SZ_BODY, CONTENT_W, bold=False)

    kf = font(fam, SZ_KICKER[0], bold=True)
    k_h = (SZ_KICKER[0] + 46) if kicker else 0
    rule_h = 34 if (kicker and theme.get("rule")) else 0
    body_gap = 40 if blines else 0
    total_h = k_h + rule_h + len(tlines) * tlh + body_gap + len(blines) * blh

    floor = H - MARGIN - 60          # au-dessus du numéro de slide
    if is_cover:
        y = max(MARGIN + 40, floor - 120 - total_h)   # couverture : bloc ancré en bas
    else:
        y = max(MARGIN + 60, (H - total_h) // 2)      # contenu : bloc centré verticalement

    if y + total_h > floor:
        raise ValueError(
            f"{slug} · slide {index} : le texte déborde même à la taille minimale. "
            f"Raccourcir le titre ou le corps ({len(title)} + {len(body)} caractères)."
        )

    # Le texte est tracé deux fois : une fois en blanc sur un masque, pour savoir
    # où l'encre tombe réellement, une fois sur l'image pour de bon. C'est le
    # masque qui permet de mesurer le fond là où ça compte.
    nf = font(fam, SZ_NUM[0], bold=False)
    y_depart = y

    def poser(dessin, coul):
        yy = y_depart
        if kicker:
            tracked(dessin, kicker, MARGIN, yy, kf, coul("accent"))
            yy += SZ_KICKER[0] + 46
            if theme.get("rule"):
                dessin.rectangle([MARGIN, yy - 22, MARGIN + 96, yy - 18],
                                 fill=coul("accent"))
                yy += rule_h - 22
        yy = draw_lines(dessin, tlines, MARGIN, yy, tf, tlh,
                        coul("fg"), coul("emph"))
        if blines:
            draw_lines(dessin, blines, MARGIN, yy + body_gap, bf, blh,
                       coul("corps"), coul("emph"))
        if not is_cta:
            dessin.text((MARGIN, H - MARGIN - 34), f"{index}/{total}",
                        font=nf, fill=coul("muted"))
        if is_cover:
            cue = "SWIPE →"
            dessin.text((W - MARGIN - dessin.textlength(cue, font=kf),
                         H - MARGIN - 40), cue, font=kf, fill=coul("accent"))

    couleurs = {"fg": fg, "corps": fg if is_cta else muted, "emph": fill_emph,
                "accent": accent, "muted": muted}

    if photo:
        img = charger_fond(conf_fond, photo, slug)
        voile = _hex_rgb(conf_fond["voile"])

        masque = Image.new("L", (W, H), 0)
        poser(ImageDraw.Draw(masque), lambda role: 255)
        cadre = masque.getbbox()
        if cadre is None:
            raise ValueError(f"{slug} · slide {index} : aucun texte à poser.")

        pire = _fond_sous_encre(img, masque)
        cible_t = conf_fond.get("contraste_titre", CONTRASTE_TITRE)
        cible_c = conf_fond.get("contraste_corps", CONTRASTE_CORPS)
        alpha = max(
            _alpha_requis(pire, _hex_rgb(couleurs["fg"]), voile, cible_t),
            _alpha_requis(pire, _hex_rgb(couleurs["corps"]), voile, cible_c),
            _alpha_requis(pire, _hex_rgb(couleurs["accent"]), voile, cible_c),
        )
        if alpha > VOILE_MAX:
            raise ValueError(
                f"{slug} · slide {index} : la photo « {photo['cle']} » est trop claire "
                f"sous le texte, il faudrait un voile à {alpha:.0%} et le fond "
                f"disparaîtrait. Choisir une autre photo.")
        img = poser_voile(img, (0, cadre[1], W, H), alpha, voile)

        # Contrôle après composition, sur les pixels et non sur le modèle.
        obtenu = _fond_sous_encre(img, masque)
        reel_t = _contraste(obtenu, _hex_rgb(couleurs["fg"]))
        reel_c = min(_contraste(obtenu, _hex_rgb(couleurs["corps"])),
                     _contraste(obtenu, _hex_rgb(couleurs["accent"])))
        if reel_t < cible_t - 0.1 or reel_c < cible_c - 0.1:
            raise ValueError(
                f"{slug} · slide {index} : après voile, contraste mesuré sous le "
                f"texte {reel_t:.2f}:1 pour le titre et {reel_c:.2f}:1 pour le corps, "
                f"en dessous des cibles {cible_t}:1 et {cible_c}:1. "
                f"Photo « {photo['cle']} » à remplacer.")
        d = ImageDraw.Draw(img)

    poser(d, lambda role: couleurs[role])
    return img


# ---------------------------------------------------------------- spec

def charger_manifeste(theme):
    """Index des fonds photo du client, par clé. Vide si le thème n'en a pas."""
    conf = theme.get("fond")
    if not conf:
        return None
    chemin = ROOT / conf["manifeste"]
    if not chemin.exists():
        raise ValueError(f"manifeste de fonds introuvable : {conf['manifeste']}")
    data = json.loads(chemin.read_text(encoding="utf-8"))
    return {p["cle"]: p for p in data["photos"]}


def load_themes():
    return json.loads(THEMES_PATH.read_text(encoding="utf-8"))


def validate(spec, themes, path):
    errs = []
    fonds = None
    theme = themes.get(spec.get("client")) or {}
    if theme.get("fond"):
        try:
            fonds = charger_manifeste(theme)
        except ValueError as exc:
            errs.append(str(exc))
    for field in ("client", "slug", "archetype", "pilier", "date_time", "cible", "slides", "caption"):
        if not spec.get(field):
            errs.append(f"champ obligatoire manquant : {field}")
    client = spec.get("client")
    if client and client not in themes:
        errs.append(f"client « {client} » absent de scripts/themes.json")
    slides = spec.get("slides") or []
    if len(slides) > MAX_SLIDES:
        errs.append(f"{len(slides)} slides — le maximum est {MAX_SLIDES}")
    if len(slides) < 4:
        errs.append(f"{len(slides)} slides — un carrousel en dessous de 4 slides n'en est pas un")
    for i, s in enumerate(slides, 1):
        if not s.get("title"):
            errs.append(f"slide {i} : titre manquant")
        brut = f"{s.get('title', '')} {s.get('body', '')}"
        if brut.count("**") % 2:
            errs.append(f"slide {i} : balise ** non refermée")
        groupes = brut.count("**") // 2
        if groupes > 2:
            errs.append(f"slide {i} : {groupes} groupes accentués — maximum 2. "
                        f"Tout accentuer revient à ne rien accentuer")
        words = len(brut.replace("**", " ").split())
        if words > 40:
            errs.append(f"slide {i} : {words} mots (maximum 40)")
        cle = s.get("photo")
        if cle and fonds is not None:
            if cle not in fonds:
                errs.append(f"slide {i} : fond « {cle} » absent du manifeste")
            else:
                fond = fonds[cle]
                if not fond.get("matiere"):
                    errs.append(
                        f"slide {i} : fond « {cle} » est un mur nu de logement vide "
                        f"({fond['sujet']}). Un fond sans matière ne fait pas "
                        f"une image, il fait une tache grise")
                if fond.get("provenance") == "libre":
                    en_clair = brut.replace("**", " ").lower()
                    mots = [m for m in DESIGNE_UN_BIEN if m in en_clair]
                    if mots:
                        errs.append(
                            f"slide {i} : le texte désigne un bien précis "
                            f"({', '.join(mots)}) alors que le fond « {cle} » est une "
                            f"photo d'ambiance sous licence libre. Le lecteur croirait "
                            f"voir un mandat de l'agence. Mettre une photo du client "
                            f"ou réécrire la slide")
                    if not fond.get("licence"):
                        errs.append(
                            f"slide {i} : fond « {cle} » sans licence renseignée")
        elif fonds is not None and not cle:
            errs.append(f"slide {i} : champ photo manquant (le thème a des fonds)")
    texts = [spec.get("caption", "")] + [
        f"{s.get('kicker', '')} {s.get('title', '')} {s.get('body', '')}" for s in slides]
    if any("[" in t for t in texts):
        errs.append("placeholder « [ » restant dans un texte publié")
    if errs:
        raise ValueError(f"{path.name} :\n  - " + "\n  - ".join(errs))
    return spec


def render_spec(path, themes, check_only=False):
    spec = validate(json.loads(path.read_text(encoding="utf-8")), themes, path)
    theme = themes[spec["client"]]
    slides = spec["slides"]
    fonds = charger_manifeste(theme)
    out = ROOT / "medias" / spec["client"] / "carrousels" / spec["slug"]

    files = []
    for i, slide in enumerate(slides, 1):
        img = render_slide(slide, theme, i, len(slides), spec["slug"], fonds)
        name = f"slide-{i:02d}.png"
        files.append(name)
        if not check_only:
            out.mkdir(parents=True, exist_ok=True)
            img.save(out / name, "PNG")

    if check_only:
        return out, files

    caption = spec["caption"].strip()
    tags = " ".join(spec.get("hashtags", []))
    (out / "caption.txt").write_text(f"{caption}\n\n{tags}\n".strip() + "\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({
        "client": spec["client"],
        "slug": spec["slug"],
        "archetype": spec["archetype"],
        "pilier": spec["pilier"],
        "date_time": spec["date_time"],
        "networks": spec.get("networks", theme.get("networks", ["instagram"])),
        "type": "POST",
        "draft": True,
        "auto_publish": False,
        "slides_in_order": files,
        "caption_file": "caption.txt",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out, files


def main():
    ap = argparse.ArgumentParser(description="Rend les carrousels hebdomadaires.")
    ap.add_argument("paths", nargs="+", help="specs JSON ou dossiers de specs")
    ap.add_argument("--check", action="store_true", help="valide sans rien écrire")
    args = ap.parse_args()

    themes = load_themes()
    specs = []
    for raw in args.paths:
        p = Path(raw)
        if not p.is_absolute():
            p = ROOT / p
        specs.extend(sorted(p.rglob("*.json")) if p.is_dir() else [p])
    specs = [s for s in specs if s.name not in ("manifest.json", "themes.json")]

    failures = 0
    for spec_path in specs:
        try:
            out, files = render_spec(spec_path, themes, args.check)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            failures += 1
            print(f"✗ {exc}")
            continue
        verb = "ok" if args.check else "rendu"
        print(f"✓ {spec_path.relative_to(ROOT)} — {len(files)} slides {verb} → "
              f"{out.relative_to(ROOT)}")

    if failures:
        print(f"\n{failures} carrousel(s) en erreur.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

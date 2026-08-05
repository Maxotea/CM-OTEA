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

try:
    from PIL import Image, ImageDraw, ImageFont
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


# ---------------------------------------------------------------- texte

def wrap(draw, text, fnt, max_w):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def block(draw, text, families, sizes, max_w, bold=False, leading=1.24):
    """Rend un bloc à la plus grande taille qui tient, sans jamais passer sous le plancher."""
    start, floor = sizes
    size = start
    while True:
        fnt = font(families, size, bold)
        lines = wrap(draw, text, fnt, max_w)
        if size <= floor:
            return fnt, lines, int(size * leading)
        # 4 lignes max pour un titre, 6 pour un corps : au-delà, la slide dit deux choses
        if len(lines) <= (4 if bold else 6):
            return fnt, lines, int(size * leading)
        size -= 2


def draw_lines(draw, lines, x, y, fnt, lh, fill):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tracked(draw, text, x, y, fnt, fill, tracking=6):
    """Texte lettré espacé — réservé aux kickers, qui doivent se lire comme une étiquette."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


# ---------------------------------------------------------------- rendu d'une slide

def render_slide(slide, theme, index, total, slug):
    is_cta = slide.get("cta") or index == total
    is_cover = slide.get("cover") or index == 1

    bg = theme["cta_bg"] if is_cta else theme["bg"]
    fg = theme["cta_fg"] if is_cta else theme["fg"]
    accent = theme["cta_fg"] if is_cta else theme["accent"]
    muted = theme["cta_fg"] if is_cta else theme["muted"]

    fam = theme.get("font_family", ["DejaVu Sans"])
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    title = slide.get("title", "")
    if theme.get("uppercase_titles"):
        title = title.upper()
    body = slide.get("body", "")
    kicker = (slide.get("kicker") or "").upper()

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

    if kicker:
        tracked(d, kicker, MARGIN, y, kf, accent)
        y += SZ_KICKER[0] + 46
        if theme.get("rule"):
            d.rectangle([MARGIN, y - 22, MARGIN + 96, y - 18], fill=accent)
            y += rule_h - 22

    y = draw_lines(d, tlines, MARGIN, y, tf, tlh, fg)
    if blines:
        y = draw_lines(d, blines, MARGIN, y + body_gap, bf, blh, muted if not is_cta else fg)

    nf = font(fam, SZ_NUM[0], bold=False)
    if not is_cta:
        d.text((MARGIN, H - MARGIN - 34), f"{index}/{total}", font=nf, fill=muted)
    if is_cover:
        cue = "SWIPE →"
        d.text((W - MARGIN - d.textlength(cue, font=kf), H - MARGIN - 40),
               cue, font=kf, fill=accent)
    return img


# ---------------------------------------------------------------- spec

def load_themes():
    return json.loads(THEMES_PATH.read_text(encoding="utf-8"))


def validate(spec, themes, path):
    errs = []
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
        words = len(f"{s.get('title', '')} {s.get('body', '')}".split())
        if words > 40:
            errs.append(f"slide {i} : {words} mots (maximum 40)")
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
    out = ROOT / "medias" / spec["client"] / "carrousels" / spec["slug"]

    files = []
    for i, slide in enumerate(slides, 1):
        img = render_slide(slide, theme, i, len(slides), spec["slug"])
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

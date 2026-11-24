#!/usr/bin/env python3
"""Post image seul (4:5) sur photo de fond, mise en page et contrôles de carrousel.py.

Usage : python3 scripts/post-photo.py posts/<client>/<lot>.json [--check]
Spec : {"client": "...", "posts": [{"slug", "photo", "kicker", "title", "body"?}]}
Sortie : medias/<client>/posts/<slug>.jpg. Une slide unique est à la fois couverture
(bloc ancré en bas) et dernière slide (pas de numéro, pas de « SWIPE »).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import carrousel  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    if len(args) != 1:
        raise SystemExit(__doc__)
    spec = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    theme = carrousel.load_themes()[spec["client"]]
    fonds = carrousel.charger_manifeste(theme)
    if not fonds:
        raise SystemExit(f"{spec['client']} : pas de fonds photo dans le thème")
    out = carrousel.ROOT / "medias" / spec["client"] / "posts"
    erreurs = 0
    for post in spec["posts"]:
        if post.get("photo") not in fonds:
            print(f"✗ {post['slug']} : photo « {post.get('photo')} » absente du manifeste")
            erreurs += 1
            continue
        try:
            img = carrousel.render_slide(post, theme, 1, 1, post["slug"], fonds)
        except ValueError as exc:
            print(f"✗ {exc}")
            erreurs += 1
            continue
        if "--check" not in sys.argv:
            out.mkdir(parents=True, exist_ok=True)
            img.save(out / f"{post['slug']}.jpg", quality=93)
        print(f"✓ {post['slug']} ({post['photo']})")
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()

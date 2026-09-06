"""Les configurations du dépôt se recoupent : le même compte vit dans plusieurs fichiers.

Tant qu'il n'y a pas de source unique des comptes (voir ameliorations/BACKLOG.md), ce test
est le filet : un blog_id qui diverge entre deux fichiers, c'est un client qui reçoit le
tableau d'un autre, ou une relève qui écrit sur le mauvais compte Metricool.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import publier  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = json.loads((ROOT / "reviews/config.json").read_text(encoding="utf-8"))["comptes"]
CLIENTS = json.loads((ROOT / "recaps/clients-config.json").read_text(encoding="utf-8"))["comptes"]
THEMES = json.loads((ROOT / "scripts/themes.json").read_text(encoding="utf-8"))


def test_reviews_config_sans_doublon():
    slugs = [c["slug"] for c in REVIEWS]
    blog_ids = [c["blog_id"] for c in REVIEWS]
    prefixes = [c["prefixe"] for c in REVIEWS if c.get("actif")]
    assert len(set(slugs)) == len(slugs)
    assert len(set(blog_ids)) == len(blog_ids)
    assert len(set(prefixes)) == len(prefixes), "deux comptes actifs partagent un préfixe de référence"


def test_blog_ids_de_publier_concordent_avec_la_review():
    par_slug = {c["slug"]: c["blog_id"] for c in REVIEWS}
    for slug, blog_id in publier.BLOG_IDS.items():
        assert slug in par_slug, f"{slug} est dans publier.BLOG_IDS mais pas dans reviews/config.json"
        assert par_slug[slug] == blog_id, f"{slug} : blog_id différent entre publier.py et reviews/config.json"


def test_chaque_compte_de_la_review_est_connu_du_compte_rendu():
    connus = {c["blog_id"] for c in CLIENTS}
    for compte in REVIEWS:
        assert compte["blog_id"] in connus, \
            f"{compte['slug']} ({compte['blog_id']}) absent de recaps/clients-config.json"


def test_clients_config_sans_doublon_de_blog_id():
    blog_ids = [c["blog_id"] for c in CLIENTS]
    assert len(set(blog_ids)) == len(blog_ids)


def test_chaque_dossier_de_carrousels_a_sa_da_et_son_blog_id():
    for dossier in sorted(p for p in (ROOT / "carrousels").iterdir() if p.is_dir()):
        assert dossier.name in THEMES, f"{dossier.name} : pas de DA dans scripts/themes.json"
        assert dossier.name in publier.BLOG_IDS, f"{dossier.name} : pas de blog_id dans publier.py"


def test_noms_des_specs_de_carrousels_portent_leur_date():
    """`publier.py --semaine` retrouve une spec par son préfixe de date : il doit y être."""
    for spec in sorted((ROOT / "carrousels").rglob("*.json")):
        data = json.loads(spec.read_text(encoding="utf-8"))
        assert spec.name.startswith(data["date_time"][:10]), \
            f"{spec.relative_to(ROOT)} : le nom ne commence pas par sa date {data['date_time'][:10]}"
        assert data["client"] == spec.parent.name, \
            f"{spec.relative_to(ROOT)} : client « {data['client']} » dans un dossier « {spec.parent.name} »"
        assert data["slug"] == spec.stem, f"{spec.relative_to(ROOT)} : slug ≠ nom de fichier"


def test_toutes_les_specs_de_carrousels_passent_le_check():
    resultat = subprocess.run([sys.executable, "scripts/carrousel.py", "carrousels/", "--check"],
                              cwd=ROOT, capture_output=True, text=True)
    assert resultat.returncode == 0, resultat.stdout + resultat.stderr


def test_bilan_de_sante_s_execute():
    resultat = subprocess.run([sys.executable, "scripts/sante.py"],
                              cwd=ROOT, capture_output=True, text=True)
    assert resultat.returncode == 0, resultat.stdout + resultat.stderr
    assert "Bilan de santé" in resultat.stdout

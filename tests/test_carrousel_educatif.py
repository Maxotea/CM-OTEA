"""Le style « educatif » des carrousels (scripts/carrousel_educatif.py), testé à blanc.

Il rend les slides des specs `style: educatif` du dépôt sans rien écrire, et vérifie que
sa validation refuse ce que la doctrine refuse : gabarit inconnu, plus de 40 mots, crochet,
tiret cadratin, liste trop longue, couverture ou CTA mal placés.
"""

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import carrousel  # noqa: E402
import carrousel_educatif  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
THEMES = carrousel.load_themes()
SPECS = sorted(p for p in (ROOT / "carrousels").rglob("*.json")
               if json.loads(p.read_text(encoding="utf-8")).get("style") == "educatif")


def _spec():
    return json.loads(SPECS[0].read_text(encoding="utf-8"))


def test_le_depot_a_au_moins_un_carrousel_educatif():
    assert SPECS, "aucune spec style educatif : le test ne vérifie rien"


@pytest.mark.parametrize("spec_path", SPECS, ids=lambda p: p.stem)
def test_chaque_spec_educatif_se_rend_sans_ecrire(spec_path):
    out, files = carrousel.render_spec(spec_path, THEMES, check_only=True)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    assert len(files) == len(spec["slides"])


def test_la_premiere_slide_est_la_couverture_et_la_derniere_le_cta():
    spec = _spec()
    spec["slides"][0]["gabarit"] = "chapitre"
    errs = carrousel_educatif.valider(spec, THEMES)
    assert any("couverture" in e for e in errs)
    spec = _spec()
    spec["slides"][-1]["gabarit"] = "chapitre"
    errs = carrousel_educatif.valider(spec, THEMES)
    assert any("cta" in e for e in errs)


def test_un_gabarit_inconnu_est_refuse():
    spec = _spec()
    spec["slides"][1]["gabarit"] = "photo"
    assert any("gabarit" in e for e in carrousel_educatif.valider(spec, THEMES))


def test_plus_de_40_mots_crochet_et_tiret_sont_refuses():
    spec = _spec()
    spec["slides"][1]["body"] = " ".join(["mot"] * 41)
    assert any("mots (maximum 40)" in e for e in carrousel_educatif.valider(spec, THEMES))
    spec = _spec()
    spec["slides"][1]["body"] = "Un fait [à confirmer]."
    assert any("placeholder" in e for e in carrousel_educatif.valider(spec, THEMES))
    spec = _spec()
    spec["slides"][1]["body"] = "Un fait — et un tiret."
    assert any("tiret" in e for e in carrousel_educatif.valider(spec, THEMES))


def test_une_liste_porte_deux_a_cinq_items():
    spec = _spec()
    spec["slides"][1] = {"gabarit": "liste", "title": "Liste", "items": ["un"]}
    assert any("2 à 5 items" in e for e in carrousel_educatif.valider(spec, THEMES))


def test_un_texte_qui_deborde_est_refuse_au_rendu():
    spec = _spec()
    theme = THEMES[spec["client"]]
    slide = {"gabarit": "chapitre", "kicker": "Trop long", "title": "Un titre qui prend toute la place possible sur la slide",
             "body": " ".join(["beaucoup"] * 90)}
    with pytest.raises(ValueError, match="déborde"):
        carrousel_educatif.rendre_slide(spec, slide, theme, 2, 7)


def test_le_theme_filmakers_porte_le_bloc_educatif():
    conf = THEMES["otea-filmakers"]["educatif"]
    for champ in ("serie", "mention", "pied", "sauge", "graphite", "mono_family"):
        assert conf.get(champ), champ


def test_les_specs_educatifs_ne_portent_pas_de_photo():
    """Typographique par construction : les images de compétition restent aux reels."""
    for p in SPECS:
        for i, s in enumerate(json.loads(p.read_text(encoding="utf-8"))["slides"], 1):
            assert "photo" not in s, f"{p.name} slide {i}"


def test_la_validation_classique_delegue_au_style_educatif(tmp_path):
    spec = _spec()
    spec["slides"][1]["gabarit"] = "photo"
    chemin = tmp_path / "2026-11-18-x.json"
    chemin.write_text(json.dumps(spec), encoding="utf-8")
    with pytest.raises(ValueError, match="gabarit"):
        carrousel.validate(spec, THEMES, chemin)

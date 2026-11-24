"""Garde-fous de carrousel.py ajoutés le 24/11/2026 (refonte R.O.I. en charte V3)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import carrousel  # noqa: E402


def _theme():
    return carrousel.load_themes()["jlawsongolf"]


def test_kicker_trop_long_refuse():
    slide = {"kicker": "Une mention beaucoup trop longue pour tenir dans la marge", "title": "Titre"}
    with pytest.raises(ValueError, match="kicker"):
        carrousel.render_slide(slide, _theme(), 2, 4, "test")


def test_kicker_court_accepte():
    assert carrousel.render_slide({"kicker": "Guide", "title": "Titre"}, _theme(), 2, 4, "test")

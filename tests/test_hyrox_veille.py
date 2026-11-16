"""Veille résultats HYROX : lecture d'une fiche, textes et créneau, sans réseau."""

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import hyrox_veille as hv  # noqa: E402

# Extrait minimal d'une fiche HYRESULT (Rome 2026, Pierre et Antoine), au format échappé
# du flux Next.js, tel que la page le sert.
PAGE = (
    '<a href="/ranking/s9-2026-rome-hyrox-pro-doubles-men">'
    r'\"place\":\"Rome 2026\",\"athletes\":[{\"slug\":\"pierre-huiban\",\"name\":\"Pierre Huiban\",'
    r'\"claimed\":false},{\"slug\":\"antoine-bouhana\",\"name\":\"Antoine Bouhana\",\"claimed\":false}]'
    r'\"children\":[\"#\",1]}],\"in AG\",\" \",\"35-39\"'
    r'\"name\":\"Total Time\",\"time\":3214,\"rank\":12,\"num_idps\":292'
    r'\"name\":\"Runs\",\"time\":1700,\"rank\":20,\"num_idps\":292'
    r'\"name\":\"Wall Balls\",\"time\":202,\"rank\":10,\"num_idps\":292'
    r'\"name\":\"Row\",\"time\":260,\"rank\":40,\"num_idps\":292'
)
CONFIG = json.loads((ROOT / "hyrox" / "veille.json").read_text(encoding="utf-8"))


def test_lecture_de_la_fiche():
    r = hv.lire_resultat("X", PAGE)
    assert (r["ville"], r["division"], r["temps"]) == ("Rome", "Pro Doubles Men", "53:34")
    assert (r["rang"], r["partants"], r["rang_ag"], r["ag"]) == (12, 292, 1, "35-39")
    assert [a["slug"] for a in r["athletes"]] == ["pierre-huiban", "antoine-bouhana"]
    assert "Runs" not in r["stations"] and r["stations"]["Wall Balls"] == ["3:22", 10]


def test_fiche_sans_chrono_n_est_jamais_postee():
    try:
        hv.lire_resultat("X", PAGE.replace("Total Time", "Autre"))
    except ValueError:
        return
    raise AssertionError("une fiche sans chrono doit être refusée")


def test_textes_ne_disent_que_la_fiche_et_taguent_le_partenaire_une_fois():
    r = hv.lire_resultat("X", PAGE)
    spec, legende = hv.textes(r, CONFIG, CONFIG["comptes"]["pierre-huiban"])
    assert spec["chrono"] == "53:34" and spec["titre"] == ["Age group", "winner."]
    assert legende.count("@antoine_bhna") == 1
    assert "53:34. 12th out of 292, 1st in the 35-39 age group." in legende
    assert "—" not in legende and "LFG" not in legende
    assert "#roadtohongkong" in legende and "#hyroxrome" in legende


def test_creneau_dans_l_heure_et_dans_la_plage():
    paris = hv.PARIS
    t = hv.creneau(dt.datetime(2026, 11, 14, 15, 7, tzinfo=paris), 60, ["07:00", "22:30"])
    assert (t.hour, t.minute) == (16, 15)
    nuit = hv.creneau(dt.datetime(2026, 11, 14, 23, 0, tzinfo=paris), 60, ["07:00", "22:30"])
    assert (nuit.day, nuit.hour, nuit.minute) == (15, 7, 0)


def test_le_stock_photo_de_pierre_est_complet():
    stock = json.loads((ROOT / "photos" / "pierre-huiban.json").read_text(encoding="utf-8"))
    for p in stock["photos"]:
        assert p["provenance"] == "reelle" and p["url"].startswith("https://")
        assert (ROOT / p["masque"]).exists() and p.get("empreinte")

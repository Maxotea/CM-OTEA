"""Crédit des photographes : la règle du 06/11/2026 (Jean-Philippe Homé-Sanfaute)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import credits  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
JP = {"cle": "home-sanfaute", "nom": "Jean-Philippe Homé-Sanfaute", "instagram": "",
      "prefixes_fichier": ["HOME-SANFAUTE"], "dans_credit": ["Homé-Sanfaute"]}


def test_photo_reconnue_par_la_nomenclature_du_fichier():
    e = {"drive_nom": "HOME-SANFAUTE-260702-103350-00186.jpg"}
    assert credits.photographe(e, [JP]) is JP
    assert credits.photographe({"drive_nom": "20260702-maxime.jpg"}, [JP]) is None


def test_legende_creditee_une_seule_fois_avec_le_compte():
    jp = dict(JP, instagram="@compte")
    photos = [{"drive_nom": "HOME-SANFAUTE-1.jpg"}, {"drive_nom": "HOME-SANFAUTE-2.jpg"}]
    une = credits.crediter("Texte.", photos, [jp])
    assert une == "Texte.\n\nPhotos : @compte"
    assert credits.crediter(une, photos, [jp]) == une


def test_sans_compte_le_nom_suffit_et_le_manque_est_signale():
    photos = [{"drive_nom": "HOME-SANFAUTE-1.jpg"}]
    assert credits.ligne_credit(photos, [JP]) == "Photos : Jean-Philippe Homé-Sanfaute"
    assert credits.comptes_manquants(photos, [JP]) == ["Jean-Philippe Homé-Sanfaute"]
    assert credits.crediter("Texte.", [{"drive_nom": "autre.jpg"}], [JP]) == "Texte."


def test_toutes_ses_photos_des_manifestes_sont_creditees():
    ph = credits.charger()
    for nom in ("otea-production", "otea-filmakers"):
        for p in json.loads((ROOT / "photos" / f"{nom}.json").read_text(encoding="utf-8"))["photos"]:
            if (p.get("drive_nom") or "").startswith("HOME-SANFAUTE"):
                assert credits.photographe(p, ph), p["cle"]
                assert "Homé-Sanfaute" in p["credit"], p["cle"]
                assert not any(t in p["credit"] for t in ("—", "–"))


def test_registre_sans_tiret_cadratin():
    texte = (ROOT / "photos" / "photographes.json").read_text(encoding="utf-8")
    assert "—" not in texte and "–" not in texte


def test_formule_linkedin_donnee_par_jean_philippe():
    jp = next(p for p in credits.charger() if p["cle"] == "home-sanfaute")
    photos = [{"drive_nom": "HOME-SANFAUTE-1.jpg"}]
    assert credits.ligne_credit(photos, [jp], reseau="linkedin") == "Photos : @Jean-Philippe Homé-Sanfaute"

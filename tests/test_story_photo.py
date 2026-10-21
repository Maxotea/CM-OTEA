"""Le moteur des stories photo (scripts/story-photo.py) refuse plutôt que de livrer une image fautive.

Images synthétiques uniquement : aucun réseau, aucune photo client. Les polices sont celles du
dépôt (fonts/), que le moteur indexe sans installation.
"""

import copy
import importlib.util
import json
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("story_photo", ROOT / "scripts" / "story-photo.py")
sp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sp)

THEMES = json.loads((ROOT / "scripts" / "themes.json").read_text(encoding="utf-8"))
CARTE = {"cle": "lun", "jour": "Belle semaine", "registre": "VIDÉO D'ENTREPRISE",
         "phrase": "Une vidéo utile commence par un **objectif**, pas par une caméra."}
CARTE_ROI = {"cle": "s4", "jour": "5 ou 10 km à ton rythme", "registre": "L'EFFORT CRÉE LE LIEN",
             "phrase": "Courir d'abord.\n**Parler ensuite.**"}


def _theme(client="otea-production"):
    return copy.deepcopy(THEMES[client])


def _uni(gris):
    return Image.new("RGB", (sp.W, sp.H), (gris, gris, gris))


@pytest.fixture(scope="module")
def rendu_clair():
    return sp.composer(_uni(255), _theme(), CARTE, visages=[], calque=True)


@pytest.fixture(scope="module")
def rendu_sombre():
    return sp.composer(_uni(12), _theme(), CARTE, visages=[], calque=True)


# ---------------------------------------------------------------- tirets et placeholders

@pytest.mark.parametrize("ou, champ, valeur", [
    ("carte", "jour", "Belle semaine — lundi"),
    ("carte", "phrase", "Une vidéo utile – pas une caméra."),
    ("carte", "phrase", "Une vidéo utile -- pas une caméra."),
    ("story", "pied", "DEVIS — LIEN EN BIO"),
    ("story", "nom", "OTEA – PRODUCTION"),
    ("story", "mention", "PARIS -- LA DÉFENSE"),
    ("carte", "phrase", "Rendez-vous le [DATE]."),
])
def test_tirets_et_placeholders_refuses_dans_tous_les_champs(ou, champ, valeur):
    theme, carte = _theme(), dict(CARTE)
    (carte if ou == "carte" else theme["story"])[champ] = valeur
    with pytest.raises(ValueError, match="texte refusé"):
        sp.composer(_uni(40), theme, carte, visages=[])


def test_tiret_dans_le_registre_du_theme_refuse():
    theme = _theme()
    theme["story"]["registre"][1] = "CAPTATION — ÉVÉNEMENT"
    with pytest.raises(ValueError, match=r"story\.registre\[1\]"):
        sp.verifier_textes(theme, CARTE)


def test_registre_inconnu_refuse():
    with pytest.raises(ValueError, match="absent de la liste"):
        sp.verifier_textes(_theme(), dict(CARTE, registre="DRONE"))


def test_les_themes_du_depot_n_affichent_aucun_tiret():
    for client in ("otea-production", "otea-filmakers", "run-on-invest"):
        sp.verifier_textes(THEMES[client], CARTE_ROI if client == "run-on-invest" else
                           dict(CARTE, registre=""))


# ---------------------------------------------------------------- visages

@pytest.mark.parametrize("boite", [
    (400, 300, 640, 560),     # front sous le voile du haut et dans sa rampe
    (400, 700, 640, 960),     # menton dans la rampe du bas
    (380, 1300, 700, 1500),   # en plein sous la phrase
])
def test_visage_coupe_par_l_encre_refuse(boite):
    with pytest.raises(ValueError, match="visage"):
        sp.composer(_uni(40), _theme(), CARTE, visages=[boite])


def test_visage_dans_la_bande_nette_accepte():
    rendu = sp.composer(_uni(40), _theme(), CARTE, visages=[[400, 520, 640, 840]])
    assert rendu["info"]["bande_nette"] == (480, 880)


def test_boites_visage_obligatoires():
    with pytest.raises(ValueError, match="boîtes visage non fournies"):
        sp.composer(_uni(40), _theme(), CARTE, visages=None)


def test_visage_45_sous_le_voile_d_un_carrousel_refuse(monkeypatch):
    theme = _theme()
    entree = {"cle": "p1", "url": "https://exemple.invalid/p1.jpg", "matiere": True,
              "provenance": "client", "visage_45": [[380, 900, 700, 1150]]}
    monkeypatch.setattr(sp.carrousel, "charger_manifeste", lambda th: {"p1": entree})
    monkeypatch.setattr(sp.carrousel, "charger_fond", lambda conf, p, slug: Image.new("RGB", (1080, 1350), (20, 20, 20)))
    spec = {"client": "otea-production", "slug": "essai",
            "slides": [{"title": f"Titre {i}", "body": "Un corps court.", "photo": "p1"} for i in range(4)]}
    with pytest.raises(ValueError, match="sous le voile"):
        sp.verifier_carrousel(spec, theme)
    entree["visage_45"] = [[380, 60, 700, 260]]
    sp.verifier_carrousel(spec, theme)
    del entree["visage_45"]
    with pytest.raises(ValueError, match="visage_45 absente"):
        sp.verifier_carrousel(spec, theme)


# ---------------------------------------------------------------- contraste

def _toutes_les_cibles_tenues(mesures):
    assert mesures, "aucune mesure"
    for element, (contraste, cible) in mesures.items():
        assert contraste >= cible, f"{element} : {contraste}:1 pour une cible de {cible}:1"


def test_contraste_atteint_sur_une_image_claire(rendu_clair):
    _toutes_les_cibles_tenues(rendu_clair["mesures"])
    assert rendu_clair["mesures"]["phrase"][1] == 7.0
    assert rendu_clair["mesures"]["registre_actif"][1] == 4.5
    assert rendu_clair["mesures"]["kicker"][1] == 3.0
    haut, bas = rendu_clair["voile"]
    assert 0.8 < haut <= sp.VOILE_MAX and 0.8 < bas <= sp.VOILE_MAX


def test_contraste_atteint_sur_une_image_sombre_sans_voile_inutile(rendu_sombre):
    _toutes_les_cibles_tenues(rendu_sombre["mesures"])
    assert rendu_sombre["voile"] == (0.35, 0.55)


def test_voile_du_calque_calcule_sur_la_photo(rendu_clair, rendu_sombre):
    for rendu in (rendu_clair, rendu_sombre):
        attendu = tuple(round(min(1.0, v + sp.MARGE_CALQUE), 2) for v in rendu["voile"])
        assert rendu["voile_calque"] == attendu
        assert rendu["calque"].mode == "RGBA"
        _toutes_les_cibles_tenues(rendu["mesures_calque"])
    assert rendu_clair["voile_calque"] != rendu_sombre["voile_calque"]


def test_controle_des_frames_sous_le_voile_du_calque(rendu_sombre):
    bilan = sp.controler_images([_uni(12), _uni(255)], rendu_sombre)
    assert not bilan["frame 1"]["manques"]
    assert bilan["frame 2"]["manques"], "une frame blanche sous un voile calculé pour du noir doit échouer"


def test_grain_mesure_et_registre_souligne_si_l_accent_ne_tient_pas():
    """R.O.I. : grain 26 posé avant la mesure ; sur fond blanc, le Blaze ne tient pas 4,5:1 sur
    le registre une fois le grain posé, l'élément allumé passe en Craie souligné de Blaze."""
    rendu = sp.composer(_uni(255), _theme("run-on-invest"), CARTE_ROI, visages=[])
    _toutes_les_cibles_tenues(rendu["mesures"])
    assert rendu["info"]["registre_souligne"] is True
    assert "souligne" in rendu["mesures"]


def test_rampes_smoothstep_sans_cassure():
    masque = sp.voile(0.9, 0.9)
    colonne = [masque.getpixel((0, y)) for y in range(sp.H)]
    pas = [abs(b - a) for a, b in zip(colonne, colonne[1:])]
    assert max(pas) <= 3
    assert colonne[sp.HAUT_PLEIN + 1] >= colonne[sp.HAUT_PLEIN] - 1
    assert colonne[600] == 0 and colonne[1500] == round(0.9 * 255)


def test_source_trop_petite_refusee():
    with pytest.raises(ValueError, match="source trop petite"):
        sp.composer(Image.new("RGB", (1440, 960), (40, 40, 40)), _theme(), CARTE, visages=[])


# ---------------------------------------------------------------- polices

def test_police_introuvable_erreur_explicite():
    with pytest.raises(sp.PoliceIntrouvable, match="police introuvable : Police Absente Black"):
        sp.police(["Police Absente Black"], 40)


def test_police_introuvable_au_rendu_sans_repli():
    theme = _theme()
    theme["story"]["polices"]["titre"] = ["Forma DJR Display Inexistante"]
    with pytest.raises(sp.PoliceIntrouvable, match="aucun repli"):
        sp.composer(_uni(40), theme, CARTE, visages=[])


def test_polices_des_trois_themes_presentes_dans_le_depot():
    for client in ("otea-production", "otea-filmakers", "run-on-invest"):
        for noms in THEMES[client]["story"]["polices"].values():
            chemin = Path(sp.police(noms, 30).path)
            assert chemin.is_relative_to(ROOT / "fonts"), f"{client} {noms} : {chemin} hors du dépôt"
    assert not list((ROOT / "fonts").rglob("*orma*")), "aucun fichier Forma DJR dans le dépôt"


# ---------------------------------------------------------------- provenance

def test_photo_ia_refusee_hors_run_on_invest(monkeypatch):
    entree = {"cle": "ia1", "url": "https://exemple.invalid/ia1.jpg", "provenance": "ia",
              "personne_identifiable": False, "matiere": True}
    monkeypatch.setattr(sp.carrousel, "charger_manifeste", lambda th: {"ia1": entree})
    for client in ("otea-production", "otea-filmakers"):
        with pytest.raises(ValueError, match="image IA"):
            sp.charger_photo("ia1", _theme(client))
    entree["personne_identifiable"] = True
    with pytest.raises(ValueError, match="personne identifiable"):
        sp.charger_photo("ia1", _theme("run-on-invest"))


def test_story_ne_part_jamais_d_un_fond_prepare(monkeypatch):
    entree = {"cle": "cle-sans-original-12-10", "url": "https://exemple.invalid/fond-4-5.jpg",
              "provenance": "client", "matiere": True}
    monkeypatch.setattr(sp.carrousel, "charger_manifeste", lambda th: {"x": entree})
    with pytest.raises(ValueError, match="jamais du fond 4:5"):
        sp.charger_photo("x", _theme())


# ---------------------------------------------------------------- logotype

def test_logotype_pose_et_mesure_dans_le_masque_du_haut(tmp_path):
    logo = Image.new("RGBA", (300, 100), (0, 0, 0, 0))
    logo.paste((241, 241, 241, 255), (10, 10, 290, 90))
    logo.save(tmp_path / "logo.png")
    theme = _theme()
    theme["story"]["logo"]["fichier"] = str(tmp_path / "logo.png")
    rendu = sp.composer(_uni(255), theme, CARTE, visages=[])
    assert rendu["info"]["nom"] == "logotype" and rendu["secours"] is None
    x0, y0, x1, y1 = rendu["masques"]["nom"].getbbox()
    assert 96 <= x0 <= 101 and 250 <= y0 <= 255 and y1 <= 290      # 40 px de haut, posé à (96, 250)
    assert rendu["mesures"]["nom"][0] >= 4.5


def test_logotype_absent_secours_signale(tmp_path):
    theme = _theme()
    theme["story"]["logo"]["fichier"] = str(tmp_path / "absent.png")
    rendu = sp.composer(_uni(40), theme, CARTE, visages=[])
    assert rendu["info"]["nom"] == "nom saisi (SECOURS)"
    assert "SECOURS" in rendu["secours"]

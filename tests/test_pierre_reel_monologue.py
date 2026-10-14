"""Gabarit « monologue » de scripts/pierre-reel-ralenti.py (référence @rundadlift
DeHgY1RxPfB, demande de Maxime du 13/10/2026).

Découpage et horodatage des mots, refus des tirets, couleurs, position du bloc,
contraste mesuré sous le texte, lecture des rushes par URL. Sans réseau ni rush :
les fonds sont synthétiques et le relais HTTP est nourri par une fausse source.
Les deux rendus vidéo de bout en bout ne tournent que si ffmpeg est présent.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("pierre_reel_ralenti",
                                               ROOT / "scripts" / "pierre-reel-ralenti.py")
prr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(prr)

POLICES = str(ROOT / "fonts")
W, H, Y0 = prr.W, prr.H, prr.BANDE[0]
CLES_SOUS_TITRE = ("horodatages", "tenue", "mot_en_cours")


def bloc(lignes, t=0.0, fin=3.0, jaunes=(), **opts):
    st = {"t": t, "fin": fin, "lignes": lignes,
          "mots_jaunes": jaunes if isinstance(jaunes, str) else list(jaunes)}
    st.update({k: v for k, v in opts.items() if k in CLES_SOUS_TITRE})
    return prr.preparer_bloc(st, POLICES, {k: v for k, v in opts.items() if k not in CLES_SOUS_TITRE})


def coeur(m):
    """Pixels de la bande au cœur des lettres d'un mot (glyphe pleinement opaque)."""
    y, x, g, _ = m.couche
    ys, xs = np.nonzero(g >= 1.0)
    assert len(ys), m.texte
    return ys + y, xs + x


def encre(img, seuil=8):
    """Boîte de l'encre (pixels du calque nettement plus clairs que le halo noir)."""
    a = np.asarray(img)
    m = (a[..., 3] > 200) & (a[..., :3].max(axis=-1) > 150)
    ys, xs = np.nonzero(m)
    return xs.min(), xs.max(), ys.min(), ys.max()


# ---------------------------------------------------------------- découpage et horodatage

def test_decoupage_dans_l_ordre_de_lecture():
    mots = prr.decouper(["He won't remember", "Rome, or 53:34."])
    assert mots == [(0, "He"), (0, "won't"), (0, "remember"), (1, "Rome,"), (1, "or"), (1, "53:34.")]


def test_horodatage_proportionnel_a_la_longueur_des_mots():
    # 1 + 3 + 2 lettres sur 1,2 s : 0,2 s par lettre
    assert prr.horodater(["a", "bbb", "cc"], 1.0, 2.2) == [1.0, 1.2, 1.8]
    inst = prr.horodater(["Some", "sessions", "are", "average."], 0.0, 4.0)
    ecarts = np.diff(inst + [4.0])
    assert np.allclose(ecarts / ecarts.sum(), np.array([4, 8, 3, 8]) / 23, atol=1e-3)


def test_horodatage_avec_tenue_du_bloc_complet():
    assert prr.horodater(["aa", "bb"], 0.0, 3.0, tenue=1.0) == [0.0, 1.0]
    with pytest.raises(SystemExit):
        prr.horodater(["aa"], 2.0, 2.5, tenue=0.5)


def test_horodatages_explicites_et_controles():
    b = bloc(["Some sessions"], 0.0, 2.0, horodatages=[0.2, 0.9])
    assert [m.t for m in b.mots] == [0.2, 0.9]
    with pytest.raises(SystemExit, match="horodatages"):
        bloc(["Some sessions"], 0.0, 2.0, horodatages=[0.2])
    with pytest.raises(SystemExit, match="horodatages"):
        bloc(["Some sessions"], 0.0, 2.0, horodatages=[0.9, 0.2])


def test_le_format_textes_du_chantier_est_accepte():
    spec = {"textes": [{"debut": 0.4, "fin": 3.8, "texte": "He won't remember\nRome, or 53:34.",
                        "jaunes": ["53:34."], "mots": [{"mot": m, "t": 0.4 + 0.4 * i} for i, m in
                                                        enumerate("He won't remember Rome, or 53:34.".split())]}]}
    st = prr.sous_titres_de(spec)[0]
    assert st["lignes"] == ["He won't remember", "Rome, or 53:34."]
    assert st["horodatages"][0] == 0.4 and len(st["horodatages"]) == 6
    b = prr.preparer_bloc(st, POLICES)
    assert [m.jaune for m in b.mots] == [False] * 5 + [True]


# ---------------------------------------------------------------- refus

@pytest.mark.parametrize("tiret", ["\u2014", "\u2013", "--"])
def test_refus_des_tirets(tiret):
    with pytest.raises(SystemExit, match="tiret"):
        bloc([f"Rome {tiret} 53:34"])
    with pytest.raises(SystemExit, match="tiret"):
        prr.preparer_sous_titres({"sous_titres": [{"t": 0, "fin": 2, "lignes": ["Rome"]}],
                                  "legende": f"Rome {tiret} 53:34"}, POLICES)
    with pytest.raises(SystemExit, match="tiret"):
        prr.verifier_tirets(f"a{tiret}b")


def test_trait_d_union_simple_permis():
    b = bloc(["First of the 35-39."], jaunes=["35-39"])
    assert [m.texte for m in b.mots if m.jaune] == ["35-39."]


def test_refus_de_trois_lignes_et_d_une_ligne_trop_large():
    with pytest.raises(SystemExit, match="deux lignes"):
        bloc(["one", "two", "three"])
    with pytest.raises(SystemExit, match="trop large"):
        bloc(["Because I know there will come a day when"])


def test_refus_des_sous_titres_qui_se_chevauchent_et_de_la_voix():
    spec = {"sous_titres": [{"t": 0, "fin": 2, "lignes": ["Not most"]},
                            {"t": 1.5, "fin": 3, "lignes": ["nights"]}]}
    with pytest.raises(SystemExit, match="chevauchent"):
        prr.preparer_sous_titres(spec, POLICES)
    spec = {"sous_titres": [{"t": 0, "fin": 2, "lignes": ["Not most"]}], "voix": [{"fichier": "x.mp3"}]}
    with pytest.raises(SystemExit, match="muet"):
        prr.preparer_sous_titres(spec, POLICES)


def test_mots_jaunes_casse_ponctuation_et_suites():
    b = bloc(["I want him to see", "me show up anyway."], jaunes=["SHOW UP", "anyway"])
    assert [m.texte for m in b.mots if m.jaune] == ["show", "up", "anyway."]
    assert all(bloc(["Not most nights"], jaunes="*").mots[k].jaune for k in range(3))
    with pytest.raises(SystemExit, match="introuvable"):
        bloc(["Not most nights"], jaunes=["days"])


# ---------------------------------------------------------------- couleurs et allumage

def test_couleurs_blanc_casse_et_jaune():
    b = bloc(["He won't remember", "Rome, or 53:34."], 0.0, 5.0, jaunes=["53:34"], fondu_sortie=0)
    calque = prr.composer([b], 4.9)
    for m in b.mots:
        ys, xs = coeur(m)
        px = calque[ys, xs]
        assert (px[:, 3] == 255).all()
        attendu = prr.JAUNE_MONO if m.jaune else prr.BLANC_CASSE
        assert (np.abs(px[:, :3].astype(int) - attendu) <= 1).all(), m.texte
    assert prr.JAUNE_MONO == (242, 209, 36)


def test_allumage_mot_a_mot_avec_fondu_court():
    b = bloc(["Some sessions", "are average."], 0.0, 4.0, fondu_sortie=0)
    k = 2                                   # « are »
    t = b.mots[k].t
    ys, xs = coeur(b.mots[k])
    assert (prr.composer([b], t - 0.01)[ys, xs, 3] == 0).all()
    mi = prr.composer([b], t + prr.FONDU / 2)[ys, xs, 3]
    assert 100 < np.median(mi) < 160      # à mi-fondu
    assert (prr.composer([b], t + prr.FONDU)[ys, xs, 3] == 255).all()
    # les mots déjà allumés ne bougent pas quand le suivant arrive
    ys0, xs0 = coeur(b.mots[0])
    avant = prr.composer([b], t - 0.01)[ys0, xs0]
    apres = prr.composer([b], t + prr.FONDU)[ys0, xs0]
    assert (avant == apres).all()
    # le bloc disparaît à `fin` (coupe sèche ici)
    assert prr.composer([b], 4.0)[..., 3].max() == 0


def test_fondu_de_sortie_du_bloc():
    b = bloc(["Not most nights"], 0.0, 3.0)
    ys, xs = coeur(b.mots[0])
    assert np.median(prr.composer([b], 3.0 - prr.FONDU / 2)[ys, xs, 3]) < 160


def test_mot_en_cours_en_jaune_facon_karaoke():
    b = bloc(["Some sessions are"], 0.0, 3.0, mot_en_cours=True, fondu_sortie=0)
    t1 = b.mots[1].t + prr.FONDU
    calque = prr.composer([b], t1)
    for k, attendu in ((0, prr.BLANC_CASSE), (1, prr.JAUNE_MONO)):
        ys, xs = coeur(b.mots[k])
        assert (np.abs(calque[ys, xs, :3].astype(int) - attendu) <= 1).all()


# ---------------------------------------------------------------- position

def test_bloc_d_une_ligne_centre_a_la_hauteur_mesuree():
    b = bloc(["Some sessions"], 0.0, 3.0, jaunes="*", fondu_sortie=0)
    x0, x1, y0, y1 = encre(prr.composer([b], 2.9))
    assert abs((x0 + x1) / 2 - W / 2) <= 2
    base = H * 0.7588                      # ligne de base mesurée sur la référence
    assert abs(b.mots[0].base - base) < 0.01
    assert abs((y1 + Y0) - base) <= 3      # pas de jambage : l'encre s'arrête sur la base
    assert abs((y0 + Y0 + y1 + Y0) / 2 / H - 0.75) < 0.006


def test_bloc_de_deux_lignes_aux_proportions_de_la_reference():
    b = bloc(["Because I know there", "will come a day"], 0.0, 3.0, jaunes="*", fondu_sortie=0)
    x0, x1, y0, y1 = encre(prr.composer([b], 2.99))
    # référence DeH2T6FOUuJ : encre de 0,7165 à 0,7835 H, bloc centré à 0,750 H
    assert abs((y0 + Y0) / H - 0.7165) < 0.004
    assert abs((y1 + Y0) / H - 0.7835) < 0.004
    bases = sorted({round(m.base, 2) for m in b.mots})
    assert abs(bases[1] - bases[0] - H * 0.0352) < 0.01
    for i in (0, 1):
        mots = [m for m in b.mots if m.ligne == i]
        gauche, droite = mots[0].x, mots[-1].x + mots[-1].largeur
        assert abs((gauche + droite) / 2 - W / 2) < 0.5


def test_ligne_incomplete_deja_a_sa_place_definitive():
    """La 2e ligne en cours d'allumage paraît décalée à gauche, comme sur la référence :
    chaque ligne est centrée sur son texte complet, les mots ne bougent jamais."""
    b = bloc(["Because I know there", "will come a day"], 0.0, 3.0, jaunes="*", fondu_sortie=0)
    t = b.mots[5].t + prr.FONDU             # « will come » allumés, « a day » pas encore
    calque = prr.composer([b], t)
    bande = calque[int(b.mots[4].base) - Y0 - 50:int(b.mots[4].base) - Y0 + 5]
    ys, xs = np.nonzero((bande[..., 3] > 200) & (bande[..., :3].max(axis=-1) > 150))
    assert (xs.min() + xs.max()) / 2 < W / 2 - 40
    assert abs(xs.min() - b.mots[4].x) < 8


# ---------------------------------------------------------------- contraste

def test_fond_sombre_sans_voile():
    b = bloc(["He won't remember", "Rome, or 53:34."], jaunes=["53:34"])
    fond = np.full((prr.BANDE[1] - Y0, W, 3), 60, np.uint8)
    voile, c = prr.regler_voile(b, fond)
    assert voile == 0 and c >= prr.CONTRASTE_CIBLE


def test_fond_clair_voile_local_leger():
    b = bloc(["He won't remember", "Rome, or 53:34."], jaunes=["53:34"])
    fond = np.full((prr.BANDE[1] - Y0, W, 3), 255, np.uint8)
    assert prr.mesurer_contraste(b, fond, 0.0) < prr.CONTRASTE_CIBLE
    voile, c = prr.regler_voile(b, fond)
    assert 0 < voile <= prr.VOILE_MAX and c >= prr.CONTRASTE_CIBLE
    # le voile est bien dessiné derrière le bloc, et seulement autour
    calque = prr.composer([b], 2.9)
    assert calque[..., 3].max() > 0
    assert calque[:5, :, 3].max() == 0 and calque[:, :5, 3].max() == 0


def test_cible_inatteignable_signalee():
    b = bloc(["Not most nights"], jaunes="*", voile_max=0.02)
    fond = np.full((prr.BANDE[1] - Y0, W, 3), 255, np.uint8)
    voile, c = prr.regler_voile(b, fond)
    assert voile == 0.02 and c < prr.CONTRASTE_CIBLE


def test_contraste_au_pire_pixel():
    """Un seul point blanc sous une lettre suffit à faire tomber la mesure."""
    b = bloc(["Not most nights"], jaunes="*")
    fond = np.full((prr.BANDE[1] - Y0, W, 3), 30, np.uint8)
    haut = prr.mesurer_contraste(b, fond, 0.0)
    ys, xs = coeur(b.mots[1])
    fond[ys[0], xs[0]] = 255
    assert prr.mesurer_contraste(b, fond, 0.0) < haut


# ---------------------------------------------------------------- image

def test_filtre_noir_et_blanc():
    f = prr.filtre_nb_monologue()
    assert f.startswith("hue=s=0,curves=master=") and "noise=c0s=6:c0f=t" in f
    assert f.endswith("format=gray") and "eq=" not in f
    assert "eq=contrast=1.2" in prr.filtre_nb_monologue(contraste=1.2)
    assert "noise" not in prr.filtre_nb_monologue(grain=0)


# ---------------------------------------------------------------- rushes à distance

def test_source_rush_url_index_et_local(tmp_path, monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:9999")
    url, entree = prr.source_rush("https://exemple.invalid/rush.mp4", str(tmp_path))
    assert url == "https://exemple.invalid/rush.mp4" and entree == ["-http_proxy", "http://127.0.0.1:9999"]
    index = {"FX3POST20260926_7351.MP4": "ID7351"}
    url, entree = prr.source_rush("7351", str(tmp_path), index)
    assert url == "https://drive.usercontent.google.com/download?id=ID7351&export=download&confirm=t"
    (tmp_path / "FX3POST20260926_7374.MP4").write_bytes(b"")
    chemin, entree = prr.source_rush("7374", str(tmp_path), index)
    assert chemin.endswith("FX3POST20260926_7374.MP4") and entree == []
    for k in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        monkeypatch.delenv(k, raising=False)
    assert prr.source_rush("7351", str(tmp_path), index)[1] == []


@pytest.mark.parametrize("contenu", [
    {"_doc": "x", "clips": [{"clip": "FX3POST20260926_7351.MP4", "id": "A"}]},
    [{"name": "FX3POST20260926_7351.MP4", "id": "A"}],
    {"FX3POST20260926_7351.MP4": "A"},
    {"FX3POST20260926_7351.MP4": {"id": "A"}},
])
def test_index_drive_formats(tmp_path, contenu):
    p = tmp_path / "index.json"
    p.write_text(json.dumps(contenu), encoding="utf-8")
    assert prr.trouver_dans_index(prr.charger_index_drive(str(p)), "7351") == "A"


def test_relais_ne_demande_que_des_plages_bornees(tmp_path):
    blob = os.urandom(5 * 1024 * 1024 + 123)
    appels = []

    def fausse_source(url, a, b):
        appels.append((a, b))
        return blob[a:b + 1], len(blob)

    relais = prr.Relais(str(tmp_path / "cache"), telecharger=fausse_source, bloc=1024 * 1024)
    ouvreur = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        adresse = relais.adresse("https://exemple.invalid/rush.mp4")
        req = urllib.request.Request(adresse, headers={"Range": "bytes=1500000-"})
        with ouvreur.open(req, timeout=30) as r:
            assert r.status == 206
            assert r.headers["Content-Range"] == f"bytes 1500000-{len(blob) - 1}/{len(blob)}"
            assert r.read() == blob[1500000:]
        assert all(b - a + 1 <= 1024 * 1024 for a, b in appels)
        n = len(appels)
        req = urllib.request.Request(adresse, headers={"Range": "bytes=2000000-2000099"})
        with ouvreur.open(req, timeout=30) as r:
            assert r.read() == blob[2000000:2000100]
        assert len(appels) == n             # servi depuis le cache disque
    finally:
        relais.fermer()


# ---------------------------------------------------------------- rendus de bout en bout

FFMPEG = prr.binaire_ffmpeg()
avec_ffmpeg = pytest.mark.skipif(not (shutil.which(FFMPEG) or os.path.exists(FFMPEG)),
                                 reason="ffmpeg absent")


def _rush_synthetique(dossier):
    subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=1920x1080:rate=100", "-t", "0.6", "-pix_fmt", "yuv420p",
                    "-c:v", "libx264", "-preset", "ultrafast",
                    str(dossier / "FX3POST20260926_9999.MP4")], check=True)


def _infos(chemin):
    return subprocess.run([FFMPEG, "-hide_banner", "-i", str(chemin)],
                          capture_output=True, text=True).stderr


def _image(chemin, t):
    out = subprocess.run([FFMPEG, "-v", "error", "-ss", str(t), "-i", str(chemin), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.uint8).reshape(H, W, 3)


@avec_ffmpeg
def test_rendu_monologue_muet_noir_et_blanc(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _rush_synthetique(tmp_path)
    spec = {"gabarit": "monologue", "sortie": "m.mp4", "ralenti": 4, "flou_bouge": 2,
            "plans": [{"clip": "9999", "debut": 0, "duree": 0.5, "slog3": False}],
            "sous_titres": [{"t": 0.2, "fin": 1.9, "lignes": ["Not most nights"],
                             "mots_jaunes": ["nights"]}]}
    total = prr.monter(spec, str(tmp_path), POLICES, str(tmp_path / "absente.cube"))
    assert total == 2.0
    infos = _infos(tmp_path / "m.mp4")
    assert "1080x1920" in infos and "25 fps" in infos and "yuv420p" in infos
    assert "Audio" not in infos
    img = _image(tmp_path / "m.mp4", 1.7).astype(int)
    b = prr.preparer_sous_titres(spec, POLICES, total)[0]
    ys, xs = coeur(b.mots[2])
    px = img[ys + Y0, xs]
    assert np.median(px[:, 0]) > 200 and np.median(px[:, 2]) < 110      # « nights » jaune
    hors_texte = img[:Y0 - 100]
    assert np.abs(hors_texte[..., 0] - hors_texte[..., 2]).mean() < 2   # image en N&B


def test_carton_reconnu_et_duree_a_l_ecran():
    assert prr.carton_du_plan({"clip": "CARTON NOIR", "duree": 0.88}) == "noir"
    assert prr.carton_du_plan({"carton": "noir", "duree": 0.88}) == "noir"
    assert prr.carton_du_plan({"clip": "7351", "duree": 0.5}) is None
    with pytest.raises(SystemExit, match="carton inconnu"):
        prr.carton_du_plan({"clip": "CARTON ROSE", "duree": 1})
    spec = {"ralenti": 4}
    assert prr.duree_ecran({"clip": "CARTON NOIR", "duree": 0.88}, spec) == 0.88      # pas ×4
    assert prr.duree_ecran({"clip": "CARTON NOIR", "duree": 0.5, "ralenti": 2}, spec) == 1.0
    assert prr.duree_ecran({"clip": "7351", "duree": 0.5}, spec) == 2.0


@avec_ffmpeg
def test_carton_noir_sans_rush_entre_deux_plans(tmp_path, monkeypatch):
    """Un carton ne lit aucun rush (ni local ni Drive), s'enchaîne aux plans et porte
    son sous-titre ; la vidéo reste muette, à la bonne durée, image près."""
    monkeypatch.chdir(tmp_path)
    _rush_synthetique(tmp_path)
    vus = []

    def sources(clip):
        vus.append(clip)
        return prr.trouver_rush(str(tmp_path), clip), []
    spec = {"gabarit": "monologue", "sortie": "c.mp4", "ralenti": 4,
            "plans": [{"clip": "9999", "debut": 0, "duree": 0.25, "slog3": False},
                      {"clip": "CARTON NOIR", "debut": 0, "duree": 0.88, "ralenti": 1},
                      {"clip": "9999", "debut": 0.2, "duree": 0.38, "ralenti": 2, "slog3": False}],
            "sous_titres": [{"t": 1.08, "fin": 1.8, "lignes": ["RUN 1 4:24"], "mots_jaunes": ["4:24"]}]}
    total = prr.monter_monologue(spec, sources, POLICES, str(tmp_path / "absente.cube"))
    # ralenti ×2 d'un rush 100p : 0,38 s → 19 images exactement (pas 20), aucune dérive des coupes
    assert abs(total - 2.64) < 1e-9 and vus == ["9999", "9999"]
    assert "Duration: 00:00:00.76" in _infos(tmp_path / "_plan2.mp4")
    assert "Duration: 00:00:02.64" in _infos(tmp_path / "_base.mp4")
    infos = _infos(tmp_path / "c.mp4")
    assert "1080x1920" in infos and "Audio" not in infos and "Duration: 00:00:02.64" in infos
    img = _image(tmp_path / "c.mp4", 1.6).astype(int)
    assert img[:Y0 - 100].mean() < 25                                      # fond noir, grain léger
    b = prr.preparer_sous_titres(spec, POLICES, total)[0]
    ys, xs = coeur(b.mots[2])
    px = img[ys + Y0, xs]
    assert np.median(px[:, 0]) > 200 and np.median(px[:, 2]) < 110          # « 4:24 » jaune


def _plage(chemin):
    """« pc » (plage pleine, yuvj420p) ou « tv » (plage limitée) du flux vidéo."""
    ligne = next(l for l in _infos(chemin).splitlines() if "Video:" in l)
    return "pc" if ("(pc" in ligne or "yuvj" in ligne) else "tv"


@avec_ffmpeg
def test_carton_noir_reste_noir_apres_un_rush_fx3_plage_pleine(tmp_path, monkeypatch):
    """Les rushes FX3 sont en 4:2:2 10 bits plage PLEINE (pc). Sans conversion, le plan
    sortait en yuvj420p, la concaténation en copie gardait ce drapeau pour toute la base,
    et le carton (plage limitée) sortait gris foncé : médiane 17/255 mesurée le 13/10/2026
    sur 7351 suivi d'un CARTON NOIR. Tous les morceaux doivent sortir en plage limitée."""
    monkeypatch.chdir(tmp_path)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=1920x1080:rate=100", "-t", "0.6",
                    "-pix_fmt", "yuv422p10le", "-color_range", "pc",
                    "-c:v", "libx264", "-preset", "ultrafast",
                    str(tmp_path / "FX3POST20260926_9998.MP4")], check=True)
    assert _plage(tmp_path / "FX3POST20260926_9998.MP4") == "pc"
    spec = {"gabarit": "monologue", "sortie": "n.mp4", "ralenti": 4,
            "plans": [{"clip": "9998", "debut": 0, "duree": 0.25, "slog3": False},
                      {"clip": "CARTON NOIR", "duree": 1.0}],
            "sous_titres": [{"t": 0.2, "fin": 0.9, "lignes": ["Test"], "mots_jaunes": []}]}
    total = prr.monter(spec, str(tmp_path), POLICES, str(tmp_path / "absente.cube"))
    assert total == 2.0
    for f in ("_plan0.mp4", "_plan1.mp4", "_base.mp4", "n.mp4"):
        assert _plage(tmp_path / f) == "tv", f
    carton = _image(tmp_path / "n.mp4", 1.5).astype(int)
    assert np.median(carton) < 5                                           # noir, pas gris
    plan = _image(tmp_path / "n.mp4", 0.5).astype(int)
    assert plan.max() > 150                                                # le plan garde ses blancs


@avec_ffmpeg
def test_gabarit_reel_inchange(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _rush_synthetique(tmp_path)
    spec = {"gabarit": "reel", "sortie": "r.mp4", "ralenti": 4,
            "plans": [{"clip": "9999", "debut": 0, "duree": 0.25, "slog3": False}],
            "textes": [{"debut": 0.1, "fin": 0.9, "texte": "Station eight."}]}
    assert prr.monter(spec, str(tmp_path), POLICES, "absente.cube") == 1.0
    infos = _infos(tmp_path / "r.mp4")
    assert "1080x1920" in infos and "Audio" not in infos
    spec["textes"][0]["texte"] = "Station \u2014 eight."
    with pytest.raises(SystemExit, match="tiret"):
        prr.monter(spec, str(tmp_path), POLICES, "absente.cube")


def test_police_du_depot_d_abord_pour_le_monologue(tmp_path):
    """Une Fraunces quelconque posée à plat dans --polices (coupe opsz 9 du Mac, un
    tiers plus large) ne doit pas remplacer l'instance calibrée du dépôt."""
    shutil.copy(ROOT / "fonts" / "fraunces" / "Fraunces-Regular.ttf", tmp_path / "Fraunces-SemiBold.ttf")
    depot = str(ROOT / "fonts" / "fraunces" / "Fraunces-SemiBold.ttf")
    assert prr.fichier_police(str(tmp_path), "Fraunces-SemiBold.ttf", True) == depot
    assert prr.fichier_police(str(tmp_path), "Fraunces-SemiBold.ttf") == str(tmp_path / "Fraunces-SemiBold.ttf")
    assert prr.fichier_police(str(tmp_path), "Fraunces-Regular.ttf").endswith("fonts/fraunces/Fraunces-Regular.ttf")
    with pytest.raises(SystemExit, match="introuvable"):
        prr.fichier_police(str(tmp_path), "Absente.ttf")


def test_rampe_du_plan_controlee():
    assert prr.rampe_du_plan({"clip": "7378", "debut": 1.6, "duree": 1.18}) is None
    p = {"clip": "7378", "debut": 1.6, "duree": 1.18, "exposition": 65, "exposition_fin": 25}
    assert prr.rampe_du_plan(p) == (1.6, pytest.approx(2.78))
    assert prr.rampe_du_plan(dict(p, rampe=[2.15, 2.78])) == (2.15, 2.78)
    with pytest.raises(SystemExit, match="hors du plan"):
        prr.rampe_du_plan(dict(p, rampe=[2.15, 3.0]))
    with pytest.raises(SystemExit, match="hors du plan"):
        prr.rampe_du_plan(dict(p, rampe=[2.5, 2.2]))
    with pytest.raises(SystemExit, match="sans `exposition_fin`"):
        prr.rampe_du_plan({"clip": "7378", "debut": 1.6, "duree": 1.18, "rampe": [1.7, 2.0]})


@avec_ffmpeg
def test_rampe_d_exposition_sur_un_plan_log(tmp_path, monkeypatch):
    """M1-R7 carte 2 (14/10/2026) : le plan passe d'un fond noir à la zone FINISH éclairée ;
    une exposition unique laissait le début trop sombre ou brûlait la fin. Avec
    `exposition_fin` et `rampe`, l'exposition reste celle de départ avant la rampe, finit à
    `exposition_fin`, et passe progressivement de l'une à l'autre, sans rien changer d'autre."""
    monkeypatch.chdir(tmp_path)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "lavfi", "-i",
                    "color=c=0x606060:size=1920x1080:rate=100", "-t", "1.2", "-pix_fmt", "yuv420p",
                    "-c:v", "libx264", "-preset", "ultrafast",
                    str(tmp_path / "FX3POST20260926_9997.MP4")], check=True)
    lut = str(tmp_path / "slog3.cube")
    prr.ecrire_lut(lut)

    def medianes(nom, **cles):
        spec = {"gabarit": "monologue", "sortie": nom, "ralenti": 4, "grain": 0,
                "plans": [dict({"clip": "9997", "debut": 0.1, "duree": 0.5, "exposition": 1}, **cles)],
                "sous_titres": [{"t": 0.2, "fin": 1.9, "lignes": ["Test"], "mots_jaunes": []}]}
        assert prr.monter(spec, str(tmp_path), POLICES, lut) == 2.0
        assert "Audio" not in _infos(tmp_path / nom)
        # secondes du reel : rush 0,1 + t / 4 ; la rampe [0,3 ; 0,5] du rush tombe de 0,8 à 1,6 s
        return [float(np.median(_image(tmp_path / nom, t)[:Y0 - 100])) for t in (0.1, 0.5, 1.0, 1.3, 1.7, 1.9)]

    fixe = medianes("fixe.mp4")
    fort = medianes("fort.mp4", exposition=8)
    egale = medianes("egale.mp4", exposition_fin=1)
    rampe = medianes("rampe.mp4", exposition_fin=8, rampe=[0.3, 0.5])
    assert max(fixe) - min(fixe) < 2 and fort[0] > fixe[0] + 30          # le fond uni ne bouge pas
    assert all(abs(e - f) < 1.5 for e, f in zip(egale, fixe))              # rampe neutre : image inchangée
    assert abs(rampe[0] - fixe[0]) < 1.5 and abs(rampe[1] - fixe[1]) < 1.5  # avant 0,3 s du rush
    assert fixe[2] + 5 < rampe[2] < rampe[3] < fort[3] - 5                 # pendant la rampe, progressive
    assert abs(rampe[4] - fort[4]) < 1.5 and abs(rampe[5] - fort[5]) < 1.5  # après 0,5 s du rush

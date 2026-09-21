"""Le montage de reel se règle sans ffmpeg : grille de durées, décision stéréo,
gain, correction d'exposition, lecture des scènes dans les noms, répartition
des plans. Ce sont les règles qui garantissent « 90 s, stéréo, homogène »."""

import importlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
rm = importlib.import_module("reel-montage")


def _somme(durees):
    return sum(durees) - (len(durees) - 1) * rm.TRANSITION


def test_grille_tombe_sur_la_duree():
    for total in (30, 60, 90):
        for carton in (False, True):
            d = rm.grille_durees(total, carton)
            assert abs(_somme(d) - total) < 1e-6
            assert d[0] == rm.DUREE_ACCROCHE
            if carton:
                assert d[-1] == rm.DUREE_CARTON
            assert all(rm.PLAN_MIN - 0.01 <= x for x in d[1:-1])


def test_grille_se_resserre():
    d = rm.grille_durees(90, False)
    milieu = d[1:-1]
    assert milieu == sorted(milieu, reverse=True)


def test_decision_stereo():
    assert rm.decision_stereo(dict(canaux=0, rms=[], crete=[]))[1] is None
    assert rm.decision_stereo(dict(canaux=1, rms=[-20], crete=[-3]))[1] == "pan=stereo|c0=c0|c1=c0"
    # micro-cravate sur le canal droit seulement
    diag, pan = rm.decision_stereo(dict(canaux=2, rms=[-120, -22], crete=[-120, -4]))
    assert pan == "pan=stereo|c0=c1|c1=c1" and "droit" in diag
    # canal gauche 15 dB au-dessus : on ne garde que lui
    assert rm.decision_stereo(dict(canaux=2, rms=[-20, -35], crete=[-3, -18]))[1] == "pan=stereo|c0=c0|c1=c0"
    # vraie stéréo (écart raisonnable) : conservée
    assert rm.decision_stereo(dict(canaux=2, rms=[-20, -24], crete=[-3, -6]))[1] is None


def test_gain_borne_et_sans_saturation():
    assert rm.gain_plan(dict(canaux=0, rms=[], crete=[])) == 0.0
    assert rm.gain_plan(dict(canaux=1, rms=[-40], crete=[-25])) == rm.GAIN_MAX_DB
    assert rm.gain_plan(dict(canaux=2, rms=[-2, -2], crete=[0.0, 0.0])) == -rm.GAIN_MAX_DB
    # à -30 dB RMS mais crête à -4 dB : le gain s'arrête avant la saturation
    assert rm.gain_plan(dict(canaux=1, rms=[-30], crete=[-4])) == 3.0


def test_correction_exposition_bornee():
    f, m = rm.correction_plan(dict(YAVG=118, YLOW=48, YHIGH=188))
    assert f == "eq=contrast=1.000:brightness=0.000"
    f, m = rm.correction_plan(dict(YAVG=30, YLOW=5, YHIGH=20))
    assert m["contraste"] == rm.CORR_CONTRASTE[1] and m["brightness"] == rm.CORR_LUMA_MAX
    # clair mais tenu (hautes lumières sous le seuil) : eq doux, pas la courbe
    f, m = rm.correction_plan(dict(YAVG=200, YLOW=60, YHIGH=218, CLIP=0.0))
    assert m["surexpose"] is False and f.startswith("eq=")
    assert rm.CORR_CONTRASTE[0] <= m["contraste"] <= 1.0 and m["brightness"] == -rm.CORR_LUMA_MAX


def test_surexpose_detecte_les_trois_signaux():
    assert not rm.surexpose(dict(YAVG=118, YLOW=48, YHIGH=188, CLIP=0.0))
    assert not rm.surexpose(dict(YAVG=212, YLOW=120, YHIGH=219, CLIP=0.0))   # clair, tenu
    assert rm.surexpose(dict(YAVG=170, YLOW=90, YHIGH=225, CLIP=0.0))        # moyen haut + hautes brûlées
    assert rm.surexpose(dict(YAVG=140, YLOW=60, YHIGH=233, CLIP=0.0))        # 90e centile au blanc
    assert rm.surexpose(dict(YAVG=150, YLOW=60, YHIGH=210, CLIP=0.05))       # 5 % de pixels brûlés (ciel)


def _croissante(points):
    return all(b[0] > a[0] and b[1] > a[1] for a, b in zip(points, points[1:]))


def test_courbe_surexpo_croissante_et_bornee():
    for stats in (dict(YAVG=229, YLOW=180, YHIGH=236, CLIP=0.86),
                  dict(YAVG=170, YLOW=90, YHIGH=225, CLIP=0.0),
                  dict(YAVG=150, YLOW=60, YHIGH=210, CLIP=0.05)):
        pts = rm.courbe_surexpo(stats)
        assert pts[0] == (0.0, 0.0) and pts[-1][0] == 1.0
        assert _croissante(pts)
        assert all(0.0 <= v <= rm.BLANC_MAX for _, v in pts)
        # les tons moyens redescendent, sans jamais tomber sous la cible
        y = (stats["YAVG"] - 16) / 219
        x_moy, v_moy = min(pts[1:], key=lambda p: abs(p[0] - y))
        assert v_moy < y and v_moy >= y - rm.SUREXPO_TIRAGE_MAX - 1e-6


def test_courbe_surexpo_plan_brule_ne_s_effondre_pas():
    # tout est blanc : aucun point intermédiaire ne survit, le blanc descend
    # vers les tons moyens visés mais pas plus bas
    pts = rm.courbe_surexpo(dict(YAVG=249, YLOW=245, YHIGH=255, CLIP=0.92))
    assert pts == [(0.0, 0.0), (1.0, 0.72)]


def test_correction_plan_surexpose_passe_par_la_courbe():
    f, m = rm.correction_plan(dict(YAVG=229, YLOW=180, YHIGH=236, CLIP=0.86))
    assert m["surexpose"] is True and m["clip"] == 0.86
    assert f.startswith("curves=master='0/0 ") and f.endswith("',eq=saturation=1.04")
    pts = rm.courbe_surexpo(dict(YAVG=229, YLOW=180, YHIGH=236, CLIP=0.86))
    assert m["courbe"] == " ".join("%g/%g" % p for p in pts)


def test_scene_par_nom():
    assert rm.scene_par_nom("/x/scene-03-prise-2.mov") == (3, 2)
    assert rm.scene_par_nom("/x/sc03_t2.mp4") == (3, 2)
    assert rm.scene_par_nom("/x/Plan 7 take 1.MOV") == (7, 1)
    assert rm.scene_par_nom("/x/C0012.MP4") is None


def _scene(nom, duree):
    return [dict(fichier=nom, duree=duree)]


def test_repartition_une_scene_par_plan_puis_surplus_aux_longues():
    scenes = [_scene("a", 10), _scene("b", 40), _scene("c", 10)]
    plans = rm.repartir_plans(scenes, [0, 0, 0], [2.5, 2.0, 2.0, 2.0, 3.0])
    assert [p["scene"] for p in plans] == [1, 2, 2, 2, 3]
    for p in plans:
        marge = 10 * rm.MARGE_RUSH if p["fichier"] != "b" else 40 * rm.MARGE_RUSH
        assert p["debut"] >= marge - 1e-6
    # les trois plans de « b » sont à des moments différents, dans l'ordre
    debuts = [p["debut"] for p in plans if p["fichier"] == "b"]
    assert debuts == sorted(debuts) and len(set(debuts)) == 3


def test_repartition_plus_de_scenes_que_de_plans_et_accroche():
    scenes = [_scene(str(i), 10) for i in range(8)]
    plans = rm.repartir_plans(scenes, [0] * 8, [2.5, 2.0, 3.0], accroche=5)
    assert plans[0]["scene"] == 5
    assert len(plans) == 3 and len({p["scene"] for p in plans}) == 3


def test_echapper_chemin_lut():
    assert rm.echapper("/Volumes/Disque:vert/it's.cube") == "/Volumes/Disque\\:vert/it\\'s.cube"


def _plans_fcp():
    return [dict(fichier="/V/nina/a.mov", debut=1.0, duree=2.5, scene=1, audio=True, gain_db=3.0,
                 duree_rush=8.0, pan=None, diag_son="stéréo → conservée", mesure_image=dict(surexpose=False)),
            dict(fichier="/V/nina/b.mov", debut=0.5, duree=2.2, scene=2, audio=True, gain_db=0.0,
                 duree_rush=5.0, pan="pan=stereo|c0=c0|c1=c0", diag_son="mono → dupliqué",
                 mesure_image=dict(surexpose=True, YAVG=229.0, clip=0.86)),
            dict(fichier="/V/nina/a.mov", debut=4.0, duree=3.0, scene=1, audio=False, gain_db=0.0,
                 duree_rush=8.0, pan="silence", diag_son="aucune piste", mesure_image=dict(surexpose=False))]


def _frames(t):
    n, d = t[:-1].split("/")
    assert int(d) == rm.FPS
    return int(n)


def test_fcpxml_timeline_dure_ce_que_dure_le_rendu(tmp_path):
    plans = _plans_fcp()
    titre = tmp_path / "t.png"
    titre.write_bytes(b"png")
    chemin = tmp_path / "reel.fcpxml"
    total = rm.ecrire_fcpxml(str(chemin), "reel", plans, str(titre), None)
    attendu = round((sum(p["duree"] for p in plans) - (len(plans) - 1) * rm.TRANSITION) * rm.FPS)
    assert total == attendu
    root = ET.parse(chemin).getroot()
    assert root.get("version") == "1.8"
    fmt = root.find("resources/format")
    assert (fmt.get("width"), fmt.get("height")) == (str(rm.W), str(rm.H))
    # un rush = une ressource, même s'il sert deux fois ; le titre en plus
    assets = root.findall("resources/asset")
    assert [a.get("name") for a in assets] == ["a.mov", "t.png", "b.mov"]
    assert assets[0].get("src").startswith("file:///") and assets[0].get("src").endswith("/V/nina/a.mov")
    seq = root.find("library/event/project/sequence")
    assert _frames(seq.get("duration")) == attendu
    clips = seq.findall("spine/asset-clip")
    trans = seq.findall("spine/transition")
    assert len(clips) == 3 and len(trans) == 2
    # bord à bord, fondus centrés sur les coupes
    pos = 0
    for k, c in enumerate(clips):
        assert _frames(c.get("offset")) == pos
        pos += _frames(c.get("duration"))
    assert pos == attendu
    for c, t in zip(clips[1:], trans):
        assert _frames(t.get("offset")) == _frames(c.get("offset")) - _frames(t.get("duration")) // 2
    # les poignées des fondus restent dans la plage [debut, debut+duree] de chaque plan
    for k, (c, p) in enumerate(zip(clips, plans)):
        start = _frames(c.get("start"))
        assert start >= round(p["debut"] * rm.FPS)
        assert start + _frames(c.get("duration")) <= round((p["debut"] + p["duree"]) * rm.FPS)


def test_fcpxml_transporte_gain_titre_et_marqueurs(tmp_path):
    plans = _plans_fcp()
    titre = tmp_path / "t.png"
    titre.write_bytes(b"png")
    carton = tmp_path / "c.png"
    carton.write_bytes(b"png")
    chemin = tmp_path / "reel.fcpxml"
    rm.ecrire_fcpxml(str(chemin), "reel", plans, str(titre), str(carton))
    clips = ET.parse(chemin).getroot().findall("library/event/project/sequence/spine/asset-clip")
    assert len(clips) == 4 and clips[-1].get("name") == "Carton de fin"
    assert _frames(clips[-1].get("duration")) == round(rm.DUREE_CARTON * rm.FPS) - rm.frames(rm.TRANSITION) // 2
    assert clips[0].find("adjust-volume").get("amount") == "+3.0dB"
    assert clips[1].find("adjust-volume") is None
    t = clips[0].find("asset-clip")
    assert t.get("lane") == "1" and t.get("offset") == clips[0].get("start")
    assert clips[0].get("audioRole") == "dialogue" and clips[2].get("audioRole") is None
    marques = [m.get("value") for m in clips[1].findall("marker")]
    assert len(marques) == 2 and marques[0].startswith("Son : mono") and "surexposé" in marques[1]
    assert [m.get("value") for m in clips[2].findall("marker")] == ["Son : aucune piste, poser une ambiance"]
    assert clips[0].findall("marker") == []


def test_plages_parole_garde_une_respiration():
    # prise de 10 s : parole 0-3, blanc 3-4.2, parole 4.2-7, blanc 7-9.5, parole 9.5-10
    plages = rm.plages_parole([(3.0, 4.2), (7.0, 9.5)], 10.0)
    g = rm.SILENCE_GARDE
    assert plages == [(0.0, round(3.0 + g, 3)), (round(4.2 - g, 3), round(7.0 + g, 3)),
                      (round(9.5 - g, 3), 10.0)]
    # un blanc en tête et une miette en queue disparaissent
    assert rm.plages_parole([(0.0, 1.0), (9.9, 10.0)], 10.0) == [(round(1.0 - g, 3), 10.0)]
    # pas de blanc : la prise entière
    assert rm.plages_parole([], 5.0) == [(0.0, 5.0)]


def test_appliquer_coupes_remplit_la_duree_en_sautant_les_blancs():
    plages = [(0.0, 3.1), (4.1, 7.1), (9.4, 10.0)]
    plan = dict(fichier="a", debut=1.0, duree=4.0)
    segs, saute = rm.appliquer_coupes(plan, plages)
    assert segs == [(1.0, 2.1), (4.1, 1.9)]
    assert abs(sum(d for _, d in segs) - 4.0) < 1e-6
    assert abs(saute - 1.0) < 1e-6
    # pas assez de parole après debut : on ne touche pas au plan
    assert rm.appliquer_coupes(dict(fichier="a", debut=9.0, duree=4.0), plages) is None
    # une seule plage suffit : rien à couper, on garde la fenêtre d'origine
    assert rm.appliquer_coupes(dict(fichier="a", debut=0.0, duree=2.0), plages) is None


def test_couleur_hex():
    assert rm.couleur("#F3E9D2", (0, 0, 0)) == (243, 233, 210)
    assert rm.couleur("1f1f1f", (0, 0, 0)) == (31, 31, 31)
    assert rm.couleur("#abc", (0, 0, 0)) == (170, 187, 204)
    assert rm.couleur(None, (1, 2, 3)) == (1, 2, 3)


def test_carton_cta_aux_couleurs_du_client(tmp_path):
    from PIL import Image
    logo = tmp_path / "logo.png"
    Image.new("RGBA", (400, 200), (255, 0, 0, 255)).save(logo)
    png = tmp_path / "cta.png"
    rm.carton_cta(str(png), "Réservez votre table\\nninaramen.fr", 540, 960,
                  fond="#F3E9D2", encre="#1F1F1F", logo=str(logo))
    im = Image.open(png).convert("RGB")
    assert im.size == (540, 960)
    assert im.getpixel((5, 5)) == (243, 233, 210)            # fond de la charte
    couleurs = {im.getpixel((x, y)) for x in range(0, 540, 6) for y in range(0, 960, 6)}
    assert (255, 0, 0) in couleurs                            # le logo est posé
    assert (31, 31, 31) in couleurs                           # le texte est dans l'encre demandée


def test_fcpxml_blancs_coupes_un_clip_par_bout(tmp_path):
    plans = [dict(fichier="/V/a.mov", debut=1.0, duree=3.0, scene=1, audio=True, gain_db=0.0,
                  duree_rush=20.0, segments=[(1.0, 1.4), (3.2, 1.6)], blancs_coupes=0.8),
             dict(fichier="/V/b.mov", debut=0.5, duree=2.0, scene=2, audio=True, gain_db=0.0,
                  duree_rush=9.0)]
    chemin = tmp_path / "reel.fcpxml"
    total = rm.ecrire_fcpxml(str(chemin), "reel", plans, None, None)
    clips = ET.parse(chemin).getroot().findall("library/event/project/sequence/spine/asset-clip")
    assert [c.get("name")[-5:] for c in clips[:2]] == ["(1/2)", "(2/2)"]
    assert len(clips) == 3
    # bord à bord, et la somme fait exactement la durée du rendu
    pos = 0
    for c in clips:
        assert _frames(c.get("offset")) == pos
        pos += _frames(c.get("duration"))
    assert pos == total == round((3.0 + 2.0 - rm.TRANSITION) * rm.FPS)
    # le 2e bout du plan 1 commence bien à 3.2 s dans la source
    assert _frames(clips[1].get("start")) == round(3.2 * rm.FPS)
    # marqueurs et titre seulement sur le premier bout
    assert clips[1].findall("marker") == []


def _dv2():
    import importlib.util
    chemin = Path(__file__).resolve().parent.parent / "projets" / "nina-ramen" / "davinci-v2.py"
    spec = importlib.util.spec_from_file_location("davinci_v2", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_davinci_v2_segments_clip_en_images_source():
    dv = _dv2()
    fps = 30
    # clip V1 : images 60 à 300 (2 s à 10 s) ; parole 0-3.12, 4.08-7.12, 9.38-10
    plages = [(0.0, 3.12), (4.08, 7.12), (9.38, 10.0)]
    segs = dv.segments_clip(60, 300, plages, fps, 0.35)
    assert segs == [(60, 94), (122, 214), (281, 300)]
    assert all(s0 >= 60 and s1 <= 300 for s0, s1 in segs)
    # clip entièrement dans une plage : inchangé, un seul bout
    assert dv.segments_clip(10, 80, plages, fps, 0.35) == [(10, 80)]
    # clip entièrement dans un blanc : on ne perd pas d'image
    assert dv.segments_clip(95, 120, plages, fps, 0.35) == [(95, 120)]


def test_davinci_v2_nom_projet():
    dv = _dv2()
    assert dv.nom_projet("Nina Ramen / Chatgpt") == ("Nina Ramen", "Chatgpt")
    assert dv.nom_projet("Nina RAmen/Chatgpt") == ("Nina RAmen", "Chatgpt")
    assert dv.nom_projet("Chatgpt") == (None, "Chatgpt")

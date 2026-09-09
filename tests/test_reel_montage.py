"""Le montage de reel se règle sans ffmpeg : grille de durées, décision stéréo,
gain, correction d'exposition, lecture des scènes dans les noms, répartition
des plans. Ce sont les règles qui garantissent « 90 s, stéréo, homogène »."""

import importlib
import sys
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
    f, m = rm.correction_plan(dict(YAVG=230, YLOW=40, YHIGH=250))
    assert rm.CORR_CONTRASTE[0] <= m["contraste"] <= 1.0 and m["brightness"] == -rm.CORR_LUMA_MAX


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

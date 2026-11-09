"""Le logo néon se règle sans ffmpeg : géométrie du placement, ordre et timing du
tracé, remplissage, suivi d'une surface qui bouge. Ce sont les règles qui
garantissent « le logo se dessine dans le sens de lecture et reste collé au mur »."""

import importlib
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
vx = importlib.import_module("vfx-logo")

REG = {"duree_trace": 0.8, "duree_remplissage": 0.5, "neon": vx.hex_rgb("#C9A2FF"),
       "remplissage": vx.hex_rgb("#EDE4FF"), "opacite": 0.9, "lueur_finale": 0.35,
       "force_lueur": 0.8, "flou": 0.0, "eclairage": 0.0, "scintillement": False}


def _logo_trois_blocs():
    """Trois « lettres » carrées séparées, de gauche à droite."""
    img = Image.new("RGBA", (300, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for x in (10, 120, 230):
        d.rectangle([x, 10, x + 60, 70], fill=(255, 255, 255, 255))
    return vx.Logo(img)


def test_homographie_retrouve_les_coins():
    src = np.array([[0, 0], [100, 0], [100, 50], [0, 50]], float)
    dst = np.array([[212, 80], [610, 140], [590, 330], [190, 300]], float)
    h = vx.homographie(src, dst)
    assert np.allclose(vx.appliquer(h, src), dst, atol=1e-6)


def test_homographie_robuste_ignore_un_repere_qui_a_glisse():
    src = np.array([[0, 0], [100, 0], [100, 50], [0, 50], [50, 25], [20, 40], [80, 10]], float)
    vrai = vx.homographie(src[:4], src[:4] * 1.1 + [30, 12])
    dst = vx.appliquer(vrai, src)
    dst[5] += [40, 0]                       # un repère a glissé le long d'une poutre
    h, fiables = vx.homographie_robuste(src, dst)
    assert not fiables[5] and fiables.sum() == 6
    assert np.allclose(vx.appliquer(h, src[:4]), vx.appliquer(vrai, src[:4]), atol=1e-3)


def test_cles_interpolees_et_tenues():
    cles = [{"t": 1.0, "coins": [[0, 0], [10, 0], [10, 10], [0, 10]]},
            {"t": 3.0, "coins": [[20, 0], [30, 0], [30, 10], [20, 10]]}]
    assert vx.interpoler_cles(cles, 0.0)[0, 0] == 0          # tenu avant la première clé
    assert vx.interpoler_cles(cles, 2.0)[0, 0] == pytest.approx(10)
    assert vx.interpoler_cles(cles, 9.0)[0, 0] == 20         # tenu après la dernière


def test_lettres_dans_le_sens_de_lecture():
    logo = _logo_trois_blocs()
    assert logo.n == 3
    xs = np.mgrid[0:logo.H, 0:logo.W][1]
    centres = [xs[logo.rang == r].mean() for r in range(3)]
    assert centres == sorted(centres)


def test_trace_en_cascade_puis_complet():
    av = vx.avancement_lettres(5, 0.2, 0.8)
    assert all(a >= b for a, b in zip(av, av[1:]))           # la première lettre est devant
    assert av[0] > 0 and av[-1] == 0
    assert np.all(vx.avancement_lettres(5, 0.8, 0.8) == 1.0)  # tout est tracé à la fin


def test_rien_au_debut_rempli_a_la_fin():
    logo = _logo_trois_blocs()
    dessus, lueur = vx.calques(logo, 0.0, REG)
    assert dessus[..., 3].max() < 0.05 and lueur.max() < 0.05
    dessus, _ = vx.calques(logo, 2.0, REG)
    dedans = logo.alpha > 0.99
    assert dessus[..., 3][dedans].mean() == pytest.approx(REG["opacite"], abs=0.02)
    # pendant le tracé, seul le contour s'allume, pas l'intérieur
    dessus, _ = vx.calques(logo, 0.5, REG)
    interieur = logo.alpha > 0.99
    interieur &= logo.contour < 0.01
    assert dessus[..., 3][interieur].max() < 0.05
    assert dessus[..., 3][logo.contour > 0.5].max() > 0.9


def test_logo_opaque_refuse(tmp_path):
    p = tmp_path / "plein.png"
    Image.new("RGBA", (200, 60), (255, 255, 255, 255)).save(p)
    with pytest.raises(SystemExit):
        vx.charger_logo(str(p))


def test_incrustation_reste_dans_sa_zone():
    logo = _logo_trois_blocs()
    image = np.zeros((300, 400, 3), np.float32) + 0.2
    coins = np.array([[100, 100], [300, 110], [300, 180], [100, 170]], float)
    out = vx.incruster(image, logo, coins, 2.0, REG)
    change = np.abs(out - image).max(axis=2) > 0.02
    ys, xs = np.nonzero(change)
    assert change.any()
    assert xs.min() > 40 and xs.max() < 360 and ys.min() > 40 and ys.max() < 240


def _texture(taille=(480, 360)):
    alea = np.random.default_rng(3)
    petit = alea.random((taille[1] // 4, taille[0] // 4))
    img = Image.fromarray((petit * 255).astype(np.uint8)).resize(taille, Image.BICUBIC)
    return img


def test_suivi_reste_colle_a_la_surface():
    """Un mur texturé qui glisse et tourne (12° en 15 images, bien plus qu'un vrai
    plan) : les coins suivis retombent sur les vrais à 2 pixels près."""
    mur = _texture()
    coins0 = np.array([[180, 140], [300, 140], [300, 220], [180, 220]], float)

    def image(k):
        a = np.radians(0.8 * k)
        tx, ty = 3.0 * k, -2.0 * k
        c, s = np.cos(a), np.sin(a)
        cx, cy = 240, 180
        # matrice image -> mur (ce que PIL attend)
        inv = np.linalg.inv(np.array([[c, -s, cx - c * cx + s * cy + tx],
                                      [s, c, cy - s * cx - c * cy + ty], [0, 0, 1]]))
        g = mur.transform(mur.size, Image.AFFINE, tuple(inv[:2].flatten()), Image.BICUBIC)
        vrai = np.array([[c * (x - cx) - s * (y - cy) + cx + tx,
                          s * (x - cx) + c * (y - cy) + cy + ty] for x, y in coins0])
        return np.asarray(g, np.float64) / 255, vrai

    g0, _ = image(0)
    suivi = vx.Suivi(g0, coins0, coins0, rayon=14, recherche=12)
    for k in range(1, 16):
        g, vrai = image(k)
        h = suivi.avancer(g)
        assert h is not None
    assert np.abs(vx.appliquer(h, coins0) - vrai).max() < 2.0

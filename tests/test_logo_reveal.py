"""L'effet « logo qui se construit » se règle sans ffmpeg ni modèle : le prompt garde
le lieu intact, les réglages pointent vers le bon modèle, et le contrôle de la
dernière image refuse un plan qui a dérivé."""

import importlib
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
lr = importlib.import_module("logo-reveal")


def test_chaque_style_garde_le_lieu_et_la_camera():
    for style in lr.STYLES:
        for mode in lr.DEBUT:
            prompt = lr.construire_prompt(style, "the round green logo", mode)
            assert "Locked-off camera" in prompt
            assert "preserve the input image exactly" in prompt
            assert "the round green logo" in prompt
            assert "\u2014" not in prompt and "\u2013" not in prompt


def test_le_mode_debut_fin_vise_l_image_de_fin():
    prompt = lr.construire_prompt("pieces", "the logo", "debut-fin")
    assert "end frame" in prompt
    reglages = lr.reglages_higgsfield("debut-fin")
    assert reglages["model"] == "kling3_0" and reglages["sound"] == "off"
    assert [m["role"] for m in reglages["medias"]] == ["start_image", "end_image"]
    assert reglages["use_unlim"] is False


def test_le_mode_une_image_reste_sur_le_turbo():
    reglages = lr.reglages_higgsfield("une-image")
    assert reglages["model"] == "kling3_0_turbo"
    assert [m["role"] for m in reglages["medias"]] == ["start_image"]


def test_style_inconnu_explique_quoi_choisir():
    with pytest.raises(ValueError, match="choisis parmi"):
        lr.construire_prompt("explosion", "the logo")


def _facade(avec_logo=True, decalage=0):
    image = Image.new("RGB", (720, 1280), (40, 60, 80))
    d = ImageDraw.Draw(image)
    d.rectangle((0, 900, 720, 1280), fill=(120, 120, 120))
    if avec_logo:
        d.ellipse((200 + decalage, 300, 520 + decalage, 620), fill=(30, 220, 140))
    return image


def test_ecart_nul_sur_la_meme_photo_et_fort_sur_un_autre_lieu():
    assert lr.ecart(_facade(), _facade()) == 0
    autre_lieu = Image.new("RGB", (720, 1280), (230, 200, 160))
    ok, message = lr.verdict(lr.ecart(_facade(), autre_lieu))
    assert not ok and "Regarde la dernière image" in message


def test_logo_mal_pose_est_vu():
    assert lr.ecart(_facade(), _facade(decalage=160)) > lr.ecart(_facade(), _facade())
    assert lr.verdict(lr.ecart(_facade(), _facade(avec_logo=False)))[0] is False


def test_photo_paysage_comparee_au_9_16():
    paysage = Image.new("RGB", (1920, 1080), (40, 60, 80))
    paysage.paste(_facade().resize((608, 1080)), (656, 0))
    assert lr.verdict(lr.ecart(_facade(), paysage))[0]


def test_couple_video_photo():
    assert lr.lire_couple("a/plan1.mp4:b/facade.jpg") == (Path("a/plan1.mp4"),
                                                          Path("b/facade.jpg"))
    with pytest.raises(ValueError, match="video.mp4:photo.jpg"):
        lr.lire_couple("plan1.mp4")


def test_zone_du_logo():
    assert lr.lire_zone("100,662,200,205") == (100, 662, 200, 205)
    with pytest.raises(ValueError, match="cx,cy,rx,ry"):
        lr.lire_zone("100,662")


def test_les_styles_plats_interdisent_le_volume():
    for style in ("trace", "encre"):
        prompt = lr.construire_prompt(style, "the logo")
        assert "Strictly flat 2D" in prompt and "no extrusion" in prompt


def test_zone_de_grain():
    assert lr.lire_rectangle("1000,3950,2900,4880") == (1000, 3950, 2900, 4880)
    with pytest.raises(ValueError, match="bas droit"):
        lr.lire_rectangle("10,10,5,20")

"""Le tirage compte bien une chance par ami identifié et une par story."""

import importlib.util
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("tirage", RACINE / "scripts" / "tirage-concours.py")
tirage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tirage)


def test_chances(tmp_path):
    f = tmp_path / "c.txt"
    f.write_text(
        "alice : @bob\n"
        "alice : @carla et @bob\n"   # bob déjà compté
        "bob : je cours le 13\n"
        "@dan : @dan @oteafilmakers\n"  # s'identifier soi-même ou le compte ne compte pas
        "pro_agence : @x\n",
        encoding="utf-8",
    )
    amis = tirage.lire_commentaires(f)
    chances = tirage.calculer_chances(amis, stories={"bob"}, exclus={"oteafilmakers", "pro_agence"})
    assert chances == {"alice": 3, "bob": 2, "dan": 1}


def test_bandeau_ne_deborde_pas(tmp_path):
    from PIL import Image
    spec_b = importlib.util.spec_from_file_location("bandeau", RACINE / "scripts" / "concours-bandeau.py")
    bandeau = importlib.util.module_from_spec(spec_b)
    spec_b.loader.exec_module(bandeau)
    src = tmp_path / "s.jpg"
    Image.new("RGB", (1080, 1920), (30, 30, 30)).save(src)
    bandeau.bandeau(src, tmp_path / "o.jpg", "@oteafilmakers", 1606)
    assert (tmp_path / "o.jpg").exists()


def test_bandeau_tiktok_reste_hors_interface(tmp_path):
    """Sur TikTok le bandeau parle de republier, pas de story, et reste au-dessus de la légende."""
    from PIL import Image
    spec_b = importlib.util.spec_from_file_location("bandeau", RACINE / "scripts" / "concours-bandeau.py")
    bandeau = importlib.util.module_from_spec(spec_b)
    spec_b.loader.exec_module(bandeau)
    textes = " ".join(t + u for t, u in bandeau.leviers("tiktok", "@oteafilmakers"))
    assert "STORY" not in textes.upper() and "REPUBLIE" in textes
    src = tmp_path / "s.jpg"
    Image.new("RGB", (1080, 1920), (30, 30, 30)).save(src)
    bandeau.bandeau(src, tmp_path / "o.jpg", "@oteafilmakers", 1310, "tiktok")
    import pytest
    with pytest.raises(SystemExit):
        bandeau.bandeau(src, tmp_path / "o2.jpg", "@oteafilmakers", 1606, "tiktok")

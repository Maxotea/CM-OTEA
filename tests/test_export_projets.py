"""L'export des Projets Claude : instructions tirées du kit, fiches présentes, zips lisibles."""
import importlib.util
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("export_projets", RACINE / "scripts" / "export_projets_claude.py")
export_projets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export_projets)


def test_export_complet(tmp_path):
    zips = export_projets.exporter(tmp_path / "out")
    assert len(zips) == 9
    for z in zips:
        with zipfile.ZipFile(z) as archive:
            noms = archive.namelist()
            if z.name.startswith("00-"):
                assert any(n.endswith("README.md") for n in noms), z.name
                assert sum(n.endswith("SKILL.md") for n in noms) >= 8, z.name
                continue
            assert any(n.endswith("INSTRUCTIONS.md") for n in noms), z.name
            assert len(noms) >= 2, z.name


def test_instructions_sans_tiret_cadratin(tmp_path):
    export_projets.exporter(tmp_path / "out")
    for f in (tmp_path / "out").glob("*/INSTRUCTIONS.md"):
        texte = f.read_text(encoding="utf-8")
        assert "—" not in texte and "–" not in texte, f.parent.name
        assert "[CLIENT]" not in texte, f.parent.name


def test_ton_du_client_repris_de_la_configuration(tmp_path):
    export_projets.exporter(tmp_path / "out")
    texte = (tmp_path / "out" / "04-La-Galerie-Immobiliere" / "INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert "vouvoiement" in texte

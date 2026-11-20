#!/usr/bin/env python3
"""Prépare un dossier prêt à importer pour chaque Projet Claude (ou Cowork) d'OTEA.

Un zip du kit Cowork (.claude/cowork-kit), puis pour chaque Projet : INSTRUCTIONS.md (le texte à coller dans le champ instructions) et les
fichiers de la base de connaissances, plus un zip. Les sources restent dans le dépôt : on
régénère après toute modification, on ne retouche jamais les copies.

    python3 scripts/export_projets_claude.py [dossier_de_sortie]      # défaut : o/projets-claude

Les instructions communes viennent de .claude/references/kit-cowork.md (une seule source).
"""
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
REF = RACINE / ".claude" / "references"
SKILLS = RACINE / ".claude" / "skills"
CLIENTS = SKILLS / "cm-metricool" / "references" / "clients"
KIT = REF / "kit-cowork.md"


def bloc_du_kit(prefixe_section: str) -> str:
    """Premier bloc de code de la section du kit dont le titre commence par prefixe_section."""
    texte = KIT.read_text(encoding="utf-8")
    for section in texte.split("\n## "):
        if section.startswith(prefixe_section):
            m = re.search(r"```\n(.*?)\n```", section, flags=re.S)
            if m:
                return m.group(1).strip() + "\n"
    raise SystemExit(f"bloc introuvable dans le kit : section « {prefixe_section} »")


def tons() -> dict:
    cfg = json.loads((RACINE / "recaps" / "clients-config.json").read_text(encoding="utf-8"))
    return {c["nom"]: c.get("ton") for c in cfg["comptes"]}


def instructions_client(nom_client: str, nom_config: str | None) -> str:
    ton = tons().get(nom_config) if nom_config else None
    ligne_ton = (
        f"Ton du client : {ton}.\n"
        if ton
        else "Ton du client : non renseigné dans la configuration, lis la fiche et demande en cas de doute.\n"
    )
    return bloc_du_kit("4.").replace("[CLIENT]", nom_client) + "\n" + ligne_ton


def projets() -> dict:
    sm = REF / "social-media-ceo"
    pilotage = [(f.name, f) for f in sorted(sm.glob("0*.md"))]
    pilotage += [(f.name, f) for f in sorted((sm / "cadres").glob("smc-*.md"))]
    pilotage += [(f"offre-{f.name}", f) for f in sorted((RACINE / "offre").glob("*.md"))]
    return {
        "01-OTEA-pilotage": {"instr": bloc_du_kit("2."), "fichiers": pilotage},
        "02-Compta-OTEA": {
            "instr": bloc_du_kit("3."),
            "fichiers": [("smc-ops-finance.md", sm / "cadres" / "smc-ops-finance.md")],
        },
        "03-J-Lawson-Golf": {
            "instr": instructions_client("J Lawson Golf", "J Lawson Golf"),
            "fichiers": [("fiche-jlawsongolf.md", CLIENTS / "jlawsongolf.md")],
        },
        "04-La-Galerie-Immobiliere": {
            "instr": instructions_client("La Galerie Immobilière", "La Galerie Immobilière"),
            "fichiers": [("fiche-la-galerie-immobiliere.md", CLIENTS / "la-galerie-immobiliere.md")],
        },
        "05-Pierre-Huiban": {
            "instr": instructions_client("Pierre Huiban", "Pierre Huiban"),
            "fichiers": [
                ("fiche-pierre-huiban.md", CLIENTS / "pierre-huiban.md"),
                ("banque-photos-pierre-huiban.md", CLIENTS / "banque-photos-pierre-huiban.md"),
            ],
        },
        "06-Run-On-Invest": {
            "instr": instructions_client("Run On Invest", "Run On Invest"),
            "fichiers": [("fiche-run-on-invest.md", CLIENTS / "run-on-invest.md")],
        },
        "07-OTEA-Production-et-Filmakers": {
            "instr": instructions_client("OTEA Production et Otea Filmakers", "Otea Filmakers"),
            "fichiers": [
                ("fiche-otea-production.md", CLIENTS / "otea-production.md"),
                ("fiche-otea-filmakers.md", CLIENTS / "otea-filmakers.md"),
            ],
        },
        "08-ConfShine": {"instr": None, "fichiers": []},  # traité à part, voir confshine()
    }


def confshine(dossier: Path) -> None:
    src = CLIENTS / "confshine"
    texte = (src / "instructions-projet-claude.md").read_text(encoding="utf-8")
    instr = texte.split("\n---\n", 1)[1].strip() + "\n"
    (dossier / "INSTRUCTIONS.md").write_text(instr, encoding="utf-8")
    subprocess.run(["sh", str(src / "build-dossier.sh"), str(dossier / "CONFSHINE-dossier.md")],
                   check=True, capture_output=True)


def exporter(sortie: Path) -> list[Path]:
    if sortie.exists():
        shutil.rmtree(sortie)
    sortie.mkdir(parents=True)
    zips = []
    kit = RACINE / ".claude" / "cowork-kit"
    archive = sortie / "00-cowork-kit.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(kit.rglob("*")):
            if f.is_file():
                z.write(f, f"cowork-kit/{f.relative_to(kit)}")
    zips.append(archive)
    for nom, p in projets().items():
        dossier = sortie / nom
        dossier.mkdir()
        if nom == "08-ConfShine":
            confshine(dossier)
        else:
            (dossier / "INSTRUCTIONS.md").write_text(p["instr"], encoding="utf-8")
            for cible, source in p["fichiers"]:
                shutil.copyfile(source, dossier / cible)
        archive = sortie / f"{nom}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(dossier.iterdir()):
                z.write(f, f"{nom}/{f.name}")
        zips.append(archive)
    return zips


if __name__ == "__main__":
    cible = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "o" / "projets-claude"
    for z in exporter(cible):
        print(f"{z.name:48s} {z.stat().st_size // 1024:5d} Ko")

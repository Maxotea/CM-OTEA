"""La règle d'écriture du dépôt, vérifiée sur ce qui sort vers un client.

Aucun tiret cadratin (« — ») ni demi-cadratin (« – ») dans un texte destiné au client :
c'est la signature la plus reconnaissable d'un texte produit par une IA. La règle vit
dans `.claude/memories/redaction-sans-tirets.md` ; ce test est là pour qu'elle survive
aux prochaines modifications. Les commentaires de code et la documentation interne ne
sont pas concernés.
"""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import review  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TIRETS = ("—", "–")


def _chaines(valeur, chemin=""):
    """Toutes les chaînes d'une structure JSON, avec leur chemin pour un message utile."""
    if isinstance(valeur, str):
        yield chemin, valeur
    elif isinstance(valeur, dict):
        for cle, v in valeur.items():
            yield from _chaines(v, f"{chemin}.{cle}" if chemin else cle)
    elif isinstance(valeur, list):
        for i, v in enumerate(valeur):
            yield from _chaines(v, f"{chemin}[{i}]")


def _fautes(texte):
    return [t for t in TIRETS if t in texte]


def test_specs_de_carrousels_sans_tiret_cadratin():
    fautes = []
    for spec in sorted((ROOT / "carrousels").rglob("*.json")):
        data = json.loads(spec.read_text(encoding="utf-8"))
        for chemin, texte in _chaines(data):
            if chemin in ("note", "cible"):   # notes internes, jamais publiées
                continue
            if _fautes(texte):
                fautes.append(f"{spec.relative_to(ROOT)} : {chemin}")
    assert not fautes, "tiret cadratin dans un texte publié :\n  " + "\n  ".join(fautes)


def test_modele_du_mail_de_review_sans_tiret_cadratin():
    texte = (ROOT / "recaps" / "modele-mail-review.md").read_text(encoding="utf-8")
    fautes = [f"ligne {i}" for i, l in enumerate(texte.splitlines(), 1) if _fautes(l)]
    assert not fautes, "tiret cadratin dans le modèle de mail : " + ", ".join(fautes)


def test_modeles_du_compte_rendu_client_sans_tiret_cadratin():
    """Seules les lignes citées (« > ») et l'objet sont envoyées au client."""
    chemin = ROOT / ".claude/skills/cm-metricool/references/compte-rendu-hebdo-clients.md"
    fautes = [f"ligne {i}" for i, l in enumerate(chemin.read_text(encoding="utf-8").splitlines(), 1)
              if (l.startswith(">") or l.startswith("Objet")) and _fautes(l)]
    assert not fautes, "tiret cadratin dans un modèle client : " + ", ".join(fautes)


def test_fichier_de_review_sans_tiret_cadratin(tmp_path):
    """Le mode d'emploi et la table que le client ouvre dans Google Sheets."""
    import openpyxl
    compte = {"slug": "c", "nom": "Client", "prefixe": "C", "blog_id": 1}
    brouillons = [{"id": 1, "draft": True, "text": "Texte propre", "media": [],
                   "providers": [{"network": "instagram"}],
                   "publicationDate": {"dateTime": "2026-09-07T18:00:00"}}]
    chemin = tmp_path / "f.xlsx"
    review.ecrire_fichier(compte, date(2026, 9, 7), brouillons, chemin)
    wb = openpyxl.load_workbook(chemin)
    fautes = []
    for ws in wb.worksheets:
        if ws.title == "_tech":
            continue
        for ligne in ws.iter_rows(values_only=True):
            for cellule in ligne:
                if isinstance(cellule, str) and _fautes(cellule):
                    fautes.append(f"{ws.title} : « {cellule[:50]} »")
    assert not fautes, "tiret cadratin dans le fichier client :\n  " + "\n  ".join(fautes)

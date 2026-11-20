"""La récupération quotidienne du Drive ne doit tomber sur aucun fichier de photos/.

Le job drive.yml lit TOUS les manifestes chaque matin : un seul fichier mal formé pour lui
(une note de banque sans liste « photos », des photos hébergées ailleurs que sur le Drive)
faisait échouer la récupération de tous les clients. Testé sans réseau.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import drive_sync  # noqa: E402

PHOTOS = Path(__file__).resolve().parent.parent / "photos"


def _sans_reseau(drive_id):
    raise AssertionError(f"téléchargement inattendu de {drive_id}")


def test_un_fichier_sans_liste_photos_est_saute(tmp_path, monkeypatch):
    (tmp_path / "note.json").write_text(json.dumps({"_doc": "note", "visuels": []}))
    monkeypatch.setattr(drive_sync, "PHOTOS", tmp_path)
    monkeypatch.setattr(drive_sync, "telecharger", _sans_reseau)
    assert drive_sync.synchroniser("note", dry_run=True) == 0


def test_une_photo_sans_drive_id_ni_empreinte_est_ignoree(tmp_path, monkeypatch):
    manifeste = {"photos": [
        {"cle": "a", "url": "https://cdn/a.jpg"},                # hébergée ailleurs
        {"cle": "b", "empreinte": "0123456789abcdef"},           # déjà récupérée
    ]}
    (tmp_path / "client.json").write_text(json.dumps(manifeste))
    monkeypatch.setattr(drive_sync, "PHOTOS", tmp_path)
    monkeypatch.setattr(drive_sync, "telecharger", _sans_reseau)
    assert drive_sync.synchroniser("client", dry_run=True) == 0


def test_une_photo_deposee_dans_le_drive_est_toujours_recuperee(tmp_path, monkeypatch):
    manifeste = {"photos": [{"drive_id": "abc", "drive_nom": "photo.jpg"}]}
    (tmp_path / "client.json").write_text(json.dumps(manifeste))
    monkeypatch.setattr(drive_sync, "PHOTOS", tmp_path)
    monkeypatch.setattr(drive_sync, "ROOT", tmp_path)
    monkeypatch.setattr(drive_sync, "telecharger", lambda i: (b"octets-" + i.encode(), "jpg"))
    assert drive_sync.synchroniser("client", dry_run=True) == 1
    # Le dry-run ne réécrit pas le manifeste.
    assert json.loads((tmp_path / "client.json").read_text()) == manifeste


def test_tous_les_manifestes_du_depot_passent_la_synchronisation(tmp_path, monkeypatch):
    # Le dépôt réel, comme le job du matin, sans réseau : une entrée à récupérer reçoit des
    # octets factices, et les dossiers de travail sont créés hors du dépôt.
    monkeypatch.setattr(drive_sync, "ROOT", tmp_path)
    monkeypatch.setattr(drive_sync, "telecharger", lambda i: (b"octets-" + i.encode(), "jpg"))
    for manifeste in sorted(PHOTOS.glob("*.json")):
        avant = manifeste.read_bytes()
        drive_sync.synchroniser(manifeste.stem, dry_run=True)
        assert manifeste.read_bytes() == avant, manifeste.name

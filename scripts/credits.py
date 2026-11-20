"""Crédit des photographes sur les posts.

Une photo de la banque qui vient d'un photographe (registre photos/photographes.json) doit
le citer dans la légende. Règle de Maxime du 06/11/2026 : Jean-Philippe Homé-Sanfaute est
crédité sur chaque post qui utilise une de ses photos, avec la formule qu'il a donnée :

    LinkedIn  : « Photos : @Jean-Philippe Homé-Sanfaute »  (tag de son profil)
    Instagram : « Photos : @compte »  (nom seul tant que le compte n'est pas renseigné)
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRE = ROOT / "photos" / "photographes.json"


def charger(registre=REGISTRE):
    if not Path(registre).exists():
        return []
    return json.loads(Path(registre).read_text(encoding="utf-8"))["photographes"]


def photographe(entree, photographes=None):
    """Le photographe d'une entrée de manifeste, ou None."""
    if not entree:
        return None
    photographes = charger() if photographes is None else photographes
    nom_fichier = (entree.get("drive_nom") or entree.get("nom") or "").upper()
    credit = entree.get("credit") or ""
    for ph in photographes:
        if any(nom_fichier.startswith(p.upper()) for p in ph.get("prefixes_fichier", [])):
            return ph
        if any(m.lower() in credit.lower() for m in ph.get("dans_credit", [])):
            return ph
    return None


def mention(ph, reseau="instagram"):
    """Comment le nommer sur ce réseau."""
    if reseau == "linkedin" and ph.get("mention_linkedin"):
        return ph["mention_linkedin"]
    compte = (ph.get("instagram") or "").lstrip("@").strip()
    if reseau in ("instagram", "facebook", "tiktok") and compte:
        return f"@{compte}"
    return ph["nom"]


def _photographes_de(entrees, photographes):
    vus = []
    for e in entrees:
        ph = photographe(e, photographes)
        if ph and ph["cle"] not in [v["cle"] for v in vus]:
            vus.append(ph)
    return vus


def ligne_credit(entrees, photographes=None, reseau="instagram"):
    """La ligne à poser en fin de légende, ou "" si aucune photo n'est créditée."""
    vus = _photographes_de(entrees, photographes)
    if not vus:
        return ""
    formule = vus[0].get("formule") or "Photos : "
    return formule + ", ".join(mention(ph, reseau) for ph in vus)


def crediter(legende, entrees, photographes=None, reseau="instagram"):
    """Ajoute la ligne de crédit à une légende, une seule fois."""
    ligne = ligne_credit(entrees, photographes, reseau)
    if not ligne or ligne in legende:
        return legende
    return f"{legende.rstrip()}\n\n{ligne}"


def comptes_manquants(entrees, photographes=None):
    """Photographes crédités dont le compte Instagram n'est pas encore renseigné."""
    return sorted({ph["nom"] for e in entrees
                   if (ph := photographe(e, photographes)) and not ph.get("instagram")})

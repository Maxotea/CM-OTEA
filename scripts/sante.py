#!/usr/bin/env python3
"""Le bilan de santé de l'outil CM : ce qui va, ce qui cloche, ce qui manque pour la semaine.

    python3 scripts/sante.py            # rapport, sortie 0 quoi qu'il arrive
    python3 scripts/sante.py --strict   # sortie 1 dès qu'un ⚠ est levé (pour un garde-fou CI)

Une commande, sans réseau ni secret, qui répond en trois secondes aux questions que l'on
se pose chaque matin en ouvrant le dépôt :

  - les configurations disent-elles la même chose ? (un compte clos encore actif dans la
    review, un blog_id qui diverge, un compte de review sans fichier Drive) ;
  - le carrousel du prochain mercredi est-il écrit pour chaque compte actif ? C'est la
    panne silencieuse la plus fréquente : l'action du vendredi ne trouve aucune spec et
    sort en erreur, personne ne regarde, le client reçoit une semaine sans carrousel ;
  - les fichiers de review de la semaine prochaine existent-ils ? (à partir du vendredi) ;
  - la relève a-t-elle laissé des ✅ en échec dans le journal ? (post introuvable, refus
    Metricool) : chacun est un accord client non honoré ;
  - des textes destinés au client portent-ils un tiret cadratin ?
  - combien de médias clients attendent une qualification (sujet, pilier vides) ?

Le rapport est en Markdown : il se lit dans un terminal comme dans le résumé d'un run
GitHub Actions (variable GITHUB_STEP_SUMMARY). C'est la première chose que lit la revue
quotidienne de l'outil (.claude/taches-planifiees/review-quotidienne-outil/).
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIRETS = ("—", "–")


def _json(chemin):
    return json.loads((ROOT / chemin).read_text(encoding="utf-8"))


def _prochain(jour_semaine, depuis=None, strict=True):
    """La prochaine date tombant ce jour (0 = lundi … 6 = dimanche), strictement après `depuis`."""
    d = depuis or date.today()
    ecart = (jour_semaine - d.weekday()) % 7
    if ecart == 0 and strict:
        ecart = 7
    return d + timedelta(days=ecart)


# ---------------------------------------------------------------- les contrôles

def comptes():
    """Vue unifiée des comptes : reviews/config.json enrichi de recaps/clients-config.json."""
    reviews = _json("reviews/config.json")["comptes"]
    clients = {c["blog_id"]: c for c in _json("recaps/clients-config.json")["comptes"]}
    vue = []
    for r in reviews:
        c = clients.get(r["blog_id"], {})
        vue.append({**r, "client_actif": c.get("actif", True) if c else None, "client": c})
    return vue


def controle_configs(vue):
    lignes = []
    for c in vue:
        if c["client"] == {}:
            lignes.append(("⚠", f"{c['slug']} : absent de recaps/clients-config.json"))
        if c.get("actif") and c["client_actif"] is False:
            lignes.append(("⚠", f"{c['slug']} : compte clos dans clients-config.json mais encore "
                                f"actif dans reviews/config.json : un fichier de review lui est "
                                f"généré chaque vendredi pour rien"))
        if c.get("actif") and not c.get("drive_fichier"):
            lignes.append(("⚠", f"{c['slug']} : actif dans la review mais sans drive_fichier : "
                                f"la relève ne lit rien"))
    return lignes


def controle_carrousels(vue, aujourd_hui):
    """Le carrousel du mercredi, pour chaque compte actif qui a une DA de carrousel."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from publier import BLOG_IDS  # noqa: E402
    themes = set(_json("scripts/themes.json")) - {"_doc"}
    actifs = [c["slug"] for c in vue
              if c["client_actif"] is not False and c["slug"] in BLOG_IDS and c["slug"] in themes]
    lignes = []
    # Le vendredi, l'action vise le mercredi de la semaine SUIVANTE : dès le vendredi on
    # regarde donc deux mercredis, sinon on ne verrait le manque qu'après l'échec du run.
    mercredis = [_prochain(2, aujourd_hui)]
    if aujourd_hui.weekday() >= 4:
        mercredis.append(mercredis[0] + timedelta(days=7))
    for mercredi in mercredis:
        manquants = [s for s in actifs
                     if not list((ROOT / "carrousels" / s).glob(f"{mercredi}-*.json"))]
        if manquants:
            lignes.append(("⚠", f"carrousel du mercredi {mercredi:%d/%m} : aucune spec pour "
                                f"{', '.join(manquants)} (carrousels/<client>/{mercredi}-<slug>.json)"))
        else:
            lignes.append(("✓", f"carrousel du mercredi {mercredi:%d/%m} : spec présente pour "
                                f"les {len(actifs)} comptes actifs"))
    return lignes


def controle_reviews(vue, aujourd_hui):
    """À partir du vendredi, le fichier de la semaine suivante doit exister par compte actif."""
    if aujourd_hui.weekday() < 4:
        return [("·", "fichiers de review de la semaine prochaine : générés le vendredi à 7h00")]
    lundi = _prochain(0, aujourd_hui)
    lignes = []
    for c in vue:
        if not c.get("actif"):
            continue
        chemin = ROOT / "reviews/a-envoyer" / f"{c['slug']}-{lundi}.xlsx"
        if chemin.exists():
            lignes.append(("✓", f"{c['slug']} : fichier de la semaine du {lundi:%d/%m} généré"))
        else:
            lignes.append(("⚠", f"{c['slug']} : pas de fichier de review pour la semaine du "
                                f"{lundi:%d/%m} (aucun brouillon dans Metricool, ou job generer en échec)"))
    return lignes


def controle_journal(vue, aujourd_hui):
    """Les ✅ que la relève n'a pas pu honorer, sur les deux dernières semaines."""
    lignes = []
    limite = (aujourd_hui - timedelta(days=14)).isoformat()
    for c in vue:
        chemin = ROOT / "reviews/etat" / f"{c['slug']}.json"
        if not chemin.exists():
            continue
        etat = json.loads(chemin.read_text(encoding="utf-8"))
        for semaine, refs in etat.get("semaines", {}).items():
            if semaine < limite:
                continue
            for ref, entree in refs.items():
                resultat = entree.get("resultat") or ""
                if entree.get("decision") == "OK" and ("introuvable" in resultat or "échec" in resultat):
                    lignes.append(("⚠", f"{c['slug']} {ref} (semaine du {semaine}) : ✅ du client "
                                        f"non honoré : {resultat}"))
                elif entree.get("en_attente"):
                    lignes.append(("·", f"{c['slug']} {ref} : ✅ retenu, {resultat.split(':')[0]}"))
    return lignes or [("✓", "journal des décisions : aucun ✅ en échec sur deux semaines")]


def _chaines(valeur):
    if isinstance(valeur, str):
        yield valeur
    elif isinstance(valeur, dict):
        for k, v in valeur.items():
            if k not in ("note", "cible"):
                yield from _chaines(v)
    elif isinstance(valeur, list):
        for v in valeur:
            yield from _chaines(v)


def controle_tirets():
    fautes = 0
    for spec in (ROOT / "carrousels").rglob("*.json"):
        fautes += sum(any(t in s for t in TIRETS) for s in _chaines(json.loads(spec.read_text(encoding="utf-8"))))
    modele = (ROOT / "recaps/modele-mail-review.md").read_text(encoding="utf-8")
    fautes += sum(any(t in l for t in TIRETS) for l in modele.splitlines())
    if fautes:
        return [("⚠", f"{fautes} texte(s) client avec un tiret cadratin (python3 -m pytest tests/test_style.py)")]
    return [("✓", "aucun tiret cadratin dans les textes client")]


def controle_medias():
    lignes = []
    for manifeste in sorted((ROOT / "photos").glob("*.json")):
        photos = json.loads(manifeste.read_text(encoding="utf-8")).get("photos", [])
        a_qualifier = [p for p in photos if not p.get("sujet") or not p.get("pilier")]
        if a_qualifier:
            lignes.append(("·", f"{manifeste.stem} : {len(a_qualifier)} média(s) déposé(s) par le client "
                                f"sans sujet ni pilier, à qualifier avant usage"))
    return lignes


# ---------------------------------------------------------------- le rapport

def bilan(aujourd_hui=None):
    aujourd_hui = aujourd_hui or date.today()
    vue = comptes()
    sections = [
        ("Configurations", controle_configs(vue) or [("✓", "reviews/config.json, clients-config.json et publier.py concordent")]),
        ("Carrousel du mercredi", controle_carrousels(vue, aujourd_hui)),
        ("Review client", controle_reviews(vue, aujourd_hui)),
        ("Journal des décisions", controle_journal(vue, aujourd_hui)),
        ("Règle d'écriture", controle_tirets()),
        ("Médias clients", controle_medias() or [("✓", "aucun média en attente de qualification")]),
    ]
    return aujourd_hui, sections


def rendre(aujourd_hui, sections):
    alertes = sum(1 for _, lignes in sections for niveau, _ in lignes if niveau == "⚠")
    titre = f"## Bilan de santé de l'outil CM, {aujourd_hui:%d/%m/%Y}"
    sortie = [titre, "", f"**{alertes} point(s) d'attention.**" if alertes else "**Rien à signaler.**", ""]
    for nom, lignes in sections:
        sortie.append(f"### {nom}")
        sortie.extend(f"- {niveau} {texte}" for niveau, texte in lignes)
        sortie.append("")
    return "\n".join(sortie), alertes


def main():
    ap = argparse.ArgumentParser(description="Bilan de santé de l'outil CM.")
    ap.add_argument("--strict", action="store_true", help="sortie 1 dès qu'un ⚠ est levé")
    ap.add_argument("--date", help="faire le bilan comme si on était ce jour (YYYY-MM-DD)")
    args = ap.parse_args()

    texte, alertes = rendre(*bilan(date.fromisoformat(args.date) if args.date else None))
    print(texte)
    resume = os.environ.get("GITHUB_STEP_SUMMARY")
    if resume:
        with open(resume, "a", encoding="utf-8") as f:
            f.write(texte + "\n")
    return 1 if (args.strict and alertes) else 0


if __name__ == "__main__":
    sys.exit(main())

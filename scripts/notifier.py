#!/usr/bin/env python3
"""Vide la file des signaux de veille de la review client et prévient Maxime.

    python3 scripts/notifier.py [--dry-run]

Le problème résolu : un client corrige son tableau le mercredi soir, et personne ne le
sait avant le récap du lundi suivant. scripts/review.py relève déjà les fichiers trois
fois par jour et sait donc, à chaque passage, si le tableau a bougé — il dépose ce
constat dans reviews/etat/notifications.json. Ce script est l'autre moitié : il porte le
signal jusqu'au téléphone.

Deux canaux, cumulables, dans cet ordre de fiabilité :

  1. NOTIF_WEBHOOK (secret du dépôt) — une URL qui reçoit le signal en JSON. C'est le
     canal utile : branchée sur un « Catch Hook » Zapier, elle devient un mail, un SMS,
     une notification WhatsApp ou une notif push, au choix, sans rien changer ici.
  2. Une issue GitHub, toujours. Une par client et par semaine, les signaux suivants
     arrivent en commentaire du même fil. Gratuit, sans réglage, et ça sert d'archive :
     on voit après coup quand le client a répondu.

Rien n'est perdu si l'envoi échoue : le signal reste « en_attente » et repart au passage
suivant. Un signal envoyé est mémorisé pour ne jamais être répété.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "reviews" / "etat" / "notifications.json"
MEMOIRE = 50  # signaux envoyés qu'on garde en mémoire, pour la trace

ICONES = {"termine": "🎉", "premiers_retours": "🔔", "nouveaux_retours": "✏️",
          "decision_illisible": "⚠️"}


def _poster(url, charge, entetes):
    requete = urllib.request.Request(
        url, data=json.dumps(charge).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", **entetes})
    with urllib.request.urlopen(requete, timeout=30) as reponse:
        return json.loads(reponse.read() or b"{}")


def envoyer_webhook(url, evenements):
    """Un POST par lot de signaux. Le corps est plat exprès : un Zap le lit sans code."""
    tete = evenements[0]
    charge = {
        "source": "review-hebdo",
        "client": tete["nom"],
        "semaine": tete["semaine"],
        "type": tete["type"],
        "titre": tete["titre"],
        "detail": " ".join(e["detail"] for e in evenements),
        "lien": tete.get("lien"),
        "signaux": evenements,
    }
    _poster(url, charge, {})


def corps_issue(evenements):
    lignes = []
    for e in evenements:
        lignes.append(f"{ICONES.get(e['type'], '•')} **{e['titre']}**")
        lignes.append("")
        lignes.append(e["detail"])
        if e.get("lien"):
            lignes.append("")
            lignes.append(f"[Ouvrir le tableau du client]({e['lien']})")
        lignes.append("")
        lignes.append(f"<sub>relevé le {e['quand'].replace('T', ' à ')}</sub>")
        lignes.append("")
        lignes.append("---")
        lignes.append("")
    return "\n".join(lignes).rstrip("-\n ")


def envoyer_issue(depot, jeton, numero, evenements):
    """Crée le fil de la semaine, ou commente celui qui existe. Retourne son numéro."""
    entetes = {"Authorization": f"Bearer {jeton}",
               "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    corps = corps_issue(evenements)
    if numero:
        _poster(f"https://api.github.com/repos/{depot}/issues/{numero}/comments",
                {"body": corps}, entetes)
        return numero
    tete = evenements[0]
    cree = _poster(
        f"https://api.github.com/repos/{depot}/issues",
        {"title": f"🔔 Retours client — {tete['nom']} — semaine du {tete['semaine']}",
         "body": corps,
         "labels": ["review-client"]},
        entetes)
    return cree.get("number")


def main():
    ap = argparse.ArgumentParser(description="Envoie les signaux de veille de la review client.")
    ap.add_argument("--dry-run", action="store_true", help="montrer sans envoyer")
    args = ap.parse_args()

    if not FILE.exists():
        print("Aucune file de signaux — rien à envoyer.")
        return 0
    file = json.loads(FILE.read_text(encoding="utf-8"))
    en_attente = file.get("en_attente") or []
    if not en_attente:
        print("File vide — rien à envoyer.")
        return 0

    webhook = os.environ.get("NOTIF_WEBHOOK")
    jeton = os.environ.get("GITHUB_TOKEN")
    depot = os.environ.get("GITHUB_REPOSITORY")
    if not args.dry_run and not webhook and not (jeton and depot):
        print("✗ aucun canal disponible (ni NOTIF_WEBHOOK, ni GITHUB_TOKEN + "
              "GITHUB_REPOSITORY) — les signaux restent en file.", file=sys.stderr)
        return 1

    # Un envoi par client et par semaine : le client voit un fil par semaine, pas un
    # message par ligne corrigée.
    lots = {}
    for e in en_attente:
        lots.setdefault((e["client"], e["semaine"]), []).append(e)

    fils = file.setdefault("fils", {})
    partis, restes, echecs = [], [], 0
    for (client, semaine), evenements in lots.items():
        titres = ", ".join(e["titre"] for e in evenements)
        if args.dry_run:
            print(f"[dry-run] {client} / {semaine} : {titres}")
            restes.extend(evenements)
            continue
        try:
            if webhook:
                envoyer_webhook(webhook, evenements)
            if jeton and depot:
                cle = f"{client}:{semaine}"
                fils[cle] = envoyer_issue(depot, jeton, fils.get(cle), evenements)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            print(f"✗ {client} / {semaine} : envoi impossible — {exc}", file=sys.stderr)
            restes.extend(evenements)
            echecs += 1
            continue
        print(f"🔔 {client} / {semaine} : {titres}")
        partis.extend(evenements)

    if not args.dry_run:
        file["en_attente"] = restes
        file["envoyes"] = (file.get("envoyes") or [])[-(MEMOIRE - len(partis)):] + partis
        FILE.write_text(json.dumps(file, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n{len(partis)} signal(aux) envoyé(s), {len(restes)} en attente.")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Relit les posts déjà planifiés dans Metricool et signale ceux qui sont incomplets.

    python3 scripts/audit_posts.py
    python3 scripts/audit_posts.py --client la-galerie-immobiliere --jours 180

Deux défauts, tous les deux rencontrés en production, tous les deux invisibles tant qu'on ne
relit pas le post entier — la vignette du calendrier Metricool ne les montre pas :

  - **la promesse de slides non tenue** : une légende écrite pour un carrousel (« Swipez pour
    découvrir → », « en quelques slides ») posée sur un post qui n'a qu'un seul média. Le
    lecteur cherche une suite qui n'existe pas. Relevé en juillet 2026 sur Pierre Huiban, puis
    le 07/08/2026 sur La Galerie Immobilière — deux fois le même lot, deux fois découvert à
    l'œil, des semaines après coup.
  - **le placeholder oublié** : un [VAINQUEUR] ou un [Prénom] resté dans le texte parce que le
    brouillon a été créé avant l'événement et jamais repris.

Ne signale que ce qui est mécaniquement faux. En particulier, un post feed **sans média n'est
pas signalé** : c'est l'état normal d'un brouillon dont la photo, faute d'URL publique, sera
attachée à la main dans Metricool. Signaler cet état noierait les vrais défauts.

Lit, n'écrit rien. Comme publier.py, conçu pour tourner dans GitHub Actions : la politique
réseau des sessions distantes bloque app.metricool.com.

Secrets attendus : METRICOOL_USER_ID, METRICOOL_TOKEN.
"""

import argparse
import os
import re
import sys
from datetime import date, timedelta

from publier import BLOG_IDS, metricool

# « Swipez », « faites défiler », « en quelques slides » : une légende qui annonce une suite.
PROMESSE = re.compile(r"\bslides?\b|\bswip\w*|faites?\s+d[ée]filer|d[ée]filez|carrousel", re.I)
# [VAINQUEURE], [Prénom], [MARQUE + CLUBS] : un gabarit jamais repris après l'événement.
PLACEHOLDER = re.compile(r"\[[^\]\n]{2,40}\]")


def type_de(post):
    """Le type réel du post. instagramData fait foi : c'est lui qui distingue STORY et REEL.

    twitterData annonce POST même sur une story — le lire en premier ferait auditer les stories
    comme des posts feed.
    """
    for cle in ("instagramData", "facebookData"):
        t = (post.get(cle) or {}).get("type")
        if t:
            return t
    return "POST"


def auditer(client, debut, fin):
    """Retourne les défauts trouvés sur un compte, dans l'ordre de publication."""
    posts = metricool("/scheduler/posts", blogId=BLOG_IDS[client],
                      start=f"{debut}T00:00:00", end=f"{fin}T23:59:59").get("data", [])
    defauts = []
    for p in sorted(posts, key=lambda x: x.get("publicationDate", {}).get("dateTime", "")):
        if type_de(p) == "STORY":
            continue
        texte = p.get("text") or ""
        medias = len(p.get("media") or [])
        quand = p.get("publicationDate", {}).get("dateTime", "?")
        if PROMESSE.search(texte) and medias <= 1:
            defauts.append((quand, p["id"], f"légende de carrousel, {medias} média(s)", texte))
        restes = PLACEHOLDER.findall(texte)
        if restes:
            defauts.append((quand, p["id"], f"placeholder {' '.join(restes)}", texte))
    return defauts


def main():
    ap = argparse.ArgumentParser(description="Signale les posts planifiés incomplets.")
    ap.add_argument("--client", help="ne relire qu'un compte, ex. la-galerie-immobiliere")
    ap.add_argument("--jours", type=int, default=120,
                    help="profondeur de la relecture, à partir d'aujourd'hui (défaut : 120)")
    ap.add_argument("--strict", action="store_true",
                    help="sortir en erreur si un défaut est trouvé. Sans ce drapeau le script "
                         "signale et rend la main : un défaut de rédaction ne doit pas faire "
                         "échouer la publication des carrousels de la semaine")
    args = ap.parse_args()

    absents = [v for v in ("METRICOOL_USER_ID", "METRICOOL_TOKEN") if not os.environ.get(v)]
    if absents:
        raise SystemExit(f"secrets manquants : {', '.join(absents)}")

    clients = [args.client] if args.client else sorted(BLOG_IDS)
    inconnus = [c for c in clients if c not in BLOG_IDS]
    if inconnus:
        raise SystemExit(f"compte inconnu : {', '.join(inconnus)}")

    debut = date.today()
    fin = debut + timedelta(days=args.jours)
    total = 0
    for client in clients:
        try:
            defauts = auditer(client, debut, fin)
        except Exception as exc:
            print(f"✗ {client} : {exc}", file=sys.stderr)
            continue
        if not defauts:
            print(f"✓ {client} — rien à signaler")
            continue
        total += len(defauts)
        print(f"\n⚠️  {client} — {len(defauts)} post(s) à reprendre")
        for quand, post_id, motif, texte in defauts:
            print(f"   {quand} · id {post_id} · {motif}")
            print(f"      « {texte.splitlines()[0][:70]} »")

    print(f"\n{total} défaut(s) sur {len(clients)} compte(s), du {debut} au {fin}.")
    return 1 if (total and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())

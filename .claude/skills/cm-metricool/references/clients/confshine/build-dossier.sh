#!/bin/sh
# Assemble les fiches du dossier ConfShine en un seul document, destiné à la base de
# connaissances du projet Claude « ConfShine ».
#
#   sh build-dossier.sh [chemin/de/sortie.md]
#
# Les fiches individuelles restent la source de vérité : régénérer après toute
# modification plutôt que d'éditer le document assemblé.

set -e
cd "$(dirname "$0")"
OUT="${1:-CONFSHINE-dossier.md}"

sed -n '1,/^---$/p' en-tete-dossier.md > "$OUT"

for f in brief.md cible-client.md offres-tarifs.md fiche-client.md \
         banque-medias.md scripts-reels.md calendrier-2026-09.md; do
  printf '\n\n---\n\n' >> "$OUT"
  sed -e 's/^### /#### /' -e 's/^## /### /' -e 's/^# /## /' "$f" >> "$OUT"
done

echo "écrit : $OUT ($(wc -c < "$OUT") octets)"

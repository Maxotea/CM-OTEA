#!/usr/bin/env bash
# Montage V1 du reel Nina Ramen depuis le disque dur vert.
# Usage : ./projets/nina-ramen/montage.sh [dossier des rushs] [options reel-montage.py…]
set -euo pipefail
cd "$(dirname "$0")/../.."
export PATH="$HOME/.local/node/bin:$PATH"     # ffmpeg / ffprobe sur le Mac

DOSSIER="${1:-}"
if [ -n "$DOSSIER" ]; then shift; fi
if [ -z "$DOSSIER" ]; then
  for base in /Volumes/*; do
    for cand in "$base/Nina Ramen" "$base/NINA RAMEN" "$base/nina ramen" "$base/Nina-Ramen"; do
      if [ -d "$cand" ]; then DOSSIER="$cand"; break 2; fi
    done
  done
fi
if [ -z "$DOSSIER" ] || [ ! -d "$DOSSIER" ]; then
  echo "✗ dossier « Nina Ramen » introuvable sur /Volumes : branche le disque vert" >&2
  echo "  ou passe le chemin : $0 \"/Volumes/VERT/Nina Ramen\"" >&2
  exit 1
fi
echo "• rushs : $DOSSIER"
python3 scripts/reel-montage.py "$DOSSIER" \
  --titre "NINA RAMEN" --duree 90 --look ramen \
  --sortie o/nina-ramen-reel-v1.mp4 "$@"

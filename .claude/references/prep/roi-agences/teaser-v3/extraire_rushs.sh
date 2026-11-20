#!/bin/zsh
# Extrait les morceaux de rushs utilisés par le teaser v3 (1080p ProRes 422, dossier $1).
# HYROX (S-Log3) : LUT OTEA_HYROX_SLog3_Look_v2. GO Entrepreneurs : filmé à la verticale,
# on recadre une bande 16:9 dans l'image redressée (sinon l'image est écrasée).
set -e
OUT=${1:-rushs}; mkdir -p "$OUT"
LUT="/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/OTEA/OTEA_HYROX_SLog3_Look_v2.cube"
cp "$LUT" "$OUT/lut.cube"
R="$HOME/Desktop/HYROX ROME 2026/FX3POST20260926_"
B="$HOME/Desktop/HYROX BORDEAUX 2026/RUSHS/FX3POST20260930_"
TL="/Volumes/VERT SSD/HYROX TOULOUSE/VIDEO/FX3HYROXTLS20260319_"
G="/Volumes/ORANGE SSD/GO ENTREPRENEURS/VIDEO/"
hyrox(){ ffmpeg -v error -y -ss $3 -t $4 -i "$2" -an -vf "scale=1920:1080:flags=lanczos,lut3d=file=$OUT/lut.cube" -c:v prores_ks -profile:v 2 -pix_fmt yuv422p10le "$OUT/$1.mov"; }
go(){ f=$(ls "$G"FX3202604*_$1.MP4); ffmpeg -v error -y -ss $2 -t $3 -i "$f" -an -vf "crop=2160:1215:0:$(( $4 * 4 )),scale=1920:1080:flags=lanczos" -c:v prores_ks -profile:v 2 -pix_fmt yuv422p10le "$OUT/$1.mov"; }
hyrox 7341 "${R}7341.MP4" 0 8;   hyrox 7319 "${R}7319.MP4" 0 4;   hyrox 7338 "${R}7338.MP4" 0 2.2
hyrox 7367 "${R}7367.MP4" 1.5 3; hyrox 7374 "${R}7374.MP4" 2 2.5; hyrox 7366 "${R}7366.MP4" 0 1.5
hyrox 7086 "${B}7086.MP4" 12 4;  hyrox 7088 "${B}7088.MP4" 0 3;   hyrox 7105b "${B}7105.MP4" 9 3.5
hyrox 7106b "${B}7106.MP4" 11.5 5.5; hyrox 7127 "${B}7127.MP4" 0 5; hyrox 7137 "${B}7137.MP4" 0 6
hyrox 7138 "${B}7138.MP4" 0 5;   hyrox 7104 "${B}7104.MP4" 4 4
hyrox 1065 "${TL}1065.MP4" 8 9;  hyrox 1135 "${TL}1135.MP4" 2 8
go 1256 0 9 410; go 1261 0 7 450; go 1270 0 4.5 520; go 1339 2 10 200; go 1349 0 1.44 220

# Teaser R.O.I. v3

Motion design (titres.html) et flashs de vrais rushs OTEA (HYROX Rome, Bordeaux,
Toulouse ; GO Entrepreneurs à Paris La Défense Arena), calés sur « Runaway » à 138 BPM.
Aucun plan généré, aucun coureur torse nu.

1. `./extraire_rushs.sh rushs` : extraits 1080p (LUT S-Log3, GO recadré en 16:9).
2. `node rendu-titres.mjs titres 25` puis `MASQUE=1 node rendu-titres.mjs masques 25`.
3. `python3 montage.py rushs expo.json titres masques master.mov` (expo.json : exposition par plan).
4. Ajouter la musique (début à 32,437 s dans le morceau) et encoder en H.264.

Le plan de coupe est dans `plan.py`.

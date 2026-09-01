# Stories : aucune bande son

**Règle de Maxime, 04/08/2026.** Toute vidéo de story livrée dans Metricool
part **muette**. On ne colle plus de fond sonore au montage.

## Pourquoi
Maxime ajoute lui-même l'audio dans l'interface Instagram au moment de valider
(sticker musique natif, son tendance). Une piste incrustée l'en empêche et se
superpose mal aux usages de la plateforme.

## Ce que ça implique à la production
- Assemblage ffmpeg : **pas de `-map <audio>`**, et ajouter `-an`.
  ```
  ffmpeg -i fond.mp4 -i calque.png -filter_complex "..." -map "[v]" -an ...
  ```
- Pour retirer le son d'une vidéo déjà rendue, pas besoin de ré-encoder :
  ```
  ffmpeg -i in.mp4 -an -c copy out.mp4
  ```
- `scripts/fond-sonore-stories.py` n'est **plus appelé pour les stories**. Il
  reste au dépôt : il peut servir à d'autres formats (reels, montages longs) si
  Maxime le redemande explicitement.
- Vérifier après rendu : `ffprobe` ne doit remonter aucun flux audio.

## Périmètre
Tous les comptes, sans exception : J Lawson, La Galerie, Run On Invest,
Pierre Huiban, Le Loft, Gossip, OTEA.

## État au 19/08/2026 : conforme partout
Les 10 comptes ont été balayés et chaque vidéo de story programmée vérifiée à
l'`ffprobe`. Détail des médias et de la procédure :
`_portage/REPRISE-STORIES-PHOTOS.md`.

**Deux pièges vérifiés à la dure :**
- Ne jamais déduire qu'un compte est muet parce que ses stories « sont
  anciennes ». OTEA PRODUCTION portait du son sur ses 3 cartes photo. Seul
  `ffprobe` tranche.
- Lister le calendrier **jusqu'au bout**, pas sur 15 jours : J Lawson avait 30
  stories de septembre hors de la première fenêtre, dont 18 encore sonores.

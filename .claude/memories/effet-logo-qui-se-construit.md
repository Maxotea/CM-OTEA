---
name: effet-logo-qui-se-construit
description: "Effet demandé par Maxime le 07/11/2026 pour les aftermovies et montages : sur la VRAIE photo d'un lieu, le logo est absent puis s'assemble tout seul et se pose à sa place. i2v Kling 3.0 image de début + image de fin, contrôle de la dernière image, fin sur la vraie photo."
metadata:
  node_type: memory
  type: process
  modified: 2026-11-07T00:00:00.000Z
---

**Demande de Maxime, 07/11/2026 :** « Apprends à faire cet effet pour les prochains
after-movie et montages », sur le reel
[DeD1VHeuHfb](https://www.instagram.com/reel/DeD1VHeuHfb/) (@welamall, 18 s,
2 827 j'aime). Inspiration n° 4 de
`.claude/skills/cm-metricool/references/inspirations-montage.md`.

## Ce qu'on voit dans le reel (mesuré image par image)

- **Trois plans de 6 s, coupe franche** (0 à 6,4 s, 6,5 à 12,4 s, 12,5 à 18,2 s).
  Aucune coupe à l'intérieur d'un plan : c'est un seul plan i2v à chaque fois.
- **Le lieu ne bouge pas.** Caméra fixe, façade identique du début à la fin. Seul
  le logo vit.
  1. Enseigne de façade : le logo rond se dessine, puis les lettres « JUST FOR FUN »
     arrivent en volume, une par une, et se calent.
  2. Façade large : le pictogramme manette s'allume en vert, les lettres se
     posent à côté dans l'ordre de lecture.
  3. Gros plan du logo rond : un disque sombre pivote face caméra, la manette se
     trace dessus en néon vert.
- Le reel est une vitrine d'outil (« Prompt + photo = vidéo », modèle « Omni
  Flash ») : on ne reprend **pas** cet habillage, seulement l'effet, en plein cadre.
- **Défaut visible chez eux :** au milieu du plan 2 on lit « JUST FOIF » puis
  « JUST FOR UN ». Le modèle épelle mal tant que le logo n'est pas posé. Notre
  méthode règle ça (voir plus bas).

## Pourquoi c'est permis par nos règles

C'est la règle 2 de `CLAUDE.md` appliquée à un logo : **vraie photo du client,
animée en i2v**. Aucun lieu inventé, aucun visage. Si une personne est dans le
cadre, choisir une autre photo : le modèle déforme les visages
(`stories-vraies-photos-sans-ia.md`).

## La chaîne, dans l'ordre

1. **Choisir les photos.** Trois vraies photos où le logo est net, de face ou de
   trois quarts : la façade large, l'enseigne, le logo en gros plan (ou le stand,
   la scène, le kakémono sur un événement). Recadrer en 9:16 dans PIL **avant**
   tout (piège mesuré du 28/08 : un i2v 9:16 lancé depuis une photo paysage
   réinvente le lieu).
2. **Fabriquer l'image de début : la même photo, sans le logo.** Sur un mur uni
   ou en dégradé : `python3 scripts/logo-reveal.py effacer photo-916.jpg --zone
   cx,cy,rx,ry --sortie photo-sans-logo.jpg` (OpenCV, en local, zéro crédit ; la
   zone est l'ellipse du logo et de son halo, en pixels). Sur un fond texturé
   (brique, bois), remplissage génératif limité à la zone du logo. Attention :
   `image_fill_area` d'Adobe ne remplit qu'en couleur unie, il ne convient pas.
   Vérifier à l'œil que rien d'autre n'a changé.
3. **Prompt et réglages :** `python3 scripts/logo-reveal.py prompt --style <style>
   --logo "<ce qui s'anime, en anglais>"`. Styles : `pieces`, `lettres`, `disque`,
   `neon` (les trois du reel, plus le néon simple). Varier le style d'un plan à
   l'autre, comme dans le reel.
4. **Animer :** `generate_video`, modèle `kling3_0`, `mode: std`, `sound: off`,
   `duration: 6`, `aspect_ratio: "9:16"`, `use_unlim: false`,
   `medias: [{photo sans logo, start_image}, {vraie photo, end_image}]`.
   **6,25 crédits par plan de 5 s** (préflight du 07/11), donc environ 20 crédits
   pour les trois plans. L'image de fin force le modèle à retomber sur le vrai
   logo : c'est ce qui manquait au reel.
5. **Contrôler et monter :** `python3 scripts/logo-reveal.py assembler
   plan1.mp4:photo1.jpg plan2.mp4:photo2.jpg plan3.mp4:photo3.jpg --sortie ...`.
   Le script compare la dernière image de chaque plan à sa photo (seuil 8 ; 4 à 6
   sur un plan sain, 50 sur un lieu différent), refuse le montage si un plan a
   dérivé, puis recadre en 1080×1920 plein cadre et **termine chaque plan sur la
   vraie photo** (fondu 0,25 s, tenue 0,6 s). Sortie muette.
6. **Son :** aucun dans le fichier. Sur un reel, Maxime pose la musique dans
   Instagram (`reels-musique-instagram.md`). Le moment fort à caler sur le son est
   l'instant où le logo se pose : vers 4,5 à 5 s de chaque plan.

## Premier essai, 07/11/2026 : réussi

Photo d'origine de la cliente Gossip Beauty Center (salon rose, logo rond
« GOSSIP Beauty Center » éclairé au mur, personne dans le cadre ; fichier
i.ibb.co du manifeste `photos/gossip-beauty-center.json`). Pas la version
« luxe » retouchée en IA (fichier `hf_…png`) : on part toujours de l'originale.

- Recadrage 9:16 **calé à gauche**, pas centré : le logo touchait le bord gauche,
  un recadrage centré l'aurait coupé. Toujours vérifier que le logo entier, halo
  compris, reste dans le cadre.
- Effacement : `--zone 100,662,200,205` sur l'image 1080×1920.
- Kling 3.0, style `pieces`, 6 s : un disque se creuse dans le mur, des éclats
  arrivent, « GOSSIP » se monte (lettres un peu espacées en cours de route), le
  disque s'éclaire et retombe sur le vrai logo. Plan
  `hf_20261107_152434_8649e4a9-64ab-4bba-b8c9-b7c133f87641.mp4` sur
  `d8j0ntlcm91z4.cloudfront.net`, réutilisable à zéro crédit.
- Contrôles : 2,0 entre la première image et la photo sans logo, **1,9** entre la
  dernière image et la vraie photo, 0,7 sur le décor (moitié droite) entre début
  et fin. Montage final 6,6 s, 1080×1920, muet. Coût : un plan, environ 7,5 crédits.

## Où l'utiliser

- **Aftermovie d'événement** (`scripts/aftermovie.py`, `MONTAGE-OTEA/aiirf`) :
  en **ouverture** (le logo de l'événement ou du client se construit sur la photo
  du lieu, avant le premier plan de rushs) ou en **plan de fin** à la place du
  carton noir. Un seul plan suffit ; trois plans, c'est un reel à part entière.
- **Reel « ouverture »** d'un commerce du portefeuille (Le Loft, Gossip Beauty
  Center, J Lawson Golf, La Galerie Immobilière) : sa vraie façade, son vrai logo.
- **Vitrine OTEA Production** : reel « on fait ça pour votre lieu », à poser
  dans la ligne des offres.

## Repli sans image de début

Si le remplissage génératif abîme le mur, mode `--mode une-image` :
`kling3_0_turbo`, vraie photo en `start_image` seule, prompt du reel (le logo
disparaît puis revient). Moins sûr : le contrôle de la dernière image devient
indispensable et le fondu sur la vraie photo cache l'éventuelle faute
d'orthographe finale.

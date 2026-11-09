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
2 827 j'aime). Inspiration n° 5 de
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

## Les deux retours de Maxime sur le premier essai (08/11/2026)

1. **Plus jamais le logo Gossip Beauty Center** pour cet effet. Les essais et les
   démos se font sur **J Lawson Golf, OTEA Production ou Otea Filmakers**.
2. **« La texture est trop 3D. »** Le logo qui sort du mur en volume, les éclats
   qui volent : non. Style par défaut désormais **à plat** (`trace` ou `encre`) :
   le logo se dessine dans la surface comme de la peinture ou de l'encre, sans
   épaisseur ni rebond. Les styles `pieces`, `lettres`, `disque` restent dans
   l'outil, uniquement sur demande.

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
   --logo "<ce qui s'anime, en anglais>"`. Par défaut `trace` (à plat) ; `encre`
   aussi à plat ; `pieces`, `lettres`, `disque`, `neon` sur demande seulement.
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

## Deuxième essai, 08/11/2026 : J Lawson Golf, à plat

Photo `HOME-SANFAUTE-260506-160020-01296.jpg` du shooting pro du 6 mai (dossier
Drive « jlawson-golf », `1XuEVMRqJOtlD7wmAUbJFV1SUhHolmiZy`, 99 originaux
téléchargeables par `https://drive.google.com/uc?export=download&id=<id>`) : le
grand symbole et « J LAWSON GOLF » imprimés sur la moquette du fitting, personne
dans le cadre. Les marques visibles au fond (Titleist, Ping) sont le vrai studio :
elles ne bougent pas. Ne jamais partir des `jlawson-ia-*.png` du même dossier, ce
sont des images IA.

- Recadrage 9:16 décalé de 470 px depuis la gauche : le texte finit au bord droit,
  on sacrifie le bout de la queue du symbole plutôt qu'une lettre.
- Effacement : masque fait à la main (symbole repéré par sa couleur jaune pâle
  dans le canal b du LAB, texte couvert par une bande), puis
  `effacer --masque masque.png --grain 1000,3950,2900,4880`. Sans `--grain`, la
  moquette devient une tache floue ; avec un grain pris trop près du logo, des
  bouts de logo réapparaissent en fantôme. Prendre un rectangle **entièrement**
  vide.
- Kling 3.0, style `trace`, 6 s, 7,5 crédits. Rendu : début propre (2,5), une
  silhouette sombre du symbole apparaît vers 0,5 s comme un pochoir, la couleur
  coule dans le symbole, puis les lettres s'impriment (en commençant par GOLF,
  pas par le J). Fin sur la vraie photo : écart **2,9**. Décor immobile : 1,1
  en haut, 1,4 en bas. Plan
  `hf_20261108_134903_e948b320-b437-417e-9748-79dff6dc6f9e.mp4`, réutilisable.

## Où l'utiliser

- **Aftermovie d'événement** (`scripts/aftermovie.py`, `MONTAGE-OTEA/aiirf`) :
  en **ouverture** (le logo de l'événement ou du client se construit sur la photo
  du lieu, avant le premier plan de rushs) ou en **plan de fin** à la place du
  carton noir. Un seul plan suffit ; trois plans, c'est un reel à part entière.
- **Reel « ouverture »** de J Lawson Golf (son logo au sol, en premier), puis
  d'autres commerces du portefeuille si Maxime le demande : leur vrai lieu,
  leur vrai logo. Pas Gossip Beauty Center (retour du 08/11).
- **Vitrine OTEA Production** : reel « on fait ça pour votre lieu », à poser
  dans la ligne des offres.

## Repli sans image de début

Si le remplissage génératif abîme le mur, mode `--mode une-image` :
`kling3_0_turbo`, vraie photo en `start_image` seule, prompt du reel (le logo
disparaît puis revient). Moins sûr : le contrôle de la dernière image devient
indispensable et le fondu sur la vraie photo cache l'éventuelle faute
d'orthographe finale.

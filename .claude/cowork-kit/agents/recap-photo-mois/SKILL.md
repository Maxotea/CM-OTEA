---
name: recap-photo-mois
description: Agent Cowork mensuel (le 28 de chaque mois, 9h, ordinateur allumé) qui fait le récap photo du mois pour OTEA Production et Otea Filmakers à partir de la galerie Photos du Mac (iPhone, tournages, projets) et le programme en brouillon dans Metricool. Utilise-le aussi quand Maxime dit « fais le récap du mois », « récap photo », « le mois en images ».
---

# Récap photo du mois (OTEA Production et Otea Filmakers)

Demande de Maxime du 22/10/2026 : « un récap photo que tu récupères dans ma galerie, dans ce que
j'ai fait, dans mes projets, photos prises avec mon iPhone ou des tournages aussi […] un petit
récap un peu humain, formel, behind the scene, mais très intimiste aussi, tout en restant corpo.
Et faire ça tous les mois. » Un carrousel par compte, chaque fin de mois.

## 0. Avant de commencer

- `cd ../CM-OTEA && git pull`. Lis `CLAUDE.md` (règles non négociables), les fiches
  `.claude/skills/cm-metricool/references/clients/otea-production.md`, `otea-filmakers.md` et
  `banque-photos-otea.md` (qui est Maxime sur les photos, photos à accord).
- Mois couvert : du 1er du mois au jour de l'exécution, plus les photos des 29, 30 et 31 du mois
  précédent si elles ne sont pas dans l'index (`recaps/medias-index.json`).
- Vérifie avec `getBrandSettings` que Instagram et Facebook sont bien connectés aux deux marques.
  Sinon, fais quand même le récap et signale-le en tête du compte rendu.

## 1. Collecter

Sources, dans cet ordre :
1. **L'appli Photos du Mac** : la photothèque iCloud (iPhone, lunettes Ray-Ban Meta, drone DJI,
   Insta360), filtrée sur les dates du mois. Exporte les originaux, EXIF conservé.
2. **Les tournages du mois** : exports Lightroom et originaux Sony (A7 IV, FX3) rangés dans
   `Médias clients/` par l'agent `tri-medias`.
3. **Ce qui s'est passé** : l'agenda Google du mois (lecture seule) et les devis signés du dossier
   `Devis et offres/`, pour savoir quels projets, quels lieux, quelles dates. C'est la seule source
   des faits écrits dans les légendes.

Écarte d'office les captures d'écran, les documents, les reçus, les photos de famille et de la
maison, les enfants, les plaques d'immatriculation lisibles, les écrans qui montrent un contenu
client confidentiel, et tout ce qui a déjà été publié (index `scan-medias.py`, Metricool des
60 derniers jours).

## 2. Choisir

**Ce qu'on cherche** : les coulisses vraies du mois. La caméra posée avant le tournage, le
plateau qui se monte, la lumière du matin sur un lieu, la route, le montage tard, Maxime au
travail. « Intimiste » veut dire le ressenti des coulisses, pas la vie privée.

**OTEA Production** (blogId 5733269, Instagram, Facebook, LinkedIn) : 6 à 10 photos.
- Tournages, plateau, matériel, lieux de captation, Maxime au travail.
- Une personne identifiable autre que Maxime (client, intervenant, participant, cadreur) n'entre
  que si son accord est noté dans `banque-photos-otea.md` (colonne Accord) ou dans le devis. Sinon,
  une photo où elle est de dos, floue ou lointaine, ou une autre photo.

**Otea Filmakers** (blogId 4728418, Instagram seul) : 6 à 10 photos.
- **Aucune personne d'autre que Maxime** (règle du 13/10/2026). Voyages, lumière, matériel en
  main, montage en route, Maxime seul.
- Pas de TikTok : le TikTok branché à la marque est celui d'OTEA Production.

**Pour les deux** :
- Vraies photos uniquement, jamais d'image générée ni retouchée par IA générative.
- Des jours et des projets différents, la photo la plus forte en premier.
- Une même photo ne sert pas aux deux comptes.
- Recadrage 4:5 (1080×1350) sans couper un visage, un geste ou un texte. Regarde chaque
  recadrage avant de le garder.

## 3. Préparer

- Originaux dans `Médias clients/otea-production/recap-AAAA-MM/` et
  `Médias clients/otea-filmakers/recap-AAAA-MM/`, nommés `AAAAMMJJ-sujet-court.jpg`. Les
  versions 4:5 vont dans un sous-dossier `4x5/`.
- Une planche contact par compte (12 vignettes au plus), avec date et sujet sous chaque photo.
- Héberge les versions 4:5 : Higgsfield `media_upload`, PUT, `media_confirm`. Contrôle ensuite le
  md5 de chaque fichier sur l'URL CloudFront (`.claude/memories/hebergement-photos-reelles-metricool.md`).

## 4. Écrire

Aucun fait inventé : un projet, un lieu, un chiffre ou un nom n'est écrit que s'il vient de
l'agenda, d'un devis ou d'une publication déjà faite. Un client n'est nommé que s'il a déjà été
nommé publiquement sur le compte ou si son accord est noté ; sinon, on reste générique (« un
séminaire à Paris », « une captation de soirée »). Aucun tiret cadratin, demi-cadratin ni « -- ».
Aucun placeholder.

**OTEA Production** : vouvoiement, « nous », corporate et humain.
- Ouverture : « <Mois> <année>, côté coulisses. »
- Deux à quatre lignes sur ce que le mois a été (types de projets, lieux, nombre de tournages si
  l'agenda le dit).
- Une ligne de coulisse vécue, qui se voit sur une photo du carrousel.
- Un merci aux équipes et aux clients, sans les nommer sans accord.
- CTA : « Un projet à tourner ? Écrivez-nous en message. » (jamais « lien en bio » tant que le
  site reste vierge).
- Une offre liée à un temps fort ne se glisse dans le récap que si elle respecte J-60 à J-30
  (`.claude/memories/anticipation-evenements.md`).
- Trois à cinq hashtags.

**Otea Filmakers** : « je », tutoiement, intime et cinématique.
- Ouverture : « <Mois>, en vrai. »
- Trois à cinq lignes courtes sur ce que le mois a été derrière la caméra : une lumière, un
  doute, une route, un plan qui a tenu.
- Une question à la communauté : « Et toi, ton mois ? »
- Trois à cinq hashtags.

## 5. Programmer (brouillon)

- **OTEA Production** : carrousel le dernier jour du mois à 12:00. Si le créneau est pris, le
  jour libre le plus proche entre le 29 et le dernier jour, sinon le 1er du mois suivant à 12:00.
- **Otea Filmakers** : carrousel le dernier jour du mois à 18:00, même règle de repli.
- Toujours en **brouillon** (`draft:true`). Les deux comptes sont en validation automatique : la
  relève les arme à son passage suivant. Vérifie `draft`, `providers` et l'ordre des médias après
  création.
- Enregistre les photos utilisées : `python3 scripts/scan-medias.py --register <fichier>.json`
  (statut `branche`), commit, push.

## 6. Rendre compte à Maxime

Un message court, avec les deux planches et les deux légendes :
- la date et l'heure de chaque publication ;
- les photos écartées faute d'accord, au cas où il veuille les obtenir ;
- « Une photo ou une phrase ne va pas ? Dis-le avant le <date de publication>, je corrige. »

## Règles

- Rien n'est supprimé, jamais, ni dans Photos ni dans `Médias clients/`.
- Jamais de visage passé par une génération IA. Jamais de personne réelle générée.
- Ne publie rien directement : brouillon seulement, la relève fait le reste.

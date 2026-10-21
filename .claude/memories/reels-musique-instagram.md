---
name: reels-musique-instagram
description: La musique d'un reel se pose dans Instagram, jamais dans le fichier ; le reel part muet et en mode notification
metadata:
  node_type: memory
  type: feedback
  modified: 2026-10-21T12:00:00.000Z
---

# Reels : la musique se pose dans Instagram

**Règle de Maxime, 21/10/2026** (« Je me suis totalement répété ») : « Pour les
publications Instagram, on va utiliser des musiques qu'on va prendre et qu'on va
rajouter via Instagram et pas intégrer directement pour éviter d'avoir audio
d'origine, mais avoir une musique utilisée via Instagram. »

## Pourquoi
Un son incrusté dans le fichier apparaît comme « audio d'origine » : le reel ne
rejoint pas la page du son, ne profite pas d'un son tendance et perd la portée
qu'Instagram donne aux reels qui utilisent sa bibliothèque.

## Ce que ça implique
- **Production** : un reel se rend **muet**, comme une story (`-an`, vérifier à
  l'`ffprobe` qu'aucun flux audio ne reste). Pas de piste Artlist ou autre
  intégrée, même « en attendant ». Voix réelle du client tournée au micro : seul
  cas où le fichier garde un son, et seulement si Maxime l'a demandé.
- **Programmation** : un reel Instagram programmé sort en **mode notification**
  (`draft:false`, `autoPublish:false`). Metricool envoie la notification à
  Maxime à l'heure prévue, il choisit la musique dans Instagram et publie.
  `scripts/review.py` (relève) applique ce mode d'office à tout reel Instagram
  sans `instagramData.audioConfiguration`.
- **Son posé par Metricool** : `audioConfiguration` exige un compte Instagram
  professionnel relié à une page Facebook. Refusé (403) sur le compte de Pierre
  Huiban le 21/10/2026. Si le compte est relié un jour, le reel peut partir en
  publication automatique avec ce son.

## Périmètre
Tous les comptes. Complète [[stories-sans-son]] (stories muettes depuis le
04/08/2026).

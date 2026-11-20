---
name: autonomie-decisions-cm
description: Ne plus poser de questions en cours de travail CM — trancher et avancer ; MAIS toujours planifier en brouillon
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 554c009b-345e-4df0-8ba6-f1dbfb275952
  modified: 2026-07-29T07:57:52.433Z
---

Le user ne veut plus être interrompu par des questions pendant le travail de community management (choix de visuels, mapping, gestion des doublons, méthode, etc.) : **trancher soi-même et avancer**, puis expliquer les choix dans le bilan final.

**Why :** validé le 28/07/2026 après que je lui aie demandé des micro-décisions à répétition (scope stories, Facebook oui/non, stories orphelines…). Il préfère un exécutant autonome qui rend compte.

**How to apply :** prendre la décision la plus cohérente avec les fiches clients ([[bulk-schedule-stories-metricool]], règles DA, « 0 post sans média ») et la signaler dans le récap. EXCEPTION EXPLICITE (choix du user, option « Décisions seulement ») : les contenus restent **toujours en brouillon** dans Metricool (`draft:true`, jamais d'autoPublish) — la publication réelle passe par sa relecture. Ne jamais basculer en publication automatique sans une nouvelle demande explicite.

**Seule exception accordée (07/10/2026) : OTEA Production et Otea Filmakers**, les deux comptes dont Maxime est lui-même le client (« tu peux considérer que c'est validé à chaque fois, car c'est moi », puis choix explicite « publication auto »). On continue de créer en brouillon ; c'est la relève GitHub (`scripts/review.py`, `validation_auto` dans `reviews/config.json`) qui passe en publication les brouillons des 14 jours à venir, avec les garde-fous de la review (média présent, pas de placeholder, pas de tiret cadratin dans une légende). Tous les autres comptes restent en brouillon strict.

**Extension du 21/10/2026 : Pierre Huiban et Run On Invest.** Maxime : « on va faire l'automatisation des postes avec Pierre parce qu'il ne les valide pas […] on va les publier », puis « Oui, passe R.O.I. en auto ». Même mécanique (`validation_auto: true`), mêmes garde-fous, plus deux nouveaux :
- un **reel Instagram** sort du brouillon en **mode notification** (`draft:false`, `autoPublish:false`) : Metricool notifie Maxime à l'heure prévue, il pose la musique dans Instagram et publie ([[reels-musique-instagram]]) ;
- une **image de feed hors 4:5 à 1.91:1** est retenue (Instagram la refuserait ou la rognerait).
Run On Invest a en plus `contenu_ia: true` : ses visuels sont générés, la mention « contenu IA » d'Instagram est cochée d'office. Pierre ne reçoit plus de tableau hebdo (`actif: false`). Tous les autres comptes restent en brouillon strict.

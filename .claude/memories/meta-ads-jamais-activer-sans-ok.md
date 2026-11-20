---
name: meta-ads-jamais-activer-sans-ok
description: Toute campagne Meta est créée en PAUSE ; l'activation (donc la dépense) n'a lieu que sur un OK explicite de Maxime, campagne par campagne
metadata:
  node_type: memory
  type: feedback
  modified: 2026-09-02T00:00:00.000Z
---

Pendant de la règle « tout contenu Metricool reste en brouillon », appliqué à
la publicité Meta : **une campagne, un ensemble de publicités ou une publicité
est toujours créé en PAUSE, et personne ne l'active à la place de Maxime.**

**Why :** activer, c'est dépenser l'argent du client. La logique d'autonomie
(« trancher et avancer ») vaut pour la préparation, pas pour l'engagement de
budget. Le connecteur Meta Ads crée d'ailleurs tout en PAUSED et demande une
confirmation explicite avant `ads_activate_entity`.

**How to apply :**
- Créer la structure complète (campagne → ensemble → creative → publicité),
  générer l'aperçu, consigner les identifiants dans la spec
  (`scripts/campagne.py journal`), puis rendre compte et s'arrêter.
- Activer seulement après une phrase sans ambiguïté de Maxime qui nomme la
  campagne (« active la campagne Vœux 2027 », « lance-la »). Un « ok » sur le
  récap général ne suffit pas. Noter qui et quand dans `validation`.
- Activer du haut vers le bas (campagne, ensemble, publicité), relire
  `effective_status` et `ads_get_errors` juste après.
- Jamais de hausse de budget au-delà des plafonds de
  `campagnes/comptes.json` sans que Maxime les relève dans le fichier.
- Couper (PAUSED) est toujours permis sans demander : c'est l'inverse d'une
  dépense.

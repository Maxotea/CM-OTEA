---
name: detection-nouveaux-medias
description: Scanner de nouveaux médias clients (SHA1) qui alimente les stories/posts de la semaine dans la tâche du lundi
metadata: 
  node_type: memory
  type: project
  originSessionId: 5d510d71-c3e4-4bee-b42d-908ed5b5c881
  modified: 2026-07-31T14:41:10.222Z
---

Créé le 30/07/2026 : `CM-OTEA/scripts/scan-medias.py` détecte les photos/vidéos déposées dans `medias/<client>/` (identité = SHA1 du contenu → un fichier renommé ou déplacé ne repasse pas pour neuf ; les dossiers `ia/`, `ia-stories/` sont ignorés). Index dans `recaps/medias-index.json`, trois statuts : `deja-exploite`, `en-reserve` (vu, jamais branché = le vivier), `branche`. Commandes : sans argument = rapport JSON des nouveaux ; `--reserve` = vivier disponible ; `--seed --statut X --client Y` = amorçage ; `--register fichier.json` = après branchement.

`CM-OTEA/scripts/carte-story.py` compose la carte story 9:16 depuis une vraie photo (fond flouté+assombri, photo nette centrée, barre charte, titre HelveticaNeue auto-ajusté, voile dégradé pour la lisibilité) et écrit AUSSI `-fond.jpg` (sans texte, à donner à l'i2v si la story doit être animée) et `-texte.png`. Jamais d'IA générative sur un visage réel.

Branché dans l'étape 4 de [[recap-hebdo-lundi]] : chaque lundi, détection → choix des emplacements (uniquement brouillons IA de la semaine, jamais un contenu validé par Maxime, plafond `max_remplacements_semaine` par client dans clients-config.json) → composition → hébergement → `bulk_replace_posts` / `bulk_schedule_stories` → `--register`.

Amorçage du 30/07/2026 : 240 médias indexés. OTEA (31) et Pierre (81) en `deja-exploite` ; **Le Loft (21, dont 20 verticales, jamais utilisées — compte encore 100 % IA) et J Lawson (107, la fiche n'en annonçait que 42) en `en-reserve`** = 128 photos disponibles.

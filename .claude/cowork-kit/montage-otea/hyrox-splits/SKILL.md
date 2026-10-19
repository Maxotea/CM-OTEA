---
name: hyrox-splits
description: Récupère les temps HYROX officiels d'un athlète (8 runs, 8 stations, Roxzone) et produit le JSON, le CSV et le SRT pour les incrustations d'un montage DaVinci Resolve, avec les scripts du dossier hyrox/ de ce dépôt. Utilise ce skill dès que Maxime prépare un montage d'un athlète HYROX (Pierre Huiban, Julie Pekmezian, Antoine Bouhana ou un autre) et veut afficher les temps par station.
---

# Temps HYROX pour un montage

Ce skill remplace l'ancien `hyrox-splits-montage` du compte, qui refaisait à la main ce que les
scripts de ce dépôt font déjà. Lis `hyrox/README.md` avant de commencer.

## Ordre des opérations

1. Identifier : athlète, ville, saison, division. Si la course n'est pas précisée, prendre la plus
   récente et le dire en une ligne.
2. Récupérer : `python3 hyrox/hyrox_hyresult.py` sur la fiche HYRESULT de l'athlète (source qui
   agrège les résultats officiels). Ne jamais contourner results.hyrox.com, qui refuse l'accès
   automatisé. Si HYRESULT ne donne pas les splits, demander à Maxime une capture d'écran et lire
   les temps dessus.
3. Vérifier : `python3 hyrox/hyrox_splits.py` recalcule la somme des 8 runs, 8 stations et Roxzone
   contre le temps final (tolérance 2 s) et produit les cumuls. Signaler tout écart et préciser si
   les résultats sont provisoires (course de moins de 48 h).
4. Livrer : les fichiers `hyrox/livrables/hyrox_<athlete>_<ville>_<annee>.{json,csv,srt}`, puis si
   Maxime le veut `python3 hyrox/hyrox_resolve_builder.py` pour le projet Resolve.

## Réponse

Une ligne (temps final, classement, meilleure station), les fichiers, et un point fort à mettre
en avant dans le montage si HYRESULT donne la moyenne de la division. Français, pas de tiret
cadratin.

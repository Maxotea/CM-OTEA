---
name: hyrox-splits
description: Récupère les temps HYROX officiels d'un athlète (8 runs, 8 stations, Roxzone) et produit le JSON, le CSV, le SRT et les cartons pour les incrustations d'un montage DaVinci Resolve, avec les scripts du dossier hyrox/ de ce dépôt. Utilise ce skill dès que Maxime prépare un montage d'un athlète HYROX (Pierre Huiban, Julie Pekmezian, Antoine Bouhana, Sylvain Gamard ou un autre) et veut afficher les temps par station.
---

# Temps HYROX pour un montage

Ce skill remplace l'ancien `hyrox-splits-montage` du compte, qui refaisait à la main (WebFetch,
calcul dans la conversation) ce que les scripts de ce dépôt font déjà. Lis `hyrox/README.md`
avant de commencer : il donne la chaîne complète et un exemple livré (Sylvain Gamard, Bordeaux 2026).

## La chaîne

1. **Identifier** : athlète, ville, saison, division. Si la course n'est pas précisée, prendre la
   plus récente de l'athlète et le dire en une ligne.
2. **Récupérer** les temps depuis HYRESULT, qui agrège les résultats officiels :
   `python3 hyrox/hyrox_hyresult.py --athlete <slug> --event <saison-annee-ville> --out hyrox/temps/<ville>-<annee>-<athlete>.txt`
   ou avec l'URL de la page résultat. Ne jamais contourner results.hyrox.com, qui refuse l'accès
   automatisé. Si HYRESULT ne donne pas les splits, demander à Maxime une capture d'écran de la
   page résultat et saisir les temps dans le fichier `temps/` à la main.
3. **Vérifier et produire** :
   `python3 hyrox/hyrox_splits.py hyrox/temps/<fichier>.txt --cartons`
   Le script recalcule la somme des 8 runs, 8 stations et Roxzone contre le temps final
   (tolérance 2 s), calcule les cumuls, et écrit `sorties/*.json`, `*.csv`, `*.srt` et les cartons
   PNG. Signaler tout écart, et préciser si les résultats sont provisoires (course de moins de
   48 h).
4. **Resolve**, si Maxime le demande : `hyrox_resolve_builder.py` depuis Workspace > Scripts >
   Utility dans DaVinci Resolve, procédure dans le README.

## Règles

- Les livrables validés vont dans `hyrox/livrables/<athlete>-<ville>-<annee>/`, comme l'exemple.
- Aucun chiffre tapé de mémoire : tout vient du fichier `temps/`, lui-même tiré de HYRESULT ou
  d'une capture lue avec Maxime.
- Français, pas de tiret cadratin ni demi-cadratin (le test de style du dépôt le vérifie).

## Réponse à Maxime

Une ligne (temps final, classement, meilleure station), la liste des fichiers produits, et un
point fort à mettre en avant dans le montage si HYRESULT donne la moyenne de la division.

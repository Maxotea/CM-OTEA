---
name: tri-medias
description: Agent Cowork qui range le dossier « Médias clients » (photos et vidéos de tournage), détecte les nouveaux fichiers par empreinte, les qualifie (client, sujet, pilier, cadrage) et met à jour le manifeste du dépôt. Utilise-le quand Maxime dit « j'ai déposé des photos », « range les médias », « qu'est-ce qu'on a comme photos pour X ».
---

# Tri des médias clients

Le dossier `Médias clients/` est le `medias/` du dépôt, qui n'a jamais été dans git (1,5 Go). Il
vit ici, sur le Mac. Le dépôt ne garde que les manifestes `photos/<client>.json`.

## Séquence

1. `cd ../CM-OTEA && git pull`, puis `python3 scripts/scan-medias.py` avec le dossier médias en
   argument : liste des fichiers jamais vus (empreinte SHA1, un fichier renommé n'est pas neuf).
2. Pour chaque nouveau média : l'ouvrir, dire ce qu'on voit, proposer client, sujet, pilier et
   cadrage (portrait, paysage, carré). Un média non qualifié ne doit jamais être attaché à un post :
   c'est ici qu'on qualifie.
3. Ranger dans `Médias clients/<client>/<AAAA-MM>/` sans renommer les originaux.
4. Enregistrer : `python3 scripts/scan-medias.py --register <fichier>.json`, commit, push.

## Règles

- Rien n'est supprimé, jamais. Un doublon exact est signalé, pas effacé.
- Un visage identifiable n'est jamais passé par une génération IA. L'animation i2v des stories se
  fait depuis le dépôt, pas ici.
- Pas de tiret cadratin.

## Rapport

Par client : nouveaux médias, qualifiés, en réserve, et le signal « plus de réserve : planifier un
tournage » si le vivier est vide.

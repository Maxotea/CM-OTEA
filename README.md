# CM OTEA — Outil CM Premium

Skill Claude Code d'automatisation du community management (Metricool via Zapier) pour les comptes gérés par OTEA Production.

## Contenu
- `.claude/skills/cm-metricool/SKILL.md` — le moteur : onboarding, calendrier éditorial, planification en masse, routine hebdo, veille trends, ROI
- `.claude/skills/cm-metricool/references/carrousels-hebdo.md` — le carrousel hebdomadaire : créneau, anatomie, archétypes, adaptation à la typologie et à la cible, planification
- `.claude/skills/cm-metricool/references/bonnes-pratiques-cm.md` — savoir CM transverse
- `.claude/skills/cm-metricool/references/clients/` — une fiche par client (+ banques photos)
- `carrousels/<client>/*.json` — les specs de carrousels, un fichier par semaine et par compte
- `scripts/carrousel.py` + `scripts/themes.json` — le générateur de slides et la DA de chaque compte

## Utilisation
Ouvrir ce repo dans Claude Code (le skill se charge automatiquement depuis `.claude/skills/`), connecter le Zapier MCP, puis : « routine hebdo », « planifie le trimestre pour [client] », « onboarde [nouveau client] »…

## Le carrousel du mercredi
Chaque compte publie **un carrousel par semaine**, le mercredi. Il remplace le post feed de ce jour-là : le volume mensuel ne change pas, le palier vendu est respecté.

```bash
pip install pillow
python3 scripts/carrousel.py carrousels/le-loft/2026-08-12-erreurs-barbe.json
python3 scripts/carrousel.py carrousels/ --check      # valide tout sans rien écrire
```

Le rendu part dans `medias/<client>/carrousels/<slug>/` (dossier ignoré par git) avec les slides numérotées dans l'ordre, la légende, et un `manifest.json` qui alimente `media01`…`media0N` de `schedule_post`.

## Ajouter un client
Dupliquer `references/clients/_template-nouveau-client.md`, remplir, créer si besoin sa `banque-photos-[client].md`, et ajouter sa DA de carrousel dans `scripts/themes.json`.

## Répartition Drive / GitHub

Deux stockages, deux rôles. Les confondre crée des copies qui divergent.

| | Rôle | Qui y écrit |
|---|---|---|
| **Boîte de dépôt Drive** (une par client, partagée avec lui) | Médias bruts : photos et vidéos prises au téléphone | Le client, et Maxime |
| **Ce dépôt GitHub** | Code, contenus rédigés, manifestes, DA, fiches clients | Maxime et Claude |

`scripts/drive_sync.py` fait le pont, **dans un seul sens** : il lit la boîte du client, repère
ce qui est nouveau, l'héberge et met à jour `photos/<client>.json`. Il ne crée, ne renomme et ne
supprime jamais rien côté Drive — c'est la boîte du client, pas la nôtre. Il tourne chaque matin
à 7 h, et à la demande (workflow « Boîtes de dépôt Drive »).

La déduplication se fait **par empreinte du contenu**, pas par nom de fichier : une même photo
envoyée deux fois depuis un téléphone n'entre qu'une fois dans le manifeste.

Un média fraîchement récupéré arrive avec un `sujet` et un `pilier` **vides**. C'est volontaire :
savoir qu'une photo montre les bacs de coiffure et non le hammam demande un œil, pas un script.
**Un média non qualifié ne doit jamais être attaché automatiquement à un post.**

⚠️ **Ne pas synchroniser le dépôt entier vers le Drive.** Une copie de ce dépôt existe dans le
Drive depuis juillet 2026, `.git` compris : elle donne l'illusion d'être à jour alors qu'elle
ignore tout ce qui a été fait depuis. Le Drive porte les médias, GitHub porte le reste.

### Mettre en place la boîte d'un nouveau client

1. Créer un dossier Drive au nom du client, ne contenant **que** ses médias.
2. Le partager : « Tous les utilisateurs disposant du lien — Lecteur », puis le donner au client.
3. Créer `photos/<client>.json` avec `client`, `drive_folder` (l'identifiant du dossier) et
   `photos: []`.
4. Lancer le workflow « Boîtes de dépôt Drive » en `dry_run` pour vérifier la lecture.

Secret nécessaire : `GOOGLE_API_KEY` — une clé API Google avec l'API Drive activée. Elle suffit
à lire un dossier partagé par lien ; aucun compte de service à créer.

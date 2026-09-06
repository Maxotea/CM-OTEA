# CM OTEA — Outil CM Premium

Skill Claude Code d'automatisation du community management (Metricool via Zapier) pour les comptes gérés par OTEA Production.

## Contenu
- `.claude/skills/cm-metricool/SKILL.md` — le moteur : onboarding, calendrier éditorial, planification en masse, routine hebdo, veille trends, ROI
- `.claude/skills/cm-metricool/references/carrousels-hebdo.md` — le carrousel hebdomadaire : créneau, anatomie, archétypes, adaptation à la typologie et à la cible, planification
- `.claude/skills/cm-metricool/references/bonnes-pratiques-cm.md` — savoir CM transverse
- `.claude/skills/cm-metricool/references/clients/` — une fiche par client (+ banques photos)
- `carrousels/<client>/*.json` — les specs de carrousels, un fichier par semaine et par compte
- `scripts/carrousel.py` + `scripts/themes.json` — le générateur de slides et la DA de chaque compte
- `scripts/review.py` + `reviews/` — la review hebdo client : le fichier Excel de validation et son aller-retour avec Metricool
- `.claude/skills/cm-metricool/references/review-hebdo.md` — le circuit complet de la review

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
4. Demander à Claude de lister le dossier : il ajoute les nouveaux fichiers au manifeste.
5. Lancer le workflow « Boîtes de dépôt Drive » en `dry_run` pour vérifier la récupération.

**Aucune clé Google n'est nécessaire**, et c'est délibéré : l'API Drive de Google Cloud impose
d'attacher une facturation. Le travail est donc coupé en deux — Claude **repère** les nouveaux
fichiers via le connecteur Drive déjà connecté, l'action les **récupère** par le lien public du
dossier partagé. Aucune des deux moitiés n'a besoin d'identifiants Google.

Seul secret utilisé : `IMGBB_API_KEY`, le même que pour les slides.

## La review hebdo client (Excel ↔ Metricool)

Le client valide sa semaine dans un fichier type Excel : légendes corrigibles dans les
cases, une décision par ligne (`✅ OK pour publier` · `✏️ À corriger` · `⛔ Ne pas
publier`), un commentaire libre. Ses ✅ passent les brouillons Metricool en **publication
automatique** — modifications comprises — sans autre geste. Un post sans décision ne part
jamais ; jamais de suppression automatique.

```bash
pip install openpyxl
python3 scripts/review.py generer   --semaine 2026-08-10 --dry-run   # ce qui serait couvert
python3 scripts/review.py appliquer --client le-loft --dry-run       # ce qui serait appliqué
```

L'action « Review hebdo client » orchestre les deux sens : `generer` le lundi à 6h30 UTC
(après les carrousels), `appliquer` trois fois par jour. Même découpe que la chaîne
photos, dans l'autre sens aussi : la **session** du lundi dépose le fichier dans le Drive
du client (connecteur, conversion en Google Sheet) et note son identifiant dans
`reviews/config.json` ; l'**action** relit le fichier par son export public — aucune clé
Google. Un retour par mail se dépose tel quel dans `reviews/retours/`. Journal des
décisions appliquées (idempotence + matière du récap) : `reviews/etat/`. Circuit complet,
garde-fous et rôle de la session : `.claude/skills/cm-metricool/references/review-hebdo.md`.

Mettre en route un nouveau client : l'ajouter à `reviews/config.json` (slug, blog_id,
prefixe, `actif: true`) — le reste suit le lundi suivant.

## La revue quotidienne de l'outil

Chaque matin à 7h30 (Paris), une routine relit l'outil comme un produit : les runs de la
nuit, les PR, les scripts, les configurations, les routines. Elle corrige ce qui tient en
une session, protège chaque correction par un test, et note le reste dans
`ameliorations/BACKLOG.md`. Revues datées dans `ameliorations/`, prompt dans
`.claude/taches-planifiees/review-quotidienne-outil/SKILL.md`. Le but : l'outil CM le plus
productif et le plus rapide du marché, vendable à d'autres community managers.

```bash
pip install openpyxl pillow pytest
python3 scripts/sante.py          # le bilan de santé : carrousel du mercredi, review, configs, journal
python3 -m pytest -q              # 69 tests, sans réseau ni secret
```

Le workflow `Tests` lance les deux à chaque push et sur chaque PR, et publie le bilan de
santé dans le résumé du run.

## Ajouts v3 (02/08/2026)
- `.claude/skills/cm-metricool/references/compte-rendu-hebdo-clients.md` — comptes rendus hebdo clients (lundi 9h) : WhatsApp prioritaire + doublon email, mode brouillon
- `.claude/skills/cm-metricool/references/roi-clients.md` et `banques-photos.md` — références transverses
- `references/clients/` couvre désormais **8 comptes** (ajout de Confshine Game et Otea Filmakers) + template + banques photos

## Migration (02/08/2026)
- `.claude/memories/` — les 7 mémoires du CM, désormais **versionnées** (elles vivaient hors du repo et ont été perdues à la migration). Les 2 règles non négociables sont rappelées dans `CLAUDE.md`.
- `.claude/taches-planifiees/recap-hebdo-publications/SKILL.md` — prompt de la tâche du lundi 9h, chemins rendus relatifs. **La Routine reste à créer.**
- `scripts/` — `carte-story.py` (composition carte story 9:16) et `scan-medias.py` (détection SHA1 des nouveaux médias). Testés sous Linux.
- `_portage/INSTALLATION.md` — état complet de la migration : ce qui marche, ce qui manque, ce qui reste à faire.

### Prérequis machine
`python3` + `Pillow` (`pip install Pillow`) et `ffmpeg` (`apt install ffmpeg` · `brew install ffmpeg` · `choco install ffmpeg`).
Le dossier `medias/` (1,5 Go) n'est pas versionné : le copier à part, sinon la tâche du lundi ne peut brancher aucune photo.

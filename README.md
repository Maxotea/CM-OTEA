# CM OTEA — Outil CM Premium

Skill Claude Code d'automatisation du community management (Metricool via Zapier) pour les comptes gérés par OTEA Production.

## Contenu
- `.claude/skills/cm-metricool/SKILL.md` — le moteur : onboarding, calendrier éditorial, planification en masse, routine hebdo, veille trends, ROI
- `.claude/skills/cm-metricool/references/bonnes-pratiques-cm.md` — savoir CM transverse
- `.claude/skills/cm-metricool/references/clients/` — une fiche par client (+ banques photos)

## Utilisation
Ouvrir ce repo dans Claude Code (le skill se charge automatiquement depuis `.claude/skills/`), connecter le Zapier MCP, puis : « routine hebdo », « planifie le trimestre pour [client] », « onboarde [nouveau client] »…

## Ajouter un client
Dupliquer `references/clients/_template-nouveau-client.md`, remplir, et créer si besoin sa `banque-photos-[client].md`.

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

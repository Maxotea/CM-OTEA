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

# reviews/ — la review hebdo client

L'aller-retour hebdomadaire de validation : un fichier Excel par client, déposé chaque
vendredi dans son dossier Drive permanent (le mail part le lundi matin), relu plusieurs
fois par jour ; ses ✅ passent les brouillons Metricool en publication automatique.
Circuit complet : `.claude/skills/cm-metricool/references/review-hebdo.md`. Moteur :
`scripts/review.py`, orchestré par l'action « Review hebdo client ».

| Ici | Quoi | Qui écrit |
|---|---|---|
| `config.json` | comptes couverts + dossier Drive permanent + fichier de la semaine | la routine Claude du vendredi (et Maxime) |
| `a-envoyer/` | les fichiers générés, un par client et par semaine | le job `generer` (Actions) |
| `retours/` | fichiers revenus par mail, nommés `<slug>-<lundi>.xlsx` | Maxime (ou la session) |
| `etat/` | journal des décisions appliquées — idempotence + matière du récap | le job `appliquer` (Actions) |

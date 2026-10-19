# Kit Cowork OTEA

Tout ce qu'il faut pour installer le côté Cowork de l'organisation décrite dans
`../references/organisation-claude.md`. Je ne peux pas écrire dans Cowork depuis une session
Code : ce dossier se copie à la main, une fois. Régénérer les zips : `python3 scripts/export_projets_claude.py`.

## 1. Le dossier de travail Cowork « OTEA »

À créer sur ton Mac, hors du clone du dépôt, et à ouvrir comme dossier de travail dans Cowork :

```
OTEA/
  CLAUDE.md              ← copie de cowork-kit/CLAUDE-cowork.md
  .claude/skills/        ← copie de cowork-kit/agents/* (un dossier par agent)
  Devis et offres/       ← déplacé depuis CM-OTEA/offre/ et .claude/references/devis/
  Présentations/         ← déplacé depuis CM-OTEA/design-presentation/ et design-video-annonce/
  Pitchs/                ← déplacé depuis CM-OTEA/.claude/references/pitch/ et prep/
  Médias clients/        ← le dossier medias/ (1,5 Go) qui n'a jamais été dans git
  Compta/                ← exports CSV Qonto, sorties de Trésorerie parfaite
  Journal/               ← le journal de bord (dépôt STRUCTUREOTEA, un README)
```

Le dépôt CM-OTEA reste cloné à côté : les agents Cowork qui touchent la review ou le récap
travaillent dedans (`git pull` avant, commit après).

## 2. Les agents Cowork (dossier `agents/`)

| Agent | Quand | Ce qu'il fait | Écrit dans |
|---|---|---|---|
| `review-vendredi` | vendredi 8h, ordinateur allumé | dépose les tableaux de review dans les Drive clients, prépare les brouillons de mail | Drive, Gmail (brouillons), `reviews/config.json` |
| `recap-lundi` | lundi 9h | récap des publications de la semaine, brouillons de CR clients, liens WhatsApp | `recaps/`, Gmail (brouillons) |
| `devis-otea` | à la demande | un devis ou une proposition depuis la grille 2026, en docx ou pdf | `Devis et offres/` |
| `tri-medias` | à la demande | range `Médias clients/`, détecte les nouveaux, qualifie sujet et pilier | `photos/<client>.json` du dépôt |
| `compta-semaine` | mardi, à la demande | import CSV Qonto dans Trésorerie parfaite, lecture du plan, mise à jour du tableau de bord | `Compta/`, tableau de bord |

Les deux premiers remplacent des routines cloud : la routine « Review, préparation du vendredi »
se désactive une fois `review-vendredi` passé deux vendredis de suite.

## 3. Les skills du compte à remplacer (dossier `skills-compte/`)

`cm-otea` et `cm-b2c` du compte disent de publier directement quand une photo a une URL publique.
C'est contraire à la règle n°1. Remplace-les par les deux dossiers de `skills-compte/` : ce sont des
aiguillages de dix lignes qui renvoient au bon endroit et rappellent la règle.

## 4. Le skill pour MONTAGE-OTEA (dossier `montage-otea/`)

`hyrox-splits` remplace le skill `hyrox-splits-montage` du compte : il appelle les scripts qui
existent déjà dans `montage-otea/hyrox/` au lieu de refaire le travail à la main. À copier dans
`MONTAGE-OTEA/.claude/skills/hyrox-splits/`, puis retirer le skill du compte.

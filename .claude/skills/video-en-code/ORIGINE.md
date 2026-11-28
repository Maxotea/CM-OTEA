# Origine et mise à jour des skills de vidéo en code

Installés le 26/11/2026 à la demande de Maxime, dans MONTAGE-OTEA et CM-OTEA.

| Dossier | Source | Version copiée | Modifié ? |
|---|---|---|---|
| `remotion-best-practices` | github.com/remotion-dev/skills, `skills/remotion-best-practices` | commit `a3f4098`, version 4.0.547 | non, copie exacte |
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry` | github.com/heygen-com/hyperframes, `skills/` (Apache 2.0, licence dans `hyperframes/LICENSE`) | commit `7c217d9`, version 0.9.99 | oui, voir plus bas |
| `motion-canvas`, `manim`, `video-en-code` | écrits pour OTEA | 26/11/2026 | sans objet |

## Ce qui a été changé dans les skills HyperFrames

Dans les trois `SKILL.md` :

- retrait du paragraphe « Usage note », qui faisait envoyer une note d'usage
  à HeyGen à chaque démarrage du skill ;
- retrait de la ligne qui faisait envoyer un avis après chaque rendu
  (`hyperframes-cli`) et de celle qui signalait chaque recherche sans
  résultat (`hyperframes-registry`) ;
- ajout en tête d'un encadré « Règles OTEA » : pas de télémétrie, rendu en
  local, prix annoncé avant toute action payante, rien envoyé en ligne sans
  accord.

Les fichiers de test (`*.test.mjs`) n'ont pas été copiés.

## Ce qui n'a pas été installé, et pourquoi

| Skill officiel | Raison |
|---|---|
| `media-use` | envoie des statistiques liées à l'adresse du compte, installe des paquets Python sans demander, range les médias dans un dossier commun à tous les clients, et demande à l'agent de ne pas annoncer les prix |
| `reverse-any-video` | payant, envoie les personnes filmées chez HeyGen pour les refaire en IA : contraire à la règle « aucune personne réelle générée » |
| `style-sampling` | payant, réécrit le `CLAUDE.md` du projet et suit un modèle téléchargé qui prime sur le skill |
| `slideshow`, `figma`, `remotion-to-hyperframes` | hors besoin pour l'instant |
| les 13 skills `remotion-*` séparés | déjà contenus dans `remotion-best-practices` (dossiers `remotion-*/REFERENCE.md`) |

## Points à connaître

- **Le skill HyperFrames télécharge son outil à chaque lancement**
  (`npx hyperframes@>=0.9.80`), sans version figée. Seuls les skills ont été
  relus, pas cet outil. Pour figer la version : variable
  `HYPERFRAMES_STANDALONE_CLI_VERSION`.
- **Remotion n'a pas de licence de redistribution écrite pour ses skills.**
  La copie dans un dépôt privé correspond à ce que fait la commande
  officielle `npx skills add remotion-dev/skills`. Ne pas publier ces
  dossiers dans un dépôt public.
- **Licence Remotion pour l'usage** : gratuite pour une personne seule ou une
  société de trois personnes au plus, payante au-delà (à vérifier sur
  remotion.dev/docs/license avant un projet client).
- **Ne pas lancer `npx remotion upgrade` ni `npx skills update`** sans relire :
  ces commandes remplacent les skills copiés ici par la dernière version en
  ligne.

## Mettre à jour

Récupérer les deux dépôts, comparer avec les dossiers d'ici, relire les
différences, refaire les trois retraits ci-dessus sur HyperFrames, puis
mettre à jour ce tableau.

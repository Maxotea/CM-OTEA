---
name: video-en-code
description: "Aiguillage entre les quatre outils de vidéo écrite en code installés le 26/11/2026 : Remotion, HyperFrames, Motion Canvas et Manim. Utilise ce skill dès que Maxime demande une animation, un motion design, un titre animé, un habillage, des sous-titres animés, un graphique ou un chiffre animé, un schéma qui se dessine, une vidéo explicative, ou dit « fais-moi une vidéo en code », sans nommer l'outil. Il choisit l'outil puis renvoie vers son skill."
---

# Vidéo en code : quel outil pour quoi

Le principe : l'animation est un fichier texte. Claude l'écrit, Maxime garde la
main sur chaque image (on corrige une ligne, on relance le rendu, le résultat
est identique à chaque fois). Rien n'est « généré » au sens d'une IA vidéo :
pas de mouvement qui flotte, pas de visage inventé.

## Le choix

| Besoin | Outil | Skill à charger |
|---|---|---|
| Habillage de reel, titres, sous-titres animés, gabarit réutilisable d'un client à l'autre, rendu en série | Remotion | `remotion-best-practices` |
| Une page web animée (HTML, CSS) transformée en vidéo, blocs tout faits, rendu hébergé chez HeyGen | HyperFrames | `hyperframes` |
| Schéma ou explication qui se construit pas à pas, calé sur une voix off | Motion Canvas | `motion-canvas` |
| Chiffres, courbes, formules, géométrie : le style « tableau noir animé » | Manim | `manim` |

En cas de doute, partir sur **Remotion** : c'est le plus complet pour du
contenu de réseaux sociaux et le seul avec un skill officiel par usage
(sous-titres, rendu, cartes, éléments prêts à l'emploi).

## Les règles d'OTEA qui s'appliquent à tous

- **Format vertical par défaut** : 1080 × 1920, 30 images par seconde.
- **Aucune musique dans le fichier** d'un reel ou d'une story : la bande son
  se pose dans Instagram.
- **Aucun tiret cadratin** dans un texte affiché à l'écran.
- **Rien n'entre dans `package.json` du dépôt.** Un projet vidéo vit dans son
  propre dossier, avec ses propres dépendances, hors de l'application
  (MONTAGE-OTEA est en zéro dépendance, CM-OTEA n'a pas de `package.json`).
  Dossier conseillé : `video-code/<client>/<projet>/`, avec `node_modules` et
  les rendus exclus de git.
- **Demander avant d'envoyer quoi que ce soit en ligne** : un rendu hébergé,
  un lien de partage ou un dépôt de médias sur un service externe ne part
  qu'avec l'accord de Maxime.
- **Licence Remotion** : gratuit pour une personne seule ou une société de
  trois personnes au plus. Au-delà, licence payante (charger
  `remotion-license` avant de répondre sur ce point).

## Origine des skills

| Skill | Source | Version |
|---|---|---|
| `remotion-*` | github.com/remotion-dev/skills (officiel) | copie du 26/11/2026 |
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry` | github.com/heygen-com/hyperframes (officiel, Apache 2.0) | copie adaptée du 26/11/2026 |
| `motion-canvas`, `manim`, `video-en-code` | écrits pour OTEA | 26/11/2026 |

Les skills officiels sont en anglais (voir `ORIGINE.md`
dans ce dossier pour les mettre à jour). Ils ne suivent donc pas la règle du
tiret cadratin : les tests de style les ignorent.

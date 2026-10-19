---
name: cm-b2c
description: Aiguillage du community management OTEA Production pour les clients particuliers (créateurs, coachs, consultants, athlètes, personal branding). Utilise ce skill dès que Maxime parle d'un client perso, d'un athlète HYROX, de Pierre Huiban, de ConfShine, de personal branding. Il ne produit rien lui-même : il renvoie au skill du dépôt et rappelle la règle du brouillon.
---

# CM B2C : où ça se fait

Le moteur B2C vit dans le dépôt **Maxotea/CM-OTEA** : skill `cm-hyrox` pour les athlètes, et
`cm-metricool` pour la planification. Le dépôt CM-BTOC est archivé depuis le 19/10/2026.

Le test qui tranche : « si cette personne arrête, est-ce que le compte a encore un sens ? » Non :
client perso, ce skill. Oui : commerce, skill `cm-otea`.

## Où aller

- **Rédiger** (reel, légende, réponse, dossier de sponsoring) : dans le Projet Claude du client
  (Pierre Huiban, ConfShine, Run On Invest). Les skills `reel-script` et `reel-lint` s'y utilisent.
- **Planifier dans Metricool** : session Claude Code sur CM-OTEA, ou routine POST CM-OTEA. Jamais
  depuis une conversation libre ou Cowork.
- **Temps HYROX pour un montage** : skill `hyrox-splits` du dépôt MONTAGE-OTEA.

## Règle qui prime

Tout en **brouillon** (`draft: true`, `autoPublish: false`), média présent ou non. Vraies images
uniquement sur un compte d'athlète, jamais de visage généré, jamais de scène de course fabriquée.
Pas de tiret cadratin. Ton de Pierre Huiban : anglais, première personne, chaleureux ; « LFG » et
l'impératif sec sont interdits.

---
name: otea-brand-identity
description: "Otea Production brand — palette (orange #FF5800), font Forma DJR Display, koru monogram, asset locations"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b24f4cdc-36bf-4f4f-aece-b8da5043f3b5
  modified: 2026-07-22T13:18:35.232Z
---

Charte graphique Otea Production (dossier : `/Users/oteaproduction/Desktop/DOC/CHARTRE GRAPHIQUE OTEA PRODUCTION/`).

**Palette officielle :**
- Accent principal — Orange `#FF5800`
- Secondaire — Vert-gris sauge `#ACC1C0`
- Encre (quasi-noir chaud) `#201E1E`
- Blanc cassé `#F1F1F1`

**Typographie :** Forma DJR Display (fichiers TTF « Testing » dans `FONT/`, poids Hairline→Black). Black (900) pour les titres. C'est une police custom, PAS sur Google Fonts — pour un rendu déterministe HyperFrames, l'inliner en base64 `@font-face` (data:font/ttf).

**Logo :** monogramme « koru/vague » (inspiration polynésienne — Otea = danse tahitienne), viewBox `0 0 1080 1082`, 2 paths. Wordmark « otea » bas-de-casse arrondi + « PRODUCTION » capitales espacées. Variantes dans `LOGOTYPE/` (HORIZONTAL, VERTICAL) et `MONOGRAMME/` (SVG + PNG, couleurs : orange/blanc/noir/vert). Icônes métier dans `ICONOGRAPHIE/` (budget, contact, equipe, gestion projet, medias, tournage).

**Handle Instagram :** @oteaproduction.

Voir aussi [[project_make_people]]. Node.js installé dans `~/.local/node/bin` (PATH ajouté à `~/.zshenv`) ; ffmpeg/ffprobe via npm global liés dans le même dossier — nécessaires pour rendre des vidéos HyperFrames.

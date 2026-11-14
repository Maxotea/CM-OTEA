---
name: pierre-photo-nb-glow
description: "DA Pierre Huiban : toute photo passe en noir et blanc contrasté, léger masque sur Pierre, glow"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-14
---

# Pierre Huiban : la photo est toujours en noir et blanc, masquée, avec glow

**Règle de Maxime, 14/11/2026**, après le visuel résultat de Cairo livré en couleur :
« c'est toujours maintenant, et retiens-le, noir et blanc, contrasté avec un léger masque
sur Pierre et l'effet glow ».

## Ce que ça veut dire sur chaque visuel de Pierre (post, carrousel photo, story)
1. **Noir et blanc contrasté** : chroma nulle, courbe en S, noirs profonds. Même famille que
   le N&B des reels monologue (`scripts/pierre-reel-ralenti.py`, `COURBE_NB`).
2. **Léger masque sur Pierre** : Pierre détouré, légèrement relevé (exposition et micro-contraste),
   le fond un cran plus sombre. *Léger* : on ne doit pas voir la découpe.
3. **Glow** : halo doux sur les hautes lumières (néons, peau éclairée), en écran, jamais sous
   les textes. Même principe que `glow_layer` de `scripts/etalonnage-punch.py`, sans teinte.
4. Seul l'accent « aube » `#E8622C` reste en couleur, dans la typo. La photo, jamais.

## Comment
`scripts/hyrox_visuel.py` (fonction `etalonner`) fait les trois. Le masque vient d'un
détourage fait une fois par photo (Higgsfield `remove_background`) et rangé dans
`photos/pierre-huiban/masques/` ; une photo sans masque prend un masque ovale centré sur
le sujet (`sujet` dans `photos/pierre-huiban.json`), à remplacer dès que possible.

## Pourquoi
C'est la signature visuelle de Pierre : celle des reels monologue en N&B. Un post en couleur
au milieu casse la grille.

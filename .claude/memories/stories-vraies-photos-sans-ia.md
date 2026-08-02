---
name: stories-vraies-photos-sans-ia
description: "Règle Maxime : stories en VRAIES photos animées par mouvement de caméra ffmpeg, jamais d'IA générative"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 554c009b-345e-4df0-8ba6-f1dbfb275952
  modified: 2026-08-02T17:21:35.545Z
---

**Maxime ne veut plus AUCUNE image ni vidéo générée par IA dans les stories clients** (dit le 31/07/2026). Les stories doivent partir de ses **vraies photos**, et « être mises en vidéo ».

**Why :** j'avais animé les visuels IA Higgsfield au lieu de ses photos (Le Loft, OTEA) — grosse erreur de ma part. Et le test image-to-video sur ses vraies photos a **déformé le visage d'un barbier** : inacceptable sur une personne réelle (c'est son image et celle de ses clients).

**How to apply :** partir de la VRAIE photo et l'**animer réellement** (i2v). ⚠️ Précision apportée le 01/08/2026 : un simple mouvement de caméra ffmpeg **ne suffit pas** — Maxime l'a refusé (« pas des images animées mais juste des zooms »). Il veut du vrai mouvement dans l'image.
1. crop 9:16 (PIL) de la photo, SANS texte ;
2. i2v `kling3_0_turbo` avec un prompt **verrouillé sur l'identité** : « Locked static camera, no zoom. Documentary realism: [micro-mouvement précis]. Every face and identity stay strictly identical to the photo — same features. No morphing, no face change, no warping, photorealistic, extremely minimal motion. » Un prompt trop vague déforme le visage (vécu sur un barbier du Loft) ;
3. **contrôler la dernière frame contre la photo source** avant de brancher — c'est là que la dérive apparaît ;
4. ffmpeg : upscale 1080×1920 + overlay du calque texte PNG (texte net, jamais passé dans le modèle).
Secours si un visage se déforme malgré le prompt renforcé : mouvement de caméra ffmpeg `zoompan` (pixels d'origine, zéro modèle) — mais uniquement en dernier recours. ⚠️ ne PAS mettre `-loop 1 -t 5` sur l'entrée image (avec `d=125` → 625 s). Voir [[hebergement-photos-reelles-metricool]] pour héberger le mp4.

**Fait au 01/08/2026** : Le Loft = 28 stories d'août ✅ et OTEA = 13 stories ✅, toutes en vraies photos **réellement animées** (i2v vérifié frame par frame). Gossip = 27 stories déjà sur ses vraies photos du lieu. **Reste : les 4 mercredis « Côté coiffure » de Gossip, encore sur un visuel IA — aucune photo de la partie coiffure dans le dossier client, à demander à Maxime.**

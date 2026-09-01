---
name: hebergement-photos-reelles-metricool
description: "Comment héberger une photo LOCALE pour l'attacher à un post Metricool (débloque vraies photos vs IA)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 554c009b-345e-4df0-8ba6-f1dbfb275952
  modified: 2026-07-31T19:08:57.374Z
---

Pour attacher une **vraie photo locale** (non-IA) à un post Metricool via l'API, il faut d'abord l'héberger sur une URL publique. Le pipeline Higgsfield le permet (validé 22/07/2026, PUT 200 + GET public 200) :

1. `media_upload` (filename + content_type ex `image/jpeg`) → renvoie `upload_url` (presigné, valide ~24h), un `media_id`, et une **URL cloudfront permanente** `https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6.../<media_id>.jpg`
2. `curl -X PUT -H "Content-Type: image/jpeg" --data-binary @fichier.jpg '<upload_url>'` → HTTP 200
3. `media_confirm` (type image, media_id) → status uploaded
4. Utiliser l'URL cloudfront comme `media01` dans `schedule_post` (exactement comme les visuels IA).

Débloque : vraies photos de tournage pour [[projet_make_people]]-style comptes, le compte OTEA Production (mix photos + IA), et Pierre Huiban (banque de vraies photos, avant considéré non-attachable). Limite : 50 Mo/fichier via media_import_url ; via upload_url pas de limite constatée (testé 2,3 Mo). Note : bucket cloudfront différent des IA (`d2ol7oe...` vs `d8j0ntlcm91z4...`) mais tous deux publics.

**Marche aussi pour les VIDÉOS mp4** (validé 30/07/2026, stories animées OTEA) : `content_type: video/mp4` + `media_confirm type video` → URL `.mp4` acceptée telle quelle par `bulk_schedule_stories` (story vidéo Metricool). **Pipeline « photo animée » réutilisable pour tous les clients** : calques PIL séparés (fond photo sans texte + PNG du texte avec scrim dégradé sombre en haut) → image-to-video Higgsfield `kling3_0_turbo` (7,5 crédits/5 s, prompt « subtle cinemagraph, slow cinematic push-in, face stays perfectly identical, no morphing » + `declined_preset_id` si le résolveur propose un preset) → ffmpeg : upscale 1080x1920 (sortie kling = 720p) + overlay du PNG texte (texte parfaitement net, seule la photo bouge) → héberger le mp4 ici. Toujours vérifier des frames extraites (visages !) avant de brancher.

**Règles apprises le 31/07/2026** (batch 18 visuels Loft/Gossip/OTEA) : (1) Si le TEXTE est incrusté dans l'image source, imposer **« Locked static camera, absolutely no zoom »** — un push-in fait sortir le texte du cadre (raté sur « Instant massage »). Toujours contrôler la DERNIÈRE frame, pas la première. (2) Inutile de ré-héberger les vidéos i2v : leur `rawUrl` Higgsfield (`d8j0ntlcm91z4...mp4`) est publique et acceptée telle quelle par `bulk_schedule_stories` — n'uploader que les fichiers assemblés localement. (3) **Outro de marque** : `ffmpeg xfade=transition=fade:duration=0.6:offset=<durée-0,6>` après avoir normalisé l'outro (`scale=1080:1920,fps=24`) → story de ~9,5 s, format story valide. (4) Texte clair sur photo claire = illisible : voile opaque + texte foncé, vérifier visuellement avant de produire les 6 déclinaisons.

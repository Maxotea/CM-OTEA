---
name: story-video-plein-cadre
description: "Chaîne validée pour une story : vraie photo du client recadrée 9:16, animée en i2v caméra verrouillée, plein cadre 1080x1920, texte incrusté après coup, muette, brouillon."
metadata:
  node_type: memory
  type: process
  originSessionId: 5d260eaa-a401-5488-9c85-8ed7413f4910
  modified: 2026-08-28T00:00:00.000Z
---

**Maxime a validé ce process le 28/08/2026** (« c'est parfait pour la galerie
immobilière, garder ce process »). C'est désormais **la façon par défaut de
produire une story**, sur La Galerie et sur tout compte qui possède de vraies
photos. Ne pas repartir d'un autre format sans qu'il le demande.

## La chaîne, dans l'ordre

1. **Recadrer en 9:16 dans PIL, avant tout.** 864×1536, centré, sans aucun
   texte. Sur La Galerie : `scripts/lg-crop-9-16.py <NN…>`, qui relève la photo
   directement sur les annonces du site du client.
2. **Animer en i2v** : `generate_video_batch`, modèle `kling3_0_turbo`,
   `duration: 5`, `aspect_ratio: "9:16"` (sortie native 720×1280),
   `use_unlim: false`, `medias: [{value: <media_id>, role: "start_image"}]`.
   **7,5 crédits par plan.** Prompt **verrouillé sur l'identité** et **caméra
   verrouillée** : ce sont la lumière, les rideaux, le feuillage qui bougent,
   jamais le cadre.
3. **Contrôler la dernière frame contre la photo source** avant de brancher
   quoi que ce soit. C'est là que la dérive apparaît.
4. **Composer en ffmpeg, plein cadre 1080×1920** : la vidéo occupe tout le
   cadre, le texte est posé par-dessus en overlay PNG. Le texte ne passe
   **jamais** dans le modèle. Sur La Galerie : `scripts/lg-story-video.py`.
5. **Sortie muette** (`-an`), règle `stories-sans-son.md`.
6. **Brancher en brouillon** via `set_post_media_list`, puis
   **`audit_publication_safety`** sur la période : total, drafts, autoPublish,
   noMedia. Règle `autonomie-decisions-cm.md`.

## Les trois pièges, tous mesurés et payés

⛔ **Ne jamais lancer l'i2v en 9:16 depuis une photo paysage.** Le modèle
**réinvente la pièce** : écart de 58,8 contre la vraie photo, aucun recadrage
de l'original ne correspond. C'est exactement le reproche de William du Loft
(« des photos qui ne sont pas prises chez moi »). Recadrer d'abord, animer
ensuite : écart 4,1 sur la première image, 6,0 sur la dernière, contre 4,0
entre deux images d'une même vidéo.

⛔ **Ne jamais loger la vidéo dans une vignette sur une carte de texte.** Testé
le 21/08 : 24 % de la surface, mouvement 1,0 contre 18,2 sur une story Run On
Invest. Maxime l'a vu tout de suite (« ce ne sont pas des vidéos »). Plein cadre,
ou rien.

⛔ **Ne jamais se contenter d'un `zoompan` ffmpeg.** Refusé par Maxime le
01/08 (« pas des images animées mais juste des zooms »). Secours **uniquement**
si un visage se déforme malgré le prompt renforcé.

⚠️ **Le travelling avant a été écarté par Maxime** (28/08) alors qu'il donnait
3× le mouvement de Run On Invest : en avançant, le modèle extrapole ce que la
photo ne montrait pas, et le contrôle de dernière frame ne vaut plus rien.
Caméra fixe.

⚠️ **Accents.** Ne jamais saisir un texte client sans accents « pour éviter un
problème d'encodage ». Vérifier la couverture glyphe par glyphe avec
`ImageFont.getmask(c).getbbox()`, et transférer le script dans la sandbox en
**gzip + base64** (`base64 -d | gunzip`, vérifié au `md5sum`) plutôt que de le
retaper.

## Réutiliser plutôt que regénérer

Les plans i2v déjà produits sont **réutilisables à zéro crédit** : ils vivent
sur `https://d8j0ntlcm91z4.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/hf_<date>_<heure>_<job_id>.mp4`.
Le mapping des 19 plans de La Galerie est dans le dictionnaire `PLANS` de
`scripts/lg-story-video.py`. Avant de lancer une nouvelle vague, regarder ce
qui existe : une vague de 14 stories a été refaite le 24/08 sans dépenser un
crédit.

## Pièges d'outillage

- `set_post_media_list` prend `blog_id` (underscore) ; `summarize_scheduled_posts`
  et `media_inventory` prennent `blogId` (camelCase). Se tromper renvoie
  « blogId, start, and end are required ».
- **Chaque PUT réussi renvoie le post sous un NOUVEL id** : relister les stories
  avant chaque nouveau mapping.
- `bulk_update_post_media` **crée un doublon** au lieu de modifier. Ne pas
  l'utiliser.
- La sandbox Higgsfield est recyclée ~10 s après chaque appel : rien ne survit
  entre deux commandes. Une URL présignée pèse ~3,4 Ko, donc **3 PUT maximum par
  commande**.

Voir aussi [[stories-vraies-photos-sans-ia]] (ce qui est interdit et ce qui ne
l'est pas), [[stories-sans-son]], [[hebergement-photos-reelles-metricool]].

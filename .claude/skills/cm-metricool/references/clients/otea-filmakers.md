# Otea Filmakers — fiche client

## Identité
- blogId : **4728418** · @oteafilmakers — **marque vitrine créative/voyage** du vidéaste, à
  traiter différemment d'OTEA PRODUCTION (5733269, B2B plateau, 12h).
- Typologie : B2B projet en vitrine — ROI en leads qualifiés (DM, formulaires). Sert aussi de
  **banc d'essai du parcours client complet** : review hebdo active, préfixe OF
  (`reviews/config.json`, Google Sheet déposé le 08/08/2026 pour la semaine du 10/08).
- Réseaux réellement utilisés par les posts feed : **Instagram + TikTok** (le brief d'origine
  citait IG/FB/TikTok/LinkedIn ; les 21 brouillons en place sont IG+TikTok — ne pas élargir sans
  décision de Maxime). Horaire feed : **18h00 Paris** (compte créateur, pas le 12h B2B).
- Ton : tutoiement créateur, voix « je ». Priorité éditoriale : **reels** — les posts feed
  portent des briefs « 🎬 À tourner » destinés à devenir des vidéos.

## DA visuelle (posée le 08/08/2026)
- **Élément de référence Higgsfield : `OteaFilmakers-Voyage`**
  (id `e9f1a0b5-d12f-439d-bd77-d4312d5eae40`, environment). DA : cinéma de voyage — golden hour,
  grade teal & or chaud, océan et vague (ADN polynésien), côtes, routes, sommets, silhouettes de
  vidéaste en contre-jour (caméra, gimbal, sac), matériel ciné en extérieur, brume atmosphérique,
  grain film 35 mm léger. **Jamais de visage identifiable, jamais de logo ni texte.**
  Réutiliser `<<<e9f1a0b5-d12f-439d-bd77-d4312d5eae40>>>` dans les prompts.
- Modèle : `cinematic_studio_2_5` (Cinema Studio Image 2.5), **4:5**, 2k — seul modèle
  compatible éléments avec le 4:5 natif feed. Limite plan pro : 4 jobs simultanés (soumettre les
  batchs quand la file est vide) ; deux faux positifs NSFW sur des paysages, résolus en
  reformulant le prompt.
- À distinguer d'`OTEA-Studio` (b40ad9de…, plateau B2B, orange #FF5800 néon) : Filmakers =
  extérieur/voyage/nature, la chaleur vient de la lumière, pas du orange studio.

## STATUT BRANCHEMENT : ✅ (08/08/2026)
- **21/21 posts feed du 03/08 au 18/09 avec visuel IA dédié** (1 image unique par post, pas de
  rotation), brouillons vérifiés (`draft:true`, `autoPublish:false`), IG+TikTok, 18:00 exact —
  pas de bug +7h : `bulk_replace_posts` pose la date en direct API avec timezone Europe/Paris.
- Contrôle final : 21 posts, `noMedia: 0`, `withPlaceholders: 0`, 1 post par créneau.
- Méthode : **`bulk_replace_posts`** (crée le post avec média + heure exacte, vérifie le
  brouillon, supprime l'ancien). Les IDs changent — le repêchage par créneau de
  `scripts/review.py` (`retrouver_post`) absorbe le changement pour la review en cours.
- ⚠️ Confirmé le 08/08/2026 : **`swap_post_media_verified` (PUT) crée des posts fantômes** —
  réponse 200 « unchanged » mais doublon 359747137 apparu sur le créneau du 03/08, purgé via
  `bulk_delete_posts`. Même famille de piège que le PUT scheduler (fiche OTEA PRODUCTION) :
  pour changer ou attacher un média, TOUJOURS `bulk_replace_posts`.
- ⚠️ 3 posts à **date passée** (03, 05, 07/08) : recréés avec visuel comme le reste, mais leur
  créneau est passé — à re-dater ou à archiver, décision Maxime.

## Banque IA (22 visuels Higgsfield, 08/08/2026)
Hébergement : CDN Higgsfield (comme la banque OTEA PRODUCTION) — Metricool référence l'URL
source (`saveExternalMediaFiles:false`), ne pas supprimer les générations du workspace.
Base : `https://d8j0ntlcm91z4.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/`

| Date | Post | Scène | Fichier |
|---|---|---|---|
| — | élément | falaise océan, vidéaste au gimbal, golden hour (image fondatrice) | hf_20260808_150405_bdb6d95c-97c0-46c6-9630-7efd8cf74997.png |
| 03/08 | 359747253 | montée nocturne à la frontale, aube dorée (discipline) | hf_20260808_150614_277d8d98-baed-42c5-85a4-724cd28716d8.png |
| 05/08 | 359747606 | bureau de montage la nuit, mains sur clavier | hf_20260808_150614_9287ceda-8bce-4803-ac0a-f0ecaeaf2d0a.png |
| 07/08 | 359747639 | belvédère, vallée, rivière et brume (lieu de rêve) | hf_20260808_151009_d6846eac-7497-4ba7-abb6-4c3784cc42c9.png |
| 10/08 | 359747646 | caméra sur trépied, crête au crépuscule (plan failli) | hf_20260808_150614_dc31275e-1df2-4535-8364-acebee5caa13.png |
| 12/08 | 359747660 | route côtière au lever, sac posé (voyager) | hf_20260808_150615_9b09f975-fb61-498d-a408-147d3ca4bc4b.png |
| 14/08 | 359747741 | assis immobile face au fjord (regarder d'abord) | hf_20260808_150615_3a02b289-6f48-4cb3-8083-ed60bf683156.png |
| 17/08 | 359747746 | plaine vide, lumière plate (page blanche) | hf_20260808_150615_7c188cf2-b09f-41a7-a691-84105edafce1.png |
| 19/08 | 359747754 | enregistreur + bonnette en forêt (le son) | hf_20260808_150615_3788af05-2617-4f0a-9b80-e33d87a2e8b6.png |
| 21/08 | 359747760 | cartes SD, disques, carnet (fin d'été) | hf_20260808_150615_9bf78e26-3c46-40e7-bc00-7dd402eddd0b.png |
| 24/08 | 359747849 | marche caméra à l'épaule, herbes en contre-jour (erreurs) | hf_20260808_150615_64091cf2-3f39-47d8-a228-361e04528188.png |
| 26/08 | 359747857 | petite caméra face au panorama immense (matériel) | hf_20260808_150615_6061ee2e-24fa-4a45-8229-2097422a61da.png |
| 28/08 | 359747869 | carnet vierge, café, fenêtre (rentrée) | hf_20260808_150614_5728bc97-877d-4f08-9aa7-76ebf4a313ac.png |
| 31/08 | 359747898 | prairie d'automne, lumière rasante (septembre) | hf_20260808_150823_cc2c2595-76d5-4579-8a9f-d6e53e8f23bf.png |
| 02/09 | 359748073 | marche gimbal, poussière dorée (marche féline) | hf_20260808_150823_f8a74482-98ce-480c-8efc-9fc7834dfe93.png |
| 04/09 | 359748079 | flat lay matériel au sol (coulisses) | hf_20260808_150823_c5daf807-fc7c-4666-8482-8f6a46d0816f.png |
| 07/09 | 359748089 | sentier en lacets vers le col (récit en 3 temps) | hf_20260808_151232_0001fc2d-36cb-4ac0-8dd6-d5bade97f83c.png |
| 09/09 | 359748094 | silhouette minuscule sur la crête (comparaison) | hf_20260808_150823_649dbd0d-cd87-4d2d-a298-8ffebcbc2983.png |
| 11/09 | 359748177 | chemin banal magnifié, brume dorée (10 min de chez soi) | hf_20260808_150823_143f07ed-7da9-49fc-a7fc-6cbad84ace83.png |
| 14/09 | 359748182 | mains refermant le laptop, nuit (finir) | hf_20260808_150823_4ed2a328-242c-4e6d-b0c8-453d5ce01213.png |
| 16/09 | 359748199 | moniteur split log / étalonné (étalonnage) | hf_20260808_150823_ddf99e52-0dfb-4b22-8a99-277baa22a405.png |
| 18/09 | 359748208 | café fumant, écran de montage, matin (rituel week-end) | hf_20260808_150823_de8665f3-6b32-4a4b-a809-941d0fc28318.png |

## Suite naturelle
- Remplacer progressivement les visuels IA par de **vraies images** (coulisses de tournage,
  extraits de réalisations avec accord) via la boîte de dépôt Drive, comme la 2ᵉ passe OTEA
  PRODUCTION — mapping thématique puis `bulk_replace_posts`.
- Les briefs « 🎬 À tourner » sont des reels en attente : passer par `reel-script` puis
  `reel-lint` avant tournage.

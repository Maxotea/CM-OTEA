# Reprise : stories vraies photos animées — état au 03/08/2026 ~14h30

Travail interrompu par la **limite de dépense mensuelle du compte Claude**
(à relever sur claude.ai/settings/usage). Tout ce qui précède est commité ;
ce fichier est le plan exact pour reprendre sans réexplorer.

## Décision de Maxime (03/08)
Stories = **vraies photos transformées en vidéo** (pipeline i2v éprouvé),
pour TOUS les comptes, y compris Run On Invest. Les cartes typographiques
de J Lawson et La Galerie sont rejetées — elles restent en brouillon
inoffensif (rien ne se publie sans validation) en attendant remplacement.
Maxime n'a **pas** les dossiers photos sous la main → « faire au mieux »
avec les photos déjà hébergées.

## Inventaire photos réellement accessibles (vérifié 03/08)
| Compte | Vraies photos | Où |
|---|---|---|
| J Lawson | ~5 candidates | posts publiés Metricool, `static.metricool.com/common/202607/6563137-mtr_*` — candidates par résolution/poids : n° 01 (…15004927010967591954.jpeg, 1448×1086), 03 (…12764512827799543594.jpeg, 1440×960), 06 (…6326575259361033427.jpeg, 1440×960), 09 (…6876674637451197532.jpg, 3840×2560), 11 (…11226288403794074990.jpg, 2560×3840, verticale). Les n° 02/08 = photos de presse (PETITES, web) à EXCLURE ; 04/05/07/10 = 1344×896/896×1344 = tailles de sortie Higgsfield → IA, à EXCLURE. **Vérification visuelle à refaire avant usage.** |
| Pierre Huiban | 11 | cloudfront d2ol7oe (mapping dans sa fiche, section Branchement) |
| Le Loft | 7 | cloudfront (stories actuelles) |
| Gossip | 7 | cloudfront (stories actuelles) |
| OTEA | ~8-10 | cloudfront |
| La Galerie | 0 | rien — bloqué photos |
| Run On Invest | 0 | rien — événement pas encore tenu |

## Pipeline de reprise (éprouvé de bout en bout aujourd'hui)
1. Sandbox Higgsfield : télécharger les photos → crop 9:16 SANS texte + calque texte PNG (PIL).
2. i2v `kling3_0_turbo` (7,5 cr/5 s), prompt verrouillé identité : « Locked static
   camera, no zoom. Documentary realism: [micro-mouvement]. Every face and identity
   stay strictly identical to the photo — same features. No morphing… »
3. **Contrôler la DERNIÈRE frame contre la photo source** (visages !) avant tout branchement.
4. ffmpeg : upscale 1080×1920 + overlay texte net + fond sonore
   (`scripts/fond-sonore-stories.py` — jl.wav / lg.wav existants ; en composer un par
   typologie pour Pierre et ROI).
5. Hébergement : media_upload (28 slots à la fois) → PUT depuis la sandbox
   (l'upload local est bloqué par le proxy) → media_confirm.
6. `bulk_schedule_stories` (brouillon, ≤12/lot) + `bulk_delete_posts` des anciennes.
   Piège connu : erreurs « Code execution error » qui ont en fait réussi → toujours vérifier par listing.

## Ordre de reprise
1. **J Lawson** : vérifier visuellement les 5 candidates → i2v → remplacer les slots
   de cartes correspondants (5 photos < 14 : les slots restants gardent leur carte, flagués).
2. **Pierre Huiban** : 11 photos → remplacer ses 31 cartes typo.
3. **Le Loft / Gossip / OTEA** : variantes semaine B (nouvelles animations/textes des
   mêmes photos) pour tendre vers la règle des 2 semaines — vraie conformité = nouvelles photos.
4. **La Galerie / ROI** : bloqués photos. ROI : teasing feed déjà en brouillon.

## Rappels
- 56 stories cartes J Lawson/Galerie en brouillon : NE PAS VALIDER (Maxime les a refusées).
- Manifest des 14 slots/textes : `assets/stories/manifest-stories-2sem.json` (titres réutilisables sur les vidéos photo).
- Budget Higgsfield : ~3 100 crédits restants — largement assez (~40 i2v ≈ 300 cr).

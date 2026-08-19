# Stories vraies photos animées — état au 19/08/2026

## ✅ J Lawson Golf : terminé (4 slots sur 14)
Les 4 photos réelles exploitables du compte sont passées en stories vidéo,
contrôle d'identité validé sur chacune. Détail complet (ids, media_ids,
chaîne de production, prompts) : `.claude/skills/cm-metricool/references/clients/jlawsongolf.md`,
section « Stories VRAIES PHOTOS ».

Les 10 slots restants gardent leur carte typographique : il n'existe pas
d'autre vraie photo utilisable sur le compte tant que `medias/` n'est pas rapatrié.

## Inventaire photos réellement accessibles (vérifié 03-04/08)
| Compte | Vraies photos | Où | Statut |
|---|---|---|---|
| J Lawson | 4 exploitables (03, 06, 09, 11) | posts publiés Metricool, `static.metricool.com/common/202607/6563137-mtr_*` | ✅ fait |
| Pierre Huiban | 11 | cloudfront d2ol7oe (mapping dans sa fiche, section Branchement) | ⏭ à faire |
| Le Loft | 7 | cloudfront (stories actuelles) | ⏭ variantes semaine B |
| Gossip | 7 | cloudfront (stories actuelles) | ⏭ variantes semaine B |
| OTEA | ~8-10 | cloudfront | ⏭ variantes semaine B |
| La Galerie | 0 | rien | ⛔ bloqué photos |
| Run On Invest | 0 | événement pas encore tenu | ⛔ bloqué — stories typo en DA du kit, voir sa fiche |

**Exclusions J Lawson, à ne pas réessayer :** photos 02/08 = photos de presse
(petites, web) ; 04/05/07/10 = 1344×896 ou 896×1344, tailles de sortie
Higgsfield donc images IA ; 01 = visuel promo The Open (texte incrusté, droits R&A).

## Ordre de reprise
1. **Pierre Huiban** : 11 photos → remplacer ses 31 cartes typo. Prévoir un fond
   sonore propre à sa typologie (plus dur que `jl.wav`).
2. **Le Loft / Gossip / OTEA** : variantes semaine B (nouvelles animations et
   nouveaux textes des mêmes photos) pour tendre vers la règle des 2 semaines.
   La vraie conformité demandera de nouvelles photos.
3. **La Galerie / ROI** : bloqués tant que Maxime n'a pas fourni de photos.

## Pièges connus
- **Plafond quotidien Higgsfield** (`grace_daily_limit_reached`, 403 sur tous les
  modèles vidéo, crédits intacts) : il se réinitialise dans la nuit. Reprendre
  via `send_later` plutôt que d'insister.
- **Timeout MCP à 60 s** sur `sandbox_exec` : garder chaque commande courte
  (`-preset veryfast` divise le rendu par 5) et **toujours enchaîner rendu + PUT
  dans la même commande**, la sandbox est détruite ~10 s après.
- **stdout tronqué au-delà de ~25 KB** : émettre les vignettes de contrôle une par
  une, ≤ 7 KB (h=190, qualité ~34).
- Erreurs « Code execution error » Zapier qui ont en fait réussi : **toujours
  vérifier par listing avant de relancer**.

## Rappels
- Manifest des 14 slots/textes : `assets/stories/manifest-stories-2sem.json`.
- Cartes typo restantes en brouillon : NE PAS VALIDER, elles seront remplacées.
- Budget Higgsfield : ~3 085 crédits (4 i2v consommés à 7,5 cr).

---

# Chantier ouvert le 04/08/2026 — stories muettes + IA pour ROI

## Règle 1 : aucune bande son sur les stories
`.claude/memories/stories-sans-son.md`. Retrait du son sans ré-encodage :
`ffmpeg -i in.mp4 -an -c copy out.mp4`, puis nouveau `media_upload`/PUT/confirm,
puis `bulk_schedule_stories` de la version muette + `bulk_delete_posts` de
l'ancienne (bien moins verbeux que `bulk_replace_posts`).

### ✅ DÉMUTAGE TERMINÉ — tous comptes, vérifié le 19/08/2026

Balayage complet des 10 comptes Metricool. Chaque vidéo de story programmée
a été contrôlée à l'`ffprobe` (`audio=0` exigé), pas seulement supposée.

| Compte | blogId | Stories à venir | Verdict |
|---|---|---|---|
| J Lawson Golf | 6563137 | 43 (19/08→30/09) | ✅ 43 muettes |
| La Galerie Immobilière | 5733302 | 13 (19→31/08) + PNG sept. | ✅ 13 remplacées |
| OTEA PRODUCTION | 5733269 | 13 (19→31/08) | ✅ 6 remplacées, 7 déjà muettes |
| Run On Invest | 6636615 | 2 (19 + 21/08) | ✅ muettes dès l'origine (photos IA) |
| Le Loft | 6191921 | 13 | ✅ aucun flux audio |
| Gossip Beauty Center | 5733306 | 13 | ✅ aucun flux audio |
| Pierre Huiban | 6572293 | 13 | ✅ stories en PNG, pas de vidéo |
| Otea Filmakers | 4728418 | 0 | — |
| Confshine Game | 6625190 | 0 | — |
| ExpliqueMoi | 6704763 | 0 | — |

**Deux surprises qui ont coûté du travail non prévu — à retenir :**
1. **OTEA PRODUCTION portait bien du son.** Ce fichier affirmait l'inverse
   (« leurs stories datent de sessions antérieures au fond sonore »). Faux :
   les 3 cartes photo composées le 29/07 (Coulisses `b7f45530`, Parlons projet
   `da10744b`, Captation `1fe49bcf`) avaient une piste. Les 4 cartes IA, non.
   → **Ne jamais conclure sans `ffprobe`.**
2. **Les stories de septembre de J Lawson étaient invisibles** dans la fenêtre
   de listing initiale (19/08→01/09). 30 stories de plus, créées le 04/08,
   dont 18 cartes pointaient encore sur les médias sonores.
   → **Toujours balayer jusqu'à la fin du calendrier, pas 15 jours.**

#### Correspondance médias muets — J Lawson (réutilisables tels quels)
Photos : `c42ca037` Le shaft · `fd54ea6e` Fers sur mesure · `52d09b09` La data
parle · `1e56a55c` Analyse Gears · `2b35934e` Côté atelier.
Cartes : `9c7aaa64` Driver · `08546cef` Réserve ton fitting · `6e0255a9` Jour de
parcours · `06321768` Objectif semaine · `491d044f` Wedges · `627412c5` Putter ·
`1638ebdf` Dernier call · `36467b17` 18 trous · `526845eb` Nouvelle semaine.

#### Correspondance médias muets — OTEA PRODUCTION
`85fc08f7` Coulisses · `422579cc` Parlons projet · `dcaa7c92` Captation
événement. (Les 4 cartes IA — Le conseil, Inspiration, Belle semaine, Idée
vidéo — étaient déjà muettes, inchangées.)

#### Correspondance médias muets — La Galerie (19→31/08, dans l'ordre)
`b9a05073` · `f900db6b` · `93487272` · `83cbee6d` · `202cc2ed` · `93a618a4` ·
`01b9a000` · `9f221602` · `baae616a` · `3c78c8c1` · `8d5175ed` · `19abe707` ·
`38e3a858`.

### Procédure de démutage (si une nouvelle vidéo sonore apparaît)
1. `ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 f.mp4 | wc -l`
   → doit rendre `0`.
2. `media_upload` **avant** la commande sandbox (la sandbox meurt ~10 s après).
3. Dans **une seule** commande : `curl` la source → `ffmpeg -i in -an -c copy out`
   (pas de ré-encodage) → `ffprobe` de contrôle → `curl -f -X PUT`.
   ≤ 5 URL présignées par commande (limite de 16 000 caractères).
4. `media_confirm` en lot, puis `bulk_schedule_stories` (≤ 7 par appel) et
   `bulk_delete_posts` des anciennes — bien moins verbeux que `bulk_replace_posts`.
5. Vérifier par `summarize_scheduled_posts` : une story par jour, aucun trou,
   aucun doublon, `draft:true` partout.

## Règle 2 : Run On Invest peut utiliser des photos IA ultra réalistes
Autorisation de Maxime du 04/08. **Limite absolue conservée : aucune personne
réelle identifiable** — on ne génère jamais le visage d'un client, d'un
participant ou de Maxime. L'exception ne vaut que pour ROI, qui n'a aucune
photo et dont l'événement n'a pas encore eu lieu.

### ✅ Fait le 19/08 — 9 photos IA générées, 4 brouillons en ligne
9 photos `soul_2` 9:16 « La Défense au petit matin » (parvis, tours de verre,
lumière rasante, coureurs de dos ou en plan large, **aucun visage
reconnaissable**), planches-contact contrôlées visuellement une par une.

Brouillons R.O.I. actuellement programmés — **c'est tout ce qui reste** :
| Date | id | Type |
|---|---|---|
| 19/08 12:00 | 363855795 | Story photo IA, muette |
| 19/08 18:00 | 363855131 | Feed photo IA (créneau 08:00 périmé → replanifié) |
| 21/08 12:00 | 363855807 | Story photo IA, muette |
| 21/08 08:00 | 363855142 | Feed photo IA |

⚠️ **Le teasing d'août est épuisé au 21/08.** Aucun des posts du 03→17/08 n'a
été validé dans l'interface : leurs créneaux sont passés, ils ont disparu.
Il reste 7 photos IA inutilisées, prêtes pour une reprise en septembre.
Habillage : `scripts/roi-photo-habillage.py`.

## Mise à jour 04/08 (suite) — lieu R.O.I. déverrouillé + IA sur le feed
- Maxime confirme : **course à La Défense**, **networking à la Plénitude Arena**.
  Le brief interdisait tout teasing du lieu sans son accord ; c'est son accord.
  **Restent verrouillés : dates, jauge, prix.**
- 3 posts feed réécrits avec le lieu (ids **357722958** 04/08 20h, **357722984**
  07/08, **357723008** 10/08). Le post d'ouverture, dont le créneau du 03/08 20h
  était passé sans validation, a été **replanifié au 04/08 20h**.
- Photos IA ultra réalistes autorisées **feed ET stories** sur ROI.
  Production à faire : ~9 visuels feed 4:5 + 9 stories 9:16 (photo IA → i2v →
  muet → habillage typo par-dessus), puis remplacement des 18 brouillons.
  Direction : La Défense au petit matin, parvis et tours, lumière rasante,
  coureurs de dos ou en plan large. **Aucun visage reconnaissable.**

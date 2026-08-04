# Stories vraies photos animées — état au 04/08/2026 02h30

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

### ✅ Fait — J Lawson, 5 vidéos / 10 stories
| Vidéo | Nouveau media_id muet | Dates | Nouveaux ids |
|---|---|---|---|
| Le shaft (photo) | `c42ca037-0252-435f-9ce5-47daf70678f9` | 04 · 18/08 | 357720588 · 357720590 |
| La data parle (photo) | `52d09b09-ad2f-4b1d-9872-5341362dbe4b` | 08 · 22/08 | 357720598 · 357720611 |
| Côté atelier (photo) | `2b35934e-deb7-40f5-906a-fb2dabf2cc10` | 15 · 29/08 | 357720619 · 357720629 |
| Analyse Gears (photo) | `1e56a55c-8b79-4ed2-96ef-54aa2774ff19` | 13 · 27/08 | 357720638 · 357720649 |
| Fers sur mesure (carte) | `fd54ea6e-b22b-4370-91d4-34575a598161` | 05 · 19/08 | 357720654 · 357720661 |

Anciennes versions sonores supprimées (357633119/132/162/181/211/226,
357397907/912, 357218619, 357218975).

### ⏳ Reste à démuter — J Lawson, 9 cartes (~18 brouillons), blog 6563137
`ed2311d9-5fe7-4af6-8596-891d3b2dab50` Driver 06+20/08 ·
`19ce8fd8-f990-45d7-a4c0-b07409a3cc04` Réserve ton fitting 07+21/08 ·
`a0648150-258b-4544-bbf4-3bc53dcc04a4` Jour de parcours 09+23/08 ·
`accd29a4-ef41-40cf-8776-38c6cccbcc93` Objectif semaine 10+24/08 ·
`5b62a0ca-bf04-429e-bc7f-cb0089c977f9` Wedges 11+25/08 ·
`30429e4b-5c29-4687-b00e-994e5f151d3d` Putter 12+26/08 ·
`33f90c29-393e-450f-92a8-d74188d3f1cc` Dernier call 14+28/08 ·
`52e4808b-0937-4b48-adb0-d789d9ea1681` 18 trous 16/08 ·
`b227dee8-906a-4db0-a507-8b0c7c361b9c` Nouvelle semaine 17/08.
⚠️ Vérifier aussi les 30 et 31/08 (hors de la fenêtre déjà listée).

### ⏳ Reste à démuter — La Galerie, 14 cartes (28 brouillons), blog 5733302
Toutes portent `lg.wav`. Même procédure.

### ⏳ À vérifier — Pierre Huiban, Le Loft, Gossip, OTEA
Leurs stories datent de sessions antérieures au fond sonore : contrôler par
`ffprobe` si un flux audio existe avant d'engager le travail.

## Règle 2 : Run On Invest peut utiliser des photos IA ultra réalistes
Autorisation de Maxime du 04/08. **Limite absolue conservée : aucune personne
réelle identifiable** — on ne génère jamais le visage d'un client, d'un
participant ou de Maxime. L'exception ne vaut que pour ROI, qui n'a aucune
photo et dont l'événement n'a pas encore eu lieu.

### À produire (remplace les 9 stories cartes typo actuelles, blog 6636615)
1. Générer des **photos IA ultra réalistes** de coureurs en ville au petit matin,
   plans larges ou de dos, cadrage 9:16 — pas de visage reconnaissable en gros plan.
   DA du kit : lumière naturelle, palette Écru/Encre, accent Blaze discret.
2. i2v (kling3_0_turbo) pour l'animation, **sans son**.
3. Habillage typographique ROI par-dessus (`scripts/roi-visuels.py` fournit la DA).
4. Remplacer les 9 stories actuelles (357483920, …931, …953, …978, …985, …990,
   357484000, …019, …034) et supprimer les anciennes.
5. Les visuels feed peuvent aussi passer en photo IA si Maxime le souhaite —
   à lui confirmer, la DA typographique du kit reste valable.

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

# 📅 Semaine du lundi 17/08 au dimanche 23/08 — récap des publications

*CR hebdo · routine « CR client Publi Hebdo » (lundi 9h00 Paris) · généré le 24/08/2026 ·
5 comptes clients + Otea Filmakers (banc d'essai) · données Metricool réelles (list/summarize
scheduled posts, plage 17→23/08).*

## ⚠️ À traiter avant tout le reste

1. **Gossip Beauty Center et J Lawson Golf : 0 publication cette semaine.** Les 10 contenus
   programmés de chacun des deux comptes sont encore intégralement en brouillon dans Metricool
   (`draft: true` sur les 10 lignes) — rien n'est parti. Ce sont deux comptes Signature payants :
   à valider en priorité dans Metricool, ou à passer en review pour que le circuit client s'en
   charge une fois débloqué (point 2).
2. **Le circuit de review client (fichier Excel/Sheet hebdo) ne fonctionne pour aucun compte
   depuis sa mise en place le 19/08.** Le job `appliquer` (3 relèves/jour) tourne mais ne trouve
   aucune décision cliente : `reviews/etat/` n'a jamais été créé. Deux causes cumulées :
   - **Aucun client n'a reçu son mail ou son message de validation** : les 5 comptes clients ont
     `email_confirme: false` et `whatsapp_confirme: false` dans `recaps/clients-config.json` —
     personne n'a encore de coordonnée confirmée, donc aucun mail/WhatsApp n'est jamais parti,
     même en brouillon envoyé à la main.
   - **Les dossiers Drive des 5 clients sont partagés en LECTEUR, pas en ÉDITEUR** (note du
     21/08 dans `reviews/config.json`) : même relevé, un client ne pourrait pas cocher ✅/✏️/⛔
     dans son tableau — il faut, une fois, passer chaque dossier « Validation hebdo — <Client> »
     en « tous les utilisateurs disposant du lien : éditeur ».
   - Conséquence : les 3 publications sorties chez Le Loft, les 2 chez La Galerie Immobilière et
     les 3 chez Pierre Huiban cette semaine sont passées par une validation manuelle de Maxime
     directement dans Metricool — pas par le circuit review.
3. **`appliquer` échoue en rouge à chaque passage depuis le 19/08** (runs #44 à #60, un job sur
   deux) à cause d'**Otea Filmakers** : son dossier Validation hebdo n'a aucune permission
   « tous les utilisateurs disposant du lien », l'export public renvoie une erreur et fait sortir
   tout le job en erreur — sans bloquer les autres comptes, mais le voyant reste rouge en continu.
   Réglage à faire une fois par Maxime sur ce dossier.
4. **Le CR du lundi n'était pas parti depuis 3 semaines** : dernier `recap-semaine-*.md` /
   `whatsapp-semaine-*.md` daté du 03/08. Celui-ci reprend le format à jour (cycle vendredi →
   lundi, dossiers Drive permanents) introduit le 19/08.

## Vue d'ensemble — semaine du 17 au 23/08

| Compte | Palier | Programmé | Publié / validé | En attente (brouillon) |
|---|---|---|---|---|
| Gossip Beauty Center | Signature | 10 (7 stories + 3 posts) | **0** | 10 |
| Le Loft | Signature | 10 (7 stories + 3 posts) | 3 | 7 |
| J Lawson Golf | Signature | 10 (7 stories + 3 posts) | **0** | 10 |
| La Galerie Immobilière | Essentiel | 9 (7 stories + 2 posts) | 2 | 7 |
| Pierre Huiban | — | 9 (7 stories + 2 posts) | 3 | 6 |

*« Publié / validé » = statut `draft: false` dans Metricool au 24/08 (parti ou passé en
publication automatique). Le détail par compte suit ; le lien vers le dossier Validation hebdo
de chaque client est rappelé à chaque section — c'est le lien permanent, à donner tel quel.*

## Gossip Beauty Center — 0 / 10 publiés ⚠️

- Lun 17 · 10h Story 📝 « Belle semaine » · 18h Post 📝 « Les tendances coiffure de la rentrée »
- Mar 18 · 10h Story 📝 « Le rituel hammam »
- Mer 19 · 10h Story 📝 « Côté coiffure » · 18h Post 📝 « Cheveux soleil/sel/chlore »
- Jeu 20 · 10h Story 📝 « Instant massage »
- Ven 21 · 10h Story 📝 « Pensez au week-end » · 18h Post 📝 « La rentrée se prépare maintenant »
- Sam 22 · 10h Story 📝 « Un lieu 100% féminin »
- Dim 23 · 10h Story 📝 « Douceur du dimanche »

Dossier Validation hebdo (permanent) : https://drive.google.com/drive/folders/1bbO5_SNq8EsFePBoRQvW8fm2KfJNvh18

## Le Loft — 3 / 10 publiés

- Lun 17 · 10h Story 📝 · 18h Post 📝 « Les coupes de la rentrée 2026 »
- Mar 18 · 10h Story 📝 « Head spa »
- Mer 19 · 10h Story ✅ · 18h Post ✅ « Tu viens pour la coupe depuis deux ans… »
- Jeu 20 · 10h Story 📝
- Ven 21 · 10h Story ✅ · 18h Post 📝 « J-10 avant la rentrée »
- Sam 22 · 10h Story 📝
- Dim 23 · 10h Story 📝

Dossier Validation hebdo (permanent) : https://drive.google.com/drive/folders/1pqpmlG9ussUd2wYiVLMXOxMcwJCwIuOl

## J Lawson Golf — 0 / 10 publiés ⚠️

- Lun 17 · 10h Story 📝 · 18h Post 📝 « Ce que l'été m'a appris au studio »
- Mar 18 · 10h Story 📝 « Le shaft »
- Mer 19 · 10h Story 📝 « Fers sur mesure » · 18h Post 📝 « Acheter ses clubs en ligne… »
- Jeu 20 · 10h Story 📝 « Driver »
- Ven 21 · 10h Story 📝 « Réserve ton fitting » · 18h Post 📝 « Trois réglages du driver »
- Sam 22 · 10h Story 📝 « La data parle »
- Dim 23 · 10h Story 📝 « Jour de parcours »

Dossier Validation hebdo (permanent) : https://drive.google.com/drive/folders/1Q8KPPL1S2mrJ6afLObZoD3sokPULdcNG

## La Galerie Immobilière — 2 / 9 publiés

- Lun 17 · 10h Story 📝 « Belle semaine »
- Mar 18 · 10h Story 📝 « La lumière »
- Mer 19 · 10h Story 📝 « Charme de l'ancien » · 18h Post ✅ « Un bien devenu vacant… »
- Jeu 20 · 10h Story 📝 « Votre projet »
- Ven 21 · 10h Story 📝 « Week-end de visites » · 12h30 Post 📝 « Les questions qu'on nous pose »
- Sam 22 · 10h49 Story ✅ « Le bien rare » (hors créneau standard 10h00 — à vérifier)
- Dim 23 · 10h Story 📝 « Inspiration »

Dossier Validation hebdo (permanent) : https://drive.google.com/drive/folders/1B8WXZ0X1dYCtuzxQ3m8wmUOPFn34YrLO

## Pierre Huiban — 3 / 9 publiés

- Lun 17 · 6h Story 📝 « Lundi. On repart. LFG »
- Mar 18 · 6h Story 📝 « Pas d'excuses »
- Mer 19 · 13h30 Story ✅ · 18h Post ✅ « Cinq erreurs qui te coûtent des minutes sur un Hyrox »
- Jeu 20 · 6h Story ✅
- Ven 21 · 6h Story 📝 « One more session »
- Sam 22 · 0h30 Post 📝 « Three goals for the end of 2026 » · 6h Story 📝 « Volume day »
- Dim 23 · 6h Story 📝 « Rest is training too »

Dossier Validation hebdo (permanent) : https://drive.google.com/drive/folders/1VGThaVWofkwv3sUqZQo-R0_sST5nvytB

## Bilan du circuit de validation client (`reviews/etat/`)

Vide pour les cinq comptes cette semaine — normal vu le point 2 ci-dessus : aucune décision
cliente n'a pu remonter (personne n'a reçu de lien, et l'écriture est bloquée côté Drive même
pour qui l'ouvrirait). Rien à intégrer côté ✏️ à corriger / ⛔ refusé / ⏳ en attente ce lundi ;
ce sera la matière du CR une fois les deux réglages du point 2 faits.

## Ce qui part ce lundi

Pour chacun des 5 comptes clients : un brouillon Gmail (destinataire vide — aucune adresse
confirmée) et un message WhatsApp prêt (lien sans numéro — aucun numéro confirmé) dans
`recaps/whatsapp-semaine-2026-08-24.md`. **Rien n'est envoyé automatiquement** : conforme à la
règle « ne jamais envoyer automatiquement » (seule exception actuelle, le mail de review du
lundi matin pour Otea Filmakers → Maxime lui-même). Maxime relit, complète le destinataire une
fois confirmé, et envoie.

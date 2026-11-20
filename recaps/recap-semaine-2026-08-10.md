# 📅 Semaine du lundi 10/08 au dimanche 16/08 — récap des publications

*Récap hebdo interne · 6 fichiers de review générés le 10/08/2026 à 08h13 UTC · source :
`reviews/a-envoyer/*.xlsx` (le job `generer` de l'action « Review hebdo client »)*

## Vue d'ensemble

**42 brouillons** couverts par les fichiers de validation : 39 sur les 5 comptes clients
(28 stories + 11 publications au fil), 3 sur Otea Filmakers (banc d'essai interne).

| Compte | Lignes | Stories | Au fil | Carrousel 12/08 |
|---|---|---|---|---|
| Gossip Beauty Center | 2 | 0 ⚠️ | 2 | ✅ dans le fichier |
| Le Loft | 10 | 7 | 3 | ✅ dans le fichier |
| J Lawson Golf | 10 | 7 | 3 | ✅ dans le fichier |
| La Galerie Immobilière | 8 | 7 | 1 | ⚠️ absent du fichier |
| Pierre Huiban | 9 | 7 | 2 | ✅ dans le fichier |
| Otea Filmakers *(interne)* | 3 | 0 | 3 | — |

**Deux bonnes nouvelles par rapport au 03/08 :** aucun placeholder à compléter et aucune
publication sans média sur les 42 lignes. Les deux points qui bloquaient la semaine
dernière (le `[VAINQUEURE]` de J Lawson, le reel Sabrina sans média) ne se reposent pas.

## 🎯 À faire cette semaine

1. **Déposer les fichiers dans le Drive des clients — c'est le point bloquant.**
   `drive_fichier` est à `null` pour les 5 comptes clients dans `reviews/config.json` :
   aucun client ne peut valider quoi que ce soit, et la relève de 4h30 / 10h30 / 16h30 n'a
   rien à lire. Tant que ce n'est pas fait, **les 39 brouillons ne partiront jamais**.
   Procédure : `.claude/skills/cm-metricool/references/review-hebdo.md`, étapes 2 à 4.

2. **Gossip Beauty Center : 0 story dans le fichier, contre 7 attendues.**
   La fiche client documente 35 stories planifiées du 28/07 au 31/08 à 10h00. Le fichier
   de review ne liste que les **brouillons** : si les stories de cette semaine n'y sont
   pas, c'est qu'elles ne sont plus en brouillon — validées en publication auto par Sarah,
   ou supprimées. À vérifier dans Metricool avant d'envoyer le compte rendu : le mail
   annonce « vos stories quotidiennes continuent », il faut que ce soit vrai.

3. **La Galerie Immobilière : le carrousel du 12/08 n'est pas dans le fichier.**
   Le journal de l'action « Carrousels hebdo » de ce matin (07h39 UTC) dit
   `la-galerie-immobiliere 2026-08-12T18:00:00 — déjà planifié, ignoré` : le carrousel
   **existe bien** dans Metricool sur ce créneau. Comme il n'apparaît pas dans le fichier
   des brouillons, il n'est plus en brouillon — donc déjà en publication automatique. Il
   partira mercredi 18h sans passer par la validation de Sabrina. À confirmer dans
   Metricool ; c'est le compte au forfait maximum, où le carrousel **s'ajoute** au post du
   vendredi au lieu de le remplacer.

4. **Pierre Huiban — le post du samedi 15/08 à 0h30 dit « Swipez → » mais n'a qu'un seul
   visuel.** La fiche client le note déjà : les posts « Swipez » sont des carrousels dont
   seule la photo de couverture a été attachée. Publier une invitation à faire défiler sur
   une image unique se voit. Soit les slides sont designées d'ici samedi, soit le texte
   perd son « Swipez → ».

## Gossip Beauty Center — 2 au fil (0 story)

- Mer 12 · 18:00 · **Carrousel (8 visuels)** · IG+FB · « Le rituel hammam, étape par
  étape » — les 5 temps dans l'ordre, rappel institut exclusivement féminin, CTA message
  privé
- Ven 14 · 18:00 · POST · IG+FB · « Venez à deux » — duo mère-fille / sœurs / amies,
  hammam + massage, CTA lien en bio

*Voir le point 2 : les 7 stories de 10h00 attendues cette semaine sont absentes du fichier.*

## Le Loft — 7 stories + 3 au fil

- Lun 10 · 10:00 STORY « Nouvelle semaine » · 18:00 POST « Head Spa d'après-été » (cuir
  chevelu : soleil, sel, transpiration)
- Mar 11 · 10:00 STORY « Head spa »
- Mer 12 · 10:00 STORY « Barbe parfaite » · 18:00 **CARROUSEL** « 5 erreurs qui flinguent
  ta barbe » (A2)
- Jeu 13 · 10:00 STORY « Rasage à l'ancienne » — *la story du jeudi est bien là cette
  semaine, celle du 06/08 manquait*
- Ven 14 · 10:00 STORY « Week-end ready » · 18:00 POST « Formule VIP » (la veille du
  15 août)
- Sam 15 · 10:00 STORY « Ouvert 7j/7 »
- Dim 16 · 10:00 STORY « Même le dimanche »

*Le post VIP cite le détail de la formule (beauté des pieds, manucure, soin visage, 45 min
de head spa, 1h30). Tarifs Planity vérifiés juillet 2026 — à faire reconfirmer par le
gérant, c'est demandé dans le mail.*

## J Lawson Golf — 7 stories + 3 au fil

- Lun 10 · 10:00 STORY « Objectif semaine » · 18:00 POST « Playoffs FedEx Cup » (les pros
  re-testent leur matériel)
- Mar 11 · 10:00 STORY « Wedges »
- Mer 12 · 10:00 STORY « Putter » · 18:00 **CARROUSEL** « Par quel fitting commencer »
  (A5, 4 cas de figure)
- Jeu 13 · 10:00 STORY « Analyse Gears »
- Ven 14 · 10:00 STORY « Dernier call » · 18:00 POST « Dispersion divisée par deux »
- Sam 15 · 10:00 STORY « Côté atelier »
- Dim 16 · 10:00 STORY « 18 trous »

*Aucune marque de matériel citée, aucun placeholder cette semaine. Relecture du déroulé
technique du carrousel demandée à John dans le mail.*

## La Galerie Immobilière — 7 stories + 1 au fil (+ le carrousel hors fichier)

- Lun 10 · 10:00 STORY « Nouvelle semaine »
- Mar 11 · 10:00 STORY « Mise en valeur »
- Mer 12 · 10:00 STORY « L'adresse » · 18:00 **CARROUSEL** « Cinq erreurs qui coûtent des
  semaines » (A2) — ⚠️ *hors fichier de validation, voir le point 3*
- Jeu 13 · 10:00 STORY « L'estimation »
- Ven 14 · 10:00 STORY « Avant de visiter » · 12:30 POST « Le prix au m² à Puteaux cet
  été » (A6 sourcé)
- Sam 15 · 10:00 STORY « Paris & Ouest »
- Dim 16 · 10:00 STORY « Douceur du dimanche »

*Le post du vendredi est le seul contenu chiffré de la semaine : ~7 376 €/m², fourchette
5 262 → 9 664 €, écart entre baromètres 7 163 → 7 633 €. Quatre baromètres relevés en
juillet 2026, cités en fin de post. Aucun honoraire, aucun taux — conforme à la fiche.*

## Pierre Huiban — 7 stories + 2 au fil

- Lun 10 · 06:00 STORY « Lundi. On repart. LFG »
- Mar 11 · 06:00 STORY « Pas d'excuses »
- Mer 12 · 06:00 STORY « La donnée parle » · 18:00 **CARROUSEL** « Une semaine type de
  prépa Hyrox »
- Jeu 13 · 06:00 STORY « Ça brûle ? »
- Ven 14 · 06:00 STORY « Encore une séance »
- Sam 15 · 00:30 POST « 3 raisons d'avoir un coach » ⚠️ *« Swipez → » sur un seul visuel,
  voir le point 4* · 06:00 STORY « Samedi = volume »
- Dim 16 · 06:00 STORY « Récup »

## Otea Filmakers — 3 au fil (banc d'essai interne)

- Lun 10 · 18:00 POST · IG+TikTok · « Le plan dont je suis le plus fier »
- Mer 12 · 18:00 POST · IG+TikTok · « Pourquoi je voyage pour filmer »
- Ven 14 · 18:00 POST · IG+TikTok · « Ma routine avant de tourner »

*Seul compte dont le `drive_fichier` est renseigné. C'est le parcours client complet en
conditions réelles — les décisions posées dans ce Sheet valident (ou non) toute la chaîne.*

## ⚠️ Points d'attention

- **Aucune décision client n'a encore jamais été appliquée.** `reviews/etat/` n'existe pas
  et la relève de ce matin (05h55 UTC) conclut « Aucune décision nouvelle — rien à
  commiter ». Il n'y a donc rien à redescendre de la semaine passée : ni publié, ni
  ✏️ à retravailler, ni ⛔ à retirer. Le circuit n'a pas encore tourné une seule fois de
  bout en bout, y compris sur Otea Filmakers.
- **Les fichiers envoyés aux clients étiquettent les stories « Post ».** Dans la colonne
  Format, les 28 lignes de story portent `Post` : `type_du()` (`scripts/review.py:93`)
  retombe sur sa valeur par défaut quand l'API ne renvoie pas de `type` dans
  `instagramData`. Le client lit « Post » pour ce qui part en story, et la colonne Légende
  lui montre le libellé interne (« Story lundi (B) — Objectif semaine ») au lieu d'une
  vraie légende. À corriger dans le script — en attendant, les comptes rendus ci-joints
  rétablissent le bon format.
- **Les stories de tous les comptes s'arrêtent au 31/08.** Signalé la semaine dernière,
  toujours ouvert : il reste 3 semaines. La reconduction de septembre (~15 min en bulk)
  devient l'échéance de la semaine prochaine.
- Aucun doublon détecté, un seul contenu par créneau sur les 6 comptes.

**Les comptes rendus clients sont prêts :** `recaps/email-semaine-2026-08-10.md` (mail) et
`recaps/whatsapp-semaine-2026-08-10.md` (liens WhatsApp pré-remplis). Aucun envoi
automatique, aucune adresse ni aucun numéro confirmé à ce jour.

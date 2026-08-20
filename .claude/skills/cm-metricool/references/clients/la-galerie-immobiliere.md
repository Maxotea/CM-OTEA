# La Galerie Immobilière — fiche client

## Profil (vérifié web juillet 2026 — lagalerieimmobiliere.com, IG @lagalerieimmobiliere)
- Positionnement : **« L'art de l'immobilier à Paris & Île-de-France »** — agence de prestige. Secteur : Paris 16e, Puteaux (92), Hauts-de-Seine. Services : transaction, location, gestion.
- Fondatrice : **Sabrina**, 15+ ans d'expérience, formée en immobilier **et architecture d'intérieur** → angle déco/mise en valeur des biens à exploiter dans le contenu.
- blogId : 5733302 · Instagram / Facebook / TikTok (@lagalerieimmobiliere). ~7,6k abonnés IG.
- Typologie ROI : très forte valeur unitaire — 1 mandat/vente signé via les réseaux couvre généralement plusieurs mois voire l'année de prestation CM. Raisonner en nombre de mandats, pas en tickets.
- Prestation CM mensuelle : [à renseigner]
- Barème honoraires : [à vérifier sur le site / auprès du client]

## Piliers de contenu (à valider avec le client)
- P1 pédagogie : conseils achat/vente/estimation, home staging (fort de l'expertise archi d'intérieur de Sabrina)
- P2 actu secteur : marché parisien, taux, tendances Île-de-France (toujours vérifier par recherche web)
- P3 coulisses : visites, mise en valeur des biens, l'agence
- P4 saisonnier : rentrée (pic d'achats), printemps
- P5 preuve sociale : biens vendus, avis clients, témoignages

## Visuels IA (Higgsfield)
- **Élément de référence : `LaGalerie-Studio`** (id `507d65bd-fc06-43c9-a9ff-60fa2f9680e6`, catégorie environment). DA : immobilier de prestige parisien — haussmannien (parquet point de Hongrie, moulures, cheminées marbre), matières nobles (laiton, marbre clair, velours taupe), lumière naturelle douce et chaude, tons beige/taupe/doré/vert sauge, plantes, sensibilité architecture d'intérieur. Rendu photo éditorial magazine. **Jamais de personne.** Réutiliser `<<<507d65bd-fc06-43c9-a9ff-60fa2f9680e6>>>` dans le prompt pour garder le style.
- Banque IA locale : `medias/la-galerie-immobiliere/ia/` — 6 visuels : salon-haussmannien (savoir-faire déco), cles-contrat-sanstexte (transaction, porte-clés vierge, espace texte en haut), facade-haussmann (coucher de soleil), cuisine-parisienne (îlot marbre, vue haussmann), terrasse-paris (toits + Tour Eiffel), bureau-estimation (maquette + plans, pilier expertise).
- Les images IA ont une URL publique cloudfront → **attachables directement au `schedule_post` via `media01`** (post planifié complet, sans ajout manuel), contrairement aux photos réelles de biens. ⚠️ Bug fuseau : `schedule_post` décale l'heure (+7h) → corriger avec `bulk_update_post_times` (conserve le draft), puis supprimer l'ancien brouillon sans média. Pour attacher à un brouillon existant : recréer le post avec `media01`=URL + supprimer l'ancien (l'action `upload_image_attach_post` exige du base64, impraticable).
- **6 posts branchés le 21/07/2026** (POST feed, pédagogie/marché/marque, jamais reels/équipe) : 18/09 façade « Où investir autour de Puteaux », 25/09 salon « Vendeur 7 erreurs », 02/10 clés « De la 1re visite à la signature », 09/10 bureau « 5 mythes estimation », 23/10 cuisine « Que regarder pendant une visite », 30/10 terrasse « Acheteur avantages fin d'année ». Tous en brouillon, à valider dans Metricool.
- ⚠️ Nuance importante immobilier : ces visuels IA sont génériques (ambiance/DA), ils ne représentent PAS de vrais biens à vendre. À réserver aux posts pédagogie/actu/marque. Pour présenter un bien réel, toujours de vraies photos.

## Stories — rotation 2 semaines, vidéo + fond sonore (03/08/2026) ✅ ACTIF
- **Règle Maxime (03/08) : aucune story identique sur 2 semaines consécutives.** Rotation de **14 cartes distinctes** en cycle A/B (A = semaines des 03, 17, 31/08 ; B = 10, 24/08). Semaine A = les 7 thèmes historiques (continuité), semaine B = 7 nouveaux (mise en valeur, l'adresse, l'estimation, avant de visiter, Paris & Ouest…).
- **28 stories VIDÉO planifiées ✅ 04→31/08 à 10:00** (ids 357219429→357220330), IG+FB, brouillon. L'ancienne rotation hebdo de 7 visuels IA (28 brouillons) a été supprimée — la suppression a renvoyé « Code execution error » mais a bien abouti (vérifié par listing, piège connu). Story du 03/08 (ancienne) laissée en place. **Contenus « Sabrina » (18h) et posts feed (12h30) non touchés.**
- **Format : cartes typographiques ANIMÉES 7,5 s avec fond musical** — cartes PIL pures (zéro IA, zéro photo, DA crème/doré/serif prestige), musique en **synthèse procédurale** (`scripts/fond-sonore-stories.py` : arpège feutré type piano, élégant — aucun sample tiers, aucun modèle génératif, zéro droits). Assemblage ffmpeg image+audio.
- Source de vérité : `assets/stories/manifest-stories-2sem.json`. Cartes : `assets/stories/la-galerie-immobiliere/`. Reconduction septembre : replanifier les mêmes 14 vidéos (URLs cloudfront réutilisables) en respectant le cycle A/B.

## Stories quotidiennes août 2026 (28/07/2026 — REMPLACÉE le 03/08)
- Banque 7 stories 9:16 `medias/la-galerie-immobiliere/ia/stories/` (lun belle-semaine, mar lumière, mer charme-ancien, jeu votre-projet, ven week-end-visites, sam bien-rare, dim inspiration). Visuels IA, rotation hebdo — abandonnée au profit de la rotation 2 semaines ci-dessus.
- ⚠️ **10 stories « Sabrina » sans média** (28/07→29/09, 18h, hebdo — ids 326979151/160/173/175/177, 326980004/005/007/011/020) : contenus face-cam du calendrier initial (adresses de Sabrina, anecdote terrain, équipe, marché immo…). **NE PAS brancher en IA** (personne réelle) ni supprimer : à TOURNER avec Sabrina (vidéos verticales), puis héberger via [[hebergement-photos-reelles-metricool]]. Sans danger en attendant : elles sont en brouillon.

## 🔇 Stories muettes — 19/08/2026
Les 13 stories vidéo du 19 au 31/08 portaient le fond sonore `lg.wav`. Elles ont
été redéposées **muettes** (`ffmpeg -an -c copy`, aucun ré-encodage : l'image est
strictement identique), en brouillon IG+FB à 10:00, aux mêmes dates.

| Date | Libellé | Nouveau média (muet) | Nouvel id |
|---|---|---|---|
| 19/08 | Story mercredi (A) — Charme de l'ancien | `b9a05073-4b2d-4a6a-9144-5eecfddf99c0` | 363859179 |
| 20/08 | Story jeudi (A) — Votre projet | `f900db6b-fd28-455e-9b89-0f03c11f69b0` | 363859185 |
| 21/08 | Story vendredi (A) — Week-end de visites | `93487272-2385-4924-8c46-ea0161fce385` | 363859189 |
| 22/08 | Story samedi (A) — Le bien rare | `83cbee6d-a5f4-4a6e-9955-928078530c98` | 363859196 |
| 23/08 | Story dimanche (A) — Inspiration | `202cc2ed-d8cb-48f3-ae59-cb88d4a5244f` | 363859200 |
| 24/08 | Story lundi (B) — Nouvelle semaine | `93a618a4-d892-4bb5-9182-38f22c66ab67` | 363859204 |
| 25/08 | Story mardi (B) — Mise en valeur | `01b9a000-e435-44e3-9483-46b3843c4b48` | 363859208 |
| 26/08 | Story mercredi (B) — L'adresse | `9f221602-ac01-4079-9164-7bf467cf7f13` | 363859313 |
| 27/08 | Story jeudi (B) — L'estimation | `baae616a-3f15-4979-8c36-21ebe7a27960` | 363859319 |
| 28/08 | Story vendredi (B) — Avant de visiter | `3c78c8c1-2fd1-4bbd-8818-f9bdb182d7b8` | 363859326 |
| 29/08 | Story samedi (B) — Paris & Ouest | `8d5175ed-09ba-409c-9723-2535550a4178` | 363859333 |
| 30/08 | Story dimanche (B) — Douceur du dimanche | `19abe707-62fb-44f5-8b68-a8b731ed5b70` | 363859340 |
| 31/08 | Story lundi (A) — Belle semaine | `38e3a858-4c48-4be8-9114-b0691b409dbc` | 363859343 |

Anciennes cartes sonores supprimées : 357220114, …123, …132, …138, …146, …154,
…168, …174, …179, 357220313, …317, …322, …330. Les stories de septembre sont des
PNG : pas de son, rien à faire. Règle : `.claude/memories/stories-sans-son.md`.

## 🔴 RETOUR CLIENT 19/08/2026 — couleurs et format des stories

Deux reproches, tous les deux fondés.

### 1. « Les stories ne sont pas à leur couleur »
Contrôle du rendu : le fond dominant des cartes est **crème/beige** (#ECE4D7,
#EFE7DC, #F3EDE4 relevés sur une frame). Cette palette ne vient **pas** de leur
charte : elle vient de l'élément IA `LaGalerie-Studio` que j'ai créé
(« beige/taupe/doré/vert sauge »), lui-même déduit du positionnement prestige.

⚠️ **La charte réelle de l'agence n'a jamais été relevée.** Cette fiche ne
contient aucun code couleur de marque, aucune police officielle — uniquement une
DA inventée. Le site `lagalerieimmobiliere.com` est bloqué par le proxy réseau,
je n'ai pas pu la vérifier depuis l'environnement.

**À obtenir de Sabrina avant toute reprise :** codes couleurs, police(s), logo
en fichier vectoriel. Tant qu'on ne les a pas, on continuera à côté.

### 2. « Ce n'est pas comme les autres comptes, c'est juste du texte »
Exact, et c'était documenté comme un pis-aller : format « cartes typographiques
ANIMÉES », c'est-à-dire une vidéo dont le seul contenu est du texte sur aplat.
La fiche justifiait ça par « 0 vraie photo disponible ».

Sauf que le compte a **6 visuels IA d'ambiance** dans sa banque
(salon haussmannien, façade, cuisine, terrasse, bureau, clés) — utilisés en feed,
jamais en story. Même sans photo de bien réel, on pouvait faire beaucoup mieux
que du texte sur fond crème.

### Ce qu'il faut refaire
1. Récupérer la charte réelle (bloquant).
2. Repasser les stories sur un fond visuel — visuels d'ambiance existants en
   attendant, vraies photos de biens dès que Sabrina en fournit.
3. Tourner enfin les 10 stories « Sabrina » face-cam en attente depuis le 28/07 :
   c'est le contenu qui différencierait vraiment ce compte.

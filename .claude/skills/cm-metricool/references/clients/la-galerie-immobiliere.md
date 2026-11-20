# La Galerie Immobilière — fiche client

> ## ⛔ COMPTE DÉSACTIVÉ · 21/10/2026
>
> Maxime a mis fin à la collaboration le 21/10/2026 (« on ne travaille plus ensemble »). **Ne plus produire de contenu, ne plus programmer, ne plus brancher de média, ne plus générer de tableau de validation ni de compte rendu client.** Le compte est sorti de la relève (`reviews/config.json`, `actif: false`), du récap du lundi et de la détection de nouveaux médias (`recaps/clients-config.json`, `actif: false`).
>
> **Ce qui restait dans Metricool au 21/10/2026 :** 59 contenus du 21/10 au 06/12, dont 47 stories et 12 posts ou reels (10 sans média). **Tous en brouillon, aucun en publication automatique** : rien ne partira tout seul. Ces brouillons n'ont pas été supprimés : la suppression est irréversible et Maxime ne l'a pas demandée.
>
> La fiche ci-dessous est conservée telle quelle, au cas où le compte reviendrait.

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

## 🎨 CHARTE RELEVÉE le 19/08/2026 (source : leurs propres publications)
Le site étant bloqué par le proxy, la charte a été relevée sur les visuels
**qu'ils ont publiés eux-mêmes** avant notre prise en charge — gabarit de série
« 5 choses à savoir sur… » (post 326876565, 21/05/2026, carrousel 8 slides).

| Rôle | Valeur | Note |
|---|---|---|
| Fond de marque | **#D4BBA5** | Sable chaud / taupe rosé. 55 % des pixels sur l'ensemble du carrousel. C'est LA couleur du compte. |
| Texte | **#292527** | Charbon chaud, presque noir. |
| Nuance claire | #DCC8B4 | Variante du fond. |
| Nuance sombre | #B2997C | Sable foncé, ombres et filets. |

**Typographie :** un serif à fort contraste pour les titres (type Playfair
Display), en bas-de-casse — pas de capitales.

**Signature visuelle, c'est le point important :** des **illustrations dessinées
à la main**, trait noir fin — note de musique, pelote, clés, maison, flèches,
points de suite. C'est ce qui donne au compte son côté chaleureux et humain.
Plus une **photo détourée** de la personne, posée en bas de la carte.

### Écart avec ce qu'on produisait
| | Eux | Nous |
|---|---|---|
| Fond | #D4BBA5 sable chaud | #ECE4D7 crème pâle — **trop clair, trop froid** |
| Titres | serif bas-de-casse | serif capitales |
| Illustration | doodles au trait, omniprésents | **aucune** |
| Photo | portrait détouré | aucune |
| Registre | chaleureux, humain, un peu joueur | prestige austère |

J'avais construit une DA « immobilier de prestige » déduite de leur
positionnement (« L'art de l'immobilier »). Leur identité réelle est beaucoup
plus chaleureuse et illustrée. D'où les deux reproches d'un coup : la couleur
**et** le fait que ce ne soit « que du texte » — chez eux, il y a toujours un
dessin ou une photo.

⚠️ Reste à confirmer auprès de Sabrina : les codes exacts (relevés à l'écran, donc
approchés à un ou deux points près) et le nom de la police.

---

## ✅ STORIES REFAITES À LEUR CHARTE — 20/08/2026 (décision Maxime)

Maxime a tranché le 20/08 : *« Je déduis depuis leur Instagram »* — on relève les
couleurs dominantes de leurs publications existantes et on s'aligne dessus,
plutôt que d'attendre une charte de Sabrina. C'est fait, sur les **21 stories**
programmées du 20/08 au 29/09.

### Ce qui a changé sur chaque carte
| | Avant | Après |
|---|---|---|
| Fond | #ECE4D7 crème pâle | **#D4BBA5** sable chaud (le leur) |
| Titre | serif **capitales** | serif Playfair Display **bas-de-casse**, #292527 |
| Filet | trait droit vectoriel | **filet tracé à main levée** |
| Illustration | aucune | **un doodle au trait** par carte (loupe, maison, spirale, clé, pelote…) |
| Pied | absent | `puteaux · paris ouest` |

Les deux reproches de Sabrina étaient liés : la couleur *et* « ce n'est que du
texte ». Le doodle répond au second. Le format reste une **carte fixe** — pas de
vidéo : la règle « aucune image ni vidéo générée par IA dans les stories » tient,
et les 6 visuels d'ambiance IA du compte n'ont donc **pas** été recyclés ici.

### Les 20 cartes (CDN Higgsfield, `…/user_2zae6klRfE97hlBWhyQP6j7d9cR/<id>.png`)
`projet bfef88b4` · `visites 79a26fd1` · `rare 4d5030b5` · `inspiration 0debc35c` ·
`semaine 51c945c6` · `valeur 4a1b1929` · `adresse beff1dd5` · `estimation 59f00560` ·
`avant daa0ac7b` · `ouest a8b43cac` · `douceur 3fd963ca` · `belle 06dc0b0b` ·
`rentree aed6ecc0` · `taux 8e2f35d6` · `ancien afdbb47d` · `dpe bd21ffb9` ·
`patrimoine 345199d7` · `gratuite 85048480` · `reperage 336d7ee1` · `fetes e6df5bdf`

La carte `visites` sert deux fois (21/08 et 05/09), d'où 20 cartes pour 21 stories.

Générateur : `lg.py`, hébergé à
`https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/7abe8946-e8eb-49aa-9ea4-b29394ff8ecd.py`
(`python3 lg.py <clé…>` → `o/lg-<clé>.png`).

### 🚨 18 posts en autoPublish sans média — neutralisés
Le compte portait **18 publications `autoPublish:true` avec `hasMedia:false`** :
14 REELs et 4 posts, du 25/08 au 27/11. Elles étaient en brouillon, donc rien ne
serait parti tout de suite — mais le jour où Sabrina ou Maxime décoche « brouillon »,
elles publiaient une coquille vide. Toutes repassées à `autoPublish:false`.

Ces 18 slots attendent les **rushes de Sabrina** : ce sont les formats parlés
(visite filmée, témoignage client, bilan de marché). Rien à produire de notre côté
tant que la vidéo n'est pas là.

Nouvelle code action créée pour ça : **`bulk_set_autopublish`**
(params `blog_id`, `post_ids` JSON, `auto_publish`). Elle force aussi `draft:true`
au passage. Comme toutes les écritures Metricool, un PUT réussi renvoie le post
sous un **nouvel id**.

### Vérification finale (20/08/2026)
`60 publications · 21 stories · 25 posts · 14 REELs · draft:true partout ·
autoPublish:false partout · aucun créneau en double · noMedia 18 = les 18 slots
vidéo en attente de rushes`

⚠️ **Leçon de méthode :** la première vérification portait sur 20/08 → 31/10 et
concluait « 10 posts en autoPublish ». En élargissant à 31/12 on en trouvait
**8 de plus** en novembre. Toujours vérifier jusqu'au bout du calendrier, pas
jusqu'au bout de la vague qu'on traite.

### Ce qui reste ouvert
- Faire valider les **codes couleur** par Sabrina : ils sont relevés à l'écran,
  donc justes à un ou deux points près, et le nom exact de la police n'est pas
  confirmé (Playfair Display est une approximation très proche).
- 3 posts portent encore un placeholder (`[Prénom]`, témoignage à recueillir).

---

## 🎬 STORIES EN VIDÉO PLEIN CADRE — 21/08/2026

Sabrina disait deux choses le 19/08 : « les storys ne sont pas à leur couleur »
**et** « ce n'est pas comme les autres comptes avec des vidéos et juste un
texte ». La couleur a été réglée le 20/08. Le format a demandé **trois
versions** dans la journée du 21/08, et les deux premières étaient ratées.

### Ce qui n'allait pas, mesuré

| | Run On Invest | v1 `zoompan` | v2 fenêtre 16:9 | **v3 plein cadre** |
|---|---|---|---|---|
| lignes de l'image qui bougent | 100 % | 24 % | 24 % | **68 %** |
| mouvement moyen sur la story | 18,2 | 1,0 | 1,0 | **2,5** |
| surface occupée par la vidéo | plein cadre | 24 % | 24 % | **60 %, pleine largeur** |

- **v1** animait la photo au `zoompan` ffmpeg. Maxime avait **déjà refusé ce
  procédé le 01/08** (« pas des images animées mais juste des zooms »).
- **v2** passait en vrai i2v mais logeait la vidéo dans une fenêtre de 940×529
  sur une carte de texte : une vignette qui frémit, pas une vidéo. En prime le
  modèle sortait du 1176×784 (3:2) forcé dans du 16:9, donc **l'image était
  étirée de 18 %**.
- **v3** est la bonne : la vidéo occupe toute la largeur sur les 60 % du haut,
  le texte est posé en bas sur un voile sable dégradé.

### La méthode, et le piège à ne jamais refaire

⛔ **Ne jamais lancer l'i2v en 9:16 depuis une photo paysage.** Testé et
mesuré : le modèle **réinvente la pièce**. Écart de 58,8 contre la vraie photo,
et aucun recadrage de l'original ne correspond. C'est exactement ce que William
du Loft a reproché le même jour (« des photos qui ne sont pas prises chez moi »).

✅ **Recadrer d'abord en 9:16 dans PIL, animer ensuite.** C'est ce que
prescrivait déjà `.claude/memories/stories-vraies-photos-sans-ia.md`, et que la
v2 avait court-circuité. Mesuré sur la même photo : **4,1** d'écart sur la
première image, **6,0** sur la dernière, contre 4,0 entre deux images d'une même
vidéo. C'est leur photo, elle bouge, rien n'est inventé.

Caméra verrouillée : ce sont la lumière, les rideaux et le feuillage derrière
les fenêtres qui bougent, pas le cadre. Une variante travelling avant a été
testée (mouvement 58, soit 3× Run On Invest) : **écartée par Maxime**, parce
qu'en avançant le modèle extrapole ce que la photo ne montrait pas et que le
contrôle de dernière frame ne vaut plus rien.

### La composition
| | |
|---|---|
| Vidéo | vraie photo d'un de leurs biens, recadrée 9:16, animée en i2v, **plein cadre 1080×1920** |
| Voile | sable **#D4BBA5** en dégradé, transparent à y=1150, opaque à y=1330 |
| Titre | Playfair Display bas-de-casse **#292527**, y=1360 |
| Filet | tracé à main levée, leur signature graphique |
| Pied | `puteaux · paris ouest` |
| Son | **aucun**, règle `stories-sans-son.md` |

### La chaîne
1. `scripts/lg-crop-9-16.py <NN…>` relève la photo sur leur site et la recadre
   en 9:16 (864×1536), sans texte.
2. i2v `kling3_0_turbo`, `aspect_ratio: "9:16"`, 5 s, **7,5 crédits par plan**.
   Sortie native 720×1280. 19 plans générés le 21/08.
3. `scripts/lg-story-video.py <clé…>` récupère le plan, l'upscale en 1080×1920
   et incruste le calque texte. Le texte ne passe **jamais** dans le modèle.

### D'où viennent les photos
Des **mandats publiés sur leur propre site**
(`lagalerieimmobiliere.com/bien-immobilier/…`) : 30 photos relevées sur trois
annonces (Suresnes, Nanterre, Colombes). Leurs biens, leurs photos. Jamais de
banque d'images, jamais la photo d'un autre compte du portefeuille.

⚠️ La numérotation `01`..`30` dépend des annonces en ligne : si un bien est
vendu et retiré, l'ordre change et le mapping de `SPEC` ne pointe plus sur la
bonne photo. À revérifier à l'œil avant toute regénération.

### ⚠️ Le piège des accents
La v2 avait été produite avec des titres **sans accents** (« bonne rentree »,
« presente », « des le premier jour »). Sur ce compte précisément, qui reproche
déjà un manque de soin, c'était inacceptable. Corrigé : Playfair Display et
Space Mono couvrent tout le français, point médian du pied compris, vérifié
glyphe par glyphe (`ImageFont.getmask(c).getbbox()`). Ne jamais saisir un texte
client sans accents « pour éviter un problème d'encodage » : héberger le script
en gzip+base64 et le décoder dans la sandbox règle le problème sans toucher au
texte.

### Vérification (21/08/2026)
`59 publications · 20 stories toutes en vidéo plein cadre · draft:true partout ·
autoPublish:false partout · noMedia 18 = les slots REEL en attente des rushes
de Sabrina`

La carte `projet` du 20/08 n'a pas été utilisée : cette story était déjà passée
quand la vague vidéo a été produite.


---

## 🔁 RETOUR EN ARRIÈRE DU CALENDRIER — 24/08/2026

Maxime : « tu avais fait de superbes stories en réutilisant les photos de biens
immobiliers, refais la même chose, car là ça ne fonctionne plus du tout et je ne
comprends pas pourquoi ».

### Ce que le calendrier contenait vraiment

Quatorze stories du 24 au 30/08, deux par jour (10h et 16h), qui n'étaient pas
celles produites le 21/08. Inspection des médias branchés :

| Créneau | Ce qui était branché | Problème |
|---|---|---|
| 10h | carte **typographique grise**, titre en capitales centrées, aucune photo | c'est exactement le reproche de Sabrina du 19/08 (« juste un texte »), et ce n'est pas leur sable |
| 16h | **photo de banque d'images** (les libellés disent « banque · agence », « banque · cuisine »), **928×1152** | ce n'est pas un de leurs biens, et le format n'est pas 9:16 : la story serait rognée ou bandée |

Les cinq stories du 31/08 au 12/09 produites le 21/08 étaient intactes et au bon
format : la régression ne portait que sur la semaine du 24 au 30.

### Ce qui a été refait

Les 14 créneaux sont rebranchés sur le format validé : **vraie photo d'un de
leurs biens, recadrée 9:16, animée en i2v, plein cadre, voile sable en bas avec
le titre**. La ligne éditoriale des libellés existants a été conservée, seul le
visuel change.

**Zéro crédit dépensé** : les 19 plans i2v du 21/08 sont réutilisés. Quatorze
photos distinctes, aucune ne repasse deux fois sur les trois semaines, et aucune
ne double les cinq déjà en ligne du 31/08 au 12/09.

Les clés sont `n24a`…`n30b` dans `scripts/lg-story-video.py`.

### ⚠️ Une publication partait toute seule
L'audit a remonté le post **365814170** du 25/08 à 18h (Facebook) en
`draft:false` / `autoPublish:true`. Neutralisé le 24/08. **Toujours relancer
`audit_publication_safety` après une intervention d'un autre outil sur le
calendrier** : ce post n'existait pas au passage du 21/08.

### Vérification (24/08/2026)
`62 publications · 62 en brouillon · 0 en autoPublish · noMedia 17 = les slots
REEL en attente des rushes de Sabrina`


---

## ✅ PROCESS VALIDÉ — 28/08/2026

Maxime : « c'est parfait pour la galerie immobilière, garder ce process ».

Le format story de ce compte est **figé** : vraie photo d'un de leurs biens,
recadrée 9:16 dans PIL, animée en i2v caméra verrouillée, **plein cadre
1080×1920**, voile sable dégradé en bas avec le titre en Playfair Display, pied
`puteaux · paris ouest`, **muette**, branchée en brouillon puis auditée. Ne pas
proposer autre chose sans qu'il le demande.

La chaîne réutilisable, avec ses trois pièges mesurés et les pièges d'outillage
Metricool, est écrite dans `.claude/memories/story-video-plein-cadre.md` pour
qu'elle s'applique par défaut sur tous les comptes, pas seulement ici.

Un détail corrigé au passage : l'index des mémoires annonçait encore « animer
les photos par mouvement de caméra ffmpeg, jamais d'i2v ». C'est cette ligne qui
avait produit la v1 en `zoompan` le 21/08. Elle dit maintenant l'inverse, qui
est la règle réelle depuis le 21/08.


---

## 📭 MAIL DE VALIDATION MANQUANT — 28/08/2026

Maxime : « je n'ai pas reçu le mail récap pour La Galerie, c'est normal ? »

Non, et il ne l'avait pas raté : **le brouillon n'a jamais été créé**. La
génération du vendredi 28/08 à 06h26 a produit cinq brouillons Gmail (J Lawson,
Le Loft, Pierre Huiban, Otea Filmakers, Gossip) et **aucun pour La Galerie**.

### La cause, vérifiée dans Drive
Le tableau de validation de La Galerie pour la semaine du 31/08 **existait déjà**
depuis le **mardi 25/08 à 15h02**, créé par une exécution antérieure. Les six
autres tableaux, eux, datent tous du 28/08 au matin. La génération du 28/08 a
donc trouvé le tableau en place et sauté le compte, mail compris.

**L'idempotence est calée sur l'existence du tableau, pas sur celle du
brouillon.** Un tableau produit hors du cycle habituel fait donc disparaître le
mail sans aucune erreur visible. À corriger dans le générateur : vérifier le
brouillon séparément du tableau.

### Ce qui a été fait
Le tableau était complet et exploitable (6 publications, LGI-01 à LGI-06, du
31/08 au 05/09). Le brouillon manquant a été recréé à la main, à Sabrina avec
Rémi en copie, sur le même modèle que les cinq autres.

Tableau : https://docs.google.com/spreadsheets/d/1UFOJ-xNx8r-_7NXovCXpPHBzZ5iz2MiaSdgHK-J0RzU/edit
Dossier : https://drive.google.com/drive/folders/1B8WXZ0X1dYCtuzxQ3m8wmUOPFn34YrLO

⚠️ **Le générateur de tableaux ne lit pas `recaps/clients-config.json`.** Gossip
a reçu son tableau et son brouillon le 28/08 au matin alors que le compte devait
être désactivé. La désactivation posée dans ce dépôt ne couvre donc que la tâche
du lundi, pas ce système. À propager.


---

## 🔁 VAGUE RELOOKÉE — 28/08/2026

Maxime : « rajouter le logo, et que le texte soit plus visible ».

### Ce qui change dans l'habillage
| | Avant | Après |
|---|---|---|
| Logo | absent | médaillon rond en haut au centre, 168 px, cerclé de sable |
| Voile sable | démarre à y=1150, alpha 245 | démarre à **y=980**, **alpha 255** |
| Titre | 78 px | **96 px** |
| Sous-titre | 31 px | **38 px**, rétrécit seul plutôt que de mordre sur le pied |
| Pied | 23 px | 26 px |

Le contraste n'était pas en cause : le sable et l'encre sont à 7,7 pour 1. Le
problème était la taille et la place.

### Le logo
Relevé sur leur site. Deux versions existent : `rond-logo2.png`, disque beige à
lettrage blanc, et `rond-logo3.webp.png`, disque noir à lettrage blanc.
**C'est la version noire qui est utilisée** : la beige est du blanc sur beige,
luminance moyenne mesurée 192 contre 36, illisible en médaillon. Le liseré sable
autour n'est pas décoratif, sans lui le disque noir disparaît sur une photo
sombre.

### Les 15 stories refaites
Du 29/08 au 13/09, une photo différente par story, aucune répétition, **zéro
crédit** (les 19 plans i2v du 21/08 sont réutilisés). Clés `d2908b` à `d1309`
dans `scripts/lg-story-video.py`.

Les trois stories des 29 et 30/08 déjà validées par Maxime en publication
automatique **n'ont pas été touchées** : les modifier aurait effacé sa
validation.

### ⚠️ Neuf stories étaient reparties en photo de banque
Les créneaux des 02, 03, 04, 06, 07, 09, 10, 11 et 13/09 (identifiants
`3676891xx`) étaient branchés sur des **PNG fixes** dont les libellés portent la
mention « banque · … ». C'est le même symptôme que la régression du 24/08 :
quelque chose écrit sur ce calendrier entre deux passages, avec exactement les
visuels que Sabrina a reprochés le 19/08. Ces neuf créneaux sont maintenant en
vidéo plein cadre sur leurs biens.

### Vérification (28/08/2026)
`25 publications · 22 brouillons · 3 en publication automatique (les validations
de Maxime des 29 et 30/08) · 2 sans média = les deux REELs en attente des rushes
de Sabrina`

## 🔒 ZONE SÛRE INSTAGRAM — 31/08/2026

Reproche de Maxime : « on ne voit pas assez bien le logo, il est caché
derrière ». Ce n'était pas un problème de taille ni de contraste, mais de
position.

L'interface Instagram recouvre le haut et le bas d'une story : barre de
progression, avatar et nom du compte en haut, barre « Envoyer un message » en
bas. Sur un cadre 1080×1920, cela fait environ **250 px en haut et 250 px en
bas**. Le médaillon était posé à y=108, donc sous la barre de progression, et
le pied de page à y=1788, donc sous la barre de message. Les deux étaient
littéralement cachés derrière l'interface.

**Règle : rien d'important en dehors de la bande 250 → 1670.**

| | avant | après |
|---|---|---|
| médaillon | 108 → 276 (Ø 168) | **300 → 490** (Ø 190) |
| voile sable | 940 | 880 |
| titre | 1210 | 1150 |
| pied de page | 1788 | **1636 → 1666** |
| pire cas bas du sous-titre | 1667 | 1607 |

Les quinze vidéos de la vague 29/08 → 13/09 ont été refabriquées et
rebranchées avec cette mise en page.

**Puis le médaillon est passé en haut à droite** (demandé le 31/08). En x il
s'aligne sur la marge du texte, 90 px, et pas sur le bord : le bord droit est
là où le pouce se pose pour faire défiler, et le liseré sable se ferait rogner
à l'affichage. Position finale : **x 800 → 990, y 300 → 490**.

## ⚠️ RÉÉCRITURE EN AUTO-PUBLISH — 31/08/2026

Troisième occurrence du processus qui réécrit ce calendrier entre deux
sessions (24/08, puis 02 → 13/09, puis celle-ci). Cette fois c'est plus grave
que des photos de banque.

Trois posts ont été **créés le 31/08 à 09h39** sous le compte
`contact@oteaproduction.com`, en `draft:false` et `autoPublish:true` :

| id | date | ce que c'était |
|---|---|---|
| 368695206 | 31/08 10h00 | story, sans libellé, partait **21 minutes plus tard** |
| 368695464 | 02/09 10h00 | story « estimation en ligne vs sur place » |
| 368695384 | 02/09 18h00 | post carrousel estimation |

Ils remplaçaient mes brouillons 367901967 et 367901986, et pointaient sur les
vidéos de la vague précédente, celles au logo caché. Les trois ont été
repassés en brouillon avant l'heure de tir, puis les deux stories rebranchées
sur les nouvelles vidéos.

Cela viole la règle non négociable n°1 : tout contenu créé dans Metricool
reste en brouillon, Maxime valide lui-même dans l'interface. Tant que la
source de ces écritures n'est pas identifiée, **passer un
`audit_publication_safety` sur 5733302 au début de chaque session**.

## Carrousel hebdo (créneau du mercredi, 18h, Instagram + Facebook)
- **Typologie** : très forte valeur unitaire, décision longue → la preuve est la maîtrise du détail. **Cible** : propriétaire ou acquéreur sur Paris 16e / Puteaux / Hauts-de-Seine, qui engage un patrimoine et craint surtout de se tromper. Jargon économique toléré, jamais technique.
- **Archétypes prioritaires** : A2 (erreurs, le plus performant sur cette cible), A5 (arbitrage), A8 (saisonnier), A7 (coulisses de l'expertise). **A6 (décryptage chiffré : taux, prix au m², DPE) uniquement après recherche web datée et sourcée.**
- **DA carrousel** (`scripts/themes.json` → `la-galerie-immobiliere`) : fond beige #EFE9E1, texte taupe #2E2A26, accent doré #B08D57, **police sérif** (Didot, repli Georgia), titres en bas-de-casse. Cohérente avec `LaGalerie-Studio`.
- **Planifiés (spec dans `carrousels/la-galerie-immobiliere/`)** : 12/08 A2 « Cinq erreurs qui coûtent des semaines » · 19/08 A5 « Vendre ou louer » · 26/08 A8 « Préparer son bien avant septembre » (angle home staging, adossé à l'expertise archi d'intérieur de la fondatrice) · 02/09 A7 « Ce que l'on regarde avant d'estimer ».
- **Réserve de sujets** : DPE et réglementation (A6, **réglementation à vérifier par recherche web à la date de publication**) · « Acheter en fin d'année : ce qui change » (A8, novembre) · « Une visite réussie, du point de vue de l'acquéreur » (A5) · remise de clés commentée (A3, dès qu'un client accepte).
- **Cadence particulière — le compte ne publie pas le mercredi.** Ses posts feed sortent le **vendredi à 12h30**. Le carrousel du mercredi ne remplace donc rien ici : il **s'ajoute**. C'est assumé, le compte est au **forfait maximum** (confirmé par Maxime, 06/08/2026) — la règle « le carrousel remplace le post du mercredi » ne s'y applique pas.
- **Vigilance** : barème d'honoraires **non vérifié** → aucun honoraire cité. Aucun prix au m², aucun taux, aucun chiffre de marché sans source datée. Le prénom de la fondatrice n'apparaît pas encore dans les slides : à ajouter si elle le valide. Ne jamais illustrer un carrousel avec un visuel IA présenté comme un bien réel.

### Le vendredi 12h30 est un post feed SIMPLE (règle du 07/08/2026)

Une légende du vendredi ne doit **jamais** contenir « Swipez », « slides » ni « faites
défiler ». Le lot planifié en juillet 2026 portait des légendes écrites pour un carrousel
posées sur des posts à un seul média : à la lecture, le post promettait une suite qui
n'existait pas — c'est ce qui a fait dire à Maxime « on dirait qu'il manque une partie ».
Le moteur de carrousels n'existait pas encore à la date de ce lot. Même défaut relevé sur
la fiche de Pierre Huiban. Le carrousel, c'est le mercredi 18h, section ci-dessus.
`scripts/audit_posts.py` vérifie ce point.

## 🎬 VIDÉO D'ANNONCE, UN MANDAT = UN REEL (proposition du 02/09/2026)

Maxime a demandé de « proposer la même chose » que https://www.diane.estate/fr.
Diane n'est pas une agence mais un logiciel de vidéos d'annonces par IA
(narration, avatar, montage, 19 à 23 $ la vidéo). Transposition complète,
prix proposé, message à Sabrina et pilote à zéro crédit sur le bien VM383 :
`offre/video-annonce-la-galerie.md`.

- Script d'assemblage : `scripts/lg-video-annonce.py` (intro, plans i2v en
  fondu, texte incrusté, outro, musique, narration optionnelle, 9:16 et 16:9).
- Spec du pilote : `videos-annonces/la-galerie-immobiliere/pilote-vm383.json`,
  crochets à remplir depuis l'annonce, rien ne s'invente.
- Ce qu'on ne reprend pas de Diane : l'avatar (jamais de visage généré), la
  voix clonée, les vues drone inventées. Vraies photos, caméra verrouillée.
- Ce format sert les créneaux REEL qui attendent des rushes depuis le 20/08 :
  un reel qui ne demande rien à Sabrina.

### Premier rendu d'essai, 03/09/2026 (zéro crédit)
Vidéo : https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/00d39a03-d49b-4902-ad8f-f206e4cc84a4.mp4
32,5 s, 1080×1920, six plans i2v du bien VM383 (photos 11, 15, 18, 13, 12,
17), musique procédurale, texte incrusté, médaillon en haut à droite. Spec :
`videos-annonces/la-galerie-immobiliere/essai-vm383.json`. Rendu dans la
sandbox Higgsfield, vérifié frame par frame (photo pleine largeur en haut,
voile sable, texte, médaillon sur chaque plan). **Aucun fait sur le bien
n'est affiché**, ni ville ni « à vendre » : l'annonce n'a pas été relevée.
Ce n'est pas la version à montrer à Rémi, c'est la preuve que la chaîne
tourne. Reste : relever l'annonce, nommer les pièces, narration, brouillon
Metricool.

## 🖼️ CARROUSELS SUR FOND PHOTO — 02/09/2026

Demande de Maxime : « plutôt mettre des photos de beaux biens immobiliers
parisiens qu'un fond uni. le texte doit ressortir ».

### Ce que le texte fait pour ressortir

Le voile n'est pas choisi à l'œil, il est calculé, slide par slide :

1. on mesure le **97e centile de luminance** de la zone réellement occupée par
   le texte. Pas la moyenne : une moyenne ment. Un titre posé sur une fenêtre
   surexposée passe la moyenne et reste illisible sur la fenêtre. Mesuré : sur
   un fond sombre percé d'une fenêtre blanche, la moyenne dit 62, le 97e
   centile dit 255 ;
2. on résout par dichotomie l'opacité minimale du voile qui amène le rapport
   WCAG à **7:1 pour le titre** et **4,5:1 pour le corps et l'accent** ;
3. le voile est un dégradé qui monte sur 150 px au-dessus du bloc et ne
   redescend jamais en dessous, sinon la fin d'une phrase retombe sur une zone
   claire ;
4. après composition **on remesure**, et la slide est refusée si le contraste
   n'y est pas. Le script échouait déjà plutôt que de livrer un texte qui
   déborde, il échoue maintenant aussi sur un texte illisible.

Rendu réel sur leurs photos, mesuré le 02/09 : couverture (photo 01, façade)
voile à 71 %, titre à **7,59:1** ; slide 3 (photo 20) voile à 67 %, titre à
**7,59:1**, corps à 5,33:1, accent à 4,49:1.

### ⚠️ Ce que leur banque photo permet, et ce qu'elle ne permet pas

Les 19 photos viennent de **leurs propres mandats publiés** sur
lagalerieimmobiliere.com. Aucune banque d'images : c'est un compte commercial.

Deux limites, relevées à la mesure et à l'œil :

- **Neuf des dix-neuf sont des logements vides** : murs blancs, pièces sans
  meuble. Le détail mesuré y tombe sous 15 sur les trois bandes. Un mur nu ne
  fait pas une image, il fait une tache grise. Le manifeste les marque
  `matiere: false` et la validation les refuse comme fond. Restent **dix
  photos exploitables** : 01, 11, 12, 13, 15, 17, 18, 20, 27, 30.
- **Elles portent le filigrane « LA GALERIE IMMOBILIÈRE »** au centre. Sur
  leur propre carrousel ce n'est pas un défaut, c'est leur signature, mais le
  filigrane et le titre se disputent le même espace.

Ce sont des photos de mandats à vendre, pas des intérieurs meublés
aspirationnels. **Demander à Sabrina des photos de biens meublés ou vendus, et
des extérieurs de quartier** reste la meilleure piste : ce sont les seules qui
peuvent illustrer un bien précis.

### 🌇 Fonds d'ambiance sous licence — 02/09/2026

Maxime : « des photos qui ne sont pas obligatoirement des biens à la vente de
La Galerie ; il faut que ces photos soient instagrammables / Pinterest ».

**La distinction qui rend ça sain.** Ce qui a coûté Le Loft, c'est d'avoir fait
passer des images pour SON salon. Un fond d'ambiance derrière un texte de
conseil ne prétend rien de tel : c'est de l'habillage, pas un mandat. Deux
provenances cohabitent donc dans le manifeste :

| | `provenance: client` | `provenance: libre` |
|---|---|---|
| Origine | leurs mandats publiés | Pexels, licence commerciale |
| Peut illustrer un bien précis | **oui** | **non, refusé par la validation** |
| Champs obligatoires | — | `licence` + `credit` |

**Le garde-fou.** Si le texte d'une slide contient « ce bien », « à vendre »,
« en exclusivité », « coup de cœur » et compagnie, et que la slide porte un
fond `libre`, la validation refuse et dit pourquoi. Testé sur trois cas :
texte général + fond libre accepté, texte de mandat + fond libre refusé,
texte de mandat + photo du client accepté.

**⛔ Pinterest n'est pas une source.** Les images qui y sont épinglées
appartiennent à des tiers. On y cherche l'esthétique, on prend les fichiers sur
Pexels, dont la licence commerciale est explicite et gratuite.

**Ce qui a été retenu.** Cinquante-huit références proposées, cinquante-six
**téléchargées et mesurées une par une** : aucune référence inventée. Trente-
quatre ont de la matière et entrent au manifeste sous les clés `P<id>` :
toits de zinc, façades haussmanniennes, ferronneries, rues de Montmartre,
voilages traversés par le soleil, cuisines chaleureuses, bibliothèques.

Planche-contact des 34, avec identifiants et luminance :
`https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/f05400a8-f92c-4cf9-bc35-5f501f31d8a0.jpg`

**L'effet du calcul de voile se voit ici.** Une façade claire (`P31058041`,
luminance 205 sous le texte) demande 68 % de voile ; le voilage au soleil
(`P3557507`, 116) n'en demande que 40 % et la photo reste largement lisible.
Le titre tient à 7,59:1 dans les deux cas. C'est tout l'intérêt de mesurer
plutôt que de fixer une opacité : la photo n'est jamais assombrie plus que
nécessaire.

### Où c'est câblé

- `scripts/carrousel.py` — `_fond_pire_cas`, `_alpha_requis`, `poser_voile`,
  `charger_fond`, et la vérification après composition dans `render_slide`.
- `scripts/themes.json` — clé `fond` de `la-galerie-immobiliere` : couleurs de
  texte sur photo et cibles de contraste.
- `photos/la-galerie-immobiliere.json` — les 19 photos, leur URL sur le site du
  client, leur luminance et leur détail mesurés, et le champ `matiere`.
- Les quatre carrousels portent une clé `photo` par slide, sans répétition à
  l'intérieur d'un même carrousel.

Les cinq autres comptes ne sont pas touchés : tout est conditionné à la
présence d'une clé `fond` dans le thème.

**État au 12/10/2026 : la bascule n'est pas faite.** La clé `fond` n'a pas été ajoutée au
thème de ce compte, et les quatre specs d'août restent sur fond plat. Raison : sur trois
des quatre carrousels refaits en fond photo, le contrôle de contraste de
`scripts/carrousel.py --check` refuse le rendu — 6,91:1 pour le titre et 4,09:1 pour le
corps là où il faut 7,0:1 et 4,5:1, même après le voile. Les photos concernées (P30702969,
P2265845, P19096629) sont trop claires sous la zone de texte. Le moteur sait faire le fond
photo ; ce qui manque, c'est une sélection de photos qui passe le contrôle, ou un voile
plus dense. À reprendre avec Maxime avant de rallumer la clé.

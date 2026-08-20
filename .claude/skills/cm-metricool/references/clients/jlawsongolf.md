# J Lawson Golf — fiche client

## ✍️ Voix éditoriale — LA VOIX DE JOHN (règle client, 03/08/2026)
Le client a fourni son texte de référence (post AIG Women's Open du 03/08) et demandé que **tous les posts** adoptent ce style. Les 33 brouillons feed (10/08 → 23/10) ont été réécrits en conséquence. Codification :
- **Première personne du fitteur** : « je », « ce que je retiens », « je mesure », « j'y serai ». Plus de « on » d'agence ni de « le studio vous… » désincarné.
- **Vouvoiement du lecteur** (« pour vous », « votre swing ») — le tutoiement des anciennes légendes est abandonné.
- **Phrases courtes, paragraphes d'une à deux lignes.** Constat technique d'abord, enseignement ensuite.
- **Clôture en maxime sobre** (« Il faut trouver l'objet qui fonctionne pour vous », « Ça ne se devine pas. Ça se mesure ») — plus de CTA criard « 👉 lien en bio ».
- **Émojis quasi absents** : 🏆 toléré sur les posts résultat, rien d'autre.
- **Hashtags conservés, 4 par post.**
- Détails techniques précis bienvenus (bounce, torque, tr/min) — c'est sa crédibilité. Jamais de chiffre inventé : reprendre ceux validés ou rester qualitatif.
- ⚠️ Les 2 posts déjà validés par Maxime (05 et 07/08, draft:false) sont restés dans l'ancien style — ne pas les toucher.
- Post de référence : « Ce que je retiens de cette saison de majors féminins : 3 victoires avec des putters "lames" (Nelly Korda x 2 et Shiho Kuwaki) et 2 avec un maillet : Haeran Ryu. Il faut trouver l'objet qui fonctionne pour vous. »

## J Lawson Golf (source : jlawsongolf.com/rendezvous.html, vérifié juillet 2026)
- Fitting Driver/bois : 160 € (~1h)
- Fitting Fers/wedges : 160 € (~1h)
- Fitting putter : 160 € (~1h)
- Analyse technique Gears full corps : 260 € (~1h30)
- Panier moyen retenu : 160 € / séance (jusqu'à 260 €)
- Formule ROI : nb de fittings pour rembourser = prestation CM mensuelle ÷ 160
  - Ex. prestation 500 €/mois → ~3 fittings/mois · 800 €/mois → 5 fittings/mois
- Typologie : vente unitaire à forte valeur, clientèle qui revient à chaque changement de matériel (LTV : re-fitting tous les 2-3 ans + bouche-à-oreille club)

## Banque photos réelle — 107 fichiers (recomptés le 30/07/2026)
- Le dossier `medias/jlawson-golf/` contient **107 photos** (69 paysage, 38 verticales), pas 42 : la note ci-dessous date d'un comptage partiel. Statut `en-reserve` dans `recaps/medias-index.json` → vivier où la tâche du lundi puise pour remplacer progressivement les visuels IA (max 4/semaine).
- Les 38 verticales comblent le « trou » signalé plus bas (verticales 9:16 pour stories) : les stories IA du compte peuvent passer en vraies photos.

## jlawsongolf (banque validée juillet 2026 — 42 photos)
- Shooting pro HOMESANFAUTE (mai 2026) : portraits fitteur (bio/coulisses), sessions fitting client (P1/P5), détails clubs/shafts (P1/P2), ambiance studio+écrans (P3/P4)
- Photos terrain IMG_14xx-16xx : atelier gripping/loft-lie (P3 reels bruts), mur de shafts (P1/P2), clubs finis (P5), écrans de mesure/data (P1/P5)
- Trous à combler : verticales 9:16 pour stories, avant/après client, photos extérieur parcours
- Élément IA Higgsfield : "JLawson-Studio" (id 12942370-e8c1-465c-9ea0-2583a9384e0c) — DA moderne tech premium, métal noir mat, LED accent chaud, bleu marine + vert, AUCUN bois

## Visuels IA (Higgsfield) + branchement
- ⚠️ **INCOHÉRENCE DA À TRANCHER** : la description de l'élément de référence JLawson-Studio dit « lumière ambrée type atelier, ambiance premium artisanale », alors que la note ci-dessus dit « tech moderne, métal noir mat, AUCUN bois ». La banque IA générée (22/07/2026) suit l'élément de référence (atelier + bois) → à valider ou régénérer en version « tech moderne sans bois » si le client préfère.
- Banque IA locale (9 visuels) `medias/jlawson-golf/ia/` : fer-fitting, mur-shafts, balles, grip, driver, wedges, launch-monitor, studio, parcours. Bleu marine + vert respectés ; contiennent du bois (établi/mur).
- Attachement : **Instagram + Facebook**, 18h (posts « résultat tournoi » du dimanche à 12h). ⚠️ Metricool refuse les dates passées → un post daté d'hier ne peut pas être branché.
- **STATUT BRANCHEMENT : ✅ (22/07/2026)** — 38/39 posts avec média (le seul sans média = 21/07, déjà passé donc non branchable). ~31 posts branchés en rotation + 6 qui avaient déjà de vraies photos (shooting HOMESANFAUTE, non touchés). Mapping : fer→fers/lie/dispersion ; mur-shafts→shaft/Ryan Fox/Toussaint ; balles→balle ; grip→regripping/rentrée sac/checklist ; driver→driver/distance ; wedges→wedges ; launch-monitor→Gears/technologie/FedEx/bilan ; studio→journée studio/index/indoor/prépa/Open France ; parcours→tournois (circuit euro, Solheim, BMW PGA, Albatros).

## Post résultat AIG Women's Open — complété le 02/08/2026
- Post du **03/08 12:00** (ancien id 352532618 → nouveau **357057266**, via `bulk_replace_posts`). Brouillon vérifié, IG+FB, heure Paris exacte.
- Résultat réel : **Shiho Kuwaki** bat Esther Henseleit en playoff (mort subite sur le 18, victoire au 2ᵉ passage) à Royal Lytham, les deux à -5 après 72 trous. Premier majeur et première victoire LPGA Tour.
- ⚠️ **Le WITB a été abandonné, volontairement.** Le calendrier prévoyait un post « dans son sac ». Aucune source fiable ne donne son sac club par club : seul un agrégateur (golfreviewsguide) liste putter Odyssey White Hot OG 2-Ball + balle Bridgestone Tour B X, page inaccessible en vérification directe et compilée *pendant* le tournoi. Règle « jamais de matériel inventé » → post recentré sur le playoff et la leçon de fitting (régularité du club sous pression). **Ne pas réintroduire de WITB sans source constructeur ou média équipement.**
- **Visuel : carte résultat typographique** (choix de Maxime, 02/08). Aucune photo de Kuwaki n'est utilisable : toutes les images de l'épreuve sont des photos d'agence (Getty — Luke Walker, Warren Little), « editorial use only », et il n'existe aucune photo d'elle sous licence libre sur Wikimedia Commons. La règle « jamais de photo d'agence sur un compte commercial » s'applique.
- Carte régénérable à l'identique :
  ```
  python3 scripts/carte-resultat.py carte.jpg \
    --surtitre "AIG WOMEN'S OPEN 2026 · ROYAL LYTHAM & ST ANNES" \
    --nom "SHIHO KUWAKI" --score "-5" --mention "VICTOIRE EN PLAYOFF" \
    --detail "Bat Esther Henseleit au 2e trou de mort subite, après 72 trous à égalité" \
    --note "PREMIER MAJEUR"
  ```
- ⚠️ **La carte a dû être attachée à la main.** L'environnement de la session n'a pas d'accès sortant vers les hôtes d'hébergement (Higgsfield, CloudFront, static.metricool) → impossible de produire l'URL publique qu'exige `media_url`. Le brouillon porte en attendant un visuel IA de links. Depuis une machine avec accès réseau normal, le pipeline `media_upload → PUT → media_confirm → bulk_replace_posts` fonctionne comme d'habitude.
- Modèle réutilisable pour tout post « résultat de tournoi » : `scripts/carte-resultat.py` (4:5, DA marine/vert/ambre).

## Stories — rotation 2 semaines, vidéo + fond sonore (03/08/2026) ✅ ACTIF
- **Règle Maxime (03/08) : aucune story identique sur 2 semaines consécutives.** Rotation de **14 cartes distinctes** en cycle A/B (A = semaines des 03, 17, 31/08 ; B = 10, 24/08). Vérifié par calcul : toute fenêtre glissante de 14 jours contient 14 stories différentes.
- **28 stories VIDÉO planifiées ✅ 04→31/08 à 10:00** (ids 357218610→357219269), IG+FB, brouillon vérifié par `get_post_raw`. L'ancienne rotation hebdo de 7 visuels IA (28 brouillons) a été supprimée. La story du 03/08 (ancienne, visuel IA fixe) a été laissée en place.
- **Format : cartes typographiques ANIMÉES 7,5 s avec fond musical** — cartes PIL pures (zéro IA, zéro photo, DA marine/vert/ambre, conforme au précédent Pierre Huiban), musique en **synthèse procédurale** (`scripts/fond-sonore-stories.py` : pulse électronique premium ~100 BPM — aucun sample tiers, aucun modèle génératif, zéro droits). Assemblage ffmpeg image+audio.
- Source de vérité de la rotation : `assets/stories/manifest-stories-2sem.json` (14 slots : titre, sous-titre, note). Cartes : `assets/stories/jlawson-golf/`. Régénération : `carte-story-typo.py` + `fond-sonore-stories.py` + ffmpeg.
- Reconduction de septembre : replanifier les mêmes 14 vidéos (URLs cloudfront dans le manifest des payloads, réutilisables telles quelles) en respectant le cycle A/B.
- 📌 Ces cartes typo sont l'intérim conforme à la règle « zéro IA dans les stories » : quand `medias/` sera rapatrié, les 38 photos verticales réelles pourront remplacer progressivement les cartes via la tâche du lundi (i2v identité verrouillée + contrôle dernière frame).

## Stories VRAIES PHOTOS (décision Maxime 03/08 : « photos transformées en vidéo ») ✅ 4 SLOTS EN PLACE
**4 slots sur 14 sont passés en vraies photos animées.** Terminé le 04/08/2026 à 02h30.

| Slot | Dates | ids brouillons | Photo source | Vidéo hébergée (media_id) |
|---|---|---|---|---|
| jeudi (B) — ANALYSE GEARS | 13/08 · 27/08 | 357397907 · 357397912 | 11 `…mtr_11226288403794074990.jpg` | `91db08d2-78fc-4e1d-b50c-833f14b7a54f` |
| mardi (A) — LE SHAFT | 04/08 · 18/08 | 357633119 · 357633132 | 03 `…mtr_12764512827799543594.jpeg` | `b68b02be-e0f5-48f4-b24a-4557f44bdd7f` |
| samedi (A) — LA DATA PARLE | 08/08 · 22/08 | 357633162 · 357633181 | 06 `…mtr_6326575259361033427.jpeg` | `e444605a-1bad-4c6e-848b-5e921d64d84d` |
| samedi (B) — CÔTÉ ATELIER | 15/08 · 29/08 | 357633211 · 357633226 | 09 `…mtr_6876674637451197532.jpg` | `9d2f7bdb-a75c-4d11-a418-c3f8c7703a38` |

Les 8 cartes typographiques de ces slots ont été supprimées (357218703, 357219041, 357218610, 357218963, 357218645, 357219000, 357218722, 357219244). Tous les brouillons vérifiés par listing : `draft:true`, `autoPublish:false`, IG+FB, média cloudfront.

### Chaîne de production (éprouvée, à rejouer telle quelle)
1. Crop 9:16 de la photo **sans aucun texte** → `media_upload` + PUT depuis la sandbox + `media_confirm`.
2. `generate_video` **kling3_0_turbo**, 9:16, 5 s, 7,5 crédits, `declined_preset_id 24bae836-2c4a-48e0-89b6-49fcc0b21612`. Prompt verrouillé identité : *« Locked static camera, no zoom, no pan. Documentary realism: [micro-mouvement]. Every face and identity stay strictly identical to the photo — same features, same glasses, same haircut, same clothes. No morphing, no new objects, no text, ambient light unchanged. »*
3. **Contrôle visuel obligatoire de la DERNIÈRE frame** contre la photo source (montage côte à côte, décodé en local). Les 4 contrôles sont passés : visage, lunettes, coupe, vêtements identiques.
4. Assemblage ffmpeg : `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920` + calque texte PNG + `jl.wav` (nappe La majeur + pulse 55 Hz ~100 BPM, `scripts/fond-sonore-stories.py`), 5,4 s, AAC.
5. Habillage : dégradé marine haut/bas, « J LAWSON GOLF » ambré + filet, titre créme (Montserrat 800, corps auto-ajusté), filet vert, sous-titre gris, accroche verte « TON MATÉRIEL À TES MESURES ». Tout tient dans la zone sûre.
6. `bulk_schedule_stories` (brouillon) puis `bulk_delete_posts` des cartes, puis **vérification par listing**.

### Reste à faire
- Photo 01 **exclue** : c'est un visuel promo The Open / Royal Birkdale (texte incrusté + droits R&A), pas une photo du studio.
- **10 slots sur 14 gardent leur carte typographique** faute de photos exploitables. Ils basculeront quand `medias/jlawson-golf/` (38 verticales réelles) sera rapatrié.
- Reconduction de septembre : réutiliser les 4 URLs vidéo ci-dessus telles quelles, en respectant le cycle A/B.

## Stories quotidiennes août 2026 (28/07/2026 — REMPLACÉE le 03/08)
- Banque 7 stories 9:16 `medias/jlawson-golf/ia/stories/` (lun nouvelle-semaine, mar shaft, mer fers, jeu driver, ven résa, sam data, dim parcours). Visuels IA, rotation hebdo — abandonnée au profit de la rotation 2 semaines ci-dessus.

## 🔇 Stories muettes — septembre traité le 19/08/2026
Le premier passage de démutage ne couvrait qu'août. **30 stories de septembre**
(créées le 04/08, ids `3578629xx`–`3578641xx`) étaient hors de la fenêtre de
listing : 18 d'entre elles pointaient encore sur les médias sonores.

- Les 12 stories **photo** de septembre pointaient déjà sur les médias muets
  (`c42ca037` Le shaft, `fd54ea6e` Fers sur mesure, `52d09b09` La data parle,
  `1e56a55c` Analyse Gears, `2b35934e` Côté atelier) — vérifiées, non touchées.
- Les 18 stories **cartes** ont été redéposées muettes aux mêmes dates
  (IG+FB, 10:00, brouillon), anciennes supprimées.

Médias muets de référence, réutilisables tels quels :
`9c7aaa64` Driver · `08546cef` Réserve ton fitting · `6e0255a9` Jour de parcours ·
`06321768` Objectif semaine · `491d044f` Wedges · `627412c5` Putter ·
`1638ebdf` Dernier call · `36467b17` 18 trous · `526845eb` Nouvelle semaine.

Vérifié par listing : **30 stories pour les 30 jours de septembre**, une par
jour, aucun trou, aucun doublon, `draft:true` partout. Août (13 stories) idem.

⚠️ Leçon : lister le calendrier **jusqu'à sa fin**, pas sur quinze jours.
Le calque typo des stories photo est versionné dans
`scripts/jlawson-photo-story.py`.

## 🔴 RETOUR CLIENT 19/08/2026 — il veut arrêter l'accompagnement
**« Les textes ne lui vont pas. »** Audit fait le jour même. Il a raison, et le
problème n'est pas l'absence de règle : **la règle existait et n'a pas été tenue.**

La section « ✍️ Voix éditoriale » ci-dessus affirme que « les 33 brouillons feed
ont été réécrits en conséquence » le 03/08. C'est faux. Un contrôle des posts
programmés montre un mélange : certains sont bien dans sa voix (ex. 31/08
« Je vous prépare un mois de contenu spécial »), beaucoup ne le sont pas.

### Écarts constatés, pièce par pièce
| Post | Écart |
|---|---|
| 24/08 (357245277) | Aucun « je ». Et surtout **« un réglage à 40 € »** — ce tarif n'existe pas, sa grille est 160 € / 260 €. **Chiffre inventé**, ce que la fiche interdit explicitement. |
| 28/08 (357245346) | Aucun « je ». « Le check-up de rentrée » = un produit qui n'est pas à son catalogue. |
| 26/08 (358746274) | **« Réservez votre créneau, lien en bio »** — le CTA nommément banni par la règle. **6 hashtags** au lieu de 4. |
| 03/09 (357867252) | « **On** mesure. **On** teste. **On** règle. » — le « on » d'agence explicitement proscrit. 5 hashtags. Pas de média. |
| 08/09 (357866239) | Aucun « je ». 5 hashtags. Pas de média. |
| 24/09 + 02/10 | La même promesse « +14 mètres au driver » sur deux posts à huit jours d'écart. Chiffre non sourcé. |

### Corrigé le 19/08
- **24/08 → 364309059**, **28/08 → 364309069** : réécrits à la première personne,
  tarif inventé supprimé, 4 hashtags. Anciens supprimés.
- 26/08 (carrousel 8 slides) : texte corrigé prêt, **non appliqué** — l'action
  `update_post_text_only` échoue et `bulk_replace_posts` ne prend qu'un média,
  elle détruirait les 7 autres slides. **À corriger à la main dans Metricool.**

### Reste à faire
- Passe complète sur les ~25 posts feed restants (sept. → 23/10) : première
  personne, 4 hashtags, zéro CTA « lien en bio », zéro chiffre non sourcé.
- 4 posts sans média (03/09, 08/09, 17/09, 24/09) : Instagram refusera de publier.
- 3 posts avec placeholder `[VAINQUEUR]` / `[RÉSULTAT]` non résolu.
- Dédoublonner la promesse « +14 mètres ».

### Leçon
Écrire la règle dans la fiche ne suffit pas. Toute réécriture de voix doit se
terminer par un **contrôle poste par poste** : présence du « je », comptage des
hashtags, recherche des CTA bannis, et vérification que chaque chiffre cité
existe dans la grille tarifaire vérifiée.

## ✅ PASSE COMPLÈTE DU 20/08/2026 — les 32 posts feed sont conformes
Reprise du calendrier **21/08 → 23/10** (32 posts feed + 42 stories). Contrôle
post par post contre la règle « voix de John », pas de déclaration sur parole.

### Ce qui a été corrigé
| Post | Écart | Correction |
|---|---|---|
| 21/08 driver | « c'est souvent 10 mètres de plus » — chiffre non sourcé, pas de « je » | « je récupère souvent de la distance sans changer une seule pièce du club » |
| 26/08 carrousel | « Réservez votre créneau, lien en bio » + 6 hashtags | CTA banni supprimé, clôture en maxime, 4 hashtags |
| 02/09 carrousel | « Prenez rendez-vous, lien en bio » + 6 hashtags | idem — **les 8 slides sont intactes** |
| 03/09 | « **On** mesure. **On** teste. **On** règle. » + 5 hashtags + sans média | réécrit en « je », 4 hashtags, photo studio attachée |
| 04/09 | « −6 points d'index » non sourcé | promesse chiffrée retirée, récit conservé |
| 07/09 · 09/09 · 16/09 · 25/09 · 30/09 | aucune première personne | recalés sur « je » |
| 08/09 | pas de « je », 5 hashtags, sans média | réécrit, photo atelier attachée |
| 17/09 | « 400 shafts au mur » — **doublon avec le 18/09**, 5 hashtags, sans média | ré-angle sur le point de flexion et la façon de charger le club |
| 24/09 | « +14 m » + « six points d'index » + « dispersion divisée par deux » — trois chiffres non sourcés — et **doublon du 02/10** | entièrement ré-angle sur l'Open de France, zéro chiffre |
| 02/10 | « +14 mètres de carry » non sourcé | garde les trois réglages, remplace le chiffre par « je l'ai mesuré avant et après » |
| 07/10 | « la moitié des golfeurs joue trop fin » — statistique inventée | « beaucoup de golfeurs… sans le savoir » |
| 09/10 | « le bilan de fin de saison » = produit hors catalogue | ramené à « une séance au studio » |
| 14/10 | délais fournisseurs présentés comme un fait général | attribué à lui : « hors saison, je récupère les shafts plus vite » |
| 16/10 · 23/10 | « 90 minutes » donné comme la durée d'une séance | corrigé sur la grille réelle : **1 h fitting (160 €) / 1 h 30 Gears (260 €)**, et les deux posts Toussaint ont été différenciés |
| 19/10 · 21/10 | pas de « je », sans média | réécrits, photos attachées |
| 23/09 | « Viktor Hovland en tête d'affiche » — plateau annoncé, non vérifiable | mention retirée |
| 21/09 · 28/09 · 05/10 · 14/09 | placeholders `[VAINQUEUR]` / `[RÉSULTAT]` / `[WITB]` flous | reformulés avec la date de complétion **et** l'exigence de source (« uniquement si une source constructeur ou un média équipement le publie, sinon supprimer ce paragraphe ») — cf. la leçon Kuwaki plus haut |

### Les 7 posts sans média sont branchés
Instagram refuse un post sans visuel : les 7 brouillons concernés (03, 08, 17,
24/09 et 19, 21, 23/10) portent désormais une **vraie photo du compte**
(shooting HOMESANFAUTE / atelier), choisie après contrôle visuel de chaque
image, pas au hasard :

| Date | Photo | Sujet |
|---|---|---|
| 03/09 | `202607/…mtr_9796660200785221361.jpg` | John à l'atelier, club en main |
| 08/09 | `202608/…mtr_2368656243603853072.jpg` | portrait studio |
| 17/09 | `202607/…mtr_12764512827799543594.jpeg` | mur de shafts + écran |
| 24/09 | `202608/…mtr_4850984026945789902.jpg` | John avec un client devant les sacs |
| 19/10 | `202607/…mtr_772896934238071130.jpg` | portrait extérieur, fin de journée |
| 21/10 | `202607/…mtr_6326575259361033427.jpeg` | simulateur, frappe devant l'écran de mesure |
| 23/10 | `202607/…mtr_15004927010967591954.jpeg` | séance de fitting client |

⚠️ Ce sont des photos **déjà parues** en juillet-août. C'est un pis-aller
assumé : mieux vaut une photo revue à deux mois qu'un post qu'Instagram
refuse. À remplacer dès que `medias/jlawson-golf/` (107 photos) sera rapatrié —
le dossier est vide dans cet environnement.

**Photos exclues du vivier après contrôle visuel :** les visuels promo The Open
/ Royal Birkdale et AIG Women's Open (texte incrusté + droits R&A), et les
photos d'agence de joueurs pros. Règle « jamais de photo d'agence sur un compte
commercial ».

### Vérifié par listing après coup
`74 posts · 32 feed · 42 stories · draft:true partout · autoPublish:false
partout · noMedia:0 · un seul post par créneau, aucun doublon.`

### Outillage : deux code actions créées le 20/08
`update_post_text_only` échoue systématiquement (erreur 500). Deux actions
maison la remplacent :
- **`dump_post_texts`** (blogId, start, end, kind) — les textes complets, sans
  les tableaux média. Indispensable pour auditer une voix.
- **`retext_posts`** (blog_id, items) — réécrit **uniquement** le texte, média
  intact (carrousels compris). Le secret : l'API renvoie des champs qu'elle
  refuse en écriture (`PublicationStatusCode`) → il faut retirer `creationDate`,
  `uuid`, `creatorUser*`, `hasNotReadNotes` et ne garder que `network` dans
  chaque `providers[]` avant le PUT.
- **`media_inventory`** (blogId, start, end) — quels posts n'ont pas de média,
  et quelle URL sert combien de fois. C'est ce qui a révélé les 7 posts nus.

⚠️ **Piège `bulk_update_post_media` :** elle **crée un nouveau post** au lieu de
modifier l'existant. Il faut supprimer l'ancien derrière, sinon le créneau se
retrouve en double. Vérifié : 81 posts après, 74 après nettoyage.

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

## Stories quotidiennes août 2026 (28/07/2026)
- Banque 7 stories 9:16 `medias/la-galerie-immobiliere/ia/stories/` (lun belle-semaine, mar lumière, mer charme-ancien, jeu votre-projet, ven week-end-visites, sam bien-rare, dim inspiration). Vérifiées (1 régénérée pour texte dupliqué).
- **31 stories planifiées ✅** 01→31/08 à 10:00, IG+FB, brouillon, via `bulk_schedule_stories`.
- ⚠️ **10 stories « Sabrina » sans média** (28/07→29/09, 18h, hebdo — ids 326979151/160/173/175/177, 326980004/005/007/011/020) : contenus face-cam du calendrier initial (adresses de Sabrina, anecdote terrain, équipe, marché immo…). **NE PAS brancher en IA** (personne réelle) ni supprimer : à TOURNER avec Sabrina (vidéos verticales), puis héberger via [[hebergement-photos-reelles-metricool]]. Sans danger en attendant : elles sont en brouillon.

## Carrousel hebdo (créneau du mercredi, 18h, Instagram + Facebook)
- **Typologie** : très forte valeur unitaire, décision longue → la preuve est la maîtrise du détail. **Cible** : propriétaire ou acquéreur sur Paris 16e / Puteaux / Hauts-de-Seine, qui engage un patrimoine et craint surtout de se tromper. Jargon économique toléré, jamais technique.
- **Archétypes prioritaires** : A2 (erreurs, le plus performant sur cette cible), A5 (arbitrage), A8 (saisonnier), A7 (coulisses de l'expertise). **A6 (décryptage chiffré : taux, prix au m², DPE) uniquement après recherche web datée et sourcée.**
- **DA carrousel** (`scripts/themes.json` → `la-galerie-immobiliere`) : fond beige #EFE9E1, texte taupe #2E2A26, accent doré #B08D57, **police sérif** (Didot, repli Georgia), titres en bas-de-casse. Cohérente avec `LaGalerie-Studio`.
- **Planifiés (spec dans `carrousels/la-galerie-immobiliere/`)** : 12/08 A2 « Cinq erreurs qui coûtent des semaines » · 19/08 A5 « Vendre ou louer » · 26/08 A8 « Préparer son bien avant septembre » (angle home staging, adossé à l'expertise archi d'intérieur de la fondatrice) · 02/09 A7 « Ce que l'on regarde avant d'estimer ».
- **Réserve de sujets** : DPE et réglementation (A6, **réglementation à vérifier par recherche web à la date de publication**) · « Acheter en fin d'année : ce qui change » (A8, novembre) · « Une visite réussie, du point de vue de l'acquéreur » (A5) · remise de clés commentée (A3, dès qu'un client accepte).
- **Vigilance** : barème d'honoraires **non vérifié** → aucun honoraire cité. Aucun prix au m², aucun taux, aucun chiffre de marché sans source datée. Le prénom de la fondatrice n'apparaît pas encore dans les slides : à ajouter si elle le valide. Ne jamais illustrer un carrousel avec un visuel IA présenté comme un bien réel.

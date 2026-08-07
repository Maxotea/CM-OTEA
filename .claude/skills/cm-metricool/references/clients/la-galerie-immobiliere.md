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

## ⚠️ Posts « Swipez → » du lot de juillet : une couverture, pas de slides (constaté 07/08/2026)

Le lot planifié en juillet contient des légendes écrites **pour un carrousel** (« Swipez pour
découvrir → », « en quelques slides ») posées sur des posts qui n'ont **qu'un seul média**, parfois
aucun. À la lecture, le post promet une suite qui n'existe pas — c'est exactement ce qui a fait dire
à Maxime « on dirait qu'il manque une partie ». Le moteur de carrousels n'existait pas encore à la
date de ce lot. Même défaut déjà relevé sur Pierre Huiban (voir sa fiche).

**Tous en brouillon : rien n'est jamais parti en ligne.** Inventaire au 07/08/2026 :

| Date | Post | Médias | Ce qu'il faut |
|---|---|---|---|
| ~~07/08 12:30~~ | « Tendances prix été 2026 — les chiffres clés » | 1 | **traité** → refait pour le 14/08, voir plus bas |
| 02/10 12:30 | « De la première visite à la signature » | 1 | vrai récit client → accord du client, ou basculer en carrousel A1 |
| 09/10 12:30 | « 5 mythes sur l'estimation » | 1 | carrousel A4 — sujet déjà outillé, à écrire dans `carrousels/` |
| 13/10 18:00 | REEL « Découvrez un autre métier » | 0 | **placeholder `[collaborateur]`** → nommer la personne, puis tourner |
| 16/10 12:30 | « 5 choses à savoir sur [Prénom] » | 1 | **placeholder non rempli** + photo de la personne → demander à Sabrina |
| 30/10 12:30 | « Acheteur : avantages fin d'année » | 1 | carrousel A8 |
| 06/11 12:30 | « Nos clients en parlent » | 0 | vrais témoignages → demander à Sabrina |
| 20/11 12:30 | « L'équipe — qui fait quoi ? » | 0 | vraies photos d'équipe → demander à Sabrina |

**Règle qui en découle : sur ce compte, le vendredi 12h30 est un post feed SIMPLE.** Le carrousel,
c'est le mercredi 18h (section suivante). Une légende du vendredi ne doit donc jamais contenir
« Swipez », « slides » ni « faites défiler ». `scripts/audit_posts.py` vérifie ce point.

### Post du 07/08 refait pour le 14/08 12:30 (créneau vendredi qui était vide)

Le créneau du 07/08 était déjà passé au moment du constat, et le 14/08 n'avait aucun post feed.
Chiffres **relevés le 07/08/2026** sur quatre baromètres publics — appartements Puteaux
**7 376 €/m²** et fourchette **5 262 → 9 664 €/m²** (SeLoger, juillet 2026) · maisons 8 364 €/m² ·
12 mois : appartements **-0,1 %**, maisons **-0,6 %** · moyenne tous biens selon la source :
**7 163 €** (PAP, 1er juillet 2026), 7 407 € (MeilleursAgents), **7 633 €** (RealAdvisor, juillet
2026). L'écart entre baromètres, 470 €/m², vaut ~33 000 € sur 70 m².

Les baromètres sont **nommés ici mais pas dans la légende** : MeilleursAgents et PAP captent les
mêmes requêtes « estimation gratuite » que l'agence, autant ne pas leur envoyer d'attention. La
légende dit « quatre baromètres de prix en ligne, relevés de juillet 2026 », la source vérifiable
reste dans cette fiche.

```
Cet été, le mètre carré à Puteaux se négocie autour de 7 376 euros pour un appartement. Le chiffre est juste. Il ne dit presque rien de votre bien.

Trois enseignements des relevés de juillet 2026.

1. Le marché ne bouge plus. Sur douze mois, les appartements varient de -0,1 %, les maisons de -0,6 %. À l'échelle d'un marché, c'est l'immobilité.

2. L'écart, lui, reste considérable. Toujours à Puteaux, toujours cet été : de 5 262 à 9 664 euros le mètre carré selon le bien.

3. Les baromètres en ligne ne s'accordent pas. De 7 163 à 7 633 euros selon la source, au même mois. Sur un appartement de 70 mètres carrés, ce seul écart déplace le prix affiché de près de 33 000 euros.

La conséquence tient en une phrase : quand la moyenne stagne, ce n'est plus le marché qui porte le prix, c'est la place de votre bien dans la fourchette.

Écrivez-nous en message privé pour savoir où se situe le vôtre.

Sources : quatre baromètres de prix en ligne, relevés de juillet 2026.

#immobilierputeaux #prixaumetrecarre #hautsdeseine #marcheimmobilier #estimation #immobilierprestige
```

Média : reprendre celui déjà attaché au brouillon du 07/08
(`https://static.metricool.com/zapier/202607/5733302-file-5314915366995617872.png`). IG + FB,
brouillon, `autoPublish` à faux. **Une fois le 14/08 créé, le brouillon du 07/08 (id 351958147)
n'a plus d'objet et peut être supprimé.** Chiffres à revérifier si la publication glisse d'un mois :
un relevé de juillet ne se cite plus en octobre.

## Carrousel hebdo (créneau du mercredi, 18h, Instagram + Facebook)
- **Typologie** : très forte valeur unitaire, décision longue → la preuve est la maîtrise du détail. **Cible** : propriétaire ou acquéreur sur Paris 16e / Puteaux / Hauts-de-Seine, qui engage un patrimoine et craint surtout de se tromper. Jargon économique toléré, jamais technique.
- **Archétypes prioritaires** : A2 (erreurs, le plus performant sur cette cible), A5 (arbitrage), A8 (saisonnier), A7 (coulisses de l'expertise). **A6 (décryptage chiffré : taux, prix au m², DPE) uniquement après recherche web datée et sourcée.**
- **DA carrousel** (`scripts/themes.json` → `la-galerie-immobiliere`) : fond beige #EFE9E1, texte taupe #2E2A26, accent doré #B08D57, **police sérif** (Didot, repli Georgia), titres en bas-de-casse. Cohérente avec `LaGalerie-Studio`.
- **Planifiés (spec dans `carrousels/la-galerie-immobiliere/`)** : 12/08 A2 « Cinq erreurs qui coûtent des semaines » · 19/08 A5 « Vendre ou louer » · 26/08 A8 « Préparer son bien avant septembre » (angle home staging, adossé à l'expertise archi d'intérieur de la fondatrice) · 02/09 A7 « Ce que l'on regarde avant d'estimer ».
- **Réserve de sujets** : DPE et réglementation (A6, **réglementation à vérifier par recherche web à la date de publication**) · « Acheter en fin d'année : ce qui change » (A8, novembre) · « Une visite réussie, du point de vue de l'acquéreur » (A5) · remise de clés commentée (A3, dès qu'un client accepte).
- **Cadence particulière — le compte ne publie pas le mercredi.** Ses posts feed sortent le **vendredi à 12h30**. Le carrousel du mercredi ne remplace donc rien ici : il **s'ajoute**. C'est assumé, le compte est au **forfait maximum** (confirmé par Maxime, 06/08/2026) — la règle « le carrousel remplace le post du mercredi » ne s'y applique pas.
- **Vigilance** : barème d'honoraires **non vérifié** → aucun honoraire cité. Aucun prix au m², aucun taux, aucun chiffre de marché sans source datée. Le prénom de la fondatrice n'apparaît pas encore dans les slides : à ajouter si elle le valide. Ne jamais illustrer un carrousel avec un visuel IA présenté comme un bien réel.

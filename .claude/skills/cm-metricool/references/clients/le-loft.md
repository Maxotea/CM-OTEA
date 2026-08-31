# Le Loft (Puteaux) — fiche client

> ## ⛔ CONTRAT TERMINÉ — 31/08/2026
>
> **William a mis fin au contrat.** Ne plus produire de contenu, ne plus
> programmer, ne plus brancher de média, ne plus générer de compte rendu
> client. Le compte est sorti du récap du lundi et de la détection de
> nouveaux médias (`recaps/clients-config.json`, `actif: false`).
>
> **État de Metricool à l'arrêt :** 37 contenus restants du 31/08 au 31/12,
> **tous en brouillon, aucun en publication automatique**. Rien ne partira
> tout seul. Trois d'entre eux sont sans média (19, 21 et 23/10). **Rien n'a
> été supprimé** : la suppression est irréversible et Maxime ne l'a pas
> demandée.
>
> **Ce qui reste en suspens et devient sans objet :** le carrousel « faux
> drama » du 28/08 (post 366400245) dont les planches 5 et 6 sont inversées,
> la réponse WhatsApp à William jamais envoyée, les 9 posts Pierre Huiban
> égarés dans ce calendrier (`327013311` à `327013327`), et la refonte en
> vraies photos qui attendait le push de `medias/le-loft/`.
>
> **Ce qu'il faut en retenir.** Le 21/08, William écrivait : « 80 % des posts
> sont des photos qui ne sont pas prises chez moi ». Dix jours plus tard, il
> arrête. Le grief documenté porte sur la pertinence du contenu, pas sur le
> prix. C'est la seule lecture appuyée sur des traces ; s'il a donné une autre
> raison de vive voix, elle n'est pas consignée ici.
>
> La fiche ci-dessous est conservée : elle sert si le compte revient, et les
> tarifs Planity relevés en juillet ont demandé du travail.

## Profil et tarifs VÉRIFIÉS juillet 2026 (Planity : planity.com/le-loft-92800-puteaux)
- Positionnement : "le barbier le plus complet de France" — 120 m², 7j/7 10h-20h, 4,9/5 (302 avis), 33 rue Godefroy, Puteaux. À côté de La Défense.
- blogId : 6191921 · Instagram UNIQUEMENT (@le_loft_barbier). Ton : tutoiement énergique, punchy ("Book ton rdv"), masculin ouvert (head spa mixte, kids). Horaire posts : 18h.
- Tarifs : coupe 25-30 € · coupe transformation 45 € · barbe 25-28 € (soignée+colo 45 €) · rasage à l'ancienne 30 € · formules coupe+barbe 48-65 € · HEAD SPA 60-120 € (différenciateur n°1) · formule VIP 120 € · soin visage 30-60 € · manucure 20-30 € (express -50% pendant coupe = offre réelle) · bronzage UV 15 € sans rdv · enfant 20-25 € · étudiant 22 €.
- ROI (typologie LTV forte) : 1 client fidélisé coupe+barbe (48 €, ttes les 4 sem.) ≈ 620 €/an ; 1 habitué head spa ≈ 780-1440 €/an. 2-3 nouveaux clients fidélisés/mois couvrent une prestation CM.
- Piliers : head spa (star du contenu), barbe/coupe pédagogie, preuve 4,9/5, saisonnier (rentrée kids/étudiants, Movember en novembre à préparer fin octobre), offres réelles uniquement.
- Prestation CM mensuelle : [à renseigner]

## Visuels IA (Higgsfield)
- **Élément de référence : `LeLoft-Studio`** (id `1bcd4818-3566-4970-b6f9-1236651fd981`, catégorie environment). DA : ambiance masculine premium — surfaces marbre/cuir noir mat, accents laiton doré/cuivre, lumière chaude ambrée type atelier, bois foncé et vert profond, bouteilles de soin ambrées, LED chaudes, faible profondeur de champ, rendu photo éditorial. **Jamais de visage** (compte commercial réel → pas de faux clients/barbiers présentés comme le salon). Pilier différenciateur head spa : vapeur, serviette chaude roulée, galets, plantes vertes. Réutiliser `<<<1bcd4818-3566-4970-b6f9-1236651fd981>>>` dans le prompt pour garder le style.
- Banque IA locale COMPLÈTE (9 visuels) dans `medias/le-loft/ia/` : outils-marbre, headspa, rasage, fauteuil (barbershop), soin-barbe, soin-visage, manucure, bronzage, salon (vue d'ensemble). Couvre tous les piliers pour rotation.
- Attachement : **compte Instagram UNIQUEMENT** (pas Facebook), horaire 18h. Recréer le post via `schedule_post` avec `media01`=URL publique + `instagram:true`, `facebook:false`, `draft:true`, `autoPublish:false`, puis corriger l'heure (bug +7h → `bulk_update_post_times` à 18:00) et supprimer l'ancien brouillon sans média. Vérifier `resolvedParams.blogId.label` = LE LOFT à chaque création (le résolveur peut se tromper de compte).
- **STATUT BRANCHEMENT : ✅ TERMINÉ (22/07/2026)** — 39 posts branchés en rotation, vérif finale = 0 post sans média. Compte 100% POST (aucun reel). ⚠️ Zapier rate-limite les `schedule_post` après ~6 créations (erreur "halted"/followUpQuestion) → vagues de 6 avec pause ~90s ; ~1 création/vague échoue (résolveur compte) → refaire avec instruction compte explicite ; les suppressions ont parfois « MCP connection lost »/« Code execution error » mais suppriment quand même (vérifier via list). Mapping thématique : head spa→routine/soin masculin/coulisses/chute/cocooning/rituel japon/kids ; rasage→rasage/serviette chaude ; soin-barbe→barbe été/coloration/automne/hiver/chute ; fauteuil→dégradé/coupe rentrée/week-end/transformation ; salon→120m²/août/équipe/rentrée 7j7/WWW/toussaint ; soin-visage→soin visage/épilation ; manucure→manucure/VIP ; bronzage→bronzage ; outils→avis 4,9/5. Mapping par thème : head spa→posts head spa/antistress/cocooning ; rasage→rasage/serviette chaude ; soin-barbe→barbe/coloration/barbe hiver ; fauteuil/salon→coupe/dégradé/transformation/espace 120m²/équipe ; soin-visage→soin visage/épilation ; manucure→manucure/VIP ; bronzage→bronzage/bonne mine ; outils→avis 4,9/5.

## Banque VRAIES PHOTOS — 21 photos (shooting pro, déposées le 15/07/2026)
- ⚠️ **INEXPLOITÉES à ce jour** (découvert le 30/07/2026) : le compte tourne encore 100 % en visuels IA alors que ces photos couvrent les piliers. Elles sont en `medias/le-loft/`, statut `en-reserve` dans `recaps/medias-index.json` → la tâche du lundi les branchera automatiquement sur les brouillons de la semaine (max 4/semaine).
- 20 verticales 2832×4240 (idéales stories 9:16) + 1 paysage. Contenu : **head spa** (93, 98, 99, 104, 105 — bac lumière bleue/ambrée, le pilier n°1), **soin visage/masque** (97, 103), **barbe & tondeuse** (95, 96, 101), **équipe dans le salon** (09, 11), **portraits barbiers sous le néon LF** (04→08, coupe-degrade-BTS), **vues salon** (94, 100, 102).
- Ces photos montrent de vraies personnes → **composition PIL uniquement** (`scripts/carte-story.py`), jamais d'IA générative sur les visages. La règle « jamais de visage » de la DA visait les faux visages IA ; les vrais barbiers et clients photographiés sont au contraire l'atout du compte.

## Stories quotidiennes août 2026 (28/07/2026)
- Banque 7 stories 9:16 `medias/le-loft/ia/stories/` (lun nouvelle-semaine, mar head-spa, mer barbe, jeu rasage, ven week-end, sam ouvert-7j7 10h-20h, dim même-le-dimanche). Vérifiées sans coquille.
- **31 stories planifiées ✅** 01→31/08 à 10:00, Instagram uniquement, brouillon, via code action `bulk_schedule_stories` (heure Paris exacte, pas de bug +7h). Des stories pré-existantes du calendrier initial existent aussi sur août.
- 🟢 Validations du gérant vues (28/07) : stories mar 04 & ven 07/08 + post soin-visage 05/08 passés en publication auto (l'UI vide le texte-note des stories validées, normal).

## 🎥 Stories VIDÉO — VRAIES PHOTOS, ZÉRO IA (31/07/2026, version finale)
- ⛔ **RÈGLE ABSOLUE POSÉE PAR MAXIME** : plus aucune image ni vidéo générée par IA dans les stories. Les visuels IA Higgsfield sont abandonnés pour ce compte.
- **Méthode retenue — VRAIE ANIMATION i2v sur la photo réelle** (Maxime a explicitement refusé le simple zoom : « pas des images animées mais juste des zooms »). Pipeline : crop 9:16 → i2v `kling3_0_turbo` sur la photo SANS texte → ffmpeg upscale 1080×1920 + overlay du calque texte PNG (texte net, jamais déformé).
- ⚠️ **Prompt i2v obligatoire sur photo de personne réelle** : « Locked static camera, no zoom. Documentary realism: [micro-mouvement précis]. His/Every face and identity stay strictly identical to the photo — same features. No morphing, no face change, no warping, photorealistic, extremely minimal motion. » Un prompt trop vague **déforme le visage** (constaté le 31/07 sur « rasage » photo 06 : visage modifié → régénéré avec le prompt renforcé, OK au 2ᵉ essai). **Contrôler systématiquement la dernière frame contre la photo source avant de brancher.**
- Alternative de secours si un visage se déforme malgré tout : mouvement de caméra pur en ffmpeg `zoompan` (aucun modèle génératif, pixels d'origine). ⚠️ Ne pas mettre `-loop 1 -t 5` sur l'entrée image : avec `d=125` cela produit 625 s de vidéo.
- **Mapping slot → photo** : lun `11` (équipe dans le salon) · mar `104` (head spa lumière bleue/ambrée) · mer `95` (barbe, tondeuse) · jeu `06` (barbier tondeuse face caméra) · ven `05` (barbier qui pointe l'objectif) · sam `09` (équipe assise, vue large) · dim `103` (soin visage, masque). Cartes + vidéos dans `medias/le-loft/stories-video/`.
- DA texte : titre Didot doré `#CEAA69` interlettré + filet + sous-titre Baskerville italique crème, sur voile noir dégradé (opaque jusqu'à y=360).
- **28 stories d'août ✅** (01→31/08 hors 02, 04, 07 validées par Maxime), brouillon, Instagram uniquement.

## 🎥 Stories VIDÉO (31/07/2026 — version IA, ABANDONNÉE)
- Les 7 visuels IA de la rotation passés en **vidéo 5 s** (i2v `kling3_0_turbo`, caméra verrouillée, textes incrustés vérifiés nets sur les 7 — voir [[hebergement-photos-reelles-metricool]] pour le pipeline). Sources publiques `d8j0ntlcm91z4.../hf_20260730_11*.mp4`, réutilisables telles quelles.
- **28 stories d'août en vidéo ✅** (27 remplacements + la story manquante du **jeudi 06/08 recréée**, id 356530482 — à supprimer si son absence était volontaire). Brouillon, Instagram uniquement. Les 3 stories validées par Maxime (02, 04, 07/08) restent en visuel fixe, non touchées. Vérifié : 31/31 jours couverts, 0 doublon.
- ⚠️ **Les 21 vraies photos du salon restent inexploitées pour les stories** : elles montrent de vraies personnes (barbiers, clients) → **interdiction d'i2v générative sur les visages**. Deux options propres : (a) cartes PIL fixes via `scripts/carte-story.py` ; (b) animer uniquement les photos SANS visage (vues salon 94/100/102, détails head spa). À trancher avec Maxime.

---

## 🔴 AUDIT DU 20/08/2026 — William veut arrêter, et les faits lui donnent raison

Message de William reçu le 20/08 à 11:05 : il arrête à la fin du mois. Trois
reproches, plus le prix. **Les trois sont vérifiés et fondés.** Ce qui suit est
l'état réel du compte, relevé dans Metricool, pas une reformulation du reproche.

### Reproche 1 — « 80 % des posts sont des photos qui ne sont pas prises chez moi »

Exact. Contrôle visuel des publications du feed sur la période qu'il juge
(20/07 → 19/08) :

| Date | Sujet | Visuel réellement publié |
|---|---|---|
| 22/07 | Barbe été | **photo IA — avec un visage d'homme** qui n'est ni un client ni un barbier du Loft |
| 24/07 | Avis 4,9/5 | visuel IA (outils sur marbre) |
| 31/07 | 120 m² | visuel IA (fauteuil, lumière bleue) — ne ressemble pas au salon |
| 05/08 | Soin visage | visuel IA (flacons, nature morte générique) |
| 10/08 | Cuir chevelu | visuel IA (bac head spa, vapeur) |
| 12/08 | Barbe qui pique | carrousel 100 % typographique |
| 19/08 | Coupe depuis 2 ans | carrousel 100 % typographique |

Soit **zéro photo réelle du salon sur tout le mois**. Le post du 22/07 viole en
plus la règle inscrite dans cette fiche depuis juillet — *« Jamais de visage »* :
un faux visage IA présenté comme le salon sur un compte commercial réel.

Et pendant ce temps : **les 21 vraies photos du shooting pro, livrées le
15/07, n'ont jamais été utilisées.** Elles sont toujours `en-reserve` dans
`recaps/medias-index.json`, un mois plus tard. La fiche le signalait déjà au
30/07 (« INEXPLOITÉES à ce jour ») — le signal a été écrit, jamais traité.

### Reproche 2 — « ou des photos de l'équipe qui ont déjà été postées »

Exact aussi, et c'est structurel. Le feed tourne sur une **rotation de 9 visuels
IA** rebranchés sur 39 posts (documenté plus haut : « 39 posts branchés en
rotation »). Neuf images pour trente-neuf publications : la répétition n'est pas
un accident, elle est dans la méthode.

### Reproche 3 — « rien vu passer du modèle femme de juillet, ni de post avec Anthony »

Confirmé côté outil : aucun fichier de ce shooting n'existe dans le dépôt ni
dans l'index médias. Les 21 photos indexées sont les barbiers, l'équipe et les
vues du salon — pas de modèle femme, pas de séquence Anthony.
⚠️ **À vérifier auprès de Maxime : ces rushes ont-ils été livrés ?** S'ils l'ont
été et ne sont jamais arrivés jusqu'ici, c'est une rupture dans la chaîne
d'ingestion, pas un oubli de production.

### Le volume réellement publié

Sur 31 jours (20/07 → 19/08), côté feed :

- **9 publications parties**, dont **un doublon** — le reel « Découvrez notre
  nouvel espace » publié deux fois, le 20/07 et le 21/07. Donc **8 contenus
  uniques**.
- **5 posts produits et jamais partis**, restés en brouillon non validé :
  bronzage 27/07, reel 04/08, août 07/08, **VIP 15 août** (périmé), coupes
  rentrée 17/08.
- Plusieurs stories dans le même cas (01, 08, 17, 18/08).

Autrement dit : **un tiers de la production est mort en brouillon.** La règle
« tout reste en brouillon, le client valide » est saine, mais elle n'a de sens
que si quelqu'un relance. Personne ne relançait. C'est ça que William ressent
comme « des réseaux si peu alimentés » — le travail existait, il ne sortait pas.

⚠️ **La prestation mensuelle contractée n'est pas renseignée** dans cette fiche
(champ « Prestation CM mensuelle : [à renseigner] », toujours vide). On ne peut
donc pas dire objectivement si 8 posts/mois est au-dessus ou en dessous de
l'engagement. **À combler en priorité** — pour ce client et pour tous les autres.

### 9 publications d'un AUTRE client garées dans ce compte

Le calendrier du Loft contenait **9 publications appartenant à Pierre Huiban** —
Hyrox, stations, sled push, « réunion comité de direction Europe », hashtags
`#LFG #LexisNexis` — datées du 17/06 au 15/07. Jamais publiées (brouillon), mais
présentes dans le calendrier que le client peut ouvrir.

IDs : `327013311, 327013312, 327013313, 327013314, 327013315, 327013317,
327013318, 327013326, 327013327`.

⛔ **Leur suppression a été bloquée par le garde-fou de sécurité de la session.**
Elles sont toujours là. À supprimer manuellement, ou lors d'une session avec la
permission de suppression groupée.

### Ce qui est récupérable tout de suite

Les 7 stories vidéo d'août ont été fabriquées **à partir des vraies photos** et
sont hébergées publiquement. Leur première image est la photo source, en
1080×1920 : vrais barbiers, vraie équipe, vrai néon LF, vrai salon. Elles sont
donc réutilisables immédiatement pour refaire le feed en attendant les
originaux — recadrage 4:5 possible sans perte de largeur.

Les originaux 2832×4240 restent sur le poste de Maxime (`medias/` est dans
`.gitignore`, donc absent de la session distante) : la refonte propre suppose
qu'ils soient poussés.

### Ce qui est corrigé à ce stade

- Les 4 posts armés en `autoPublish:true` + `draft:false` pour les 20→23/08 ont
  été neutralisés le 20/08 (voir `bonnes-pratiques-cm.md`).
- Compte vérifié : **40 publications, brouillon partout, autoPublish nulle part**,
  3 posts sans média (19, 21, 23/10).

### La leçon, et elle vaut pour tout le portefeuille

Le compte a été monté sur des visuels IA « en attendant les vraies photos ».
Les vraies photos sont arrivées le 15/07. Le provisoire n'a jamais été remplacé,
et un signal explicite écrit dans cette fiche le 30/07 est resté sans suite
pendant trois semaines.

**Règle qui en découle : dès que de vraies photos existent pour un compte
commercial, les visuels IA sont retirés du calendrier — pas mis en réserve,
retirés.** Un visuel IA sur un commerce réel n'est acceptable que tant qu'il
n'existe strictement aucune alternative, et jamais avec un visage.


---

## 🎭 CARROUSEL « FAUX DRAMA » — 28/08/2026

Maxime a envoyé la trend de **@teamoperou14_** (restaurant péruvien, Paris 14e)
et demandé de la reprendre pour Le Loft, en mettant en avant **le soin barbier
mais surtout le côté bien-être, head spa compris**.

### La mécanique de la trend, relevée sur le post source
Six planches. Une fausse accusation publique en capitales sur la première
(« VOUS ÊTES PARTIES SANS PAYER ! »), puis le prétexte sert à dérouler toute la
carte plat par plat, et la dernière planche révèle la blague : « IL N'Y A JAMAIS
EU DE SOFIA ET INÈS. On voulait juste trouver une excuse pour vous montrer nos
plats. » Le ressort est l'appât : on lit par curiosité de ragot, on reste pour
le produit.

### L'adaptation
Sept planches. Un client fictif est accusé d'être parti sans payer, et la liste
de ce qu'il a « pris » est le parcours complet du salon. La montée porte sur le
bien-être : la coupe et la barbe sont expédiées en deux planches, **le head spa
occupe le centre**, le soin visage suit, et la chute nomme l'offre entière.

| # | Photo | Titre |
|---|---|---|
| 1 | équipe dans le salon | il est parti sans payer |
| 2 | barbier, geste précis | il a commencé par la coupe |
| 3 | taille de barbe | puis il a pris la barbe |
| 4 | **le bac head spa** | **et là, il a demandé le head spa** |
| 5 | soin visage, masque | il a enchaîné sur le soin visage |
| 6 | barbier face objectif | il est reparti comme ça |
| 7 | équipe, vue large | ce client n'a jamais existé |

**Aucun nom inventé.** Le post source nommait deux clientes ; ici le client
reste anonyme. Sur un commerce de quartier, un prénom sur une accusation de vol,
même démentie à la planche 7, peut être attribué à un habitué réel.

### D'où viennent les photos
`medias/le-loft/` est ignoré par git et absent des conteneurs de session. Les
21 vraies photos du shooting du 15/07 **restent accessibles autrement** : les
sept stories vidéo d'août branchées sur le compte sont ces mêmes photos animées
en i2v, hébergées sur CloudFront. On extrait la première frame, et **on recadre
le bas en 4:5** parce que le texte des stories est incrusté en haut du cadre
9:16. Contrôle OCR du haut de chaque planche avant de brancher : aucun titre de
story ne doit survivre au recadrage.

Le mapping story vers thème a été retrouvé en lisant le texte incrusté à l'OCR,
pas en faisant confiance aux noms de fichiers.

### La composition
| | |
|---|---|
| Format | 1080×1350, le 4:5 du feed |
| Voile | noir #0E0E0E en dégradé, transparent à y=600, opaque à y=830 |
| Titre | Playfair Display bas-de-casse passé en capitales, doré **#CEAA69**, interlettré |
| Filet | doré, la signature graphique du compte |
| Corps | Libre Baskerville italique crème **#F0E6D8** |

Script : `scripts/loft-carrousel-trend.py`.

### Vérification (28/08/2026)
Post **366400245**, vendredi 28/08 à 18h, Instagram seul, `draft:true`,
`autoPublish:false`, 7 médias. Accents contrôlés à l'OCR sur les sept planches.

⚠️ `schedule_post` a refusé la création trois fois de suite (« You need to
include at least one provider »), en booléens comme en chaînes. C'est le
résolveur Zapier qui perd les indicateurs de réseau. **Passer par
`bulk_schedule_posts` puis `set_post_media_list`** : cette chaîne crée en
brouillon, à l'heure de Paris exacte, et accepte les sept médias d'un carrousel.

⚠️ Sept publications du 26/08 au 02/09 sont en `draft:false` / `autoPublish:true`.
Elles ne viennent pas de cette intervention : c'est la signature d'une
validation faite dans l'interface. À confirmer avec Maxime si ce n'est pas lui.


### 🎨 Version Canva restylable — 28/08/2026

Maxime a trouvé la première version « trop mainstream, basique, sans
originalité » et a demandé le carrousel dans Canva pour le retravailler. Le
problème de fond : dans la version Metricool, **le texte est incrusté dans le
pixel**, donc rien n'est restylable. La version Canva sépare les couches.

| | |
|---|---|
| Design | `DAHTTxdmbK0`, « Le Loft, carrousel il est parti sans payer » |
| Édition | https://www.canva.com/d/Vhf-e_sCZONE3z3 |
| Lecture | https://www.canva.com/d/iiYWzOHlM2ZEXjX |
| Structure | 7 pages 1080×1350. Par page : la photo en fond plein cadre, deux voiles noirs (transition + fond de texte), un filet doré, un titre et un corps de texte |
| Titre | 72 px gras **#CEAA69** |
| Corps | 32 px italique **#F0E6D8** |

Les photos sont les **mêmes vraies photos du salon**, mais **nues** : recadrées
4:5, sans texte ni voile incrustés. Elles sont dans la bibliothèque Canva sous
`Loft 1 equipe salon` à `Loft 7 equipe chute`. Tout est déplaçable, recolorable,
remplaçable.

⚠️ **`generate-design` ne produit qu'une seule page**, même pour un carrousel de
sept planches demandé explicitement. Il a aussi posé un fond généré par IA sur
la page 1, contraire à la règle du compte. La méthode fiable est de créer le
design puis d'ajouter les pages une à une avec `add_page`, `insert_fill`,
`insert_shape` et `add_text`, puis de styler avec `format_text` dans un second
appel (le `locator_id` n'existe qu'après création du texte).

⚠️ **Deux photos étaient interverties.** Le mapping story vers thème du 31/07
donnait `97e07089` pour le soin visage : c'est faux, c'est le barbier qui pointe
l'objectif, et le soin visage est `692cb848`. Corrigé dans le design. À
répercuter si ce mapping est réutilisé ailleurs.

À revoir à l'œil : la photo de la planche 2 (« il a commencé par la coupe »)
montre un barbier avec un téléphone, pas un geste de coupe. Elle vient du bas du
cadre 9:16 de la story « rasage à l'ancienne ». Si une vraie photo de coupe
existe dans `medias/le-loft/`, elle sera meilleure.

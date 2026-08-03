# Run On Invest (R.O.I.) — fiche client (onboardé 03/08/2026)

> **Source de vérité : le brief client** (plateforme de marque V2.1, fourni par Maxime le 03/08/2026).
> Tout contenu doit le respecter à la lettre. Cette fiche n'en est que le résumé opérationnel.

## Identité
- blogId Metricool : **6636615** (l'ancien « brand sans nom » de la passation — mystère résolu)
- Réseaux : **Instagram uniquement** (@runoninvest). Logo posé dans Metricool en août.
- Concept : course + rencontre **réservée aux entrepreneurs et indépendants** — 5 ou 10 km à son rythme, puis un vrai temps d'échange. Ni club de running, ni afterwork.
- Signature : *On court d'abord. On parle ensuite.* (sur visuels : *Courir d'abord. Parler ensuite.*)
- Descripteur verrouillé au logo : COURSE & NETWORKING — ENTREPRENEURS

## Ligne éditoriale
- **3 piliers** (chaque post s'appuie sur au moins un) : 1. l'effort crée le lien · 2. zéro pitch · 3. la régularité paie.
- **Ton** : tutoiement TOUJOURS, phrases courtes, du concret (distances, horaires, places), marque de sport pas cabinet. **Max 1 emoji, max 5 hashtags.**
- **Interdits** : « networking premium », « écosystème », « disruptif », vocabulaire de club fermé, promesses de business, jargon sportif d'initié (VMA, seuil, fractionné), vouvoiement.
- Exemple validé à imiter : « Samedi, 8h30. 5 ou 10 km. Puis un petit-déj où personne ne pitche. 30 places, c'est tout. »

## DA (typographique par design — les cartes typo sont l'identité, pas un pis-aller)
- Couleurs : Blaze `#FF4A17` (accent unique) · Encre `#111111` · Écru `#EDE7DD` (fond défaut) · Craie `#F7F4EF` · Béton `#8C877E` · Braise `#D93A0E` (rare). Équilibre 55 % Écru / 30 % Encre / 15 % Blaze.
- 3 familles de visuels jamais mélangées : fond Écru / fond Encre / aplat Blaze.
- Contraste : jamais de Blaze en petit corps sur Écru ; l'orange = aplat, gros titre ≥40 px, ou texte sur Encre.
- Typos (Google Fonts) : **Archivo Expanded 900** (titres capitales, interlettrage −3,5 %, pleine largeur) · **Space Mono** (mentions techniques : horaires, distances, GPS) · Archivo 400/500 (corps).
- Constantes : logo haut-gauche marge 6,5 % · mentions mono haut-droite · barre Blaze 8 px · grain 26 % · stories : 200 px de zone libre haut et bas.

## ⛔ Confidentialité (brief §6)
- **Négociations sponsors (« Projet Foulée ») : rien ne se publie** tant qu'un partenariat n'est pas signé ET validé pour annonce.
- **Arena 2027 (La Défense) : zéro teasing** sans validation explicite de Maxime — ni lieu, ni dates, ni jauge, ni prix.
- Jamais de budgets, jauges prévisionnelles, chiffres financiers.

## ⚠️ Données factuelles — RIEN de confirmé au 03/08/2026
Dates d'édition, ville/lieu, fréquence (mensuelle pressentie), jauge (30 vs 80 à trancher), URL d'inscription, handle définitif : **tout est à confirmer**. Les valeurs des gabarits du kit (12 sept., Tête d'Or, 45.7797°N, Camille Roussel, 73 %…) sont **fictives — ne jamais les publier**. Règle : placeholder `[À CONFIRMER : …]` + signalement, jamais d'invention.

## Calendrier — Phase teasing (démarrage 03/08/2026 au soir) ✅ ACTIF
**18 brouillons Instagram vérifiés** (`draft:true`, `autoPublish:false`, média présent sur chacun) : 9 posts feed + 9 stories, du 03/08 au 21/08.

### Posts feed — lun/mer/ven (03/08 20h00 puis 08h00)
| Date | id | Visuel | Angle |
|---|---|---|---|
| 03/08 20:00 | 357485089 | f1 aplat Blaze | Ouverture — « Quelque chose démarre » |
| 05/08 08:00 | 357485140 | f2 fond Encre | Ce que ce n'est pas |
| 07/08 08:00 | 357485169 | f3 fond Écru | Pour qui ? |
| 10/08 08:00 | 357484441 | f4 fond Encre | Concept complet |
| 12/08 08:00 | 357484464 | f5 fond Écru | Pilier 01 — l'effort crée le lien |
| 14/08 08:00 | 357484489 | f6 aplat Blaze | Pilier 02 — zéro pitch |
| 17/08 08:00 | 357484523 | f7 fond Écru | Pilier 03 — la régularité paie |
| 19/08 08:00 | 357484576 | f8 fond Encre | Punchline — 3 cafés ou 1 heure de course |
| 21/08 08:00 | 357484595 | f9 fond Écru | Le format-type |

### Stories — mêmes jours, 12h00 (03/08 à 20h30)
9 stories vidéo **toutes différentes** (ids 357483920, …931, …953, …978, …985, …990, 357484000, …019, …034) : Ça démarre · Ni club ni afterwork · Pour les entrepreneurs · On court d'abord · Au 3e km · Zéro pitch · La régularité paie · 5 ou 10 km · Le format.
- **Cadence 3/semaine assumée** (les jours de post) tant que le compte n'a pas d'audience : la règle « aucune story identique sur 2 semaines » est respectée par construction — les 9 sont uniques sur toute la période.

### Fabrication des visuels — `roi_gen.py`
- Cartes typographiques PIL en DA stricte : Archivo Expanded 900 (titres, interlettrage −3,5 %) + Space Mono (mentions), 3 familles jamais mélangées (Écru / Encre / aplat Blaze), logo haut-gauche marge 6,5 %, mention mono haut-droite, barre Blaze, grain 26 %, zones libres 200 px haut/bas en story.
- **Stories = animation ffmpeg** (push-in lent 1→1,06, barre Blaze qui se déploie, fondus) + fond sonore procédural `roi.wav` (cadence de foulée ~168 BPM, oscillateurs purs — zéro sample tiers, zéro modèle génératif, zéro droits).
- **Zéro IA générative, zéro photo** : conforme à la règle stories, et cohérent avec le brief qui fait de la typo l'identité de la marque. À remplacer par de vraies photos animées dès la première édition (cf. règle générale).
- Feed 1080×1350, stories 1080×1920, rendus depuis un master 1350 px.

### Pièges rencontrés (à ne pas réapprendre)
- ⚠️ **`bulk_schedule_posts` ignore `media_url`** → il crée des posts SANS média, or Instagram refuse un post sans média. Utiliser **`bulk_replace_posts`** (qui, lui, envoie bien `media`) ou corriger juste après par un replace. Vérifier systématiquement par listing.
- Passer `networks: ["instagram"]` explicitement : sans ce paramètre les code actions ajoutent Facebook par défaut (les 6 posts d'origine étaient en IG+FB à tort, corrigés le 03/08).

### Reste à faire
- Pas de témoignage ni de citation participant : l'événement n'a pas eu lieu — rien à citer sans inventer.
- Remplacer les placeholders `[À CONFIRMER : …]` dès que Maxime a les infos d'édition (date, ville, lieu, fréquence, jauge, URL).

## Tarifs / ROI
- Modèle économique non communiqué (billetterie ? sponsors ?) — pas de module ROI. À revoir quand le brief s'étoffera.

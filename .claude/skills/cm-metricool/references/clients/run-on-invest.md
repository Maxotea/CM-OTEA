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

## ⛔ Confidentialité (brief §6) — mise à jour du 04/08/2026
- ✅ **LIEU DÉVERROUILLÉ par Maxime le 04/08** : la course se déroule à **La Défense**, le temps de networking à la **Plénitude Arena**. Publiable.
- **Négociations sponsors (« Projet Foulée ») : rien ne se publie** tant qu'un partenariat n'est pas signé ET validé pour annonce.
- **Toujours verrouillé sur l'Arena** : ni **dates**, ni **jauge**, ni **prix**. Le déverrouillage du 04/08 porte sur le lieu, rien d'autre.
- Jamais de budgets, jauges prévisionnelles, chiffres financiers.

## ⚠️ Données factuelles
- ✅ **Confirmé 04/08** : lieu de la course = La Défense · lieu du networking = Plénitude Arena.
- ❌ **Toujours à confirmer** : dates d'édition, heure, fréquence (mensuelle pressentie), jauge (30 vs 80 à trancher), URL d'inscription, handle définitif. Placeholder `[À CONFIRMER : …]` obligatoire, jamais d'invention.
- Les valeurs des gabarits du kit (12 sept., Tête d'Or, 45.7797°N, Camille Roussel, 73 %…) sont **fictives — ne jamais les publier**.

## 🖼️ Visuels : photos IA ultra réalistes autorisées (04/08/2026)
Maxime autorise les **photos IA ultra réalistes** sur ce compte, **feed et stories**, en remplacement des cartes typographiques.
- **Limite absolue maintenue : aucune personne réelle identifiable.** Coureurs génériques, plans larges ou de dos, pas de visage reconnaissable en gros plan. On ne génère jamais le visage d'un client, d'un participant ou de Maxime.
- Direction : La Défense au petit matin — parvis, tours de verre, lumière rasante. Palette compatible kit (Écru/Encre, accent Blaze discret). L'habillage typographique du kit reste posé par-dessus (`scripts/roi-photo-habillage.py` — feed et calque story).
- Stories : photo IA → i2v `kling3_0_turbo` → **muet** (règle stories sans son).
- L'exception ne vaut que pour ce compte, tant qu'aucune édition n'a eu lieu et qu'il n'existe aucune vraie photo.

## Calendrier — état réel au 19/08/2026 ⚠️

**Le teasing d'août est épuisé.** Les 18 brouillons du 03 au 17/08 n'ont jamais
été validés dans l'interface : leurs créneaux sont passés, Metricool les a
retirés. Il ne reste que 4 brouillons, tous en photo IA :

| Date | id | Type |
|---|---|---|
| 19/08 12:00 | 363855795 | Story photo IA — « 5 ou 10 km. Ton rythme. » (muette) |
| 19/08 18:00 | 363855131 | Feed — « Trois cafés. Ou une heure de course. » |
| 21/08 12:00 | 363855807 | Story photo IA — « Le format » (muette) |
| 21/08 08:00 | 363855142 | Feed — « Le format, simple. » |

Le créneau feed du 19/08 08:00 était déjà passé : replanifié à 18:00 le jour même.

**À décider avec Maxime :** relancer une vague en septembre. 7 des 9 photos IA
générées le 19/08 (La Défense au petit matin) sont inutilisées et prêtes.
Habillage typographique : `scripts/roi-photo-habillage.py` (feed 1080×1350 +
calque story 1080×1920, mention « LA DÉFENSE » en haut à droite).

### Fabrication des visuels — `scripts/roi-visuels.py` (cartes typo) et `scripts/roi-photo-habillage.py` (photos IA)
- Cartes typographiques PIL en DA stricte : Archivo Expanded 900 (titres, interlettrage −3,5 %) + Space Mono (mentions), 3 familles jamais mélangées (Écru / Encre / aplat Blaze), logo haut-gauche marge 6,5 %, mention mono haut-droite, barre Blaze, grain 26 %, zones libres 200 px haut/bas en story.
- **Stories = animation ffmpeg** (push-in lent 1→1,06, barre Blaze qui se déploie, fondus), **sans aucune bande son** — `-an` obligatoire au montage (`.claude/memories/stories-sans-son.md`). Le `roi.wav` procédural de la première version n'est plus utilisé.
- Les cartes typo restent valables comme famille de visuels. Depuis le 04/08 elles cohabitent avec les **photos IA** autorisées sur ce compte (voir plus haut). À remplacer par de vraies photos dès la première édition.
- Feed 1080×1350, stories 1080×1920, rendus depuis un master 1350 px.

### Pièges rencontrés (à ne pas réapprendre)
- ⚠️ **`bulk_schedule_posts` ignore `media_url`** → il crée des posts SANS média, or Instagram refuse un post sans média. Utiliser **`bulk_replace_posts`** (qui, lui, envoie bien `media`) ou corriger juste après par un replace. Vérifier systématiquement par listing.
- Passer `networks: ["instagram"]` explicitement : sans ce paramètre les code actions ajoutent Facebook par défaut (les 6 posts d'origine étaient en IG+FB à tort, corrigés le 03/08).

### Reste à faire
- Pas de témoignage ni de citation participant : l'événement n'a pas eu lieu — rien à citer sans inventer.
- Remplacer les placeholders `[À CONFIRMER : …]` dès que Maxime a les infos d'édition (date, ville, lieu, fréquence, jauge, URL).

## Tarifs / ROI
- Modèle économique non communiqué (billetterie ? sponsors ?) — pas de module ROI. À revoir quand le brief s'étoffera.

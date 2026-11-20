---
name: credit-photographe-home-sanfaute
description: Toute photo de Jean-Philippe Homé-Sanfaute (fichiers HOME-SANFAUTE-*) le crédite dans le post, avec son compte Instagram
type: feedback
---

**Règle (Maxime, 06/11/2026, sur le retour de Jean-Philippe) :** chaque post qui utilise une
photo de Jean-Philippe Homé-Sanfaute le crédite, avec la mention de son compte Instagram.

**Why :** ce sont ses photos (shooting commandé par OTEA, mais l'auteur reste lui). Il l'a fait
remarquer, il a raison. C'est aussi un partenaire : il apporte des clients à OTEA (mise en
relation Pure Ocean du 22/10/2026), le citer entretient la relation.

**How to apply :**
- **Reconnaître ses photos** : `drive_nom` qui commence par `HOME-SANFAUTE` (nomenclature de ses
  livraisons, ex. `HOME-SANFAUTE-260702-103350-00186.jpg`), ou champ `credit` à son nom dans
  `photos/otea-production.json` et `photos/otea-filmakers.json` (clés 01 à 46). 42 photos au
  06/11/2026. Les 5 photos « séance studio, photographe à confirmer » restent à vérifier avec Maxime.
- **Formule donnée par Jean-Philippe (message du 06/11/2026)** : sur LinkedIn,
  `Photos : @Jean-Philippe Homé-Sanfaute`, en tapant le @ dans LinkedIn et en choisissant son
  profil dans la liste, sinon le tag ne prend pas (un texte envoyé par Metricool reste du texte).
  Sur Instagram, `Photos : @compte` ; compte pas encore donné, donc nom seul en attendant.
- **Légende (carrousel, post simple, reel avec ses photos)** : ligne en fin de légende, avant
  les hashtags. Une légende qui part sur Instagram et LinkedIn à la fois prend la formule
  Instagram ; `carrousel.py` rappelle de corriger la ligne côté LinkedIn. `scripts/carrousel.py`
  l'ajoute tout seul dès qu'une slide utilise une de ses photos. Pour un post écrit à la main
  (cm-metricool), l'ajouter soi-même.
- **Story** : pas de légende, donc sticker mention de son compte. `scripts/story-photo.py`
  affiche `CRÉDIT À POSER` quand la photo est à lui ; le rappeler dans le texte du brouillon.
- **Son compte** : `photos/photographes.json`, champ `instagram` (sans le @). Seule source :
  ne jamais le recopier ailleurs ni le deviner. Tant qu'il est vide, crédit par le nom seul et
  avertissement au rendu.
- Crédit du PDF `_credit-photos-HOME-SANFAUTE_Jean-Philippe.pdf` (swisstransfer, Mac de Maxime)
  : s'il impose une formule différente, c'est elle qui fait foi, à reporter dans `credits.py`.

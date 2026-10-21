# MAKE PEOPLE — stratégie de communication & de déploiement

> Périmètre : lancement public du jeu (web d'abord, makepeople.net), réseaux
> sociaux organiques, France en premier. Aligné sur `ROADMAP-ECOSYSTEME.md`
> (« le jeu doit naître d'une audience, pas l'inverse »).

## 1. Positionnement

**Le jeu de ta vie.** MAKE PEOPLE transforme les rituels du matin en odyssée :
XP dans la vraie vie, carte de héros qui se réédite, et une progression qui va
de ton île jusqu'aux étoiles.

- **Cible primaire** : 20-40 ans francophones déjà sensibles au développement
  personnel doux (Miracle Morning, journaling, habit trackers) mais fatigués
  des apps culpabilisantes. C'est l'angle différenciant n°1 : *le seul jeu
  d'habitudes conçu pour ne jamais te faire honte* (pirogues de secours,
  retour bienveillant « les étoiles n'ont pas bougé »).
- **Différenciation n°2** : les **étoiles-guides** — les joueurs avancés
  éclairent anonymement ceux qui commencent. Personne d'autre ne l'a ;
  c'est LA mécanique à montrer dès que le social sera visible à l'écran.
- **Promesse courte** (bios, descriptions) : « Ta vie tient en 4 jauges.
  Rituels du matin, XP, carte de héros. » (pas de promesse de prix dans la
  com' : l'app a vocation à devenir payante à moyen terme)
- **Ton** : chaleureux, aventureux, bienveillant — jamais d'injonction,
  jamais de « productivité ». On parle d'odyssée, d'escales, d'étoiles.

## 2. La vidéo hero (livrée avec cette stratégie)

| Élément | Valeur |
|---|---|
| Format | 9:16 vertical, 1080×1920, ~40 s |
| Structure | Hook chiffré (4 jauges) → 3 étapes (rituels / progression / odyssée) → cliffhanger (« devenir l'étoile ») → CTA unique (makepeople.net, gratuit) |
| Style | Grammaire visuelle verrouillée du site (storybook encré, palette orange brûlé/encre/crème/sauge/or) — continuité totale site ↔ pub |
| Voix | **Maxime, posée à la publication** — le master v2 est livré sans piste audio ; script 94 mots (🟢 95/100 au lint rétention) en téléprompteur, timings ligne à ligne dans `captions.tsv` |
| Musique | **Choisie par Maxime dans l'app à la publication** (son tendance Instagram/TikTok, volume bas sous la voix) — meilleur reach que toute musique embarquée |
| Sous-titres | Non incrustés (choix) — au besoin, sous-titres automatiques de la plateforme |
| Prix | **Aucune mention de gratuité** dans la vidéo ni les légendes (montée en payant prévue à moyen terme) |
| Fichiers | `marketing/video/` : master MP4 v2, script, timeline ; storyboard dans `marketing/storyboard/` |

**Déclinaisons à tirer du master** (montage par simple recoupe, aucun
retournage) :
- **Cut 15 s** (hook + odyssée + CTA) pour la 2ᵉ semaine.
- **3 variantes de hook** déjà écrites dans `marketing/video/SCRIPT.md`
  pour A/B tester la première seconde sans changer le reste.
- **Boucle muette 20 s** (plans seuls + texte) pour épingle de profil / site.

## 3. Écosystème de comptes

| Plateforme | Compte | Rôle | Cadence cible |
|---|---|---|---|
| Instagram Reels | compte dédié MAKE PEOPLE (à créer) + relais Otea Production | Canal principal FR, lien bio → makepeople.net | 3 reels/sem |
| TikTok | compte dédié | Reach froid, hooks testés ici d'abord | 3-4/sem (mêmes reels) |
| YouTube Shorts | chaîne MAKE PEOPLE | Longue traîne + futur long format | 2-3/sem (repost) |
| LinkedIn (perso Maxime) | build in public | Crédibilité, partenariats marques (trésors sponsorisés) | 1 post/sem |

Règle : **une seule production, quatre distributions.** Tout reel est tourné
une fois, décliné partout, légendes adaptées (voir §7).

## 4. Ligne éditoriale — 4 piliers

1. **L'odyssée documentée (40 %)** — Maxime documente SA propre odyssée :
   vrais rituels du matin, vraie série, vraie carte de héros qui monte.
   C'est le canal d'acquisition prévu par la roadmap : le jeu comme point de
   chute des contenus Miracle Morning, pas l'inverse.
2. **Le jeu-produit (25 %)** — trailer, plans du monde, nouveautés
   (le manu, les pirogues de secours, les trésors). Style storybook verrouillé.
3. **La méthode (25 %)** — valeur pure : SAVERS, humeur, gratitudes,
   micro-habitudes de 5 minutes. Ce pilier recrute la cible avant même de
   parler du jeu.
4. **La communauté-étoiles (10 %, croît avec la base)** — lumières laissées
   par les joueurs (anonymes, avec accord), jalons (« 1 000 membres de
   l'équipage fondateur »), réponses en commentaires.

## 5. Calendrier de déploiement

### Phase 0 — Amorçage (S-4 → S0, avant tout lancement public)
- Publier les 2 premiers reels « odyssée documentée » + 1 reel méthode par
  semaine sur les comptes fraîchement créés (rodage algorithme + preuve
  sociale minimale avant le trailer).
- Vérifier les prérequis roadmap **bloquants pour un lancement public** :
  politique de confidentialité + export/suppression des données (RGPD),
  événements analytics minimaux (D1/D7/D30) — sans eux on lance à l'aveugle.
- Préparer la page d'atterrissage : le site-odyssée existant + bloc
  « Équipage fondateur » visible.

### Phase 1 — Lancement (S0 → S+2)
- **J0** : trailer hero sur les 4 canaux à 18 h-19 h (pic FR), épinglé partout.
  CTA unique : jouer sur makepeople.net + rejoindre l'Équipage
  fondateur (tarif fondateur promis — l'urgence honnête).
- **J+2 → J+14** : 1 contenu/jour en alternant les piliers (jamais deux
  fois « produit » d'affilée). Le cut 15 s part à J+7 avec la 2ᵉ variante
  de hook.
- Répondre à **100 % des commentaires** pendant 14 jours (signal algorithme
  + premiers membres d'équipage = premiers ambassadeurs).

### Phase 2 — Rythme de croisière (S+2 → bêta stores)
- Cadence §3 tenue ; chaque fin de mois : 1 reel « bilan d'odyssée » avec
  les chiffres réels (inscrits, lumières laissées, séries tenues) — la
  transparence est cohérente avec la marque.
- Batch mensuel : 1 session de production = 12-15 reels (pipeline §8).
- Quand la bêta iOS/Android (phase 3 roadmap) approche : rebascule du CTA
  vers la liste TestFlight, puis re-lancement « stores » avec un 2ᵉ trailer
  (mêmes plans, fin différente : « télécharge-le »).

## 6. KPI — on mesure les leads, pas la portée

| Étape | Indicateur | Seuil d'alerte |
|---|---|---|
| Vidéo | Rétention 3 s (hook) et complétion | < 50 % à 3 s ⇒ changer de variante de hook |
| Trafic | Clics lien bio → makepeople.net | — |
| Activation | Comptes créés / visiteurs | < 20 % ⇒ problème de landing, pas de vidéo |
| **Cœur** | **Inscriptions Équipage fondateur** (mesurables en D1) | objectif : 100 avant la bêta stores |
| Rétention | D1/D7/D30 (dès analytics posés) | — |

Pas de budget pub payant en phase 0-1 : l'organique valide le message
d'abord. Si un reel dépasse nettement les autres, alors seulement :
50-100 € de boost sur CE reel pour tester l'acquisition payée.

## 7. Légendes prêtes à poster (trailer J0)

**Instagram / TikTok**
> Et si ta vie était un jeu — sans la culpabilité ?
> Rituels du matin, XP sur tes vraies journées, une carte de héros qui
> évolue avec toi. Et quand tu rates un jour : une pirogue de secours,
> pas une punition. ⛵
> 🎮 Lien en bio. Les 100 premiers rejoignent l'Équipage fondateur.
> #miraclemorning #habitudes #developpementpersonnel #routinematinale #jeu

**YouTube Shorts** : même texte sans hashtags, + lien cliquable en
description.

**LinkedIn (Maxime)**
> J'ai passé [X] mois à construire un jeu où l'XP se gagne dans la vraie
> vie. Voici pourquoi (et le trailer). → makepeople.net

## 8. Pipeline de production (répétable)

Cette vidéo a établi l'usine ; chaque reel suivant coûte ~30 min + ~350
crédits Higgsfield max :
1. Script : skills maison `reel-script` → `reel-lint` (seuil : 🟢 ≥ 80).
2. Keyframes : Recraft V4.1, préambule de style **byte-identique** au
   design-brief + palette hex verrouillée (`app/design-brief.md`).
3. Animation : Seedance 2.0, image→vidéo 1080p 9:16, audio off.
4. Voix : Maxime à la publication (gabarit de timing IA en option pour
   caler le montage, une ligne par section).
5. Montage : CI GitHub — commit de `marketing/video/timeline.json` ⇒ le
   workflow `render-video` exécute `build.sh` (normalisation, fondus,
   title card Forma DJR, inserts cartes réelles, mix VO, sous-titres
   incrustés + `.srt`) et committe le master + les frames de contrôle.
6. Rapatriement d'assets à l'unité : commit de
   `marketing/media-manifest.json` → le workflow `fetch-media` ramène tout
   dans le repo (vignettes storyboard, etc.).

## 9. Risques & garde-fous

| Risque | Garde-fou |
|---|---|
| Voix à poser sur chaque publication (dépendance à Maxime) | Le téléprompteur + timings (`SCRIPT.md`, `captions.tsv`) rendent la prise rapide ; gabarit VO IA possible en dépannage pour les déclinaisons |
| Dépendance à un seul canal | 4 plateformes dès J0, la liste e-mail (équipage fondateur, D1) est le seul actif possédé |
| Données humeur = quasi-santé | Jamais de ciblage pub sur ces signaux ; pas de retargeting santé ; RGPD réglé avant lancement (roadmap) |
| Burn-out de production | Batch mensuel + pipeline §8 ; 60 % du contenu (odyssée + méthode) se tourne au téléphone sans production lourde |
| Le trailer surpromet le social | Les étoiles-guides sont v1 : dans la com', montrer ce qui existe (laisser une lumière), pas un réseau social complet |

## 10. Qui fait quoi

- **Seul Maxime peut** : créer les comptes sociaux dédiés, publier (comptes
  personnels), choisir la musique tendance in-app, valider le tarif
  fondateur affiché en légende.
- **Automatisable ensuite** (agence/skills existants) : calendrier,
  scripts, lint, génération des plans, montage, reporting mensuel.

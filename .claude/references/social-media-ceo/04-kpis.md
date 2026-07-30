# SOCIAL MEDIA CEO — Dictionnaire KPI

La base `KPIS` porte environ 200 champs. Une ligne = un mois.
Chaque ligne est reliée au mois précédent et au mois suivant (calcul des
évolutions) et au mois comptable.

Deux natures de champ :
- **saisie** (`number`) — la donnée brute relevée dans les plateformes ;
- **affichage** (`formula`) — le rendu formaté ou le calcul dérivé.
  Un champ dont le nom contient « (affichage) » ne se remplit jamais à la main.

---

## Les 6 regroupements

| Bloc | Contenu |
|---|---|
| **FINANCIER** | CA du mois, CA mois précédent, Évolution CA, Revenu moyen, Devis envoyés, Factures envoyées, Taux de conversion devis / facture |
| **MARKETING - COMMERCIAL** | Nombre de leads, Taux de conversion de leads, Coût par lead, Nombre de calls prospects, Nombre de cold emails, Nouveaux clients, ROI marketing, ROI, Impressions publicitaires, Clics publicitaires, Taux de clics publicité (CTR) |
| **MARKETING - EMAILS** | Emails collectés, Taux d'ouverture des emails, Taux de clics dans les emails |
| **RÉSEAUX SOCIAUX** | la grille plateforme × métrique (ci-dessous) |
| **OPÉRATIONNEL** | Nombre de tâches complétées, Nombre de projets terminés, Durée moyenne des projets |
| **RELATIONS** | Nombre d'interactions clients |

---

## La grille réseaux sociaux

7 plateformes — préfixes utilisés dans les noms de champs :

| Préfixe | Plateforme |
|---|---|
| `IG` | Instagram |
| `LK` | LinkedIn |
| `FB` | Facebook |
| `X` | X / Twitter |
| `YT` | YouTube |
| `TikTok` | TikTok |
| `PN` | Pinterest |

10 métriques par plateforme :

| Métrique | Nature |
|---|---|
| Fans | saisie |
| Impressions totales | saisie |
| Vidéos vues totales | saisie |
| Likes | saisie |
| Commentaires | saisie |
| Reach moyen organique | saisie |
| Top Impressions / vues | saisie |
| Top taux d'engagement organique | saisie |
| Taux d'engagement organique | calcul |
| Interactions moyennes par post | calcul |
| Nombre de post | calcul (compté depuis la base `Contenu`) |

Chaque métrique existe en double : la valeur brute et sa version « (affichage) ».

> **Ce qu'il faut vraiment relever chaque mois par plateforme :**
> fans, impressions, vidéos vues, likes, commentaires, reach moyen, meilleur post
> (impressions + taux d'engagement). Le reste se calcule.

---

## Le rituel mensuel de KPI

1. Créer la ligne du mois dans `KPIS` (bloc « AJOUTER LE MOIS POUR LE CALCUL DES KPIs »).
2. Relier au mois précédent et au mois comptable.
3. Relever les 7 saisies par plateforme active — les plateformes non utilisées
   restent vides, pas à zéro (sinon les moyennes sont faussées).
4. Saisir emails / publicité si applicable.
5. Vérifier que Tâches, Projets, Contenus, Devis-factures, Échanges du mois sont
   bien reliés à la ligne (sinon les compteurs opérationnels sont faux).
6. Lire les blocs FINANCIER / MARKETING / OPÉRATIONNEL du Suivi KPIs.
7. Reporter dans les `Key results` concernés → comparer aux paliers Moyen / Bien / Wow.

**Côté clients** : les analyses mensuelles ne vivent pas ici mais dans la page
« Analyse » de chaque portail client. La base `Analyse par post` est le lien entre
les deux.

---

## Lecture : quoi regarder d'abord

| Signal | Où | Ce qu'il dit |
|---|---|---|
| Évolution CA | FINANCIER | la seule métrique qui compte à la fin |
| Taux de conversion devis / facture | FINANCIER | problème d'offre ou de prix si bas |
| Taux d'engagement organique par plateforme | RÉSEAUX SOCIAUX | qualité du contenu, à comparer mois à mois et pas entre plateformes |
| Reach moyen organique | RÉSEAUX SOCIAUX | portée réelle, indépendante du nombre de posts |
| Top post du mois | RÉSEAUX SOCIAUX | matière première du recyclage |
| Nombre de post | RÉSEAUX SOCIAUX | régularité — à croiser avec le reach avant de conclure |
| Durée moyenne des projets | OPÉRATIONNEL | dérive de rentabilité |

Piège classique : comparer un taux d'engagement Instagram à un taux LinkedIn.
Les dénominateurs diffèrent. Ne comparer qu'une plateforme à elle-même.

---
name: smc-kpi-review
description: Clôture et lecture des KPIs mensuels SOCIAL MEDIA CEO — quelles métriques relever par plateforme (IG, LK, FB, X, YT, TikTok, Pinterest), comment les rattacher au mois, comment lire l'évolution et mettre à jour les key results contre les paliers Moyen/Bien/Wow. Utilise ce skill quand l'utilisateur veut faire son bilan du mois, analyser ses performances ou celles d'un client, comprendre un taux d'engagement, préparer un reporting client, ou parle d'OKR, de key results ou d'objectifs à réviser.
---

# Revue KPI — SOCIAL MEDIA CEO

Référentiel : `.claude/references/social-media-ceo/04-kpis.md`.

## Principe

Une ligne de la base `KPIS` = un mois. Elle est reliée au mois précédent (calcul
des évolutions) et au mois comptable. Six blocs : FINANCIER, MARKETING-COMMERCIAL,
MARKETING-EMAILS, RÉSEAUX SOCIAUX, OPÉRATIONNEL, RELATIONS.

Les champs dont le nom contient « (affichage) » sont des formules : **ne jamais
les remplir à la main**.

## Ce qu'il faut relever chaque mois, par plateforme

Préfixes : `IG` Instagram · `LK` LinkedIn · `FB` Facebook · `X` · `YT` YouTube ·
`TikTok` · `PN` Pinterest.

Sept saisies par plateforme active :

1. Fans
2. Impressions totales
3. Vidéos vues totales
4. Likes
5. Commentaires
6. Reach moyen organique
7. Top Impressions/vues + Top taux d'engagement organique (le meilleur post)

Le taux d'engagement, les interactions moyennes par post et le nombre de posts
sont calculés.

**Une plateforme non utilisée reste vide, pas à zéro.** Un zéro fausse les
moyennes et les évolutions.

## Séquence de clôture

1. Créer la ligne du mois, relier au mois précédent et au mois comptable.
2. Saisir les métriques sociales (ci-dessus).
3. Saisir emails (collectés, taux d'ouverture, taux de clics) et publicité
   (impressions, clics) si applicable.
4. **Vérifier les rattachements** : Tâches, Projets, Contenus, Devis & factures,
   Recettes & dépenses, Suivi des échanges du mois doivent pointer vers cette
   ligne. Sinon les compteurs opérationnels et financiers sont faux — c'est
   l'erreur la plus fréquente.
5. Lire les trois blocs de synthèse du Suivi KPIs.
6. Reporter les résultats dans les `Key results` concernés.

## Lire les chiffres

Ordre de lecture :

| Rang | Métrique | Ce qu'elle dit |
|---|---|---|
| 1 | Évolution CA | la seule qui tranche |
| 2 | Taux de conversion devis / facture | problème d'offre ou de prix si bas |
| 3 | Reach moyen organique par plateforme | portée réelle, indépendante du volume |
| 4 | Taux d'engagement organique | qualité du contenu |
| 5 | Top post du mois | matière du recyclage |
| 6 | Nombre de post | régularité, à croiser avec le reach |
| 7 | Durée moyenne des projets | dérive de rentabilité |

**Deux règles de prudence :**

- Ne jamais comparer un taux d'engagement entre plateformes — les dénominateurs
  diffèrent. Comparer une plateforme à elle-même, mois après mois.
- Un mois isolé ne dit rien. Toujours regarder la tendance sur 3 mois avant de
  conclure quoi que ce soit.

Quand un chiffre baisse, chercher d'abord une explication mécanique (moins de
posts, changement de format, mois court, saisonnalité) avant de conclure à un
problème de contenu.

## Key results — les trois paliers

Un key result porte `Attente Moyen`, `Attente Bien`, `Attente Wow`, une valeur de
départ, et un mode de calcul `DELTA` (progression) ou `CUMUL` (accumulation).

À la clôture : renseigner le résultat, situer contre les trois paliers, et
signaler explicitement le palier atteint. Ne pas cocher `Atteint ?` avant le
palier `Bien`.

## Reporting client

Les analyses mensuelles clients ne vivent **pas** dans `KPIS` mais dans la page
« Analyse » du portail client concerné. La base `Analyse par post` fait le lien.

Un reporting client se construit avec : évolution des fans, reach, taux
d'engagement, top 3 des posts, répartition par pilier, et ce qui est proposé pour
le mois suivant. Rester factuel sur les chiffres, ne pas surinterpréter une
variation inférieure à ~10 %.

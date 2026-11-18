# Lecture media buyer : décider avec peu de budget

La méthode de pilotage chiffré des campagnes, pour les comptes à petit budget
(5 à 20 € par jour). L'outil : `scripts/ads_analyse.py`. Les seuils de
comparaison : `campagnes/reperes.json`, chacun avec sa source.

## Le constat qui commande tout

Avec 42 € sur une semaine, un test A/B sur le CTR ne veut rien dire. Exemple
calculé par `ads_analyse.py taille` : pour voir un CTR de 1,5 % passer à
1,95 % (+30 %), il faut environ 13 000 impressions par pub, soit près de
160 € au CPM de 6 €. Sous ce volume, l'écart entre deux pubs est du hasard.

Conséquences, sans exception :

1. **Une campagne, un ensemble, une ou deux pubs.** Pas d'éclatement par
   audience ni par placement : chaque division coupe un budget déjà maigre et
   empêche Meta de sortir de l'apprentissage.
2. **On juge sur le résultat business, pas sur le CTR.** Le chiffre qui
   compte est le coût par prospect qualifié (message, DM, commentaire qui
   demande une date ou un devis), relevé à la main dans la boîte de réception
   et passé au script avec `--prospects N`. Les clics renseignent, ils ne
   décident pas.
3. **On teste une seule chose par campagne, d'une campagne à la suivante.**
   L'angle (vœux, séminaire, vacances), le format (post boosté, pub avec
   bouton Message), le visuel (photo, reel). Chaque bilan note ce qui a été
   testé et ce qu'on en retient, dans `meta.journal` de la spec.
4. **On cumule les apprentissages.** Après chaque campagne terminée, les
   chiffres mesurés (CTR, CPM, coût par prospect) entrent dans
   `campagnes/reperes.json` avec leur source. C'est ainsi que le compte se
   construit un repère propre au lieu d'un chiffre de mémoire.

## Le circuit de lecture

| Moment | Relevé à faire dans la session | Commande |
|---|---|---|
| J+1 | `ads_get_ad_entities` niveau `ad`, `date_preset: maximum`, champs de `reporting.md` + `effective_status` | `diagnostic` : diffuse ou pas, rythme de dépense |
| J+3 | même relevé | `diagnostic` : premières tendances, aucune décision |
| J+7 | même relevé + prospects relevés à la main | `diagnostic --prospects N` : le verdict |
| fin | même relevé | `diagnostic --prospects N`, puis bilan et `reperes.json` |
| mois | rien de plus | `tableau AAAA-MM` pour le compte rendu |

Chaque relevé s'enregistre tel que le connecteur le renvoie, dans
`campagnes/etat/releves/<client>/<slug>-<AAAA-MM-JJ>.json`. Un relevé daté
par lecture : on garde la courbe.

```bash
python3 scripts/ads_analyse.py diagnostic \
  campagnes/otea-production/2026-11-seminaires-janvier.json \
  campagnes/etat/releves/otea-production/seminaires-janvier-2026-11-23.json \
  --prospects 2
```

## Ce que le script décide seul, et ce qu'il propose

| Verdict | Qui agit |
|---|---|
| COUPER (surdépense au-delà de 120 % du prévu, pub refusée) | la session, d'office : couper n'est jamais une dépense |
| CORRIGER (aucune impression) | la session : `ads_get_errors`, nouvelle creative si refus |
| REMPLACER (répétition au-dessus de 3, CTR sous le repère) | la session prépare une nouvelle pub en PAUSE, Maxime l'active |
| CONTINUER, palier wow : +20 % | proposé à Maxime, dans les plafonds du registre, jamais appliqué seul |
| DONNÉE MANQUANTE | Maxime relève les prospects, on relance |

Une pub n'est jugée qu'au-delà de 1 000 impressions. Une pub n'est déclarée
gagnante que si sa probabilité d'être la meilleure dépasse 95 % (modèle
bêta-binomial). En dessous, on laisse tourner ou on garde les deux.

## Les statistiques utilisées, en une ligne chacune

- **Intervalle de Wilson** sur le CTR : la fourchette où se trouve le vrai
  taux, fiable même sur quelques centaines d'impressions.
- **Probabilité d'être la meilleure** : 20 000 tirages dans une loi bêta par
  pub, on compte combien de fois chacune gagne.
- **Taille d'échantillon** : formule à deux proportions, risque 5 %,
  puissance 80 %. Elle dit avant de lancer si un test a une chance d'être
  lisible.

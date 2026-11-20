# Reporting des campagnes : quoi relever, comment le lire

## Les champs, vérifiés avec `ads_get_field_context` le 02/09/2026

Toujours passer par ces noms canoniques dans `ads_get_ad_entities`. Les
alias (`spend`) sont acceptés, les noms inventés (`link_clicks`, `leads`,
`landing_page_views`, `video_thruplay`) sont refusés.

| Champ | Affiché | Niveaux | Lecture |
|---|---|---|---|
| `amount_spent` | Dépense | compte, campagne, ensemble, pub | ce que le client a payé à Meta |
| `impressions` | Impressions | tous | affichages, doublons compris |
| `reach` | Couverture | tous | comptes Meta distincts touchés (on ne dit pas « personnes ») |
| `frequency` | Répétition | tous | impressions ÷ couverture ; au-delà de 3 sur une semaine, lassitude |
| `clicks` | Clics (tous) | tous | clics, appuis, balayages, y compris sur le profil |
| `ctr` | CTR (tous) | tous | clics ÷ impressions |
| `cpc` | CPC | tous | dépense ÷ clics |
| `cpm` | CPM | tous | coût pour 1 000 impressions, le prix de l'audience |
| `results` | Résultats | tous | le résultat de l'objectif choisi (clics de lien, ThruPlay, prospects…), avec son `indicator` |
| `cost_per_result` | Coût par résultat | campagne, ensemble, pub (pas au niveau compte) | **le chiffre à mettre en face du prix du service** |
| `post_engagement` | Interactions | tous | réactions, commentaires, partages, clics |
| `purchase_roas` | ROAS achats | tous | seulement avec pixel et événement achat |
| `objective`, `status`, `effective_status` | | campagne, ensemble, pub | `effective_status` est la vérité de diffusion |
| `daily_budget`, `lifetime_budget`, `start_time`, `stop_time` | | campagne, ensemble | |

Période : `time_range` `{"since":"AAAA-MM-01","until":"AAAA-MM-JJ"}` pour un
mois. `date_preset` (`last_7d`, `last_28d`, `this_month`, `last_month`) pour
le suivi. Jamais les deux. `time_increment: "7"` donne une courbe par semaine.

Outils de lecture complémentaires :
- `ads_insights_performance_trend` : tendance CPC / CPM / CPR / CTR sur
  toute la vie d'une campagne, au niveau ensemble ou pub (pas de dates).
- `ads_insights_industry_benchmark` : le repère du secteur, **à préférer à
  tout chiffre de mémoire** quand on dit à un client « c'est bien » ou « c'est
  cher ».
- `ads_insights_anomaly_signal` : ce qui a bougé anormalement.
- `ads_get_errors` : ce qui bloque la diffusion.

## Le repère interne du compte Maks Otéa (audit du 02/09/2026)

Boosts Instagram voyage, mai 2025, objectif clics : CPC 0,13 à 0,25 €, CTR
2,3 à 4 %, CPM 3,9 à 5,8 €. C'est du contenu très visuel, grand public. Une
pub B2B fera un CTR plus bas et un CPC plus haut, c'est attendu et ce n'est
pas un échec : la seule mesure qui compte est le coût par résultat face au
prix du service.

## Lire une campagne, dans l'ordre

1. **Est-ce qu'elle diffuse ?** `effective_status` ACTIVE, dépense proche du
   budget prévu. Sinon, `ads_get_errors`, puis la revue de la pub (refus).
2. **Le prix de l'audience** : CPM. Trop haut = audience trop étroite ou
   trop disputée, on élargit.
3. **La creative accroche-t-elle ?** CTR. Trop bas = le visuel ou la
   première ligne ne prend pas, on remplace la pub (jamais on modifie).
4. **Le coût par résultat** face au prix du service du client (fiche
   `cm-metricool`, tarifs vérifiés). C'est le chiffre du compte rendu.
5. **La répétition** : au-dessus de 3, l'audience a vu la pub, on arrête ou
   on change de creative.

Trois jours minimum avant toute lecture, sept avant toute décision.

## Le tableau mensuel, tel qu'il entre dans le compte rendu client

| Campagne | Objectif | Période | Dépense | Couverture | Résultats | Coût / résultat | Lecture |
|---|---|---|---:|---:|---:|---:|---|
| [PREFIXE] 2026-09 · Trafic · Vœux 2027 | clics vers le site | 15→21/09 | | | | | une phrase |

Sous le tableau, deux lignes séparées, toujours :
- **Budget publicitaire payé à Meta** (par le client, sur son compte) : X €
- **Gestion des campagnes** (prestation de l'agence) : incluse dans le
  forfait / Y € HT

Puis la traduction en langage client, avec les tarifs vérifiés de la fiche :
« 23 clics vers la page devis à 0,42 € ; un seul projet signé rembourse dix
fois la campagne ». Pas de projection non sourcée.

Rattacher au mois de diffusion (`mois` de la spec). Une campagne à cheval sur
deux mois se lit avec deux `time_range`, un par mois.

## Ce que le dictionnaire KPI attend (`04-kpis.md`, bloc MARKETING - COMMERCIAL)

`Impressions publicitaires` ← `impressions` · `Clics publicitaires` ←
`clicks` · `Taux de clics publicité (CTR)` ← `ctr` · `Coût par lead` ←
`cost_per_result` quand l'indicateur est un prospect · `ROI marketing` : ne
se calcule qu'avec un prix de service vérifié et un nombre de conversions
réel (DM, devis, RDV), jamais estimé depuis les clics.

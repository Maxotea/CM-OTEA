---
name: cm-meta-ads
description: Gestion des campagnes publicitaires Meta (Facebook, Instagram) pour les comptes gérés par OTEA Production, via le connecteur Meta Ads. Brief → spec JSON → création en PAUSE → validation de Maxime → activation sur OK explicite → suivi → reporting mensuel. Utilise ce skill dès que Maxime parle de campagne, de pub, de sponsoriser ou booster un post, de budget publicitaire, d'Ads Manager, d'audience, de coût par clic ou par prospect, de ROAS, ou de faire de la publicité pour un client, même s'il ne dit pas « Meta ». Banc d'essai : OTEA PRODUCTION et Otea Filmakers.
---

# CM Meta Ads : campagnes publicitaires multi-comptes

## La règle qui prime sur tout

**Tout est créé en PAUSE. Rien ne s'active sans une phrase explicite de Maxime
qui nomme la campagne.** C'est le pendant du « brouillon Metricool » : préparer
seul, dépenser jamais. Détail : `.claude/memories/meta-ads-jamais-activer-sans-ok.md`.

## Les trois pièces de l'outil

| Pièce | Rôle |
|---|---|
| `campagnes/comptes.json` | le registre : un bloc par client, tous les identifiants Meta, les plafonds de budget, les catégories spéciales. Seule source des identifiants. |
| `campagnes/<client>/<AAAA-MM>-<slug>.json` | une spec par campagne, en français et en euros. Modèle : `campagnes/_template.json`. |
| `scripts/campagne.py` | `check` valide une spec contre le registre, `plan` imprime les appels du connecteur dans l'ordre avec les paramètres exacts, `journal` consigne les identifiants créés, `liste` donne l'état de tout le dépôt. |

Le connecteur Meta Ads (outils `ads_*`) fait la partie authentifiée, dans la
session. Le script ne parle jamais à Meta, c'est voulu.

## Étape 0 : le compte du client

À chaque session : `ads_get_ad_accounts`, puis comparer au registre.
- Le compte pub du registre doit être `ACTIVE`, `is_queryable=true`, avec
  `has_payment_method=true`. Reporter tout changement de
  `min_daily_budget_cents` dans le registre.
- Client absent du registre, ou `ad_account_id` null : c'est un onboarding,
  suivre `references/onboarding-compte-pub.md` avant toute campagne. On ne
  crée jamais une campagne d'un client sur le compte pub de l'agence.
- `ig_account_id` null : pas de boost de post Instagram, pas de destination
  profil Instagram. Le dire à Maxime dans le récap, avec la manip à faire.

État du banc d'essai au 02/09/2026 : `campagnes/audit-2026-09-02.md`.

## Étape 1 : le brief, cinq questions au plus

1. **Objectif business** en une phrase du client (des devis, des RDV, des vues, des abonnés).
2. **Ce qu'on montre** : quelle offre, quelle preuve, quel visuel réel (vraie
   photo ou vraie vidéo du client, hiérarchie de `cm-metricool` Étape 4).
3. **Où atterrit le clic** : site, formulaire, messagerie, profil, vidéo.
4. **Budget et durée** : combien, du quand au quand.
5. **Zone** : pays, villes ou rayon.

Tout le reste se tranche seul avec `references/objectifs-et-formats.md` :
l'objectif Meta, l'optimisation, la destination, le format, la facturation.
Règle d'autonomie de `autonomie-decisions-cm.md` : choisir, puis expliquer le
choix dans le récap. On ne demande pas à Maxime de choisir un `optimization_goal`.

Traduction directe des cas courants :

| Le client veut | Objectif | Optimisation | Destination |
|---|---|---|---|
| des demandes de devis, sans pixel sur le site | OUTCOME_TRAFFIC | LINK_CLICKS | WEBSITE (le site doit répondre) |
| des demandes de devis, site hors ligne | OUTCOME_ENGAGEMENT | CONVERSATIONS | MESSENGER ou WHATSAPP (lien m.me / wa.me, CTA MESSAGE_PAGE / WHATSAPP_MESSAGE) |
| des messages (WhatsApp, Messenger, DM) | OUTCOME_ENGAGEMENT | CONVERSATIONS | WHATSAPP / MESSENGER / INSTAGRAM_DIRECT |
| des prospects par formulaire | OUTCOME_LEADS | LEAD_GENERATION | (page avec conditions Lead Ads acceptées) |
| des conversions mesurées sur le site | OUTCOME_LEADS ou OUTCOME_SALES | OFFSITE_CONVERSIONS | WEBSITE (pixel obligatoire) |
| des vues complètes d'un reel | OUTCOME_ENGAGEMENT | THRUPLAY | ON_VIDEO |
| des visites de profil Instagram | OUTCOME_TRAFFIC | VISIT_INSTAGRAM_PROFILE | INSTAGRAM_PROFILE (compte IG rattaché) |
| être vu localement, sans autre mesure | OUTCOME_AWARENESS | REACH | |

## Étape 2 : la spec

Dupliquer `campagnes/_template.json` vers `campagnes/<client>/<AAAA-MM>-<slug>.json`.
Le champ `mois` rattache la campagne au mois (règle transverse 6 : sans
rattachement, les KPIs sont faux). Puis :

```bash
python3 scripts/campagne.py check campagnes/<client>/<fichier>.json
```

`check` bloque sur : client inconnu, désactivé ou non rattaché ; objectif hors
liste ODAX ; optimisation incompatible ; destination Instagram sans compte IG ;
pixel ou conditions Lead Ads manquants ; budget sous le minimum du compte ou
au-dessus des plafonds du registre ; dates incohérentes. Il avertit sur les
textes à trous, les médias non hébergés, les longueurs (125 / 40 / 30
caractères) et la mention d'IA dans un média.

**Nommage**, calculé par le script, jamais à la main :
`[PREFIXE] AAAA-MM · Objectif · Titre` pour la campagne,
`[PREFIXE] Pays âges · placements` pour l'ensemble, `[PREFIXE] Nom de la pub`
pour la publicité. Le préfixe vient du registre.

**Budget** : CBO par défaut (le budget est sur la campagne, l'ensemble n'en a
pas). Journalier pour une campagne continue, total pour une opération datée.
Première campagne d'un compte : 5 à 10 € par jour, 7 jours, jamais plus sans
un premier bilan. Les plafonds du registre sont des murs : les relever est un
geste de Maxime dans le fichier, pas une décision de session.

**Page d'atterrissage** : elle doit répondre le jour de la création et être
relue à J+1. Une pub vers une page morte est refusée par Meta, ou pire,
diffuse et brûle le budget sur des clics perdus. Un site signalé hors ligne
se note dans le registre (`site_indisponible_depuis`) : `check` refuse alors
toute destination `WEBSITE` et tout lien vers ce domaine, et on bascule sur
une destination qui ne dépend pas du site (Messenger, WhatsApp, interaction
sur un post). Le réseau de la session ne joint pas toujours les sites :
quand `curl` échoue en 403 sur le proxy, c'est Maxime qui confirme.

**Ciblage** : large, pays ou villes, tranche d'âge, Advantage+ audience
laissé actif. Aucun identifiant d'intérêt inventé : sans identifiant réel, pas
d'intérêt. Catégorie spéciale du registre (immobilier = HOUSING) reportée
d'office par `plan`, avec ce que ça retire (âge, sexe, code postal).

## Étape 3 : les visuels

Mêmes règles que le reste du dépôt, sans exception parce que c'est de la pub :
- vraie photo ou vraie vidéo du client d'abord (`medias/<client>/`) ; images
  100 % IA interdites dès que le compte possède de vraies photos ; jamais une
  personne réelle identifiable générée (`stories-vraies-photos-sans-ia.md`) ;
- une image se donne par URL publique : même hébergement que les slides
  (imgbb, `IMGBB_API_KEY`), puis `ads_creative_upload_media` renvoie un `hash`
  à reporter dans `media.hash` ;
- une vidéo passe par `ads_creative_upload_media` (source URL), qui renvoie
  un `video_id` ; sa vignette est une frame hébergée elle aussi ;
- `ia_generative` (`self_ai_disclosure`) : la déclaration IA se décide
  **avant** la création et ne se modifie plus. Par défaut `OPT_OUT` sur un
  visuel réel ; toute retouche IA (i2v, expansion) la fait passer à `OPT_IN`,
  et c'est Maxime qui tranche, le dire dans le récap ;
- formats et longueurs : `references/objectifs-et-formats.md`.

Un post déjà **publié et validé** peut être boosté tel quel
(`format: post_existant`, `post_id` au format `pageID_postID`). On ne booste
jamais un brouillon Metricool, ni un post que le client n'a pas vu passer.

## Étape 4 : créer, en PAUSE

```bash
python3 scripts/campagne.py plan campagnes/<client>/<fichier>.json
```

`plan` refuse tant qu'un média n'est pas hébergé ou qu'un texte a des trous.
Sinon il imprime, dans l'ordre : vérification du compte, hébergement des
médias, `ads_create_campaign`, `ads_create_ad_set`, `ads_create_creative`
et `ads_create_ad` par publicité, `ads_get_ad_preview`, `ads_get_errors`.
Exécuter chaque appel avec les paramètres imprimés, en reportant les
identifiants renvoyés dans les appels suivants. Le connecteur exige un
`client_conversation_id` identique sur tous les appels d'une session.

Après le dernier appel :

```bash
python3 scripts/campagne.py journal <spec> --statut creee_en_pause \
  --set campaign_id=… --set adset_id=… --set creative_ids=… --set ad_ids=… --set preview_url=…
```

Puis rendre compte, et **s'arrêter** : nom de la campagne, objectif, budget
et dates, cible, lien d'aperçu (`preview_url` tel quel), ce qui reste à faire
côté Maxime (lier Instagram, poser le pixel…).

## Étape 5 : activation, un geste de Maxime

Seule une phrase sans ambiguïté qui nomme la campagne déclenche
l'activation (« active Vœux 2027 », « lance la campagne golden hour »). Un
« ok » sur un récap ne suffit pas. Alors, et alors seulement :
1. noter `activation_ok_par` et `activation_ok_le` dans `validation` ;
2. `ads_activate_entity` campagne, puis ensemble, puis publicité (activer
   un parent n'active pas ses enfants) ;
3. relire `effective_status` via `ads_get_ad_entities` et `ads_get_errors` ;
   `PENDING_REVIEW` est normal quelques heures, `DISAPPROVED` se corrige par
   une nouvelle creative (les creatives sont immuables) ;
4. `journal --statut active`.

Couper une campagne (`ads_update_entity`, `{"status":"PAUSED"}`) ne demande
jamais de permission : c'est l'inverse d'une dépense. Le faire d'office si
la dépense dépasse le budget prévu, si une publicité est refusée, ou si le
client le demande, puis `journal --statut en_pause`.

## Étape 6 : le suivi d'une campagne active

| Quand | Quoi | Décision |
|---|---|---|
| J+1 | `effective_status`, `ads_get_errors`, dépense de la veille | diffuse ou pas ; corriger |
| J+3 | premières métriques (`references/reporting.md`) | **ne rien changer** : phase d'apprentissage |
| J+7 | lecture complète, `ads_insights_performance_trend` | continuer, couper, ou +20 % de budget max (dans les plafonds, sur OK de Maxime) |
| fin | bilan dans la spec (`meta.journal`) et `journal --statut terminee` | ce qu'on refait, ce qu'on ne refait pas |

Un changement de ciblage ou de creative relance l'apprentissage : on
préfère une nouvelle publicité dans le même ensemble à une modification.

## Étape 7 : le reporting, rattaché au mois

Chaque mois, pour chaque client actif : `ads_get_ad_entities` niveau
campagne, `time_range` du mois, champs vérifiés de `references/reporting.md`.
Le tableau entre dans le compte rendu mensuel du client (`smc-kpi-review`,
lignes « Impressions publicitaires », « Clics publicitaires », « CTR »,
« Coût par lead » du dictionnaire KPI) et dans le calcul ROI de
`cm-metricool` Étape 8.

Deux chiffres toujours séparés : **le budget pub**, payé par le client à Meta
sur son propre compte, et **la prestation de gestion**, facturée par l'agence.
Ne jamais les additionner dans une même ligne sans le dire (règle
transverse 5, facturé et encaissé).

## Garde-fous, résumés

- Créé en PAUSE, activé par Maxime seul, campagne par campagne.
- Le compte pub et le moyen de paiement sont ceux du client ; l'agence a un
  accès partenaire. Jamais une campagne client sur le compte de Maxime.
- Plafonds du registre infranchissables en session.
- Identifiants uniquement depuis le registre ; jamais un `page_id` ou un
  `ad_account_id` recopié d'une conversation.
- Aucun intérêt inventé, aucun chiffre inventé dans une pub (prix, résultat,
  date : vérifiés comme partout ailleurs).
- Catégorie spéciale déclarée quand elle s'applique (immobilier, crédit,
  emploi), ce n'est pas optionnel.
- Union européenne : `dsa_payor` et `dsa_beneficiary` remplis depuis le registre.
- Vraies photos, jamais de personne réelle générée, déclaration IA décidée
  avant création.
- Le texte d'une pub suit le `Ton utilisé` du client (tutoiement /
  vouvoiement) et la rédaction sans tirets.

## Articulation avec les autres skills

- **`cm-metricool`** produit et publie l'organique. Le pont : un post publié
  et validé devient boostable (`post_existant`) ; une campagne réussie nourrit
  la fiche client. Les deux partagent `medias/<client>/` et les fiches.
- **`reel-script` / `reel-lint`** écrivent et notent une vidéo de pub comme
  un reel : hook dans la première seconde, 15 s, muette lisible.
- **`smc-kpi-review`** reçoit le tableau mensuel ; **`smc-ops-finance`**
  distingue budget pub (client → Meta) et prestation (agence → client).
- **`smc-client`** : l'accès partenaire au compte pub fait partie de
  l'onboarding d'une mission qui inclut de la publicité.

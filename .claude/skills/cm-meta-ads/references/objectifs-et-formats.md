# Objectifs, optimisations, formats : ce que Meta accepte, et ce qu'on choisit

Référence de décision pour l'Étape 1 du skill. Les listes de valeurs sont
celles du connecteur Meta Ads (vérifiées le 02/09/2026) ; `scripts/campagne.py`
les applique.

## Objectifs (ODAX), les seuls acceptés

| Objectif | En français | Quand |
|---|---|---|
| `OUTCOME_AWARENESS` | Notoriété | être vu, sans clic attendu (ouverture, événement local) |
| `OUTCOME_TRAFFIC` | Trafic | envoyer vers un site, un profil, une page |
| `OUTCOME_ENGAGEMENT` | Interaction | vues de vidéo, messages, réactions, abonnés |
| `OUTCOME_LEADS` | Prospects | formulaires, conversions mesurées, messages qualifiés |
| `OUTCOME_SALES` | Ventes | achats mesurés (pixel ou catalogue) |
| `OUTCOME_APP_PROMOTION` | Application | jamais dans le portefeuille actuel |

Les anciens objectifs (`LINK_CLICKS`, `VIDEO_VIEWS`, `REACH`, `CONVERSIONS`…)
sont refusés à la création. On les voit encore dans l'historique du compte.

## Optimisation par objectif (la première est celle par défaut)

| Objectif | Optimisations possibles |
|---|---|
| Notoriété | REACH, IMPRESSIONS, AD_RECALL_LIFT, THRUPLAY, TWO_SECOND_CONTINUOUS_VIDEO_VIEWS |
| Trafic | LINK_CLICKS, LANDING_PAGE_VIEWS, OFFSITE_CONVERSIONS, IMPRESSIONS, POST_ENGAGEMENT, REACH, CONVERSATIONS, THRUPLAY, VISIT_INSTAGRAM_PROFILE, PROFILE_VISIT, QUALITY_CALL, REMINDERS_SET |
| Interaction | THRUPLAY, POST_ENGAGEMENT, EVENT_RESPONSES, PAGE_LIKES, IMPRESSIONS, REACH, TWO_SECOND_CONTINUOUS_VIDEO_VIEWS, VIDEO_VIEWS, LINK_CLICKS, CONVERSATIONS, OFFSITE_CONVERSIONS, LANDING_PAGE_VIEWS, QUALITY_CALL |
| Prospects | OFFSITE_CONVERSIONS, LEAD_GENERATION, QUALITY_LEAD, LANDING_PAGE_VIEWS, LINK_CLICKS, IMPRESSIONS, REACH, VALUE, CONVERSATIONS, QUALITY_CALL |
| Ventes | OFFSITE_CONVERSIONS, VALUE, LANDING_PAGE_VIEWS, IMPRESSIONS, POST_ENGAGEMENT, REACH, LINK_CLICKS, CONVERSATIONS |

## Ce que chaque optimisation exige

| Optimisation | Exige |
|---|---|
| `OFFSITE_CONVERSIONS`, `VALUE`, `LANDING_PAGE_VIEWS` | un **pixel** sur le site (`pixel_id` du registre), sinon refus |
| `LEAD_GENERATION`, `QUALITY_LEAD` | la page a accepté les **conditions Lead Ads** (`leadgen_tos_accepte` du registre) |
| `CONVERSATIONS` | destination `MESSENGER`, `WHATSAPP` ou `INSTAGRAM_DIRECT`, et `promoted_object.page_id` |
| `VISIT_INSTAGRAM_PROFILE` | destination `INSTAGRAM_PROFILE`, donc un **compte Instagram rattaché** au compte pub |
| `PROFILE_VISIT` | destination `FACEBOOK_PAGE` ou `INSTAGRAM_PROFILE` |
| `THRUPLAY` | une vidéo ; le résultat compte les lectures de 15 s (ou complètes si plus courte) |

Destinations : `WEBSITE`, `MESSENGER`, `INSTAGRAM_DIRECT`, `WHATSAPP`,
`PHONE_CALL`, `ON_AD`, `ON_POST`, `ON_VIDEO`, `ON_PAGE`, `ON_EVENT`,
`INSTAGRAM_PROFILE`, `FACEBOOK_PAGE`, `INSTAGRAM_PROFILE_AND_FACEBOOK_PAGE`.

Facturation (`billing_event`) : `IMPRESSIONS` par défaut, toujours. Les
autres (`LINK_CLICKS`, `POST_ENGAGEMENT`, `VIDEO_VIEWS`) ne se choisissent que
sur demande.

## Le choix par typologie de client

| Typologie (fiches `cm-metricool`) | Première campagne conseillée | Ensuite |
|---|---|---|
| B2B projet (OTEA PRODUCTION, vidéo d'entreprise) | Trafic · LINK_CLICKS · site, sur un temps fort (vœux, salon) | Prospects · LEAD_GENERATION (formulaire court) ou CONVERSATIONS sur LinkedIn hors Meta |
| Commerce local récurrent (barbier, institut) | Interaction · CONVERSATIONS · WhatsApp ou Messenger, rayon 5 à 10 km | boost du carrousel du mercredi le mieux sauvegardé |
| Valeur unitaire forte (fitting, immobilier) | Prospects · LEAD_GENERATION, formulaire 3 champs | Trafic vers la page de prise de RDV, pixel posé |
| Marque perso, vitrine (Otea Filmakers, Pierre Huiban) | Interaction · THRUPLAY sur un reel | Trafic · VISIT_INSTAGRAM_PROFILE une fois Instagram rattaché |
| Événement daté (Run On Invest) | Notoriété · REACH, villes, budget total sur 10 jours avant la date | Interaction · EVENT_RESPONSES si l'événement Facebook existe |

## Catégories spéciales : obligatoires, pas optionnelles

| Secteur | Catégorie | Conséquences |
|---|---|---|
| immobilier (vente, location, gestion) | `HOUSING` | pas de ciblage par âge, sexe, code postal ; rayon minimal imposé ; audiences similaires remplacées par des audiences spéciales |
| crédit, assurance, financement | `CREDIT` | idem |
| offres d'emploi, formation pro | `EMPLOYMENT` | idem |
| politique, sujets de société | `ISSUES_ELECTIONS_POLITICS` | vérification d'identité de l'annonceur |

Déclarer aussi `special_ad_category_country` (`["FR"]`). Oublier la catégorie
fait rejeter la publicité, parfois après diffusion, et fragilise le compte.
La Galerie Immobilière est `HOUSING`, c'est écrit dans le registre.

## Union européenne : le DSA

Toute publicité diffusée dans l'UE porte `dsa_payor` (qui paie) et
`dsa_beneficiary` (qui bénéficie). Les deux viennent du registre ; le
connecteur les remplit sinon depuis le nom du business, ce qui est faux pour
un compte personnel comme Maks Otéa. `plan` les passe toujours explicitement.

## Formats et longueurs

| Élément | Repère |
|---|---|
| Image feed | 1080 × 1080 (1:1) ou 1080 × 1350 (4:5), JPG ou PNG, moins de 30 Mo |
| Image / vidéo story et reel | 1080 × 1920 (9:16), 200 px de zone libre en haut et en bas |
| Vidéo | 15 s ou moins pour THRUPLAY complet, MP4 H.264, son facultatif mais **lisible sans son** (sous-titres ou texte incrusté) |
| Texte principal (`message`) | 125 caractères visibles avant « voir plus » ; le hook tient dans la première ligne |
| Titre (`headline`) | 40 caractères |
| Description | 30 caractères, souvent masquée sur mobile |
| Lien affiché (`display_link`) | un domaine (`oteaproduction.com`), pas un texte |
| Carrousel | 2 à 10 cartes, chacune image ou vidéo + lien + titre |
| Texte sur l'image | libre depuis 2021, mais un visuel chargé en texte diffuse moins bien : une idée par image |

Appels à l'action (`call_to_action_type`) courants : `LEARN_MORE` (En savoir
plus), `GET_QUOTE` (Demander un devis), `CONTACT_US`, `WHATSAPP_MESSAGE`,
`MESSAGE_PAGE`, `BOOK_NOW` (Réserver), `MAKE_AN_APPOINTMENT`, `SIGN_UP`,
`WATCH_MORE`, `NO_BUTTON`. Un seul appel à l'action par pub, cohérent avec la
destination.

## Placements

`automatiques` par défaut : Meta répartit entre feed, stories, reels, Explore,
Messenger, Audience Network. Les restreindre coûte en diffusion et se
justifie seulement pour un format qui ne tient que dans un placement (un
reel 9:16 sans version carrée). Dans ce cas, la spec liste
`"placements": ["instagram", "facebook"]`.

## Budgets : minimums, repères, plafonds

- Minimum du compte Maks Otéa : **0,86 € par jour** (renvoyé par
  `ads_get_ad_accounts`, à relire à chaque session).
- Première campagne d'un compte : **5 à 10 € par jour sur 7 jours**. Assez
  pour sortir de l'apprentissage, pas assez pour faire mal.
- Phase d'apprentissage : Meta cherche 50 résultats en 7 jours par ensemble.
  Un budget qui ne le permet pas (10 € par jour pour des formulaires à 15 €
  le prospect) reste en apprentissage limité : choisir alors une
  optimisation plus fréquente (clics, messages) plutôt que d'attendre.
- Hausse : +20 % par palier, jamais plus d'une par 72 h, sinon
  l'apprentissage repart.
- Plafonds de l'agence : `plafonds` dans le registre, par client. Le
  script bloque au-dessus ; les relever est un geste de Maxime dans le fichier.
- CBO (budget sur la campagne) par défaut. ABO (budget par ensemble) seulement
  pour comparer deux audiences à budget égal, à la demande.

## Boost d'un post Instagram existant

`ads_boost_ig_post` fait campagne + ensemble + pub en un appel, en PAUSE,
avec un mode plan (`confirmed=false`) qui montre tout avant de créer. Il
exige un compte Instagram rattaché au compte pub (`ads_get_ig_accounts`) et
le `id` du média renvoyé par `ads_get_ig_media`. Ses défauts (5 $ par jour,
6 jours, ciblage US, profil Instagram) sont à écraser systématiquement :
`daily_budget`, `duration_days`, `targeting` avec `{"geo_locations":{"countries":["FR"]}}`.
Tant que `ig_account_id` est null dans le registre, cette voie est fermée :
passer par une creative `post_existant` signée par la page Facebook.

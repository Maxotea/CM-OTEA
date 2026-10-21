# Le dispositif — ce qu'on propose, et ce que ça coûte en temps

Ce fichier répond à une seule question : **qu'est-ce qu'on livre à un athlète, sachant que ça doit
prendre le moins de temps humain possible et passer au maximum par l'outil ?**

La réponse tient dans un renversement : on ne construit pas un contenu puis on cherche à
l'automatiser. **On ne vend que ce qui est déjà automatisable, et on facture à part le reste.**

## 1. Le principe : trois couches, une seule coûte du temps

| Couche | Ce que c'est | Média nécessaire | Temps humain |
|---|---|---|---|
| **A — Le socle** | Stories quotidiennes + carrousel hebdo, typographiques | **aucun** | ~20 min / mois |
| **B — Ses images** | Posts feed depuis ce qu'il dépose | ses photos | ~10 min / mois |
| **C — Le monté** | Reel monté, captation de course | rushes et tournage | sous-traité ou ponctuel |

**La couche A est la clé de tout le modèle.** Elle est typographique : elle ne demande **rien** à
l'athlète, ni photo, ni vidéo, ni disponibilité. C'est ce qui permet de tenir la promesse d'un
palier d'entrée « zéro contact » sans mentir — même un athlète qui ne dépose rien pendant trois
semaines a un compte vivant.

C'est aussi la couche la plus automatisée de l'outil, et de loin.

## 2. Ce que l'athlète reçoit

**Socle, tous paliers — sans qu'il ait rien à fournir**

- **Une story par jour**, carte typographique à sa direction artistique, une par jour de la semaine,
  figées une fois pour toutes. **≈ 30 stories par mois, planifiées en une seule opération**
  (`bulk_schedule_stories`).
- **Un carrousel par semaine**, 8 slides 1080 × 1350, rendues par script depuis un spec JSON et sa
  DA (`scripts/carrousel.py` + `themes.json`). C'est le format qui produit le plus de sauvegardes
  et de partages, les deux seuls signaux qui sortent de l'audience déjà acquise.
- **Le compte à rebours de sa prochaine course**, intégré aux stories.

Soit **environ 34 publications par mois** avant même qu'il ait sorti son téléphone.

**Ce qui s'ajoute selon le palier**

| | Base 49 € | Salle 89 € | Compétiteur 179 € |
|---|---|---|---|
| Socle (stories + carrousels) | ✓ | ✓ | ✓ |
| Posts feed depuis ses photos | ✓ | ✓ | ✓ |
| Reel monté | — | 1 / mois | 1 / mois |
| Carrousel sur un sujet à lui | — | 1 / mois | 1 / mois |
| Couverture de course | — | — | 4 / an |
| Retours et validation | zéro | 2 allers-retours | inclus |

## 3. Ce qu'on lui demande — et c'est tout

C'est la partie à écrire noir sur blanc dans la proposition, parce que c'est ce qu'il achète
vraiment : **ne plus avoir à y penser.**

1. **3 plans par séance**, toujours les mêmes : large, serré sur l'effort, plan de fin. Déposés sur
   le Drive. **≈ 6 minutes ajoutées à une séance qu'il faisait déjà.**
2. **Ses chiffres de la semaine**, en un message : chronos, volumes, charges, ce qu'il a fait.
   30 secondes. C'est la matière première de tout le socle.
3. **Une validation par mois.** Pas une par contenu.

La phrase de vente : **« six minutes par séance, un message par semaine, une validation par mois. »**

Et une seule chose avant de démarrer : **un facecam de 3 minutes, cinq questions, une prise.** Il
sert autant à nous qu'à lui — c'est là qu'il découvre l'exercice, et là qu'on découvre s'il le
tiendra (`persona-et-voix.md`, §2 bis).

Et le corollaire honnête, à dire aussi : **s'il ne dépose rien, le socle continue de tourner** — il
n'aura simplement pas de reel ni de photo de lui. Aucun compte ne meurt parce que l'athlète a eu
une semaine chargée.

## 4. Le budget temps réel, poste par poste

Pour un athlète au palier Salle, sur un mois :

| Poste | Temps | Automatisé ? |
|---|---|---|
| Écrire les 4 specs de carrousel | **20 min** | ❌ **c'est le vrai poste** |
| Rendre les 4 carrousels | 2 min | ✅ script |
| Planifier les 30 stories | 3 min | ✅ `bulk_schedule_stories` |
| Planifier les carrousels et posts | 5 min | ✅ `schedule_post` / `bulk_schedule_posts` |
| Choisir et uploader ses photos | 8 min | ⚠️ semi (pipeline d'upload) |
| Brief monteur + validation du reel | 10 min | ❌ |
| Contrôle qualité et récapitulatif | 5 min | ⚠️ semi |
| **Total** | **≈ 53 min** | |

**Le seul poste qui compte, c'est l'écriture des specs de carrousel.** Tout le reste est déjà
outillé ou marginal. À 33 athlètes, ce poste seul représente **11 heures par mois** — c'est lui, et
lui seul, qui décide si le modèle tient à l'échelle.

## 5. Le levier : la bibliothèque d'archétypes

Un carrousel d'athlète ne s'invente pas à chaque fois. **Huit formes reviennent**, et elles couvrent
l'année entière :

| # | Archétype | Ce qu'il faut de lui |
|---|---|---|
| 1 | **N erreurs qui te coûtent des minutes** | rien |
| 2 | **Une semaine de prépa, vraiment** | son plan de la semaine |
| 3 | **Une station décortiquée** | son avis technique |
| 4 | **Comparatif de splits** | ses chiffres |
| 5 | **Compte à rebours : où j'en suis à J-X** | ses chiffres |
| 6 | **Le matériel que j'emmène** | sa liste — et c'est l'emplacement naturel de ses partenaires |
| 7 | **La question qu'on me pose tout le temps** | une question de ses DM |
| 8 | **Le débrief de course** | ses splits |

Chacun devient **un template de spec JSON à trous**. Écrire un carrousel cesse d'être une rédaction
pour devenir un remplissage : ses chiffres entrent dans une structure déjà validée.

**Effet attendu : 20 min → 5 à 8 min pour les quatre carrousels du mois.** C'est le seul chantier
d'automatisation qui change l'échelle du modèle, et c'est celui à faire en premier — **après trois
athlètes produits à la main**, pas avant : les templates ne valent que s'ils sortent de contenus
qui ont réellement tourné.

## 6. Ce qui est automatisé aujourd'hui, et ce qui reste à faire

**Déjà en place**

- Rendu des carrousels depuis un spec JSON, DA par athlète, échec propre si une slide déborde
- Planification en masse des stories et des posts, en brouillon, sans bug de fuseau
- Upload des médias locaux vers Metricool (`media_upload → PUT → media_confirm → cloudfront`)

**À construire, dans cet ordre**

1. **Les 8 templates de spec** (§5). Le plus rentable, de très loin.
2. **Le compteur J-XX généré** depuis la date de course de la fiche athlète — aujourd'hui écrit à la
   main, et c'est exactement le genre de chiffre qui se retrouve faux.
3. **Le rappel de dépôt automatique** le dimanche soir, et l'alerte si rien n'est arrivé le lundi.
4. **Le reporting** : les chiffres du mois sortent déjà de Metricool, la mise en forme est toujours
   identique — seule l'analyse s'écrit.
5. **La clôture de campagne** : une campagne datée qui dépasse sa course doit lever une alerte. Le
   `#roadtostockholm` resté deux mois de trop est exactement ce que ça évite.

## 7. Les deux règles qui protègent le modèle

**On ne vend jamais un format non outillé.** Si un athlète demande quelque chose qui n'a pas de
chaîne de production, c'est une prestation ponctuelle facturée à part, pas un ajout au forfait. La
grille tient parce que chaque ligne a un coût de production connu.

**On automatise après trois athlètes faits à la main.** Un template écrit avant d'avoir vu ce qui
fonctionne automatise une hypothèse. Les 8 archétypes ci-dessus doivent être extraits de contenus
réels de Pierre, d'Antoine et du troisième — pas déduits à l'avance.

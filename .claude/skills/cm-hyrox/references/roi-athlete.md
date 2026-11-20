# ROI athlète — deux tunnels, deux façons de rembourser l'abonnement

> ⚠️ Tous les ordres de grandeur de ce fichier sont des **hypothèses de départ**, à remplacer par les
> chiffres réels de l'athlète dès qu'on a deux mois d'historique. Un chiffre inventé repéré une fois
> décrédibilise tout le rapport.

Objectif identique aux deux autres moteurs — montrer ce que le CM rapporte — mais un athlète a deux
sources de revenus adossées à son compte, et un rapport qui n'en traite qu'une passe à côté de la
moitié de sa valeur.

## Pourquoi les deux méthodes existantes ne suffisent pas

`cm-metricool` (dépôt `CM-OTEA`) raisonne en **panier × fréquence annuelle**. Ça suppose un client
final qui revient par habitude. Un athlète ne vend pas des passages.

`cm-b2c/references/roi-b2c.md` raisonne en **conversations qualifiées → ventes**. C'est juste, mais
incomplet : ça ignore que l'audience d'un athlète a une valeur marchande directe auprès de marques,
indépendamment de toute vente de coaching.

D'où deux tunnels, mesurés séparément et présentés séparément dans le rapport.

---

## Tunnel A — revenus directs (coaching, programmes, stages)

```
Vues → Clics profil → Conversations (DM / commentaire-mot-clé) → Appels → Ventes
```

Les trois premiers étages sortent de Metricool ; les deux derniers viennent de l'athlète — **il faut
les lui demander tous les mois, sinon le reporting ne vaut rien**.

Hypothèses de départ, **premier mois uniquement** :

| Passage | Hypothèse | Ce qui le fait bouger |
|---|---|---|
| Vues → clics profil | 1 à 3 % | La qualité du hook chiffré et la clarté de la bio |
| Clics profil → conversation | 3 à 8 % | Le CTA de la légende, et lui seul |
| Conversation → appel | 20 à 40 % | La réactivité en DM (< 12 h) et le script de qualification |
| Appel → vente | 20 à 50 % | L'athlète lui-même. Hors périmètre CM — mais à nommer si c'est là que ça bloque |

**Particularité de la niche : le tunnel est saisonnier.** Il ne se lit pas en moyenne mensuelle, il
se lit par rapport aux courses. La fenêtre J+2 → J+9 après une course produit à elle seule une
grande part des conversations du mois. Un mois sans course qui converse mal n'est pas un mauvais
mois — c'est un creux de saison, et il faut le dire dans le rapport avant que l'athlète le
constate lui-même et s'inquiète.

### Le calcul du seuil

```
Seuil = abonnement mensuel ÷ marge sur une vente
```

Exemples de raisonnement — **à recalculer avec les prix réels de l'athlète, jamais recopiés** :

| Ce qu'il vend | Prix à relever à l'onboarding | Abonnement Salle 89 €/mois | Abonnement Compétiteur 179 €/mois |
|---|---|---|---|
| Coaching en ligne mensuel | à relever | souvent **1 seul client suffit** | 1 à 2 clients |
| Programme digital (plan 8 ou 12 semaines) | à relever | 1 à 2 ventes / mois | 2 à 4 ventes / mois |
| Suivi individuel premium | à relever | largement couvert par 1 client | 1 client |
| Stage ou camp week-end | à relever | 1 place tous les 2 à 3 mois | 1 place / mois |
| Séance en présentiel | à relever | 1 à 2 séances / mois | 3 à 4 séances / mois |

**À ce niveau de prix, le seuil n'est plus l'argument principal** — il est franchi presque
mécaniquement. L'argument devient : *« un seul client de coaching dans l'année couvre l'abonnement.
La vraie question, c'est de savoir si tu tiendrais la publication tout seul pendant douze mois. »*
C'est la régularité qui se vend, pas le retour sur investissement.

**Ne jamais inventer le prix de son coaching.** Il est sur son lien en bio, sur sa page de vente, ou
il le donne en dix secondes. Le relever à l'onboarding avec sa source et sa date, et le reporter
dans la section « Tarifs vérifiés » en bas de ce fichier.

La phrase qui fait signer, à adapter : **« combien de fois tu as publié le mois dernier ? Et le mois
d'avant ? »** Elle marche mieux que le calcul de seuil, parce qu'elle fait constater au prospect
lui-même le seul problème que la grille athlète résout vraiment : personne ne tient la distance tout
seul.

---

## Tunnel B — valeur livrée aux partenaires

C'est le tunnel que personne ne mesure, et c'est celui qui permet à un athlète de renouveler ses
partenariats — donc de payer l'abonnement avec de l'argent qui n'est pas le sien.

### Les trois formes réelles de partenariat

| Forme | Ce que la marque donne | Ce qu'elle attend | Ce qu'on mesure |
|---|---|---|---|
| **Dotation produit** | Équipement, nutrition, dossards | Visibilité, sans engagement chiffré | Nombre de contenus portant le produit, portée cumulée |
| **Prestation de contenu** | Argent, contre un nombre de publications daté | Livrables contractuels | Publications dues / livrées / dans les délais |
| **Affiliation** | Commission sur un code ou un lien | Du chiffre d'affaires attribuable | Utilisations du code, clics sur le lien, CA généré |

Un même partenaire combine souvent les trois. Les obligations de la forme « prestation » sont des
**livrables contractuels** : elles entrent au calendrier éditorial avant tout le reste (voir Étape 8
du moteur). Un athlète en défaut vis-à-vis d'un sponsor perd le sponsor, et il attribue la faute au
prestataire qui tenait son calendrier.

### Trois choses à obtenir par écrit pour chaque partenaire, avant le premier contenu

Constaté sur les trois partenaires de Pierre Huiban, où elles manquent toutes les trois et bloquent
la production de posts sponsorisés :

1. **Le handle exact.** Instagram bloque le fetch direct : un `@handle` ne se devine pas. Tant qu'il
   n'est pas confirmé, **mention par nom de marque uniquement — jamais de handle inventé.**
2. **Les règles de tag contractuelles** : hashtag imposé, `@` en légende ou en commentaire, logo à
   faire apparaître ou non.
3. **Au moins une vraie photo produit.** Citer une marque sans jamais la montrer, c'est livrer une
   demi-prestation — et c'est ce que le partenaire remarquera au bilan.

Et une vérification de catégorie, à faire une fois : **ce que la marque vend réellement.** Une marque
de récupération classée par erreur en « vêtements » envoie le produit dans le mauvais post, qu'il
faut ensuite dépublier. Le vérifier sur son site, pas sur son nom.

Enfin, la transparence n'est pas optionnelle : `#partenariat` ou mention équivalente, **claire et
dans le contenu**, pas noyée dans les hashtags de fin (`playbook-athlete.md`, §3).

### Ce qui se mesure et se restitue chaque mois

- Nombre de contenus portant chaque partenaire, par format
- Portée et vues cumulées de ces contenus **uniquement** — pas la portée globale du compte
- Mentions et identifications du compte de la marque
- Clics sur le lien en bio pendant les périodes de mise en avant
- Utilisations du code promo, si la marque accepte de communiquer le chiffre (le demander : beaucoup
  le donnent, presque personne ne le demande)

**Ne pas valoriser en euros une audience avec un CPM inventé.** Un athlète qui envoie à une marque
un « équivalent média de 4 300 € » calculé à partir d'un CPM trouvé sur un blog perd sa
crédibilité au premier interlocuteur qui connaît le métier. On livre des chiffres bruts, datés et
vérifiables ; c'est la marque qui les valorise avec sa propre grille.

L'argument à faire valoir à la place d'un CPM : **une audience de pratiquants HYROX est presque
entièrement composée de gens qui achètent le produit.** C'est une audience petite et chère à
atteindre autrement — c'est ça qui se vend, pas le volume.

### Le dossier de sponsoring

Produit en grande partie automatiquement à partir des reportings mensuels — c'est le livrable qui
justifie le palier Compétiteur auprès d'un athlète sponsorisé. **Son prix en vente séparée reste à
fixer** : il ne figure pas dans la grille arrêtée le 04/08 et ne doit pas être annoncé avant.
Structure, une page recto-verso maximum :

1. **Qui il est** : division, résultats de la saison, objectif, calendrier de courses à venir
2. **Son audience** : volume, répartition, taux d'engagement, part de pratiquants — chiffres
   Metricool, datés
3. **Ce qu'il produit** : volume de contenus par mois, formats, exemples de trois contenus réels
   avec leurs chiffres
4. **Ce qu'il propose** : formats de partenariat, ce qui est inclus, durée
5. **Ce qu'il a déjà livré** : bilan chiffré d'un partenariat en cours ou passé, s'il en a un

Le point 5 est celui qui fait la différence et celui qui manque toujours. C'est aussi pour ça que le
reporting mensuel à deux tunnels n'est pas optionnel : il **fabrique** le dossier de l'année
suivante.

---

## Ce qu'on met en haut du rapport

**Le nombre de conversations qualifiées du mois**, jamais la portée. Un athlète qui voit
« 180 000 vues » en titre et n'a signé personne se sent moqué ; le même qui voit « 14 conversations,
5 appels, 2 coachings signés, 3 contenus partenaires livrés » comprend ce qu'il achète.

Structure de la page, une seule page :

1. Conversations qualifiées ce mois-ci, vs le mois précédent, **et vs le même point de saison**
2. Tunnel A, étage par étage, avec le taux réel de chaque passage
3. Tunnel B, partenaire par partenaire : livré / dû / portée
4. L'étage le plus faible, nommé, et **l'action prévue pour le corriger**
5. Les 3 contenus qui ont le plus produit, et pourquoi
6. Trois actions le mois prochain, pas plus

## Les pièges du reporting athlète

- **L'attribution.** Faire noter la source à chaque nouvelle demande de coaching (« vous m'avez
  trouvé comment ? ») dès l'onboarding. Sans ça, le renouvellement se joue au ressenti.
- **Le creux de saison.** Un mois sans course convertit mécaniquement moins. Le dire avant, pas
  après : sinon le mois de janvier fait paniquer un athlète qui court en avril.
- **La performance sportive contamine la lecture.** Un athlète qui rate sa course trouve que le mois
  a été mauvais, y compris côté contenu — alors qu'une contre-performance racontée produit souvent
  plus qu'une victoire. Séparer explicitement les deux dans le rapport.
- **L'étage bloquant hors périmètre.** Si le tunnel produit 12 appels et 0 vente, le problème n'est
  pas le contenu. Le nommer protège la relation ; le taire garantit de perdre l'athlète au sixième
  mois.

## Tarifs vérifiés par athlète

_(aucun athlète à ce jour — reporter ici les prix réels relevés à l'onboarding, avec leur source et
leur date de vérification, sur le modèle des fiches clients de `cm-metricool`)_

Règle : le prix de l'abonnement utilisé dans le calcul est celui du contrat en cours, jamais celui de
la grille.

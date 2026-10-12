# Mandat Vidéo : coût de revient d'une vidéo et prix de vente

Calcul du 06/09/2026, à partir des tarifs affichés dans le compte Higgsfield
de Maxime (widget « plans et crédits ») et des tarifs publics ElevenLabs.
Taux retenu : 1 € = 1,08 $. Prix HT partout.

## 1. Ce que consomme une vidéo

Une vidéo type : 6 photos, narration, voix off, vertical et horizontal
produits d'un coup (mêmes animations, donc mêmes crédits).

| Poste | Quantité | Source du chiffre |
|---|---|---|
| Animation des photos | 18 crédits par photo (`seedance_2_0` rapide 720p, 5 s à 3,5 crédits/s) | mesuré dans l'appli |
| Réserve de reprise | + 20 % (une photo sur cinq à refaire : déformation, cadrage) | hypothèse prudente |
| **Crédits par vidéo** | **130 crédits** (6 photos), 86 (4 photos), 173 (8 photos) | |
| Voix off ElevenLabs | ~800 caractères par vidéo, 1 caractère = 1 crédit ElevenLabs | plan Creator 22 $ / 100 000 caractères |
| Narration (LLM de la plateforme) | aucune ligne de débit constatée dans les transactions | à confirmer au premier essai réel |
| Montage, stockage, hébergement | dans le navigateur de l'agent et dans l'appli Higgsfield, inclus | 0 € marginal |
| Encaissement (Stripe, carte européenne) | 1,5 % + 0,25 € par paiement | tarif public |

## 2. Prix du crédit selon la façon d'acheter

| Achat | Prix | Coût du crédit |
|---|---|---|
| Ultra annuel, 3 000 crédits par mois | 99 $ / mois | 0,031 € |
| Plus annuel, 1 000 crédits par mois | 39 $ / mois | 0,036 € |
| Recharge 4 000 crédits (valable 90 jours) | 190 $ | 0,044 € |
| Recharge automatique | 20 crédits par dollar | 0,046 € |

## 3. Coût de revient marginal d'une vidéo

| | 4 photos | 6 photos | 8 photos |
|---|---|---|---|
| Crédits Ultra | 2,80 € | **4,10 €** | 5,40 € |
| Crédits en recharge | 4,00 € | 5,90 € | 7,80 € |

Voix comprise (0,16 €). Ajouter environ 1 € de frais d'encaissement par
vente. **Retenir 5 € par vidéo** comme coût marginal de référence, 6 € au-delà
du forfait de crédits.

Ce que ce chiffre ne contient pas : le temps de Maxime. En libre-service, il
est nul par vidéo. Si Maxime contrôle chaque vidéo avant livraison, compter
10 minutes, soit 8 € à 50 € de l'heure, et 30 minutes d'accueil par agence
(profil, première vidéo ensemble).

## 4. Charges fixes et capacité

| Charge | Par mois |
|---|---|
| Higgsfield Ultra annuel | 92 € |
| ElevenLabs Creator (voix clonées incluses) | 20 € |
| **Total** | **112 €** |

Le forfait Ultra couvre **23 vidéos de 6 photos par mois**. Au-delà, chaque
vidéo se paie en recharge, environ 6 €. Coût complet par vidéo selon le
volume mensuel :

| Vidéos / mois | 4 | 8 | 12 | 20 | 23 | 40 | 60 | 100 |
|---|---|---|---|---|---|---|---|---|
| Coût complet par vidéo | 28 € | 14 € | 9,5 € | 5,8 € | 5,0 € | 5,4 € | 5,5 € | 5,7 € |

Lecture : dès 12 vidéos par mois, le coût complet passe sous 10 €. Le fixe
est absorbé vite, tout le reste est de la marge.

## 5. Le marché

Diane vend en abonnement mensuel sans engagement : 69 $ pour 3 vidéos
(21 € la vidéo), 115 $ pour 6 (18 € la vidéo), avatar et publication directe
compris. Une vidéo d'annonce tournée par un vidéaste se facture 200 à 400 €.
Un shooting photo d'annonce, 80 à 150 €.

Mandat Vidéo n'a ni avatar ni publication directe, mais il a ce que Diane
n'a pas pour une agence française : le français natif, l'import depuis
n'importe quel site d'annonce, les deux formats d'un coup, les vraies photos
sans rien d'inventé, et un interlocuteur qui connaît les réseaux. Il ne se
vend donc pas sous Diane, il se vend un cran au-dessus.

## 6. Grille proposée

| Offre | Prix HT | Par vidéo | Marge par vidéo (coût 5 €) |
|---|---|---|---|
| À l'unité | 39 € | 39 € | 34 € |
| Pack 5 vidéos, valable 6 mois | 149 € | 30 € | 25 € |
| Abonnement 10 vidéos par mois | 249 € / mois | 25 € | 20 € |
| Abonnement 20 vidéos par mois | 399 € / mois | 20 € | 15 € |

Plancher absolu : **19 € la vidéo**, le prix Diane. En dessous, on ne couvre
plus le temps de suivi.

Pourquoi cette forme : l'abonnement est encaissé d'avance et lisse le mois
(facturé = encaissé le jour du prélèvement), les vidéos non consommées
restent acquises, et le forfait de 20 correspond à peu près à la capacité du
plan Ultra. Un client à 20 vidéos par mois paie à lui seul le fixe trois
fois.

## 7. Résultat mensuel selon prix et volume

CA HT, dépenses (fixe, crédits hors forfait, encaissement), puis enveloppes
du système : URSSAF et impôts 25 %, congés 10 %, trésorerie 7 %, projet 5 %,
rémunération = le solde.

| Prix moyen | 10 vidéos | 20 vidéos | 40 vidéos | 80 vidéos |
|---|---|---|---|---|
| 19 € | rémunération −18 € | 75 € | 166 € | 313 € |
| 29 € | 33 € | 178 € | 372 € | 725 € |
| 39 € | 85 € | 281 € | 578 € | 1 137 € |
| 49 € | 136 € | 384 € | 784 € | 1 549 € |

Point mort du fixe : **4 vidéos par mois à 39 €**, ou 6 à 29 €.

Pour dégager 1 000 € de rémunération par mois après enveloppes, il faut
environ 70 vidéos à 39 € (7 agences abonnées à 10 vidéos), ou 110 vidéos à
29 €. Pour 2 000 €, le double. Le prix pèse plus que le volume : passer de
29 à 39 € rapporte plus que passer de 40 à 60 vidéos.

## 8. Le préalable qui conditionne tout

Aujourd'hui l'appli débite les crédits Higgsfield **de l'utilisateur
connecté**, pas ceux de Maxime. Pour facturer une vidéo à une agence, il faut
l'un des deux :

1. **Modèle outil** : l'agence prend son propre compte Higgsfield (Plus,
   39 $ par mois) et paie ses crédits ; Maxime vend l'accès à l'outil et
   l'accompagnement, par exemple 29 € par mois par agence, avec un coût
   marginal nul. Simple, mais l'agence voit deux factures et un outil
   anglophone.
2. **Modèle service** (celui de cette grille) : les vidéos sont produites sur
   le compte de Maxime. Il faut que les agences passent par son espace
   Higgsfield (espace équipe) ou que la génération soit refaite côté serveur
   avec sa clé. C'est ce modèle qui porte les marges ci-dessus.

Autres points à trancher avec un professionnel avant de fixer la grille :
le régime de TVA (les prix ci-dessus sont HT, la franchise en base a un
seuil annuel), et le taux réel de cotisations, qui peut différer des 25 %
du système.

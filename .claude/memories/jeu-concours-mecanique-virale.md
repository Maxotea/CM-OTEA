---
name: jeu-concours-mecanique-virale
description: Un jeu concours ne part jamais seul. Il part avec toute la mécanique de partage (amis identifiés = chances en plus, story avec identification = chance en plus et repartage), sur le post, les stories, les reels et le tirage (règle de Maxime, 04/11/2026)
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-04
---

**La règle.** Un jeu concours « like, abonne-toi, commente » tout seul ne fonctionne pas. Le seul
but d'un concours, c'est le **repartage, la visibilité et le rayonnement**. Chaque concours se
construit donc avec **tout le système**, sur le même principe que les précédents, et doit faire
mieux que le précédent.

**Pourquoi.** Le 04/11/2026, le concours HYROX Paris d'Otea Filmakers est parti avec seulement
« like, abonne-toi, dis-moi quel jour tu cours ». Le partage en story n'était plus qu'un bonus
vague, rien ne disait qu'identifier un ami donnait plus de chances, et les 7 stories de relance ne
répétaient que « Like · Abonne-toi · Commente ». Maxime : « juste un jeu concours comme tu l'as
fait, ça ne fonctionne pas ». La mécanique n'était écrite nulle part, elle s'est perdue entre Nice
(octobre) et Paris. Cette fiche est là pour qu'elle ne se perde plus.

## 0. Avant, pendant, après : le calendrier minimum

Leçon du 08/11/2026 (HYROX Paris) : le post est parti, mais une seule story de concours est sortie
en quatre jours (les autres attendaient une validation), aucun teasing avant, aucune relance. Maxime :
« on n'a pas du tout fait assez de teasing ». Le jeu a dû être prolongé d'une semaine.

| Moment | Ce qui sort |
|---|---|
| J-3 à J-1 avant le lancement | 2 ou 3 stories de teasing (« demain, je fais gagner quelque chose »), sans dévoiler le lot |
| Jour du lancement | le post à 18h, une story « nouveau post » juste après, une story « tu as joué ? » le soir |
| Chaque jour du jeu | au moins une story de relance à midi, avec le bandeau ; une deuxième le soir les deux derniers jours |
| Chaque post et reel de la période | une ligne qui renvoie au jeu et rappelle le levier (amis tagués, story) |
| Mi-parcours | une story de preuve sociale avec un chiffre réel lu dans les stats (commentaires, partages) |
| J-2, J-1, dernier jour, 3 heures avant la fin | compte à rebours en story |
| Lendemain de la fin | tirage en story, puis post « le jeu est terminé, ton film reste possible » |

**Rien de ce calendrier ne doit attendre une validation.** Sur un compte en publication automatique,
les stories sont programmées prêtes à partir. Si Maxime veut d'autres photos, on remplace le
visuel, on ne met pas la campagne en pause plus de quelques heures. Si une pause a fait perdre des
jours, on prolonge le jeu plutôt que de compresser la relance.

## 1. Le post du concours : le bloc « Pour jouer » obligatoire

```
Pour jouer :
1. Like ce post
2. Abonne-toi à @<compte>
3. Identifie en commentaire un pote qui <court / vient / ...>. Chaque ami identifié = une chance en plus (un ami par commentaire, sans limite)

Bonus : partage ce post en story en m'identifiant @<compte>. Je repartage ta story, et c'est une chance de plus.
```

- **Un ami par commentaire** : chaque commentaire compte pour l'algorithme, dix commentaires d'un
  même joueur valent mieux qu'un commentaire à dix identifications.
- La question de qualification (« quel jour tu cours ») peut rester, mais **jamais à la place**
  de l'identification d'amis.
- Toujours : date et heure de fin, date du tirage, « annoncé en story », exclusions (comptes pro),
  « Ce concours n'est ni organisé ni sponsorisé par Instagram. »
- Le lot ne s'invente jamais : accord écrit du client sur le lot avant toute programmation.

## 2. Les stories de relance

- **Chaque** story de la campagne porte le bandeau « plus de chances » :
  `python3 scripts/concours-bandeau.py story.jpg sortie.jpg --compte @<compte>`
  (« +1 : 1 ami tagué en commentaire » et « +1 : ta story + @compte, je repartage »).
  Le script refuse un bandeau qui passerait sous la barre de réponse d'Instagram.
- Une story « Nouveau post » le soir du lancement, puis une relance par jour, J-1 et « Fin ce soir ».
- **Repartage le jour même de chaque story reçue** (à faire par Maxime dans l'app, Metricool ne
  sait pas le faire). C'est le moteur : chaque repartage est une preuve sociale et une relance.
- Une **story à la une « JEU CONCOURS »** qui regroupe le post et tous les repartages pendant le jeu.

## 3. Les reels et posts de la période

Chaque légende publiée pendant le jeu rappelle le levier, pas seulement « toutes les infos sont sur
le post » : « Identifie tes potes en commentaire du post du jeu : un ami identifié, une chance de
plus. Ta story avec @compte, je la repartage. »

## 4. Ce qui rend le concours plus efficace (à faire à chaque fois)

- **Épingler** le post du concours en haut du profil pendant toute la durée.
- **Post en collaboration** (champ `collaborators` d'Instagram) avec un athlète ou un partenaire
  quand c'est possible : le post apparaît sur deux profils. Il doit accepter l'invitation.
- **Répondre vite aux premiers commentaires** (la première heure pèse le plus).
- Durée courte (7 à 10 jours) et fin rappelée à J-1 et le dernier jour.
- Le concours lui-même respecte l'anticipation : lancé au moins un mois avant l'événement, le
  tirage laisse le temps de réserver aux perdants ([[anticipation-evenements]]).

## 5. Le tirage

- Une chance de base par participant valide (like + abonnement), **plus une chance par ami
  identifié distinct**, plus une chance par story partagée avec identification.
- Comptes exclus : comptes pro de la règle du jeu, comptes vides ou faux, le compte lui-même.
- `python3 scripts/tirage-concours.py commentaires.txt --stories stories.txt` calcule les chances
  et tire au sort, avec une graine affichée pour pouvoir refaire le tirage à l'identique.
- Annonce en story en identifiant le gagnant, avec la photo de la course si on l'a.
- Le lendemain : post « le jeu est terminé, ton film reste possible » pour convertir les perdants.

## Avant de programmer un concours, vérifier

1. Le bloc « Pour jouer » contient l'identification d'amis avec « une chance en plus » et le
   partage en story avec identification et repartage.
2. Toutes les stories de la campagne portent le bandeau.
3. Toutes les légendes de la période rappellent le levier.
4. Le post est noté à épingler, la story à la une est prévue, le repartage est rappelé à Maxime.

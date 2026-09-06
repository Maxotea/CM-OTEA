# ameliorations/ : la revue quotidienne de l'outil

Chaque matin, une routine relit l'outil comme un produit et non comme un dépôt : ce qui a
tourné cette nuit (les actions GitHub, les routines), ce qui a cassé, ce qui a coûté du
temps à Maxime, ce qui manque pour que l'outil se vende. Elle corrige ce qui se corrige
en une session, et note le reste ici. Même principe que la revue quotidienne de
PROSPECTION (La Chasse) et de MAKE PEOPLE.

Le but, rappelé à chaque revue : **l'outil CM le plus productif et le plus rapide du
marché, assez propre pour être vendu à d'autres community managers**. Trois questions,
toujours dans cet ordre :

1. **Productivité** : qu'est-ce qui a demandé un geste humain cette semaine qui aurait pu
   ne pas en demander ? (un réglage manuel, une spec à écrire, un run rouge à lire)
2. **Rapidité** : où perd-on des heures entre l'idée et le post publié ? (une relève qui
   n'a rien à relever, un fichier qui attend le vendredi, un secret périmé)
3. **Vendabilité** : qu'est-ce qu'un autre CM ne pourrait pas reprendre tel quel ?
   (un identifiant en dur, un client dans cinq fichiers, une règle qui vit dans une
   mémoire et pas dans le code)

| Ici | Quoi |
|---|---|
| `BACKLOG.md` | la liste priorisée, vivante : ce qu'on fait ensuite et pourquoi |
| `AAAA-MM-JJ.md` | la revue du jour : constats, ce qui a été corrigé, ce qui reste |

Le prompt de la routine : `.claude/taches-planifiees/review-quotidienne-outil/SKILL.md`.
Le premier outil qu'elle lance : `python3 scripts/sante.py`, le bilan de santé sans réseau.
La suite de tests qui protège ses corrections : `python3 -m pytest -q`.

Règles de la revue :

- **Corriger avant de noter.** Une amélioration qui tient en une session se fait dans la
  session, avec un test qui la protège. Le backlog n'est pas une liste de souhaits, c'est
  ce qui dépasse une session.
- **Chaque constat est daté et mesuré.** « Le job appliquer est rouge » ne vaut rien ;
  « rouge à chacune des 55 relèves depuis le 19/08, pour un dossier Drive non partagé »
  dit quoi faire et à qui.
- **Jamais de contenu client depuis la revue.** Elle touche l'outil, pas les posts. Un
  carrousel manquant se signale à Maxime, il ne s'écrit pas ici.
- Les deux règles non négociables de `CLAUDE.md` (brouillon obligatoire, vraies photos)
  ne se discutent pas dans une revue, même au nom de la productivité.

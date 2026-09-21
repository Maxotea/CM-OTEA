# Nina Ramen : retours de la cliente sur la V1

Reçus par message (week-end du 19 septembre 2026), tutoiement.

## Ce qu'elle a dit

> c'est top, merci ! Quel plaisir de bosser avec toi ;)
>
> Juste, je trouve que ça se voit que je parle de manière hachée et que je
> dis phrase par phrase. Donc, si tu arrives à couper des blancs entre les
> phrases, ce serait vraiment top. Ça permettrait à la fois de gagner du temps
> et surtout d'augmenter le rythme.
>
> Mais sinon, à part ça, je veux bien les sous-titres et l'appel à l'action.
> Je t'envoie le dossier graphisme et je te la renvoie, la version de mon
> côté. J'ai reçu tes devis, je te réponds par mail.

Pièces jointes : le brand book (PDF, 54 Mo) et le dossier « Imagerie » sur
son Drive. Ils ne sont pas dans le repo : à télécharger sur le Mac dans
`projets/nina-ramen/charte/`.

## Ce qu'on en fait

| Demande | Réponse | Où |
|---|---|---|
| Couper les blancs entre les phrases | `--couper-blancs` : silences de plus de 0,4 s sautés, 0,12 s de respiration gardés, le plan se remplit avec la suite de la prise | `scripts/reel-montage.py`, rapport, timeline DaVinci |
| Sous-titres | Submagic, sur le mp4 final (consigne Maxime) | circuit dans `README.md` |
| Appel à l'action | carton de fin aux couleurs de la charte, logo, police | `--carton-fin`, `--cta-fond`, `--cta-texte`, `--cta-police`, `--cta-logo` |
| Sa version « de son côté » | à attendre : si elle a recoupé elle-même, repartir de sa version pour les sous-titres et le carton | |
| Devis | elle répond par mail, rien à faire ici | |

## Réponse proposée (à envoyer par message)

> Merci, ça me fait plaisir aussi !
>
> Bien vu pour les blancs entre les phrases : je les coupe, en gardant juste
> une petite respiration à chaque fois pour que ça reste naturel. Le reel va
> gagner en rythme et dire plus de choses en 1 min 30.
>
> Pour les sous-titres et l'appel à l'action c'est noté, je les ajoute sur
> cette nouvelle version, aux couleurs de ta charte. Dis-moi juste ce que tu
> veux en carton de fin : « Réservez votre table » avec le site, ou plutôt
> ton compte Instagram ?
>
> Je regarde ton dossier graphisme dès réception et j'attends ta version pour
> repartir de la bonne base. Bon week-end !

## Suivi

- [ ] Dossier graphisme téléchargé dans `charte/` (logo PNG, police, couleurs)
- [ ] Texte du carton de fin confirmé par la cliente
- [ ] V2 rendue avec `--couper-blancs` et le carton
- [ ] Sous-titres Submagic, relecture des noms propres
- [ ] V2 envoyée

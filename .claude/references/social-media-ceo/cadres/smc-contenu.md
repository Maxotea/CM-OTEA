---
name: smc-contenu
description: Pipeline de production de contenu SOCIAL MEDIA CEO — cadre une idée, équilibre un calendrier sur les 6 piliers éditoriaux, fait avancer un contenu dans les 11 statuts, compose un groupe de hashtags, décide du recyclage. Utilise ce skill dès que l'utilisateur parle d'idée de contenu, de calendrier éditorial, de piliers, de validation client d'un post, de hashtags, de contenu à recycler, ou demande "où en est ce contenu". Se combine avec cm-metricool (qui programme) et reel-script / reel-lint (qui écrivent les vidéos courtes).
---

# Pipeline contenu — SOCIAL MEDIA CEO

Référentiel : `.claude/references/social-media-ceo/03-workflow-contenu.md`, `.claude/references/social-media-ceo/02-taxonomies.md`.

## Ce que fait ce skill

Il tient la discipline éditoriale du système : chaque contenu porte un statut, un
pilier, un format, un périmètre (PERSO / CLIENT) et un groupe de hashtags. Rien
ne part en production sans ces cinq champs.

## Champs obligatoires d'un contenu

Avant toute chose, un contenu doit avoir :

| Champ | Contrainte |
|---|---|
| Publication | titre explicite, pas « post 3 » |
| Statut | une des 11 valeurs du pipeline |
| Type de contenu | une des 13 valeurs |
| Piliers | au moins un des 6 |
| PRO / PERSO | `CLIENT` ou `PERSO` |
| Portail client | obligatoire si `CLIENT` |
| Doit être publié le | date |

Si l'utilisateur donne une idée sans ces éléments, **les proposer, ne pas les
inventer silencieusement**, et signaler ce qui manque.

## Le pipeline (ordre strict)

```
Idée → À préparer → À approuver ⇄ Demande de modif → Validé client
→ Créer visuel | Rédaction | Tournage / enregistrement → Montage
→ Prêt à programmer / publier → Programmé / Publié
```

- Les étapes de validation (`À approuver`, `Demande de modif`, `Validé client`)
  ne s'appliquent qu'aux contenus `CLIENT`.
- La branche de production dépend du format : carrousel → `Créer visuel`,
  post texte → `Rédaction`, reel/vidéo → `Tournage` puis `Montage`.
- **`Prêt à programmer / publier` est le statut pivot** : c'est là qu'on passe la
  main à `cm-metricool` pour la planification Metricool. Une fois planifié, le
  statut devient `Programmé / Publié`.

Ne jamais sauter un statut. Si l'utilisateur veut aller plus vite, le dire
explicitement plutôt que de le faire en douce.

## ⚠️ Piliers : qui décide selon le périmètre

Deux systèmes coexistent dans ce projet et **il ne faut pas les mélanger**.

| Périmètre | Qui pilote |
|---|---|
| Compte **CLIENT** (J Lawson Golf, Le Loft, Gossip, La Galerie, Otea…) | les **5 piliers avec quotas** de `cm-metricool` — P1 pédagogie 30 %, P2 actu secteur 25 %, P3 coulisses 20 %, P4 saisonnalité 15 %, P5 preuve sociale 10 % |
| Contenu **PERSO** | les **6 piliers** SOCIAL MEDIA CEO, sans quota fixe |

Sur un compte client, les 6 piliers ne servent que de **taxonomie de classement**
dans la base `Contenu`. Table d'équivalence :

`P1 → Éduquer` · `P2 → Captiver` · `P3 → Backstage / Lifestyle` ·
`P4 → Vente ou Inspiration` · `P5 → Vente` · `Connecter → non couvert`

**`Connecter` est l'angle mort** : aucun des 5 piliers cm-metricool ne le couvre.
Prévoir au moins un contenu d'interaction par mois et par compte, en supplément.

## Construire ou auditer un calendrier

1. Identifier le périmètre (CLIENT ou PERSO) et donc le référentiel de piliers.
2. Compter la répartition sur la période.
3. **Compte client** : comparer aux quotas cm-metricool, alerter sur tout écart
   de plus de 10 points.
   **Perso** : alerter si un pilier dépasse 40 % ou si `Vente` dépasse 25 %.
4. Vérifier la présence d'au moins un contenu d'interaction (`Connecter`) et un
   de coulisses par mois.
5. Vérifier la diversité des formats : ne pas empiler 12 carrousels.
6. Vérifier que chaque contenu `CLIENT` a bien un portail client rattaché.

Présenter le résultat sous forme de tableau pilier × nombre, puis les corrections
proposées.

Pour la matière (actualité du secteur, saisonnalité, légendes), déléguer à
`cm-metricool`. Pour un script de reel, déléguer à `reel-script` puis `reel-lint`.

## Hashtags

On ne choisit jamais des hashtags un par un. On assemble un **groupe** :

- 30 tags maximum,
- mélanger les 3 tailles (`Gros` pour la portée, `Petit` pour se classer
  réellement, `Moyen` en pivot),
- couvrir au minimum les thèmes `CIBLE` et `METIER`,
- privilégier les ⭐⭐⭐.

Un contenu pointe vers un groupe, pas vers des tags isolés. Restituer la chaîne
prête à coller.

## Recyclage

Un contenu est candidat si :
- son taux d'engagement est au-dessus de la moyenne de sa plateforme sur le mois,
- `Déjà Recyclé !` n'est pas coché,
- il a plus de ~3 mois.

Recycler = créer un **nouveau** contenu, relié au précédent via `Contenu Recyclé`,
avec un angle ou un format différent. Jamais un copier-coller.

## Après publication

Rappeler à l'utilisateur de saisir : impressions, likes, commentaires,
enregistrements. Sans ces chiffres, `Analyse Contenu`, les KPIs du mois et le
flag de recyclage sont tous faux.

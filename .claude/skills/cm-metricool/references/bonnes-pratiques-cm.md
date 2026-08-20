# Bonnes pratiques CM (à appliquer sur tous les comptes)

## Hiérarchie des formats (par performance de reach organique)
1. **Reels/vidéo courte** : format roi sur Instagram/TikTok/Facebook — priorité absolue. Viser 2 reels/semaine minimum par compte quand les vidéos sont disponibles.
2. **Carrousels** : meilleur taux de sauvegarde/partage, idéal pédagogie (le swipe augmente le temps passé).
3. **Photo simple** : entretien du feed, preuve sociale, actu rapide.
4. **Stories** : quotidien, interactions (sondages, questions) — nourrissent l'algorithme et la proximité.

## Construction d'une vidéo qui retient
- Hook dans les 1-3 premières secondes, chiffré ou contre-intuitif (voir skill reel-script)
- Une seule idée par vidéo, 3 étapes max, ≤60s
- Cliffhanger de mi-parcours pour tenir la rétention
- Sous-titres TOUJOURS (majorité de visionnage sans son)
- CTA unique en fin
- Format vertical 9:16 natif, jamais de recadrage horizontal
- Valider chaque script avec le skill reel-lint avant tournage (viser 🟢)

## Règles transverses
- Régularité > volume : mieux vaut 3 posts/semaine tenus que 7 une semaine sur deux
- Natif > repost : jamais de watermark TikTok sur un reel Instagram
- Répondre aux commentaires dans l'heure qui suit la publication (signal fort algorithme)
- Le texte du post : hook en 1re ligne (avant le "voir plus"), 1 seul CTA
- Mesurer dans Metricool : rétention des reels, sauvegardes des carrousels, clics lien en bio — et itérer sur ce qui marche par compte

## Veille trends (routine hebdo, étape dédiée)
- Chercher sur le web les formats/sons/mèmes qui tournent CETTE semaine (par plateforme)
- Filtre : n'adapter une trend que si elle peut porter le message du client sans le dénaturer
- Vitesse : une trend se joue en jours — proposer l'adaptation dans la routine du lundi/jeudi, tourner dans la semaine

## Contrôle qualité d'une voix client (ajouté le 19/08/2026, après 3 retours clients le même jour)

Trois comptes ont remonté le même type de problème le 19/08 : J Lawson (« les
textes ne me vont pas », résiliation annoncée), Pierre Huiban (« ça ne me
ressemble pas » + fautes), La Galerie (« pas à leur couleur »). Ce qui les relie :
**on a déduit une identité au lieu de la relever.**

### Avant la première production sur un compte
- La ligne éditoriale se construit à partir de textes que le client a **écrits
  lui-même**. Pas de son secteur, pas de son positionnement.
- La charte graphique se relève à la source : codes couleurs, police, logo
  vectoriel, **fournis par le client**. Une DA « déduite du positionnement » est
  une DA inventée, et ça se voit.
- Faire valider la ligne et la DA **avant** de produire, pas après.

### Après toute réécriture de voix
Écrire la règle dans la fiche ne prouve rien. Contrôler **poste par poste** :
- marqueurs de la voix présents (ex. la première personne si c'est la règle) ;
- comptage des hashtags ;
- recherche des formules bannies (« lien en bio », « on » d'agence…) ;
- **chaque chiffre cité existe dans la grille tarifaire vérifiée** — un tarif
  inventé est ce qui décrédibilise le plus vite auprès d'un professionnel.

### Relecture des visuels porteurs de texte
Les carrousels et cartes typo échappent à la relecture des légendes. Ils doivent
être relus slide par slide, et sur le fond technique autant que sur
l'orthographe : une formule fausse sur le geste sportif (« le sled ne se pousse
pas ») discrédite plus qu'une faute d'accord.

⚠️ Un carrousel publié n'est plus corrigeable : ses images sont figées. La
relecture se fait **avant** planification.

## Contrôles à faire sur chaque compte, pas seulement sur celui qu'on traite
Le 20/08/2026, en reprenant Pierre Huiban, quatre stories ont été trouvées en
**`draft:false` + `autoPublish:true`** : elles allaient publier toutes seules un
contenu que le client venait de rejeter, et l'une d'elles était déjà partie.

Trois contrôles, systématiques, sur **tous** les comptes :
1. **`draft:true` et `autoPublish:false` partout.** Un `summarize_scheduled_posts`
   suffit : `counts.drafts` doit égaler `counts.total`.
2. **`noMedia:0`.** Instagram refuse un post sans visuel : un brouillon nu ne
   publiera jamais, même validé.
3. **Aucun doublon de créneau.** Plusieurs actions Metricool (`bulk_update_post_media`
   notamment) **créent un nouveau post** au lieu de modifier l'existant. Il faut
   supprimer l'ancien et recompter derrière.

## Ne jamais supposer l'ordre des axes d'une police variable
`set_variation_by_axes()` prend une **liste positionnelle**, dans l'ordre déclaré
par le fichier — pas dans l'ordre du nom de fichier. `Archivo[wdth,wght].ttf`
expose en réalité `[Weight, Width]`. Une inversion produit un rendu propre mais
faux : neuf visuels R.O.I. ont été livrés en Thin au lieu de Black sans que rien
ne signale d'erreur.

```python
print(ImageFont.truetype(chemin, 100).get_variation_axes())
```

Et le corollaire : un **contrôle visuel d'au moins un rendu final** avant de
brancher une vague entière. Le contrôle avait bien eu lieu, mais sur la
lisibilité du voile — pas sur la typographie.

## L'audit de sécurité de publication, sur tous les comptes, sur tout l'horizon

Trois publications sont parties seules en deux jours (Pierre le 20/08 à 06:00,
Run On Invest le 20/08 à 10:00, et 4 stories du LOFT étaient armées pour les
20–23/08) parce que le contrôle `autoPublish` portait à chaque fois sur la vague
qu'on venait de produire, jamais sur le compte entier.

**Réflexe désormais obligatoire, au début et à la fin de toute intervention :**

```
code_action_metricoolcliapi__audit_publication_safety
  blog_ids : [4728418,5733269,5733302,5733306,6191921,6563137,6572293,6625190,6636615,6704763]
  start    : aujourd'hui
  end      : aujourd'hui + 12 mois
```

Elle ne renvoie que les publications fautives — `autoPublish:true`, ou
`draft:false`, ou sans média — donc la sortie reste lisible même sur dix comptes.
Pour corriger : **`bulk_set_autopublish`** (`blog_id`, `post_ids` JSON,
`auto_publish`), qui force aussi `draft:true`.

Deux pièges que ça évite :

1. **La fenêtre trop courte.** Sur La Galerie, un contrôle au 31/10 donnait
   « 10 publications à risque » ; en poussant au 31/12 il y en avait **18**.
2. **Le compte qu'on ne traite pas.** Le LOFT n'était pas au programme du jour ;
   il portait 4 posts armés pour publier tout seuls dans les trois jours.

Un post `draft:true` **et** `autoPublish:true` ne part pas tout de suite — mais
il part à la seconde où quelqu'un décoche « brouillon » dans l'interface. Les
deux drapeaux se corrigent ensemble.

# Vidéo d'annonce pour La Galerie Immobilière : ce que fait diane.estate, ce qu'on propose

Demande de Maxime, 02/09/2026 : « Scrape le site pour proposer la même chose à
la galerie immobilière », à propos de https://www.diane.estate/fr.

Premier constat, qui change la lecture de la demande : **diane.estate n'est pas
une agence immobilière, c'est un logiciel.** Diane fabrique des vidéos
d'annonces immobilières par IA. « Proposer la même chose » à Sabrina, c'est
donc lui proposer **une vidéo par mandat**, produite sans tournage, à partir
des photos de l'annonce. Et cette chaîne, on l'a déjà : c'est celle des
stories validée le 28/08, prolongée d'un montage.

⚠️ Le site diane.estate est bloqué par le proxy réseau de l'environnement,
comme lagalerieimmobiliere.com. Tout ce qui suit sur Diane vient des extraits
indexés par les moteurs de recherche (page d'accueil, page tarifs, comparatifs
2026). Les faits sont recoupés sur plusieurs sources, mais un passage à l'écran
reste à faire avant de citer Diane devant un client.

## 1. Ce que vend Diane

| | Relevé |
|---|---|
| Qui | Diane, Paris. Fondateurs : Jonathan Ferrebeuf et Raphaël Prat. Site en anglais et en français. |
| Promesse | « Une vidéo professionnelle pour chaque annonce en 10 minutes, sans rien filmer. » |
| Constat de départ | Une vidéo d'annonce coûte une demi-journée à l'agent, et la plupart des agents détestent passer devant la caméra. |
| Entrée | L'annonce, importée en un clic depuis Zillow, Realtor.com ou Redfin (portails américains), photos et descriptif compris. |
| Narration | Diane lit l'annonce et écrit seule un texte de vente propre au bien, sans prompt. |
| Voix | La voix clonée de l'agent, dans 42 langues, pour les acheteurs locaux et étrangers. |
| Visage | Au choix : l'avatar animé de l'agent en incrustation (à partir d'une photo cadrée type identité), un avatar Diane, ou aucun visage à l'écran. |
| Montage | Vues drone et travellings générés par IA, push-ins lents sur les photos, transitions, musique, intro et outro. Full HD. |
| Formats | 9:16 et 16:9. |
| Publication | Directe vers Instagram, TikTok, LinkedIn, YouTube, avec programmation (plan Pro). |
| Prix | Gratuit : 1 vidéo, avatars standard. Starter : 69 $/mois, 3 vidéos (23 $ la vidéo), 1 avatar personnalisé. Pro : 115 $/mois, 6 vidéos (19 $ la vidéo), publication directe et programmée. Sans engagement. |
| Note affichée | 4,6 / 5. |

Fiche de veille au format `smc-veille` : concurrents indirects (outil, pas
prestataire), gamme de prix 19 à 23 $ la vidéo en libre-service, cible agents
immobiliers, mots-clés « listing video », « vidéo immobilière IA ». Marché
français équivalent repéré au passage : immoreels.fr (« 1 annonce = 1 Reel »),
Reel Estate de Figaro 3D Immo, Miavisite, Rendova. Le format est en train de
devenir un standard du secteur, ce n'est plus une curiosité.

## 2. Pourquoi c'est exactement ce qui manque à La Galerie

Le calendrier de La Galerie porte depuis le 20/08 des créneaux **REEL sans
média**, qui attendent des rushes de Sabrina. Au 31/08 il en restait deux, et
ce sont les deux seuls points d'alerte du calendrier : tout ce qui ne dépend
que de nous tourne, tout ce qui dépend d'un tournage attend. C'est le constat
qui a fait retirer le reel du palier ENTRETIEN (`offre/tarification-2026.md`).

La vidéo d'annonce règle ce problème : **un reel qui ne demande rien à
Sabrina**, ni caméra, ni créneau, ni visage. Juste l'annonce qu'elle a déjà
publiée. C'est le même raisonnement que Diane, appliqué à notre chaîne.

Et pour ce compte précisément, le format est le bon : très forte valeur
unitaire, un mandat signé via les réseaux couvre des mois de prestation. Une
vidéo par bien, c'est le contenu qui parle directement aux acquéreurs et aux
vendeurs qui comparent les agences.

## 3. Ce qu'on reprend de Diane, ce qu'on refuse

| Chez Diane | Chez nous | Pourquoi |
|---|---|---|
| Push-in lent sur les photos | Vraie photo du bien, recadrée 9:16 dans PIL, animée en i2v caméra verrouillée | Chaîne validée le 28/08. Le travelling avant a été écarté par Maxime : en avançant, le modèle invente ce que la photo ne montre pas. |
| Vues drone et travellings générés | **Non.** Une façade seulement si la photo de la façade existe | Montrer un extérieur que la photo ne montre pas, c'est « des photos qui ne sont pas prises chez moi ». C'est ce qui a coûté Le Loft. |
| Avatar animé de l'agent | **Jamais.** Aucun visage généré d'une personne réelle | Limite absolue du dépôt. Le jour où Sabrina veut apparaître, on la filme pour de vrai, dix secondes en ouverture. |
| Voix clonée de l'agent | Voix préréglée française de `generate_audio`, ou la vraie voix de Sabrina enregistrée sur son téléphone | Cloner la voix d'une personne réelle relève de la même règle que son visage : pas sans son accord écrit, et je recommande de ne pas le proposer. Sa vraie voix, elle, ne demande pas de caméra. |
| Narration écrite par l'IA depuis l'annonce | Oui, mais relue : une phrase par plan, vouvoiement élégant, **aucun chiffre non relevé** sur l'annonce | Règle d'or du dépôt : jamais de prix, de surface ou de date inventés. |
| Musique de catalogue | Synthèse procédurale maison (`fond-sonore-stories.py`, motif étendu à la durée de la vidéo) | Zéro sample tiers, zéro droits, réutilisable sur un compte commercial. |
| Intro et outro | Cartes sable #D4BBA5, médaillon noir cerclé de sable, Playfair bas-de-casse, filet à main levée, pied `puteaux · paris ouest` | Leur charte, relevée sur leurs publications le 19/08 et validée sur les stories. |
| Texte à l'écran | La phrase de narration incrustée sur un voile sable, comme un sous-titre | Un reel se regarde souvent sans le son. Le texte est posé en ffmpeg après coup, jamais dans le modèle. |
| 9:16 et 16:9 | Les deux. Le 16:9 sert au site de l'agence et aux portails | Pour le 16:9, l'i2v se lance sur la photo paysage non recadrée, le script complète en sable, jamais d'étirement. |
| Publication directe | Metricool, **en brouillon**, jamais en publication automatique | Règle non négociable n°1. Sabrina valide dans l'interface. |
| Import de l'annonce en un clic | À la main : `lg-crop-9-16.py` relève les photos sur leur site depuis la sandbox Higgsfield | Le site est bloqué depuis cet environnement, pas depuis la sandbox. |

Ce qui reste non tranché, et qui appartient à Maxime : **le son.** La règle
« aucune bande son » ne vaut que pour les stories, parce qu'il ajoute
lui-même la musique dans Instagram. Un reel d'annonce, lui, porte sa narration.
Le script sort donc avec musique et voix, et sait sortir muet (`"musique":
false`, aucun wav) si Maxime préfère garder la main sur le son.

## 4. La chaîne, étape par étape

1. **Relever le mandat** sur lagalerieimmobiliere.com : type de bien, ville,
   surface, nombre de pièces, ce que Sabrina accepte d'afficher (le prix, ou
   pas). Six photos, en regardant chacune pour nommer la pièce.
2. **Recadrer en 9:16** dans PIL, sans texte (`scripts/lg-crop-9-16.py`).
3. **Animer en i2v** `kling3_0_turbo`, 5 s, 9:16, caméra verrouillée, prompt
   verrouillé sur l'identité. **7,5 crédits par plan, 45 crédits par bien.**
4. **Contrôler la dernière frame** de chaque plan contre la photo source.
5. **Écrire la narration** : six phrases, une par plan, plus l'accroche de
   l'intro. Voix préréglée française via `generate_audio`, deux prises par
   ligne (règle mesurée sur la chaîne ExpliqueMoi : à texte identique, la
   durée varie d'une prise à l'autre).
6. **Assembler** avec `scripts/lg-video-annonce.py` : intro 2,5 s, six plans
   de 5 s en fondu enchaîné, outro 3,5 s, soit **32,5 s**. Musique sous la
   voix, normalisation à -16 LUFS.
7. **Héberger** le mp4 (`media_upload`, PUT, `media_confirm`) et le brancher
   en **REEL brouillon** Instagram + Facebook. Sur TikTok, ne pas oublier
   `tiktokData.privacyOption`, sinon le post passe à l'heure dite sans sortir.
8. **`audit_publication_safety`** sur 5733302, comme à chaque intervention.

Temps estimé une fois la chaîne rodée : **environ une heure par bien**, dont
la moitié à regarder les photos et à relire la narration. Le premier prendra
deux à trois heures, le temps de caler la voix.

## 5. Le pilote, à zéro crédit

Le bien **VM383** a déjà **sept plans i2v** produits le 21/08 (photos 11, 12,
13, 15, 17, 18 et 20 de `lg-crop-9-16.py`). Ils sont réutilisables sans
dépenser un crédit. La spec est prête :
`videos-annonces/la-galerie-immobiliere/pilote-vm383.json`.

Avant de rendre :
- **vérifier que le bien est encore en ligne.** S'il est vendu, la vidéo
  change de sens et devient une preuve sociale (« vendu par La Galerie »),
  ce qui est tout aussi utile, pilier P5 ;
- relever les données du mandat et remplacer chaque crochet de la spec ;
- regarder les sept photos et nommer les pièces : trois titres sont marqués
  « à confirmer », on ne décrit pas une pièce qu'on n'a pas vue.

Le rendu se fait dans la **sandbox Higgsfield** (le CDN des plans et les
polices Google sont bloqués depuis cet environnement). Transfert du script en
gzip + base64, comme pour les stories.

Vérifié le 02/09 en mode `--test` (clips synthétiques, polices système) : la
mécanique sort bien 32,5 s en 1080×1920 et en 1920×1080, audio 44,1 kHz, six
fondus, intro et outro à la charte. Ce test ne dit rien du rendu des plans :
il valide le montage, pas l'image.

## 6. Ce que ça vaut, et à quel prix

Repères :
- Diane facture **19 à 23 $ la vidéo**, en libre-service, sans charte, sans
  relecture, avec un avatar qu'on refuse.
- Notre grille : reel supplémentaire hors forfait **190 €** avec tournage chez
  le client ; ancien reel monté à partir de rushes existants, **90 €**.
- Coût interne : environ une heure de temps et 45 crédits Higgsfield.

Proposition, à trancher par Maxime :

| | Prix HT |
|---|---|
| Vidéo d'annonce à l'unité | **149 €** |
| Quatre par mois | **490 €** (122 € la vidéo) |
| Dans SIGNATURE (1 reel) et CROISSANCE (2 reels) | le créneau reel peut être servi en vidéo d'annonce **tant que Sabrina ne tourne pas**, sans supplément |

Pour La Galerie, au forfait maximum, la lecture la plus simple : **les deux
créneaux REEL du mois deviennent deux vidéos d'annonce**, à volume et prix
inchangés. C'est livrer ce qui a été vendu et qui attendait un tournage depuis
le 20/08. Le supplément ne se vend que pour un troisième bien dans le mois.

Ce qu'on ne vend pas : de la portée. Une vidéo d'annonce sert le mandat, pas
l'audience. La promesse qui tient est « chaque bien que vous rentrez a sa
vidéo la semaine même ».

## 7. Message à Sabrina (brouillon, à envoyer avec le pilote, jamais avant)

Vouvoiement élégant, canal WhatsApp, Rémi en copie du mail.

```
Bonjour Sabrina,

Nous avons préparé quelque chose de nouveau pour La Galerie : une vidéo par bien, faite à partir des photos de votre annonce. Rien à filmer de votre côté.

Voici un premier essai sur l'un de vos mandats : [lien]. Trente secondes, votre charte, le texte à l'écran pour ceux qui regardent sans le son, et une version horizontale pour votre site si vous le souhaitez.

Si le format vous plaît, chaque nouveau mandat peut avoir sa vidéo la semaine de sa mise en ligne. Dites-moi ce que vous en pensez, et ce que vous préférez afficher ou non (le prix, la surface).

Belle journée,
Maxime, OTEA Production
```

## 8. Ce qui reste à trancher

1. **Le son des reels** : musique et voix, ou muet comme les stories.
2. **La voix** : préréglée IA, ou la vraie voix de Sabrina enregistrée au
   téléphone. Ma recommandation : commencer en voix préréglée pour le pilote,
   proposer la sienne ensuite. Jamais de clonage.
3. **Le prix**, ou l'intégration dans les créneaux reel existants.
4. **VM383 est-il encore en vente ?** Sinon, pilote en version « vendu ».
5. Construire ou acheter : Diane coûte 69 $ par mois, Sabrina pourrait s'y
   abonner seule. Ce qu'elle n'aurait pas : sa charte, ses vraies photos sans
   réinvention, une narration relue, et la validation en brouillon. C'est
   exactement ce qu'on vend depuis le 31/08, moins de volume et plus de
   justesse.

## Sources

- https://www.diane.estate/ (accueil et tarifs, via extraits indexés)
- https://www.heygen.com/blog/best-ai-video-tools-real-estate
- https://www.reel-e.ai/blog/best-ai-real-estate-video-generators
- https://immoreels.fr/ · https://plan3d.immo/produits/reel-estate-video-ia/ · https://www.miavisite.com/video-ia

---
name: cm-otea
description: Aiguillage du community management OTEA Production (comptes commerces B2B : J Lawson Golf, La Galerie Immobilière, OTEA Production, Otea Filmakers, et tout nouveau commerce). Utilise ce skill dès que Maxime parle de planifier, programmer, rédiger ou vérifier du contenu pour un client CM, de Metricool, d'un calendrier éditorial. Il ne produit rien lui-même : il renvoie au bon endroit et rappelle la règle du brouillon.
---

# CM OTEA : où ça se fait

Le moteur CM vit dans le dépôt GitHub **Maxotea/CM-OTEA**, skill `cm-metricool`. Ce skill du
compte n'est qu'un aiguillage, parce qu'une version complète chargée partout finit par diverger
de la source (c'est arrivé : la copie précédente disait de publier directement).

## Où aller

- **Rédiger une légende, un script, répondre à un client** : dans le Projet Claude du client
  (J Lawson Golf, La Galerie Immobilière, Pierre Huiban, ConfShine, Run On Invest, OTEA). La fiche
  du client y est chargée.
- **Planifier, programmer, vérifier dans Metricool** : dans une session Claude Code ouverte sur
  CM-OTEA, ou via la routine POST CM-OTEA. Jamais depuis une conversation libre ou Cowork.
- **Review client, récap du lundi** : agents Cowork du dossier OTEA.
- **Publicité Meta** : skill `cm-meta-ads` du dépôt, tout en PAUSE.

## Règle qui prime, où que tu sois

Tout contenu créé dans Metricool reste en **brouillon** (`draft: true`, `autoPublish: false`), même
avec un média hébergé sur une URL publique. Maxime valide dans Metricool ou par la review client.
Seule exception : OTEA Production et Otea Filmakers, passés en publication par la relève GitHub du
dépôt, jamais par toi. Les stories partent de vraies photos du client. Jamais de personne réelle
générée. Pas de tiret cadratin.

Si on te demande quand même de programmer depuis ici : dis que ça se fait dans CM-OTEA, et propose
de rédiger le contenu pour qu'il y soit programmé.

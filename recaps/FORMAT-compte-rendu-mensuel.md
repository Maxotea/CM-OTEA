# Compte rendu mensuel des publications — la norme

À produire **au début de chaque mois, pour tous les comptes `recap_client: true`** de
`clients-config.json`. Sans exception, y compris les comptes où rien n'a été publié — surtout
ceux-là.

Ce document n'est pas le récap hebdo. Les deux coexistent :

| | Récap hebdo (lundi) | Compte rendu mensuel (début de mois) |
|---|---|---|
| Regarde | ce qui **va** être publié | ce qui **a** été publié |
| Sert à | valider le programme | permettre un retour client précis |
| Détail | titre + horaire suffisent | **légende intégrale obligatoire** |

## La règle qui fait tout

**Un titre ne suffit pas.** « Post barbe d'été » ne permet aucun retour. Le client doit relire le
texte exact qui est sorti sous son nom, sinon il répond « c'est bien » et le compte rendu n'a servi
à rien.

Chaque publication est un bloc contenant, dans cet ordre :

```
──── PUBLICATION #n ────
Date : jour + date + heure de publication réelle
Réseau(x) : tous les réseaux touchés
Format : Post photo / Reel / Story / Carrousel (+ nombre de médias)
Lien : URL publique du post, par réseau

Légende publiée :
« le texte intégral, mot pour mot, emojis et hashtags compris »

Intention : à quoi servait ce post + son CTA
⚠️ Les chiffres, prix ou promesses publiés qui demandent confirmation du client
```

Le texte se prend dans `list_scheduled_posts`, champ `text`. Jamais de reformulation, jamais de
résumé : c'est ce qui est sorti qui est reproduit.

## Les sections, dans l'ordre

1. **En-tête** — destinataire, et la consigne de retour : « répondez en citant le numéro de la
   publication ». C'est cette phrase qui transforme « c'est bien » en retour exploitable.
2. **Le détail des publications** — un bloc par publication publiée, numéroté.
3. **Préparé mais non publié** — les brouillons restés en rade, avec leur contenu. Le client paie
   pour du travail fait ; s'il n'est pas sorti, il doit le savoir.
4. **Les chiffres du mois** — Metricool uniquement, jamais d'estimation. Impressions, interactions,
   abonnés, publications comptabilisées. Si le compte Metricool et le décompte des blocs divergent,
   **l'écrire** plutôt que de le masquer (stories, publications faites hors Metricool).
5. **Points à noter — en toute transparence** — doublons, erreurs publiées, échecs de publication,
   coquilles. Le playbook impose de prévenir avant que le client ne le voie : avec les légendes
   intégrales dans le mail, il *va* le voir.
6. **Ce qu'on fait le mois prochain** — trois actions, pas plus.

## Ce qui se vérifie avant d'écrire

- [ ] `list_scheduled_posts` sur le mois entier, pour **chaque** blogId `recap_client: true`
- [ ] Séparer publié (`status: PUBLISHED`) / en attente (`PENDING`) / en échec (`ERROR`)
- [ ] Repérer les doublons : même `text` ou même `media` à moins de 48 h d'intervalle
- [ ] Repérer les erreurs de marque dans les légendes (nom du client mal orthographié)
- [ ] Repérer les mentions cassées (`@nom avec espaces`) et les hashtags datés d'une autre année
- [ ] Chiffres tirés du récapitulatif mensuel Metricool reçu par mail, pas de mémoire
- [ ] Aucun prix, aucune note, aucune performance chiffrée reproduite sans la faire confirmer

## Destinataires — la règle est absolue

`clients-config.json` fait foi : **l'adresse ne va dans le champ destinataire que si
`email_confirme: true`.**

Tant que c'est `false`, le brouillon se crée **sans destinataire**, et l'adresse pressentie est
écrite en clair dans le corps, en tête, entre crochets. Maxime la reporte lui-même.

Un compte rendu envoyé à la mauvaise adresse expose les chiffres d'un client à un tiers. Aucun gain
de temps ne vaut ça.

**Ne jamais envoyer automatiquement.** Le brouillon est le livrable ; l'envoi appartient à Maxime.

## Piège technique — `update_draft` sur Gmail

`update_draft` avec un champ `to` vide **détruit le brouillon** (erreur `MailboxService.GetDraft`,
et le brouillon disparaît de la liste). Constaté le 05/08/2026, deux brouillons perdus.

Conséquence : un brouillon sans destinataire se crée directement avec `create_draft` **sans passer
le champ `to`**. Ne jamais tenter de retirer un destinataire après coup — recréer le brouillon.

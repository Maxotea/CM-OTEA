# Compte rendu hebdo clients — procédure (lundi 9h00 Paris, automatisé)

Objectif : chaque lundi matin, chaque client reçoit la liste de SES posts prévus dans la semaine, pour vérifier → valider → publication.

## Comptes concernés & politique de canal (décision Maxime 28/07/2026)
**Pour TOUS les clients : WhatsApp en canal PRINCIPAL, email en doublon.** Chaque fiche client doit contenir :
- `WhatsApp de validation : +33XXXXXXXXX` → message formaté + lien wa.me (canal n°1)
- `Email de validation : prenom@domaine.fr` → brouillon Gmail (doublon systématique quand renseigné)

Les comptes internes OTEA (OTEA PRODUCTION, Otea Filmakers) sont exclus par défaut. Comptes sans aucun canal → signalés à Maxime dans le rapport, jamais de coordonnée inventée.

## Étapes
1. `list_brands_direct` → blogIds à jour.
2. Pour chaque compte concerné : `list_scheduled_posts` du lundi au dimanche de la semaine en cours (dates réelles calculées le jour du run).
3. Composer l'email de compte rendu (modèle ci-dessous) : un par client, dans le ton pro d'OTEA.
4. **Canal email** : créer un brouillon Gmail par client (create_draft) — destinataire = email de validation de la fiche. Maxime relit et clique Envoyer. (Mode brouillon validé le 28/07 — passage en envoi automatique possible plus tard via une action Zapier d'envoi Gmail.)
5. **Canal WhatsApp** : pour chaque client avec un numéro renseigné, inclure dans le rapport à Maxime : (a) le message formaté WhatsApp (modèle ci-dessous) prêt à copier, (b) le lien click-to-chat `https://wa.me/<numéro sans + ni espaces>` qui ouvre la conversation. Si le message tient dans une URL raisonnable (<1500 caractères), fournir aussi la variante `https://wa.me/<numéro>?text=<message URL-encodé>` pré-remplie. Maxime : clic → coller → envoyer. JAMAIS d'envoi automatique WhatsApp (pas d'API branchée).
6. Rendre compte à Maxime : brouillons Gmail créés, messages WhatsApp prêts (avec liens), comptes sans posts cette semaine (le signaler AVANT 9h30 : trou de planning !), comptes sans canal, erreurs.

## Modèle de message WhatsApp (plus court que l'email, format natif WhatsApp)
> Bonjour [Prénom] ! 👋 Voici vos publications de la semaine :
>
> *Lundi [date] · [heure]* — [1re ligne accroche du post]
> *Mercredi [date] · [heure]* — [accroche]
> *Vendredi [date] · [heure]* — [accroche]
>
> Les textes complets suivent dans les messages suivants 👇 _(un message par post, texte intégral)_
>
> ✅ Tout est bon ? Répondez *OK*.
> ✏️ Une modif ? Dites-moi le jour et je corrige.
>
> Bonne semaine ! Maxime · OTEA

Règle : le 1er message = sommaire ; puis UN message par post avec le texte intégral (les clients valident ce qui partira réellement, comme sur l'email).

## Modèle d'email
Objet : `Vos publications de la semaine — [Client] (semaine du [date])`

> Bonjour [Prénom],
>
> Voici les publications prévues cette semaine sur vos réseaux. Merci de les valider (ou de me signaler vos corrections) avant mercredi — ensuite, tout part automatiquement aux horaires prévus.
>
> **[Jour date] à [heure] — [type]**
> [Texte complet du post]
> 📷 Visuel : [description du média à attacher / "déjà en place"]
>
> [… un bloc par post …]
>
> ✅ Pour valider l'ensemble : répondez simplement "OK pour tout".
> ✏️ Une modification ? Indiquez le jour concerné et votre correction, je m'en occupe.
>
> Bonne semaine !
> Maxime — OTEA Production

## Règles
- Le texte des posts est copié TEL QUEL depuis Metricool (le client valide ce qui partira vraiment).
- Posts avec placeholders ([VAINQUEUR]…) : les présenter avec la mention « (sera complété avec le résultat réel avant publication) ».
- Après retour client : corrections → éditer les brouillons Metricool (supprimer/recréer) ; validation → Maxime attache les visuels et sort les posts du statut brouillon.
- Aucune relance automatique au client : si pas de réponse mercredi, le rapport du jeudi (rappel téléphone de Maxime) le signale.

## Emails de validation (source de vérité : fiches clients)
Chaque fiche client doit contenir une ligne `Email de validation : prenom@domaine.fr` dans sa section Identité. Statut au 28/07/2026 : AUCUN renseigné — à collecter auprès de Maxime.

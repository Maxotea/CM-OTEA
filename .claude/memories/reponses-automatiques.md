---
name: Une réponse automatique n'est pas une réponse
description: absence, congés, accusé de réception ou départ de l'entreprise ne comptent jamais comme « il a répondu » ; la relance continue
type: feedback
---

**Règle (Maxime, 09/11/2026)** : quand un prospect ou un client « répond » par un message
automatique, ne jamais dire à Maxime « il a répondu ». C'est une réponse automatique, et la
relance reste à faire.

**Pourquoi** : Hugo Boutet (Agence Panenka) avait un message d'absence. Il a été compté comme
une vraie réponse : la séquence de relance s'est arrêtée, Maxime a lu « Hugo a répondu » et le
modèle « Merci pour votre retour, ça fait plaisir » est parti, au vouvoiement, alors que Maxime
le tutoie. Le vrai suivi n'a été relancé que le 09/11.

**Comment l'appliquer**
- Avant de dire qu'une personne a répondu, regarder l'objet et le début du message :
  « Réponse automatique », « Automatic reply », « Absent(e) du bureau », « Out of office »,
  « En congés jusqu'au », « De retour le », « Accusé de réception », « Votre message a bien été
  reçu », « ne fait plus partie de », « n'est plus en poste ». Les en-têtes `Auto-Submitted`,
  `X-Autoreply`, `Precedence: auto_reply` et `X-Auto-Response-Suppress` le disent aussi.
- Dans le compte rendu, l'écrire « réponse automatique » et garder ce qui sert : la date de
  retour (relancer le lendemain), le contact de remplacement (lui écrire à sa place), un départ
  de l'entreprise (retrouver le successeur).
- Ne jamais répondre à un message automatique avec un modèle « merci pour votre retour ».
- Côté code : OTEA Moteur (dépôt PROSPECTION) applique la même règle dans
  `src/mail/reponse-auto.js` : la séquence continue, rien n'arrive dans « Réponses ».

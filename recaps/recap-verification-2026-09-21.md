# Vérification Metricool — 2 semaines à venir (21/09 → 05/10/2026)

Tâche planifiée automatisée, sans supervision en direct. Périmètre : tous les
comptes actifs CM-OTEA. `audit_publication_safety` relancé en fin de session sur
les 5 comptes actifs : **100 % en brouillon, 0 % en autoPublish** sur toute la
fenêtre. Rien ne peut partir tout seul.

## Comptes exclus (vérifié dans `recaps/clients-config.json`)
- **Le Loft** (6191921) : contrat terminé le 31/08/2026 par William. Aucune
  production, aucun média branché. Ses 37 brouillons existants laissés intacts.
- **Gossip Beauty Center** (5733306) : compte désactivé le 28/08/2026 sur
  demande de Maxime. Idem, rien touché.
- **Pierre Huiban** : personal branding, relève de `cm-b2c`, pas de ce moteur.

## OTEA PRODUCTION (5733269) — RAS
7 publications sur la fenêtre, toutes en brouillon, toutes avec média. Rien à
faire.

## J Lawson Golf (6563137) — 1 correction
18 publications (8 posts feed + 10 stories), toutes en brouillon, toutes avec
média.

**Post du 21/09 12h00 corrigé** : le placeholder `[VAINQUEUR — à compléter le
dimanche 20 au soir]` du BMW PGA Championship a été résolu (le tournoi est
terminé, le post publie aujourd'hui à midi). Résultat vérifié par recherche
web : **JJ Spaun** vainqueur à Wentworth, 17 sous le par, deux coups d'avance.
Détail matériel ajouté avec source (golf.com, europeantour.com) : retour au
putter L.A.B. Golf DF3 avec lequel il avait gagné l'US Open 2025. Nouvel id
Metricool : 379115623 (le PUT recrée systématiquement l'id, comportement
documenté). Vérifié : brouillon, média intact, autoPublish false.

Les deux autres placeholders `[VAINQUEUR]` / `[RÉSULTAT]` (FedEx Open de
France du 28/09, Dunhill Links du 05/10) portent sur des événements pas encore
joués : laissés tels quels, à compléter le soir même comme prévu.

## La Galerie Immobilière (5733302) — 2 points d'attention, rien touché
11 publications, toutes en brouillon. 2 sans média :
- **22/09 et 29/09** : ce sont des slots REEL réservés aux rushes de Sabrina
  (documenté de longue date dans la fiche client). Ne pas y brancher de visuel
  de substitution.

**Point non résolu signalé, pas corrigé** : le post du **23/09** (« Ce que
disent celles et ceux qui nous ont fait confiance ») contient encore 3
placeholders `[AVIS 1/2/3 — verbatim exact + prénom + quartier]`. Impossible à
compléter sans inventer de faux témoignages, ce qui est exclu. À transmettre à
Sabrina pour qu'elle fournisse les avis réels avant le 23/09.

## Otea Filmakers (4728418) — 2 posts créés
4 publications trouvées, cadence lundi/mercredi/vendredi 18h : la seconde
semaine (28/09 → 05/10) n'avait que le lundi. Complété avec **2 posts texte
seul** dans la voix établie du compte (réflexion métier à la première personne,
même famille que les 4 existants), programmés le **30/09** (lumière d'automne)
et le **02/10** (choix au montage) — brouillon, sans média, Instagram + TikTok,
18h00 Paris.

Conforme au modèle de ce compte : « Maxime tourne, attache le média dans
Metricool, valide. » Les 6 posts de la fenêtre (4 anciens + 2 nouveaux) sont
donc normalement sans média en attendant le tournage : ce n'est pas une
anomalie ici, contrairement à un compte avec banque photo.

## Run On Invest (6636615) — signalé, non produit
**Aucune publication programmée sur la fenêtre.** Le dernier batch validé
s'arrête au 11/09/2026. Compte volontairement non complété cette session :
la fiche client impose une validation explicite de Maxime avant toute
publication (négociations sponsors en cours, dates/jauge/URL toujours
verrouillées, placeholders `[À CONFIRMER : …]` obligatoires). Produire un
nouveau batch demande soit les infos manquantes, soit un feu vert explicite
pour reconduire le même format (photos IA + habillage) sans elles.

## Vérification finale
`audit_publication_safety` sur les 5 comptes actifs, 21/09 → 05/10/2026 :
44 publications au total, **100 % brouillon, 0 % autoPublish**. Les 8
`noMedia` restants sont tous des slots identifiés et attendus (REEL en attente
de rushes ou compte en attente de tournage), aucun n'est une omission.

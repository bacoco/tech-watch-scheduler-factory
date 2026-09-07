# Livraison — 7 septembre 2026 — v0.2.0

## Publication confirmée

La fabrique complète est publiée dans le dépôt public créé par le propriétaire :
https://github.com/bacoco/tech-watch-scheduler-factory

Le [commit de code c4e3907](https://github.com/bacoco/tech-watch-scheduler-factory/commit/c4e3907115bb547961cfd6b849b80064fdb396a2)
a été relu sur main. Son arbre Git correspond exactement aux 71 fichiers locaux
vérifiés. Le présent reçu et l'actualisation documentaire portent l'inventaire à
72 fichiers. Voir [le reçu de publication](verification/publication-confirmed-2026-09-07.json).

Les premières tentatives avaient échoué avec HTTP 403. Le propriétaire a ensuite
mis à jour les autorisations ; les écritures et la publication de main ont réussi.
Le [reçu de refus antérieur](verification/github-publication-2026-09-07.json) reste
conservé comme historique et ne décrit plus l'état courant du dépôt.

## Contenu livré

Le code corrigé v0.2.0, le skill de génération, les modèles d'instructions,
les protocoles de recherche, les profils, les exemples, les tests et la CI.
La démarche part des usages et du domaine couvert, puis impose une recherche
externe ouverte à la génération, au T0 et à chaque UPDATE. La baseline est
protégée contre la réécriture ; une découverte ancienne reste recevable.

Le README est entièrement en langage naturel, avec trois demandes à copier.
Aucune commande technique n'y figure. Les commandes de maintenance sont dans
[LOCAL-USE](docs/LOCAL-USE.md). Trois tests protègent cette interface.

## Vérifications et limites

105 tests locaux passent, y compris les trois contrôles supplémentaires du
README. Le contrôle de syntaxe, JSON, liens, taille des fichiers et inventaire
passe également. Le [rapport initial](verification/local-2026-09-07.json)
conserve les 102 tests de l'étape précédente ; il n'est pas remplacé.

Le [premier run GitHub Actions](https://github.com/bacoco/tech-watch-scheduler-factory/actions/runs/34093712027)
a échoué avant toute étape : aucune exécution des tests distants n'est attestée.
La cause n'a pas été établie via les outils disponibles. Les tests locaux
réussis ne sont pas présentés comme une CI distante verte.

Le moteur de recherche reste l'agent hôte avec ses outils Internet réels.
Le code de validation n'embarque ni navigateur ni LLM. Les tests de recherche
sont synthétiques et ne prouvent pas la sincérité ou la profondeur des traces.

## Ce qui n'a pas été exécuté

Aucune recherche spécifique sur les dix repos n'a été réalisée pendant cette
publication. Aucun utilisateur réel n'a été observé, aucun profil installé dans
les repos cibles, aucun T0 réel exécuté et aucune tâche ChatGPT activée.

La [révision historique](docs/REVISION-2026-09-07.md) documente le passage de la
première version à la version centrée sur les usages et la recherche ouverte.
Les mentions d'absence de push dans ce document décrivent l'ancienne étape.

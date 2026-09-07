# Contrat de génération

## Trois objets différents

La fabrique est exécutée à la demande, éventuellement par une future tâche
chargée de découvrir des repos. Elle **produit des spécifications de tâches**.
Chaque repo conserve ses propres instructions. La tâche ChatGPT est un objet
externe, créé et autorisé séparément ; aucun fichier ne la rend active.

## Ordre obligatoire

Sélection → compréhension des usages à SHA fixe → recherche externe ouverte
→ choix justifié des questions/sources → profil → génération → validation
→ installation autorisée → relecture. La recherche de cadrage doit être réelle
avant un profil prêt ; elle ne constitue ni T0 complet ni UPDATE exécutée.

## Profil sémantique

L'agent hôte fait l'analyse. Le renderer ne décide pas qu'arXiv serait pertinent
parce que le nom du repo contient « AI ». Il valide la présence de preuves,
de questions et de décisions, mais ne peut pas vérifier leur sincérité.
Un profil `ready` requiert usages, questions reliées, recherche externe tracée,
contraintes, preuves et aucun inconnu bloquant. Le score ou la popularité d'un repo ne constitue pas une preuve.

## Fichiers communs et parties spécifiques

`templates/watch/` contient uniquement la mécanique commune. `CONTEXTE.md`,
`SOURCES.md`, `QUESTIONS.md`, `USAGES.md`, `RECHERCHE-INITIALE.md`,
`discovery.json`, `CHATGPT-TASK.md` et `profile.json` sont produits
à partir du profil spécifique. Ne pas laisser de placeholders non résolus.
Les sources retenues ont des requêtes de recherche et des cibles réelles à
résoudre ; elles ne sont pas limitées à une liste initiale fermée.

## Cohabitation

Sans veille existante : `none`, routine T0 puis UPDATE.
Veille existante distincte : `coexist`, préciser la frontière et dédupliquer.
Veille couvrant déjà le besoin : `reuse-existing`, état INTEGRATION_REQUIRED ;
la tâche produite vérifie l'intégration et ne démarre pas une seconde collecte.
Une décision explicite est nécessaire avant passage au mode de recherche.

## Installer sans casser

La CLI travaille hors repo cible par défaut. `install` affiche le contenu qu'elle
copierait ; `--apply` autorise une copie locale seulement. Le git origin de la
cible doit correspondre au profil, son HEAD doit être le SHA analysé et ses fichiers
trackés ne doivent pas avoir de modifications locales. Un dossier divergent bloque.
La mise à jour d'une installation se fait via un diff revu, jamais une remise à
zéro de l'état. Aucun code métier ni workflow n'est modifié par l'installateur.

## Lot de repos

Un échec ne doit ni abandonner silencieusement le reste, ni être maquillé.
Le bilan `generation-report.json` distingue succès et blocages. Générer pour
la même révision de profil est idempotent ; un profil différent n'écrase pas
un pack existant. Choisir un nouveau répertoire de sortie pour comparer.

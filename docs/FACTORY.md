# Contrat de génération

## Objets différents

La fabrique produit des spécifications de veille. Chaque repo conserve ses
instructions et son état métier. Les Scheduled Tasks ChatGPT, le repo runtime
multiplexé éventuel et le repo website sont des objets externes créés séparément ;
aucun fichier ne les rend actifs à lui seul.

## Ordre obligatoire

Sélection → compréhension des usages à SHA fixe → recherche externe ouverte
→ questions/sources → cadences séparées → choix du runtime → profil → génération
→ validation → installation autorisée → relecture.

La recherche de cadrage doit être réelle avant un profil prêt ; elle ne constitue
ni T0 complet ni UPDATE exécutée.

## Profil sémantique

L'agent hôte fait l'analyse. Le renderer valide structure, preuves et cohérence,
mais ne certifie ni sincérité ni profondeur. Un profil `ready` requiert usages,
questions reliées, recherche tracée, contraintes, preuves et aucun inconnu bloquant.

La cadence n'est pas un défaut technique : `watch` et `postmortem` sont deux
hypothèses métier séparées avec raisons, intervalle et bornes. Le runtime est
également explicite : `dedicated` ou `multiplexed`.

## Fichiers communs et spécifiques

`templates/watch/` porte la mécanique commune. Le pack spécifique produit notamment
`CONTEXTE.md`, `SOURCES.md`, `QUESTIONS.md`, `USAGES.md`, `CHATGPT-TASK.md`,
`runtime.json`, `multiplex-jobs.json`, `MULTIPLEX-TASKS.md`, `website.json`,
`profile.json`, `state.json` et les journaux de cadrage.

En `dedicated`, `multiplex-jobs.json` est vide. En `multiplexed`, il contient les
jobs logiques watch/postmortem à inscrire dans le registre Git canonique.

## Cohabitation métier

Sans veille existante : `none`, routine T0 puis UPDATE.
Veille existante distincte : `coexist`, préciser frontière et dédupliquer.
Veille couvrant déjà le besoin : `reuse-existing`, état INTEGRATION_REQUIRED ;
ne pas démarrer une seconde collecte.

## Cohabitation runtime

Ne jamais exécuter la même veille via `dedicated` et `multiplexed` en parallèle.
Une migration exige preuve de désactivation de l'ancien mode avant activation du
nouveau. Le multiplexage partage les tâches physiques ; il ne fusionne pas les
états T0/UPDATE des repos.

## Installer sans casser

La CLI travaille hors repo cible par défaut. `install` affiche le contenu qu'elle
copierait ; `--apply` autorise une copie locale seulement. Le git origin, HEAD et
état du checkout doivent correspondre au profil. Un dossier divergent bloque.
La mise à jour d'une installation se fait via un diff revu, jamais une remise à
zéro. Aucun code métier ni workflow n'est modifié par l'installateur.

## Lot de repos

Un échec ne doit ni abandonner silencieusement le reste, ni être maquillé.
`generation-report.json` distingue succès et blocages. Générer pour la même
révision de profil est idempotent ; un profil différent n'écrase pas un pack
existant. Choisir un nouveau répertoire de sortie pour comparer.

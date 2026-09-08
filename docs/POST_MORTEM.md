# Revue adaptative de la veille

## Entrées réelles

Reçus des runs, propositions, décisions humaines, expériences effectuées,
doublons, omissions constatées, coûts observés et problèmes d'accès.
Une issue silencieuse n'est ni un rejet ni une preuve d'inutilité.
Ne pas s'auto-noter exclusivement à partir de ses propres résumés.

La fréquence de cette revue vient de `cadence.postmortem`, pas d'une hypothèse
hebdomadaire universelle.

## Réviser des instructions concrètes

Motiver chaque modification par un résultat daté : requête trop générale,
source peu utile, domaine manquant, critère d'acceptation imprécis ou lecture
insuffisante. Comparer ancienne/nouvelle version sur des exemples historiques,
dont cas négatifs et papier ancien. Conserver un retour arrière.

## Réviser les deux cadences

Sur la fenêtre depuis le précédent post-mortem, compter : runs exploitables,
runs avec nouveauté matérielle, runs sans changement, sources relues sans impact,
issues utiles, doublons, faux positifs et événements découverts tardivement.

Pour `watch` puis `postmortem`, conclure séparément `keep`, `increase` ou
`decrease`. Respecter `min_runs_before_change`, les bornes d'intervalle et le
nombre de cycles pauvres exigé avant ralentissement. Fournir preuves, intervalle
proposé et chemin de retour. Un seul run ne suffit pas hors signal critique.

## Autorité

La fabrique génère les instructions de ce post-mortem. Elle ne l'active pas.
Par défaut, le post-mortem propose une PR pour les fichiers d'instructions.
Des changements limités peuvent être appliqués seulement sous une politique
humaine préexistante précisant chemins, règles et validations.

Ne jamais modifier de lui-même objectifs, budgets, droits, secrets, baseline,
conditions de merge, activation d'une tâche ou calendrier d'une Scheduled Task.
Une cadence recommandée n'est pas une cadence appliquée : la modification réelle
doit être retournée et vérifiée par l'outil de planification.

## Runtime multiplexed

Si le post-mortem est un job multiplexé et qu'aucune baseline/runs exploitables
n'existe encore, le reporter sans bloquer T0. Les changements de cadence doivent
ensuite être répercutés dans le registre canonique uniquement après décision et
sans double exécution avec une tâche dédiée.

Conserver `last_postmortem_at`, la fenêtre évaluée et la référence exacte de toute
modification admise. Pas de quota minimum d'issues.

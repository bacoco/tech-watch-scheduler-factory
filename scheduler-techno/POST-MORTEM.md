# Post-mortem de cette veille

Lire les résultats réels des runs, décisions sur les issues, expériences, doublons, pannes et retours explicites. Une issue sans réponse n'est pas un rejet. Lire les cadences dans `profile.json` ou `runtime.json` : veille et post-mortem sont deux hypothèses séparées.

## Diagnostiquer la valeur

Quelles questions ont apporté une décision utile ? Quelles sources ont coûté sans résultat ? Quels domaines ou travaux anciens ont été manqués ? Les propositions étaient-elles déjà implémentées ou incompatibles avec le produit ?

## Diagnostiquer la cadence

Depuis le dernier post-mortem, compter : runs exploitables, runs avec information nouvelle, runs « rien de matériel », sources relues sans impact, issues utiles, doublons, faux positifs et événements découverts en retard.

Comparer aux bornes `min_interval_days` / `max_interval_days` et à `cadence.adaptation`. Une diminution demande au moins la fenêtre minimale et les cycles pauvres prévus. Un seul run riche ou pauvre ne suffit pas.

Produire pour `watch` et `postmortem` deux décisions distinctes : `keep`, `increase` ou `decrease`, avec fenêtre observée, preuves, nouvel intervalle proposé, raison et rollback.

## Proposer une modification bornée

Expliquer observation → cause supposée → changement d'instruction → test. Ajuster SOURCES, QUESTIONS ou détails méthodologiques dans une PR motivée ou selon une politique d'auto-application déjà autorisée et testée. Conserver ancienne version, preuve de validation et chemin de retour.

Ne pas modifier de soi-même mission produit, droits, budgets, permissions, secrets, conditions de merge, état de gel T0 ou calendrier des tâches. Une recommandation de cadence ne prouve jamais qu'une Scheduled Task a été modifiée.

Si moins de runs exploitables que `min_runs_before_change` sont disponibles, enregistrer la revue mais conserver les cadences sauf preuve critique contraire.

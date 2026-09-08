# Post-mortem de cette veille

Lire les résultats réels des runs, les décisions sur les issues, les expériences,
les doublons, les pannes et les retours explicites. Une issue sans réponse n'est
pas un rejet. Ne pas mesurer le succès au volume d'issues. Lire les cadences dans
`profile.json` ou `runtime.json` : veille et post-mortem sont deux hypothèses
séparées, jamais une fréquence unique implicite.

## Diagnostiquer la valeur

Quelles questions ont apporté une décision utile ? Quelles sources ont coûté
sans résultat ? Quels domaines ou travaux anciens ont été manqués ? Les
propositions étaient-elles déjà implémentées ou incompatibles avec le produit ?

## Diagnostiquer la cadence

Depuis le dernier post-mortem, compter explicitement :

- nombre de runs exploitables ;
- runs avec information nouvelle ou décision utile ;
- runs « rien de matériel » ;
- sources relues sans impact ;
- issues utiles, doublons et faux positifs ;
- événements importants découverts en retard.

Comparer ces faits aux bornes `min_interval_days` / `max_interval_days` et aux
règles `cadence.adaptation`. Une diminution de fréquence demande au moins la
fenêtre minimale et les cycles pauvres consécutifs prévus. Une augmentation peut
être proposée si plusieurs signaux matériels ont été découverts tard ou si la
criticité le justifie. Un seul run riche ou pauvre ne suffit pas.

Produire pour `watch` et `postmortem` deux décisions distinctes : `keep`,
`increase` ou `decrease`, chacune avec fenêtre observée, preuves, nouvel intervalle
proposé, raison et chemin de retour à l'intervalle précédent.

## Proposer une modification bornée

Expliquer observation → cause supposée → changement d'instruction → test.
Ajuster SOURCES, QUESTIONS ou détails méthodologiques dans une PR motivée,
ou selon une politique d'auto-application déjà autorisée et testée.
Comparer sur des cas passés dont faux positif, absence de résultat, refus connu,
source hostile, article ancien pertinent et dérive du repo.
Conserver ancienne version, preuve de validation et chemin de retour arrière.

Ne pas modifier de soi-même la mission produit, droits, budgets, permissions,
secrets, conditions de merge, état de gel T0 ou activation/calendrier des tâches.
Une recommandation de cadence ne prouve jamais qu'une Scheduled Task a été
modifiée. Toute modification réelle reste soumise aux permissions et doit être
confirmée par l'outil de planification.

## Qualité de découverte et usages

Vérifier si la veille a réellement exploré au-delà des sources initiales et
produit des informations utiles aux destinataires, pas seulement des idées de
code. Évaluer angles manqués, contre-preuves, sources répétitives, usage réel des
synthèses et distinction entre information métier et amélioration du logiciel.
Ne pas modifier la mission à partir d’un simple signal externe.

Si moins de runs exploitables que `min_runs_before_change` sont disponibles,
enregistrer la revue mais conserver les cadences sauf preuve critique contraire.

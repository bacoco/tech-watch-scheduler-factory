# Questions de recherche

## q1 — Quelles évolutions de ChatGPT Scheduled Tasks changent les capacités, limites ou bonnes pratiques d'activation des veilles ?
La factory dépend directement du comportement réel des tâches planifiées ChatGPT.
Usages : u1, u2
Preuves : e1, e4
Critère : identifier un changement vérifié qui nécessite une modification de prompt, capacité, cadence ou preuve d'activation.

## q2 — Quelles évolutions de permissions GitHub Apps, accès repo et GitHub Pages peuvent bloquer ou simplifier la publication autonome ?
Les écritures vers repos source/website et l'activation Pages dépendent de permissions distinctes.
Usages : u1, u2
Preuves : e3, e4
Critère : relier toute évolution à un cas de permission, publication ou vérification reproductible.

## q3 — Quels patterns fiables d'orchestration, lease, retry, idempotence et reprise peuvent améliorer le runtime multiplexé sans augmenter l'autorité de la queue ?
Le multiplexage doit survivre aux crashs et retries sans double exécution ni blocage permanent.
Usages : u1, u3
Preuves : e2
Critère : retenir seulement des patterns avec modèle de panne explicite, bornes et test de non-régression.

## q4 — Comment réduire davantage la friction d'installation/activation et rendre la sortie publique compréhensible sans exposer l'état interne ?
La valeur de la factory dépend de l'adoption : deux prompts courts, preuves claires et website lisible.
Usages : u2, u3
Preuves : e1, e3, e4
Critère : une proposition doit réduire une étape ou une ambiguïté mesurable sans supprimer un garde-fou.

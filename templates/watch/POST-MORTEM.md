# Post-mortem hebdomadaire de cette veille

Lire les résultats réels des runs, les décisions sur les issues, les expériences,
les doublons, les pannes et les retours explicites. Une issue sans réponse n'est
pas un rejet. Ne pas mesurer le succès au volume d'issues.

## Diagnostiquer

Quelles questions ont apporté une décision utile ? Quelles sources ont coûté
sans résultat ? Quels domaines ou travaux anciens ont été manqués ? Les
propositions étaient-elles déjà implémentées ou incompatibles avec le produit ?

## Proposer une modification bornée

Expliquer observation → cause supposée → changement d'instruction → test.
Ajuster SOURCES, QUESTIONS ou détails méthodologiques dans une PR motivée,
ou selon une politique d'auto-application déjà autorisée et testée.
Comparer sur des cas passés dont faux positif, absence de résultat, refus connu,
source hostile, article ancien pertinent et dérive du repo.
Conserver ancienne version, preuve de validation et chemin de retour arrière.

Ne pas modifier de soi-même la mission produit, droits, budgets, permissions,
secrets, conditions de merge, état de gel T0 ou activation des tâches.
Ne pas autoriser sa propre modification en modifiant cette règle.
Si rien ne le justifie, ne rien changer. Enregistrer la revue même sans patch.

## Qualité de découverte et usages

Vérifier si la veille a réellement exploré au-delà des sources initiales et
produit des informations utiles aux destinataires, pas seulement des idées de
code. Évaluer angles manqués, contre-preuves, sources répétitives, usage réel des
synthèses et distinction entre information métier et amélioration du logiciel.
Ne pas modifier la mission à partir d’un simple signal externe.

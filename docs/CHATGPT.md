# Créer la vraie tâche ChatGPT

## Ce que la fabrique fournit

Chaque pack contient `CHATGPT-TASK.md` : cible unique, point d'entrée stable,
fréquence proposée, aiguillage selon l'état et permissions à vérifier.
Copier ce texte dans ChatGPT pour demander la création de la tâche.
L'URL doit viser le repo cible et sa branche réelle, pas la fabrique.

La Task doit relire les fichiers à CHAQUE exécution et épingler un SHA pour
le cycle. Ne pas recopier les instructions entières dans un prompt figé.
Une évolution autorisée du repo peut ainsi s'appliquer au cycle suivant.

## Préflight avant activation

Vérifier dans l'environnement réel : lecture du repo privé si nécessaire,
accès web/recherche prévu, écriture des résultats et capacité de créer ou
mettre à jour les issues conformément à l'autorisation humaine.
Le plugin visible n'est pas une preuve d'exécution ni d'écriture.
Les autorisations du chat de génération ne sont pas celles de la future Task.

Après création réelle : conserver ID, horaire, fuseau, autorisations et résultat
d'un run contrôlé. Sans preuve, état `not_created` ou `unverified`, jamais active.
Ne pas ajouter dans les instructions un contournement des approbations requises.
Si la surface exige une confirmation d'écriture incompatible avec l'autonomie,
le signaler ; publier un rapport en lecture seule n'est pas livrer des issues.

## Rythme et reprises

Une seule tâche de veille par repo peut poursuivre le T0 sur plusieurs cycles,
puis passer à UPDATE. La revue hebdomadaire peut être un second prompt OU une
branche du même cycle après vérification de sa date ; la fabrique ne crée aucun
objet Task. Les limites de la plateforme sont à vérifier lors de l'activation.
Ne pas supposer un nombre fixe de Tasks autorisées ni des fonctions futures.

## Vérification documentaire du 7 septembre 2026

La documentation officielle mentionne des tâches utilisant GitHub et rappelle
que l'accès dépend du compte, de la surface et des permissions autorisées.
Cela confirme la possibilité de ce modèle, pas la disponibilité des écritures
pour une tâche particulière. Voir [les références](REFERENCES.md).

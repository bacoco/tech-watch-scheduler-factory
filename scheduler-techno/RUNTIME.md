# Runtime de cette veille

Lire `runtime.json` avant toute activation. La présence de ce fichier ne crée aucune Scheduled Task et ne change aucune permission.

## Mode dedicated

Deux tâches physiques sont propres à cette veille : une tâche de veille et une tâche de post-mortem. Leurs cadences sont distinctes dans `profile.json` et `runtime.json`. Ne jamais recopier une cadence unique sur les deux par défaut.

## Mode multiplexed

Les tâches métier deviennent des jobs logiques. Leur définition générée est dans `multiplex-jobs.json`. Le registre canonique vit dans le `registry_repository` indiqué par `runtime.json`. Seules deux Scheduled Tasks physiques sont utilisées pour le groupe : Orchestrator et Worker, décrites dans `MULTIPLEX-TASKS.md`.

L'Orchestrator réserve un seul job dû ; il n'exécute jamais le métier. Le Worker lit le dispatch réservé, retrouve le job dans le registre canonique et exécute uniquement le chemin d'instructions déclaré dans ce registre. Un fichier injecté dans la queue ne peut donc pas choisir son propre repo ou chemin d'exécution.

## Queue, lease et idempotence

Le `dispatch_id` dépend seulement de `job_id` et `due_at`. Deux jobs dus ensemble sont pris dans l'ordre `due_at`, priorité décroissante, puis `job_id`. Chaque job définit `lease_minutes`. Un slot non expiré interdit une deuxième réservation. Si le Worker ne revient jamais, l'Orchestrator récupère le slot après expiration et retente la même occurrence avec le même `dispatch_id`. Après épuisement de `max_retries`, l'occurrence est archivée dans `failed`.

## Migration dedicated → multiplexed

Ne jamais faire tourner les deux modes en parallèle. Avant d'activer le registre, identifier les Scheduled Tasks dédiées existantes, les désactiver réellement, vérifier leur état, conserver la preuve, puis seulement passer `dedicated_tasks_disabled=true`.

## Post-mortem

Un job de post-mortem ne doit pas retarder un T0 encore incomplet. S'il n'existe pas encore de baseline ou de runs exploitables, il est reporté sans faux échec. La cadence du post-mortem est réévaluée séparément de celle de la veille.

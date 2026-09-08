# Runtime multiplexé non sélectionné

Le profil `bacoco/tech-watch-scheduler-factory` utilise `dedicated`.
Pour migrer, réviser explicitement `runtime.mode`, définir `group_id` et `registry_repository`, régénérer le pack et appliquer la garde de migration.
Ne jamais exécuter en parallèle tâches dédiées et jobs multiplexés.

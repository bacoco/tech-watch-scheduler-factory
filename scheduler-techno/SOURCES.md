# Stratégie de sources

Décisions spécifiques à `bacoco/tech-watch-scheduler-factory`. Une source listée n'est pas réputée lue lors des futurs runs : chaque cycle réexécute RECHERCHE.md.

## official — primary
- OpenAI Help : Scheduled Tasks, capacités, disponibilité, gestion.
- GitHub Docs : GitHub Apps, permissions, repository access, Pages.
Requêtes : ChatGPT Scheduled Tasks capabilities ; GitHub App repository access ; GitHub Pages publishing source.

## github — primary
Suivre les implémentations, changelogs et issues techniques directement reproductibles sur scheduling, Pages et intégrations.

## products — primary
Comparer les patterns de queues/workers gérés (AWS, Google Cloud, équivalents) pour lease, retry, checkpoint et idempotence.

## community — secondary
Utiliser les retours terrain comme signaux à corroborer par une source primaire.

## arxiv — secondary
Chercher travaux pertinents sur agents, orchestration, fiabilité et évaluation quand ils éclairent une décision.

## web_open — primary
Élargir au-delà de la liste initiale : pratiques de scheduling, publications statiques, permissions et UX d'automatisation.

## models — excluded
Le choix de modèle n'est pas le principal risque de cette factory.

## personal — excluded
Aucune donnée personnelle n'est nécessaire.

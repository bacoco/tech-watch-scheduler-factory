# Recherche de cadrage — génération

Cette recherche a été réellement exécutée le 8 septembre 2026 avant l'installation du self-watch.

## Principaux constats
1. OpenAI documente les Scheduled Tasks comme un produit capable de tâches récurrentes et de surveillance de changements ; la disponibilité dépend du compte, de l'app et de sa version.
2. GitHub Apps sépare les permissions de l'application et la sélection des repositories accessibles. Le 403 rencontré pendant ce test est précisément un cas de repository access non encore accordé.
3. GitHub Pages peut publier depuis `main` + `/(root)` ou `/docs` et exige un entry point à la racine de la source.
4. AWS et Google Cloud convergent sur des patterns utiles au runtime multiplexé : idempotence, retries bornés, checkpointing et lease/visibility timeout pour récupérer le travail après crash.

## Nouvelles directions retenues
- surveiller explicitement les changements de repository access des GitHub Apps ;
- traiter le lease Worker comme un visibility timeout et conserver un test de récupération après crash.

Le journal machine est `discovery.json`. Ce cadrage n'est pas le T0.

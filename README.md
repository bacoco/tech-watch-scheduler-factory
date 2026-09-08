# Tech Watch Scheduler Factory

**Une veille sur mesure pour ton repo, en deux copier-coller très courts dans ChatGPT, avec cadence adaptative et site public généré puis mis à jour automatiquement.**

La fabrique comprend les usages du projet, mène une recherche externe de cadrage, installe `scheduler-techno/`, sépare la cadence de veille de celle du post-mortem et choisit explicitement un runtime `dedicated` ou `multiplexed`. Après activation, la veille crée ou réutilise aussi un dépôt GitHub public séparé `nom-du-repo-website`, y génère le site puis le met à jour à chaque nouveau cycle validé.

**Tout le parcours se fait dans ChatGPT.** Pas de terminal imposé, pas de serveur à louer ni de clé d'API payante à configurer. L'[aide officielle sur les tâches](https://help.openai.com/en/articles/10291617-tasks-in-chatgpt) prévoit des comptes gratuits éligibles, avec des limites ; les accès GitHub, places disponibles et actions autorisées restent à vérifier dans le compte utilisé. Ce n'est pas une promesse de gratuité illimitée.

## 1. Préparer le scheduler du repo

Remplace **[LIEN_DU_REPO]** par le dépôt à surveiller et colle uniquement ceci dans ChatGPT :

> Dans ChatGPT, pour le dépôt [LIEN_DU_REPO], lis et applique intégralement le prompt canonique https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/prompts/PREPARE.md en utilisant [LIEN_DU_REPO] comme TARGET_REPOSITORY. Exécute réellement les actions autorisées et rends les preuves demandées.

Le détail de cette étape vit dans [`prompts/PREPARE.md`](prompts/PREPARE.md), pas dans ce README. Elle comprend l'analyse du repo, la recherche externe, les deux cadences, le runtime, le T0/UPDATE, le contrat website et l'installation de `scheduler-techno/`. Elle ne crée encore aucune tâche planifiée ni repo website.

## 2. Activer la veille et le website

Une fois `scheduler-techno/` publié dans le repo cible, remplace de nouveau **[LIEN_DU_REPO]** et colle uniquement ceci dans ChatGPT :

> Dans ChatGPT, pour le dépôt [LIEN_DU_REPO], lis et applique intégralement le prompt canonique https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/prompts/ACTIVATE.md en utilisant [LIEN_DU_REPO] comme TARGET_REPOSITORY. Active réellement le runtime déclaré et rends les preuves demandées.

Le détail vit dans [`prompts/ACTIVATE.md`](prompts/ACTIVATE.md). Cette étape crée ou réutilise les Scheduled Tasks correspondant au runtime choisi. Elle crée ou réutilise aussi le repo public `*-website`, génère le site statique, publie GitHub Pages si possible et, après chaque T0/UPDATE validé, ajoute ou met à jour l'édition puis rafraîchit automatiquement la home et l'archive.

## Ce que fait le website automatiquement

Le repo surveillé reste la source de vérité, même privé. Le repo public `owner/projet-website` ne contient que la projection éditoriale autorisée.

À la première exécution réussie, la veille doit : créer ou réutiliser le repo website, générer `index.html`, l'archive, l'édition courante, les assets et `.nojekyll`, pousser le tout sur `main`, puis activer GitHub Pages sur `main` + `/(root)` si la capacité existe.

À chaque exécution suivante validée, elle doit ajouter ou corriger l'édition concernée et reconstruire la home + l'archive sans supprimer l'historique. Le détail technique est dans [WEBSITE](docs/WEBSITE.md).

## Cadence adaptative

Chaque profil moderne contient `cadence.watch` et `cadence.postmortem`. Chacun possède une recommandation, une justification, `interval_days`, une borne minimale et une borne maximale. `cadence.adaptation` impose une fenêtre minimale avant changement et plusieurs cycles pauvres avant de ralentir.

Le post-mortem mesure les runs utiles, runs sans changement matériel, sources relues sans impact, doublons, faux positifs et événements découverts en retard. Il propose séparément `keep`, `increase` ou `decrease` pour les deux cadences, avec preuves et chemin de retour. Il ne modifie jamais une vraie tâche sans permission et preuve de cette modification.

## Runtime multiplexé

Le mode multiplexé conserve N jobs métier dans GitHub mais seulement deux Scheduled Tasks physiques. Le repo runtime contient les définitions canoniques, un slot `current-action/job.json`, les archives `completed/` / `failed/` et les reçus. Orchestrator réserve ; Worker exécute. Un dispatch ne gagne jamais le droit de choisir son propre chemin d'instructions.

Les fixtures [cadence rapide](examples/cadence-fast.json), [cadence lente](examples/cadence-slow.json) et [registre à trois jobs](examples/multiplex-registry.json) illustrent les contrats sans prétendre représenter une exécution réelle.

## Une veille sur les usages, pas seulement sur le code

Une veille peut améliorer le service, informer sur son domaine ou faire les deux. GitHub, arXiv, produits, pratiques métier, normes, communautés et sources adjacentes sont des pistes à explorer selon les usages, jamais une liste fermée. Un article ancien découvert aujourd'hui reste recevable : on ne régénère pas le T0 pour l'y faire entrer.

## Des preuves plutôt que des annonces

ChatGPT doit réellement rechercher, lire, écrire et vérifier avant d'annoncer un résultat. Les permissions d'un chat ne prouvent pas celles d'une tâche future. Aucun document privé, secret ou extrait confidentiel ne doit être transmis à un moteur de recherche ou publié dans un dépôt public. Les exemples sont synthétiques.

## Pour comprendre les détails

Les prompts canoniques sont dans [`prompts/`](prompts/README.md). Lire aussi [PROFILE](docs/PROFILE.md), [RUNTIME](docs/RUNTIME.md), [CHATGPT](docs/CHATGPT.md), [WEBSITE](docs/WEBSITE.md), [SECURITY](docs/SECURITY.md) et le [guide de génération](skills/generate-tech-watch/SKILL.md).

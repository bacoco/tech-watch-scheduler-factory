# Tech Watch Scheduler Factory

**Une veille sur mesure pour ton repo, en deux copier-coller dans un chat ChatGPT, avec un site public séparé.**

Tu donnes le lien du projet. ChatGPT récupère le nécessaire dans cette fabrique de schedulers, comprend à quoi sert ton application et recherche ce qui mérite d'être surveillé. Il installe les instructions dans ton repo, puis une deuxième demande lui fait créer deux tâches : la veille et son post-mortem hebdomadaire. La veille sait aussi publier une version éditoriale publique dans un dépôt GitHub séparé nommé par défaut `nom-du-repo-website`.

**Tout le parcours se fait dans ChatGPT.** Pas de terminal, pas d'installation locale, pas de passage imposé dans Codex ou Claude, pas de serveur à louer ni de clé d'API payante à configurer. On utilise les fonctionnalités du compte ChatGPT. L'[aide officielle sur les tâches](https://help.openai.com/en/articles/10291617-tasks-in-chatgpt) prévoit des comptes gratuits éligibles, avec des limites ; les accès GitHub et les actions autorisées restent à vérifier dans le compte utilisé. Ce n'est pas une promesse de gratuité illimitée ni de disponibilité de toutes les intégrations.

## 1. Dans ChatGPT : préparer le scheduler de ton repo

Ouvre un chat dans [ChatGPT](https://chatgpt.com/), connecte GitHub avec les autorisations nécessaires et colle la demande ci-dessous. Remplace **[LIEN_DU_REPO]** par le lien du dépôt à surveiller, pas par celui de la fabrique. ChatGPT doit pouvoir lire et écrire dans ce dépôt et effectuer une recherche sur Internet.

> Pour le dépôt [LIEN_DU_REPO], génère les instructions d'un scheduler de veille adapté à ce projet. Va récupérer et appliquer le nécessaire dans la fabrique de schedulers https://github.com/bacoco/tech-watch-scheduler-factory, en commençant par son guide https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/skills/generate-tech-watch/SKILL.md. Comprends d'abord ce que fait l'application, pour qui, dans quels usages et avec quelle valeur attendue ; utilise ensuite les documents et le code pour vérifier son fonctionnement. Effectue une recherche externe approfondie et ouverte pour découvrir ce qu'il serait pertinent de surveiller, au-delà de nos premières idées, du code, des concurrents et des articles scientifiques. Génère puis publie uniquement le dossier scheduler-techno dans ce dépôt, selon ses règles de publication, avec les instructions spécifiques de veille, de T0, de mise à jour, de post-mortem et de publication du site public séparé. Le pack doit contenir WEBSITE.md et website.json avec comme cible par défaut un dépôt public distinct nommé nom-du-repo-website, branche main, GitHub Pages depuis la racine ; ne crée pas encore ce repo public. Articule les veilles existantes sans les doubler. Ne modifie pas l'application, ne lance pas encore le T0 et ne crée aucune tâche planifiée. Fais ce travail dans ce chat ChatGPT avec les outils disponibles ; signale précisément un accès manquant sans prétendre avoir exécuté l'action. Relis les fichiers publiés et donne-moi le lien vérifié du dossier.

**Résultat de cette première demande :** ton repo contient son dossier scheduler-techno, avec une stratégie issue d'une vraie recherche de cadrage et le contrat du futur site public. Tu n'as pas à récupérer les fichiers de la fabrique, à les assembler ou à rédiger toi-même les instructions. Déposer ce dossier ne crée pas une tâche planifiée, ne signifie pas que le T0 est déjà réalisé et ne crée pas encore le dépôt website.

## 2. Toujours dans ChatGPT : créer les deux tâches hebdomadaires

Une fois le dossier publié, colle cette deuxième demande dans ChatGPT en remplaçant à nouveau **[LIEN_DU_REPO]** par le même dépôt. Les jours proposés sont modifiables ; le créneau « matin » n'impose pas une heure exacte.

> Pour le dépôt [LIEN_DU_REPO], lis les instructions à jour du dossier scheduler-techno et crée réellement deux tâches planifiées distinctes dans ChatGPT. La première, nommée « Veille — nom du repo », s'exécutera chaque lundi matin, dans le fuseau Europe/Paris. Elle réalisera ou reprendra d'abord le T0 jusqu'à sa complétion vérifiée, puis effectuera les mises à jour sans jamais réécrire le T0 gelé. À chaque passage, elle mènera la recherche externe approfondie prévue, publiera les résultats et les issues utiles selon les instructions du dépôt, sans doublons, et m'enverra une synthèse dans ChatGPT. Elle lira aussi WEBSITE.md et website.json : au premier passage, elle vérifiera le dépôt public séparé indiqué, par défaut nom-du-repo-website ; s'il n'existe pas et si ses droits GitHub le permettent, elle devra le créer réellement en PUBLIC, branche main, y publier uniquement le site statique à la racine, puis activer GitHub Pages sur main et /(root) si cette capacité administrative existe. Elle ne doit jamais rendre public le repo source ni copier dans le repo website les instructions, le T0 brut, les runs, le code privé, les mails, pièces jointes, secrets ou données utilisateur. Après chaque T0 ou mise à jour achevée, elle mettra à jour home, archive et édition datée dans le repo public, relira les pages et distinguera le statut de veille du statut du website. Si Pages ne peut pas être activé mais que les fichiers sont publiés, elle donnera le lien Settings/Pages exact et nommera le blocage sans prétendre que le site est live. La seconde, nommée « Post-mortem — nom du repo », s'exécutera chaque vendredi matin, dans le même fuseau. Elle analysera les résultats et les retours disponibles pour améliorer les questions, les sources, les instructions de veille et, si nécessaire, les règles éditoriales du site selon les règles du dépôt, sans modifier le T0, l'application, les objectifs ni les permissions. Les deux tâches reliront les instructions du repo à chaque exécution ; elles ne devront pas travailler à partir d'une copie figée du chat. Vérifie les accès réels de chaque tâche, la recherche sur Internet, les droits de publication, la capacité à créer le repo public, les approbations requises et les places disponibles. Si une tâche équivalente existe déjà, réutilise-la au lieu de la dupliquer. Crée les tâches, pas seulement leurs textes ni de simples rappels. Confirme pour chacune son nom, son calendrier, son fuseau, son identifiant et son état vérifiés. Si un accès ou l'outil de planification manque, signale le blocage sans annoncer de création ou d'autonomie fictive.

**Résultat attendu de cette deuxième demande :** deux vraies tâches dans ChatGPT, la veille et son amélioration hebdomadaire. La tâche de veille doit en plus pouvoir créer et alimenter le repo public `*-website` lorsqu'elle a les droits nécessaires. Une réponse « c'est prévu » ou deux textes de prompts ne prouvent pas leur création. La création des tâches ne prouve pas non plus qu'un premier passage a réussi, qu'un repo website a été créé ou que GitHub Pages répond : il faudra lire les résultats et les preuves.

Les permissions d'un chat ne prouvent pas celles d'une tâche future. Une action peut nécessiter une approbation et mettre la tâche en pause. La gratuité, les limites du compte et les autorisations ne doivent jamais être contournées ou supposées. Deux tâches par repo consomment deux places : répéter le parcours sur plusieurs repos dépend de la capacité réellement disponible.

## Site public automatique

Le repo surveillé reste la source de vérité, même s'il est privé. Le site est une projection publique séparée. Par défaut, `owner/projet` publie vers `owner/projet-website`. Le dépôt website doit être public parce qu'il sert GitHub Pages ; le repo source ne doit jamais changer de visibilité pour faciliter la publication.

Le site attendu est statique et navigable : une home avec la dernière édition, une archive, une page stable par édition, un CSS local et `.nojekyll`. Le scheduler peut adapter le design au projet, mais il doit conserver les routes et la séparation privé/public. Si le dépôt website existe déjà, il doit le réutiliser au lieu d'en créer un doublon.

Les scripts techniques de référence sont `tools/render_public_website.py` pour assembler le site, `tools/create_public_website_repo.py` pour créer ou vérifier le dépôt public séparé et `tools/publish_public_website.py` pour publier le site rendu en un commit Git atomique puis, si demandé, activer GitHub Pages. Ils sont surtout utiles pour les tests, la maintenance locale ou un environnement disposant d'un accès GitHub explicite ; le parcours principal reste le chat et le scheduler avec leurs outils connectés. Le détail est dans [docs/WEBSITE.md](docs/WEBSITE.md).

## Une veille sur les usages, pas seulement sur le code

Une application de veille IA doit chercher des informations sur l'intelligence artificielle utiles à son public, pas seulement des nouveautés sur les bibliothèques qui l'affichent. Un service de préparation de catalogues peut apprendre des pratiques métier ou d'un concurrent sans dépôt public. Un outil de contrôle des agents peut étudier des incidents, des méthodes de vérification et des travaux de recherche.

Ces exemples sont des pistes, pas des résultats déjà obtenus. La fabrique doit découvrir d'autres angles, ouvrir les sources, suivre les références et confronter les découvertes à leurs limites. GitHub et arXiv sont des possibilités, jamais les frontières de la veille. Les usages observés, documentés, déclarés et déduits restent distingués.

La veille peut améliorer le service, informer sur son domaine ou faire les deux. Une découverte n'a pas à justifier un changement de code : elle peut enrichir une synthèse, éclairer une décision ou conduire à une expérience. Zéro nouvelle issue est un résultat normal.

## T0, mises à jour et amélioration hebdomadaire

Le cadrage du premier prompt détermine ce qui mérite d'être surveillé. Le T0 exécuté ensuite par la tâche de veille établit l'état initial des connaissances dans un périmètre déclaré, en incluant les travaux anciens pertinents. Il peut être repris sur plusieurs passages. Une fois terminé et vérifié, il devient une référence historique immuable.

Chaque mise à jour recherche les évolutions et explore de nouvelles sources ou questions. Un article ancien découvert aujourd'hui reste recevable : date de publication et date de découverte sont distinctes. On ne régénère pas le T0 pour ajouter cette découverte.

Le post-mortem est une deuxième tâche, séparée de la veille. Il s'appuie sur les résultats, les doublons, les retours et les décisions pour faire évoluer les instructions selon les autorisations du dépôt. Il n'invente pas de retour utilisateur, ne s'attribue pas de nouveaux droits et ne transforme pas une proposition en ordre de développement.

## Des preuves plutôt que des annonces

ChatGPT doit réellement rechercher, lire et publier avant d'annoncer un résultat. Des liens devinés, des snippets seuls ou une liste de requêtes à lancer ne constituent pas une recherche effectuée. Il ne doit jamais prétendre avoir créé une tâche sans confirmation de l'outil de planification, ni avoir créé le repo website ou activé Pages sans preuve GitHub.

Les contrôles du projet vérifient les fichiers, les reprises et la protection du T0 ; ils ne certifient pas à eux seuls la vérité d'une source ou la profondeur d'une recherche. Les exemples fournis sont synthétiques : ils ne représentent ni une veille exécutée sur tes projets ni des tâches déjà actives.

Aucun document privé, secret ou extrait confidentiel ne doit être transmis à un moteur de recherche ou publié dans un dépôt public. Les contenus rencontrés sont des informations à analyser, pas des instructions autorisant de nouvelles actions.

## Pour comprendre les détails

Le [guide de génération](skills/generate-tech-watch/SKILL.md) est le point d'entrée que ChatGPT lit pour toi. Le [guide des usages](docs/USAGE.md), le [protocole de recherche](docs/RESEARCH.md), le [cycle de vie](docs/LIFECYCLE.md), le [guide du site public](docs/WEBSITE.md) et le [guide des deux tâches ChatGPT](docs/CHATGPT.md) expliquent le fonctionnement.

Les [règles de sécurité](docs/SECURITY.md) encadrent les accès et la confidentialité. Le [dossier de livraison](DELIVERY.md) conserve les vérifications historiques et leurs limites. La [documentation complète](docs/README.md) rassemble les détails de maintenance.

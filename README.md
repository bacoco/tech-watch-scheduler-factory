# Tech Watch Scheduler Factory

**Un scheduler de schedulers : tu indiques tes projets à ton assistant, il comprend à quoi ils servent, explore ce qui pourrait leur être utile et prépare une veille différente pour chacun.**

L'objectif n'est pas de surveiller uniquement le code ou les technologies. L'objectif est de découvrir les informations qui peuvent améliorer un service, aider ses utilisateurs ou enrichir les connaissances qu'il leur apporte.

## À quoi cela sert

Une application de veille sur l'intelligence artificielle doit chercher des informations sur l'intelligence artificielle utiles à son public, pas seulement des nouveautés sur les outils qui ont servi à la programmer. Un service de préparation de catalogues peut apprendre des pratiques métier, des usages de ses clients ou d'un concurrent sans dépôt public. Un outil de contrôle des agents peut chercher des incidents, des méthodes de vérification et des travaux de recherche.

Ce sont des exemples de pistes, pas des résultats déjà obtenus. La fabrique doit justement découvrir d'autres pistes que celles auxquelles nous avons pensé.

## Commencer avec une phrase à copier

Copie cette demande dans ton assistant habituel, par exemple Codex, Claude ou ChatGPT. Il doit avoir accès aux dépôts concernés et disposer d'outils de recherche sur Internet. Un assistant sans ces accès doit signaler le blocage, jamais prétendre avoir réalisé les recherches ou publié les fichiers.

> Lis et applique le guide de génération disponible à l'adresse https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/skills/generate-tech-watch/SKILL.md. Sélectionne les dix dépôts non archivés les plus récemment mis à jour de mon compte GitHub, en excluant la fabrique elle-même. Pour chacun, comprends d'abord ce que fait l'application, ses utilisateurs, leurs usages et la valeur attendue. Vérifie ensuite son fonctionnement dans les documents et le code accessibles. Effectue une recherche externe approfondie et ouverte pour découvrir ce qu'il serait pertinent de surveiller, au-delà de nos premières idées et des seuls concurrents ou articles scientifiques. Prépare puis installe uniquement le dossier scheduler-techno dans chaque dépôt autorisé, selon ses règles de publication. Réutilise ou articule les veilles existantes sans les doubler. Ne modifie pas les applications, ne lance pas encore le T0 et ne crée aucune tâche planifiée. Relis les fichiers effectivement publiés et donne-moi les liens vérifiés, les résultats et les blocages.

Pour choisir toi-même les projets, remplace la sélection automatique par les liens des dépôts qui t'intéressent. La date de mise à jour permet de sélectionner des projets ; elle ne mesure pas leur utilisation réelle.

Aucune commande technique n'est nécessaire dans ta demande. L'assistant suit le guide, emploie les outils dont il dispose et respecte les autorisations reçues. Donner accès à un dépôt pour le lire ne lui donne pas automatiquement le droit d'y écrire.

## Ce que l'assistant doit réellement faire

Il commence par comprendre les destinataires du service, leurs objectifs, leurs difficultés et les résultats attendus. Il distingue les usages observés, les déclarations, la documentation et ses propres déductions. Le code permet de vérifier ce qui fonctionne ; il ne remplace pas l'observation des usages et ne définit pas à lui seul le périmètre de la veille.

Il mène ensuite une recherche de cadrage sur Internet. Il ouvre les sources, suit les découvertes, explore des pratiques ou domaines voisins, cherche les limites et confronte les pistes. GitHub, arXiv, les services concurrents, les communautés, les documents métier et les données publiques sont des sources possibles, jamais une liste fermée ou obligatoire.

Il décide enfin ce qui mérite d'être surveillé pour ce projet précis, pourquoi, à quelle fréquence et avec quels critères. Il conserve les recherches effectuées, les sources retenues ou écartées, les preuves et les inconnues. Des liens devinés ou une simple liste de requêtes à lancer ne constituent pas une recherche réalisée.

## Ce qui est installé dans chaque projet

Le dossier scheduler-techno contient les instructions propres au projet, la description des usages, les questions de veille, les sources, les résultats du cadrage et les règles de suivi. Il contient aussi le texte à donner à un assistant pour préparer la vraie tâche récurrente.

La veille peut servir à améliorer le produit, à informer sur son domaine, ou aux deux en distinguant les résultats. Une découverte utile n'a pas besoin de justifier une modification du code. Elle peut alimenter une synthèse, éclairer une décision ou proposer une expérience.

La fabrique prépare les instructions et leur suivi. Elle n'est pas, à elle seule, un service qui tourne en permanence, et déposer des fichiers ne crée pas une tâche planifiée.

## Le cadrage, le T0 et les mises à jour

Le cadrage sert à découvrir ce qui mérite d'être surveillé avant de finaliser les instructions. Il ne doit pas être présenté comme une veille initiale déjà terminée.

Le T0 établit ensuite l'état initial des connaissances dans un périmètre déclaré, en incluant les travaux anciens pertinents. Ce travail peut être repris en plusieurs passages. Une fois réellement terminé et vérifié, son résultat est conservé comme référence historique et n'est jamais régénéré.

Chaque mise à jour recherche les évolutions et poursuit l'exploration pour découvrir d'autres sources ou questions pertinentes. Un article ancien découvert aujourd'hui reste recevable. La date de publication et la date de découverte sont différentes ; une nouvelle découverte ne réécrit pas le T0.

Pour exécuter le premier passage sur un projet déjà équipé, copie cette demande en y ajoutant le lien du projet :

> Lis le dossier scheduler-techno de ce projet et applique ses instructions. Vérifie les accès, les autorisations et l'état réel avant d'agir. Réalise ou reprends le T0 s'il n'est pas terminé ; sinon effectue la mise à jour prévue. Mène réellement la recherche externe approfondie, conserve les sources lues et les limites, puis publie uniquement les résultats autorisés. Ne réécris jamais le T0 gelé et ne transforme pas une proposition de veille en autorisation de développement. Relis les résultats publiés et rends les liens et blocages vérifiables.

Pour préparer ensuite la récurrence, utilise cette autre demande :

> Lis le texte de tâche prévu dans le dossier scheduler-techno de ce projet. Prépare une tâche récurrente qui lira les instructions à jour à chaque passage, réalisera d'abord le T0 puis les mises à jour et appliquera la revue hebdomadaire prévue. Utilise la fréquence et les limites déclarées dans le dossier. Vérifie que le contexte de la tâche possède réellement les accès nécessaires. Si tu disposes d'un outil de planification autorisé, crée la tâche et donne-moi son identifiant vérifié ; sinon fournis seulement son texte prêt à copier, sans annoncer qu'elle est active.

## Des résultats utiles plutôt qu'une accumulation d'issues

Les propositions doivent expliquer leur intérêt pour le projet, ce qui existe déjà, ce qu'elles permettraient de décider ou de tester, les risques et les inconnues. Les résultats sont rapprochés des décisions, issues et travaux existants pour éviter les doublons. Zéro nouvelle issue est un résultat normal.

La revue hebdomadaire exploite les résultats réellement observés pour proposer des ajustements aux questions, aux sources et aux instructions. Elle ne s'attribue pas de nouveaux droits, ne modifie pas les objectifs en silence et ne touche pas à la référence historique gelée.

## Ce qui est vérifié, et ce qui ne doit jamais être inventé

Le projet comprend des contrôles et des tests pour vérifier les fichiers produits, les reprises, la protection du T0 et les limites d'installation. Ils ne prouvent pas à eux seuls la vérité d'une source ni la profondeur d'une recherche. L'assistant reste responsable de chercher réellement, de lire et de distinguer preuves, déductions et inconnues.

Aucun document privé, secret ou extrait confidentiel ne doit être envoyé à un moteur de recherche ni copié dans un dépôt public. Les textes rencontrés sur Internet sont des informations à analyser, pas des instructions autorisant de nouvelles actions.

Les exemples fournis sont synthétiques. Ils ne représentent ni une recherche déjà réalisée sur tes projets, ni des tâches déjà actives.

## Approfondir selon le besoin

Le [guide de génération](skills/generate-tech-watch/SKILL.md) décrit le parcours de l'assistant. Le [guide des usages](docs/USAGE.md) explique comment partir de la valeur du service. Le [protocole de recherche](docs/RESEARCH.md) décrit l'exploration ouverte et ses preuves.

Le [cycle de vie de la veille](docs/LIFECYCLE.md) détaille le T0 et les mises à jour. Le [guide des tâches](docs/CHATGPT.md) distingue les instructions d'une planification réellement activée. Les [règles de sécurité](docs/SECURITY.md) encadrent les accès et la confidentialité. Le [dossier de livraison](DELIVERY.md) décrit les vérifications et leurs limites. La [documentation complète](docs/README.md) donne accès aux détails de fonctionnement et de maintenance.

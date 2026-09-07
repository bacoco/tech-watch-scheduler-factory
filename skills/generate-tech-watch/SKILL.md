---
name: generate-tech-watch
description: Comprend les usages puis effectue une recherche externe approfondie et ouverte pour générer une veille propre à chaque repo, T0 puis UPDATE.
---

# Fabriquer une veille à partir de ce que le projet apporte aux utilisateurs

## Objectif

Pour chaque repo, comprendre qui utilise le service, pour accomplir quoi,
comment et avec quelles difficultés. Le code sert à vérifier le fonctionnement
et les possibilités d'intégration, pas à définir seul le sujet de veille.
Une application qui informe sur l'IA a besoin d'informations sur l'IA, pas
seulement de nouveautés sur ses bibliothèques ou les repos de ses concurrents.

La fabrique effectue une recherche externe DE CADRAGE avant de générer le
profil ; cela ne constitue pas le T0 complet. Elle produit `scheduler-techno/`.
La vraie tâche est créée séparément. Aucun fichier ne l'active.

## 1. Résoudre la sélection et les droits

Accepter une liste ou les N derniers repos autorisés, non archivés, triés par
`pushed_at`. Une date de commit n'est pas une mesure d'usage. Ne pas supprimer
les forks ou projets documentaires sans analyser leur fonction. Signaler les
repos inaccessibles. Exclure la fabrique elle-même et son activité générée seule.
Annoncer génération, installation par PR ou écriture selon politique explicite.
Sans autorisation d'installation : packs et diffs hors des repos. Aucun cron.

## 2. Comprendre les usages AVANT la stack

Résoudre branche par défaut et SHA. Lire objectif, guide utilisateur, parcours,
écrans ou démonstrations, documentation métier, décisions et retours accessibles.
Chercher qui utilise le résultat, son contexte, ses alternatives (y compris
manuelles), les difficultés, la valeur produite et les critères de réussite.
Utiliser une application réellement accessible si l'accès est autorisé et sans
effet métier ; ne jamais prétendre observer son utilisation à partir du code.
Les observations, déclarations utilisateur, docs et inférences restent distinctes.
L'absence de télémétrie ou d'accès à l'interface est une limite, pas une invention.

Puis lire l'arborescence, les instructions et assez de code/tests pour vérifier
ce qui existe. Examiner les issues ouvertes ET fermées, PR et refus pertinents.
Résoudre les contradictions. Le snapshot n'est qu'une présélection à approfondir.
Aucune donnée privée ou extrait du repo ne part dans un moteur de recherche.

## 3. Formuler ce qui mérite d'être surveillé

Construire le modèle `usage` selon [PROFILE](../../docs/PROFILE.md).
Choisir `product_improvement`, `domain_intelligence` ou `both` : améliorer
l'application, informer sur son domaine, ou faire les deux avec sorties distinctes.
Relier chaque question à un usage, jamais à la seule présence d'une technologie.
Les premières idées du propriétaire et de l'agent sont des pistes, pas une liste
fermée. Ne pas confondre concurrence, implémentation et valeur métier.

## 4. Recherche externe approfondie OBLIGATOIRE à chaque génération

Appliquer [RECHERCHE](../../templates/watch/RECHERCHE.md) : recherches initiales,
élargissement à partir des découvertes, puis recherche de limites/contradictions.
Utiliser réellement les outils de recherche et ouvrir les sources pertinentes.
Explorer au-delà de GitHub, arXiv et des noms déjà proposés : pratiques métier,
services sans repo public, guides, données, normes, travaux, communautés ou
secteurs adjacents selon la fonction du projet. Aucun canal n'est universel.
Choisir ensuite les sources et questions définitives, avec raisons et preuves.

Consigner requêtes exécutées, traces, URLs lues, dates, passages, découvertes,
limites, rejets et conséquences pour les usages dans `discovery`.
Un plan de recherche, des URL devinées ou des snippets seuls ne sont PAS une
recherche effectuée. Sans accès externe effectif : profil `draft`, recherche
`blocked/partial`, blocage nommé ; ne pas fabriquer un profil `ready`.
Zéro piste nouvelle est acceptable ; aucune découverte n'est obligatoire à inventer.
Le validateur vérifie un contrat d'évidence, pas la sincérité ni la profondeur.

## 5. Intégrer l'existant puis générer

Repérer veilles/scouts/schedulers existants : `none`, `coexist`, `reuse-existing`.
Référencer les fichiers canoniques sans copier ni modifier leur état. Une veille
qui couvre déjà le besoin ne doit pas être relancée à côté. Aucun T0 d'un autre
projet n'est importé comme baseline. La recherche de cadrage reste nécessaire.

Rédiger un profil v2 puis `python -m tech_watch generate`. Le Python ne browse
pas le web et ne remplace pas l'agent de recherche. Sans terminal, appliquer les
mêmes contrats par connecteur et ne pas annoncer des tests Python exécutés.
L'état commence en `T0_REQUIRED` ou `INTEGRATION_REQUIRED`. La recherche de
cadrage reste séparée de la baseline, qui n'existe pas encore.

## 6. Installer seulement si autorisé

Écrire uniquement dans `scheduler-techno/`, selon la politique du repo.
Un pack divergent, un SHA différent ou un checkout modifié bloque l'installateur.
Pour un dossier existant, produire un diff revu qui conserve les décisions
humaines, baseline, runs, état et historique ; ne jamais réinitialiser.
Un profil v1 n'est pas rendu v2 par renommage : rechercher les usages et le web.
Épingler la révision de la fabrique dans le reçu de génération.

## 7. Relire et rendre des résultats vérifiables

Pour chaque repo : SHA, usages et limites d'observation, finalité de la veille,
recherches externes effectuées, angles trouvés au-delà des premières idées,
sources retenues/refusées (dont arXiv), intégration, fichiers et commit/PR relu.
Distinguer : `compris`, `recherche de cadrage effectuée`, `généré`, `installé`,
`T0 effectué`, `Task active`. Fournir le prompt d'activation sans activer de tâche.
L'échec d'un repo ne masque pas le résultat des autres. Aucun résultat inventé.

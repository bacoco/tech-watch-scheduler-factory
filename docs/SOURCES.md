# Choisir les sources selon le projet

## La question avant le canal

Partir des usages, des destinataires et du domaine couvert. Vérifier ensuite le
code lorsqu’il éclaire le fonctionnement ou une intégration. Le type de repo
ni sa stack ne suffisent à définir la pertinence. Appliquer RECHERCHE.md à chaque
génération, T0 et UPDATE ; les familles de canaux sont extensibles.
Pour chaque canal, expliquer ce qu'il peut apporter, ce qui doit être vérifié,
et pourquoi il peut être peu utile. Toujours produire une décision arXiv.

| Cas observé | Hypothèse de recherche à vérifier |
|---|---|
| Orchestrateur / harnais | Papiers d'évaluation, mécanismes de contrôle, code et incidents amont |
| Retouche photo | Fidélité des détails, modèles, limites des API, pratiques concurrentes |
| OCR/RAG métier | Extraction mesurée, provenance, données locales, jeux d'évaluation |
| Site vitrine | Produits comparables, accessibilité, framework, performance ; arXiv souvent secondaire |
| Pipeline météo | Données et changements de formats, modèles, révisions et disponibilité historique |
| Fork / bibliothèque | Évolutions amont, divergences, compatibilité et alternatives |

Ces hypothèses ne sont pas des profils préremplis à imposer.

## arXiv et autres travaux de recherche

Requêtes par problème et mécanisme, pas seulement « agents AI ».
Lire la méthode, les limites, les évaluations et le code lorsqu'il existe.
L'abstract seul permet une présélection, pas une conclusion d'adoption.
Quand un tableau/diagramme PDF est essentiel, le lire réellement avec l'outil
approprié ; noter les pages inaccessibles. Préférer HTML lorsque disponible.
Distinguer prépublication, publication évaluée et reproduction indépendante.
Un article ancien peut être prioritaire s'il résout un problème actuel.
Aucune règle « publié après T0 » ni seuil de popularité ne filtre la pertinence.
Conserver les identités canoniques, versions et dates de découverte.

## GitHub et produits concurrents

Lire les changements, tests, issues et limitations, pas seulement les étoiles.
Distinguer annoncé, codé, fusionné, publié, réellement observé. Une étoile ne
prouve pas la fiabilité ; un fork ou repo archivé peut contenir une bonne idée.
Chercher aussi de nouvelles sources à chaque cycle pour éviter un cercle fermé.
Comparer les fonctionnalités utiles au projet, l'effort et les incompatibilités.
Les pages marketing restent des affirmations de leur éditeur, pas des mesures.

## Communautés et sources personnelles

Les communautés donnent des signaux ; corroborer les conclusions techniques
par les sources primaires. Une indisponibilité d'accès est une limite.
Les mails ou liens auto-envoyés ne sont collectés qu'après autorisation explicite
sur comptes/périmètre. Ne jamais exporter les corps ou données perso vers une
issue publique. Leur découverte tardive suit la même règle que celle d'un papier.

## Deux axes de temps

`published_at` décrit le travail ; `first_seen_at` décrit notre connaissance.
Le T0 collecte le passé pertinent. L'UPDATE suit les changements récents ET
les connaissances auparavant inconnues. Une source de 2018 découverte après
un T0 de 2026 est un `newly_discovered_historical`, pas un T0 à reconstruire.

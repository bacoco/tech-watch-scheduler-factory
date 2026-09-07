# Livraison — 7 septembre 2026 — v0.2.0

## Contenu

Cette livraison reprend l'intégralité du code de l'archive v0.2.0 corrigée :
modèle d'usage, recherche de cadrage obligatoire, recherche ouverte pour T0 et
chaque UPDATE, sources extensibles, profils et reçus validés, protection de la
baseline, installation bornée et exemples synthétiques avec tests de régression.

Le README a été réécrit pour expliquer le bénéfice, les usages et le parcours.
La documentation de publication tient compte du dépôt public créé par le propriétaire :
https://github.com/bacoco/tech-watch-scheduler-factory

La correction historique de v0.1 vers v0.2 est conservée dans
[REVISION-2026-09-07](docs/REVISION-2026-09-07.md). Les mentions d'absence de push
qui y figurent décrivent cette ancienne étape locale, pas une limitation des outils.

## Vérifications reproductibles

[Le rapport local](verification/local-2026-09-07.json) conserve les commandes
relancées avant publication : suite de tests, contrôle du dépôt, génération et
validation des deux packs synthétiques. Le workflow CI reprend les deux premiers.

```bash
python -m unittest discover -s tests -v
python tools/check_repository.py
```

Le moteur de recherche est toujours l'agent hôte. Le Python ne dispose pas
d'un LLM ou d'un navigateur embarqué. Les validations ne certifient pas la
sincérité ou la profondeur des traces fournies. Les tests réseau sont simulés.

## Historique de publication

Les premières tentatives de publication ont été bloquées par HTTP 403. Le reçu
[historique](verification/github-publication-2026-09-07.json) conserve cet état,
antérieur à la mise à jour des autorisations par le propriétaire.

Après cette mise à jour, l'écriture du README sur la branche main a réussi :
[commit bc4344a](https://github.com/bacoco/tech-watch-scheduler-factory/commit/bc4344a9736e95bcae1ac2972ff2ce31f71b4cd8).
Le README ne contient désormais aucune commande technique : les demandes à
copier sont rédigées en langage naturel. Les commandes de maintenance sont dans
[LOCAL-USE](docs/LOCAL-USE.md). Trois tests protègent cette interface.

La présence du seul README ne suffit pas à prouver la publication intégrale.
Le contenu complet et son état de validation doivent être contrôlés sur la
branche distante après le transfert ; les reçus historiques restent historiques.

## Ce qui reste distinct de la livraison du code

Aucune recherche spécifique sur les dix repos n'a été effectuée pour cette
publication. Aucun utilisateur réel n'a été observé, aucun profil installé dans
les repos cibles, aucun T0 réel exécuté et aucune tâche ChatGPT activée.

La mise à disposition du code ne rend pas ces opérations accomplies. Le prochain
usage de la fabrique doit lire les projets et rechercher effectivement avant de
rendre des profils prêts. Une archive locale n'est pas une preuve de publication :
relire la branche distante et les fichiers au SHA livré.

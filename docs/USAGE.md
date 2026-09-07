# Comprendre la fonction et l'utilisation avant de choisir la veille

Le nom, la stack et les dépendances d'un repo ne définissent pas ce qui est
utile à ses destinataires. Deux services avec le même code peuvent appeler
des veilles différentes : informer sur un domaine ou améliorer le logiciel.

## Ordre de preuve

Lire les objectifs et guides utilisateur, parcours, écrans, démonstrations,
retours/support autorisés et décisions produit. Observer un parcours réel
lorsque l'accès autorisé le permet, sans effet métier. Puis lire le code et les
tests nécessaires pour vérifier comment le service fonctionne.
Une documentation décrit une intention. Le code décrit un comportement possible.
Ni l'un ni l'autre ne prouve l'utilisation réelle ou la fréquence d'un problème.
Marquer `observed`, `documented` ou `inferred` ; conserver limites et références.

## Modèle de pertinence

Public → situation → objectif → parcours → difficultés → critères de réussite
→ questions de veille → recherche ouverte → information ou décision utile.

`product_improvement` cherche à améliorer le service et ses parcours.
`domain_intelligence` cherche les informations que le service doit fournir.
`both` sépare ces deux besoins, les questions et les sorties associées.
Un service de veille IA doit pouvoir suivre les faits, usages, acteurs ou méthodes
IA utiles à son public sans créer artificiellement une modification de code.
Une application de lots peut bénéficier d'une méthode de contrôle qualité sans
qu'un nouveau modèle ou un repo concurrent en soit la source.

## Limites

Le modèle d'usage peut être suffisamment documenté pour préparer une veille
sans accès à la production. Dire ce qui est inféré ; ne pas inventer des tests,
utilisateurs, statistiques d'usage ou préférences pour rendre le profil prêt.
Les changements de mission relèvent du propriétaire, pas d'une découverte web.

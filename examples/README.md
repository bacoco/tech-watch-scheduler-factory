# Exemples et fixtures

`image-product.json` est un profil SYNTHÉTIQUE pour tester la génération.
Il ne prouve aucune lecture de code réel et ne doit jamais être installé dans
un repo utilisateur sans refaire l'analyse et remplacer les preuves.

`domain-watch.json` illustre une veille d'information sans modification de code.
Ses sources et parcours restent SYNTHÉTIQUES.

`cadence-fast.json` illustre un domaine volatil : veille fréquente mais
post-mortem plus espacé pour accumuler plusieurs observations.

`cadence-slow.json` illustre un domaine plus lent proche du RETEX AY11 : veille
toutes les deux semaines et post-mortem mensuel, avec hystérésis avant ralentissement.

`multiplex-registry.json` contient trois jobs logiques synthétiques pilotables par
un unique couple Orchestrator/Worker. Il sert aux tests d'ordre, idempotence,
retry, migration et refus d'autorité injectée dans la queue.

`bacoco-selection.json` donne seulement des noms de cibles proposés d'après une
demande antérieure. Ce n'est ni un classement courant ni une preuve de disponibilité.

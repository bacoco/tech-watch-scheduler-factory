# Recherche externe de cadrage et recherche récurrente

La version 0.1 mentionnait les usages mais autorisait un profil prêt sans
lecture externe, enfermait les canaux dans sept catégories et demandait trop
souvent un composant de code pour justifier un résultat. La v0.2 corrige cela.

## Contrat commun

Lire [le protocole autonome](../templates/watch/RECHERCHE.md). Il est copié
dans chaque pack et s'applique à la génération, au T0 puis à chaque UPDATE.
Lire aussi [les usages](USAGE.md) et [le profil](PROFILE.md).
Les outils réels de recherche/navigation sont ceux de l'agent hôte. Le Python
n'implémente pas un navigateur ou un modèle autonome : il contrôle les déclarations.

## Ce qui est contrôlé mécaniquement

Un profil prêt requiert usages reliés aux questions ET journal externe complet.
Le journal conserve recherches initiales, expansion et contre-recherche,
sources lues au-delà de GitHub/arXiv et de la liste de départ, indépendance
minimale des éditeurs, dates, limites et conclusions reliées aux usages.
Les familles de sources peuvent être étendues selon les découvertes.
Un ancien profil v1 doit être réellement réanalysé ; le renommer v2 ne suffit pas.

Un run T0 ou UPDATE requiert son propre `research.json`, inclus dans les
artefacts hashés. Le journal de génération ne vaut pas journal T0. Les dates
et le stage empêchent de recycler directement un ancien reçu sous un nouveau nom.
Ces contrôles ne prouvent ni la sincérité des observations ni une couverture
exhaustive. La profondeur reste une obligation d'analyse appuyée sur des traces.

## Politique de reprise

Un accès obligatoire bloqué ou une analyse insuffisante restent partiels.
Conserver les résultats, reprendre ensuite, ne pas avancer un état de réussite.
Aucune publication minimale ni nombre de découvertes n'est imposé.
Une UPDATE peut conclure « rien de nouveau » après une recherche effective.

## Références méthodologiques consultées le 7 septembre 2026

GOV.UK, Learning about users and their needs : partir des personnes, objectifs,
pratiques actuelles et difficultés ; ne pas confondre un besoin avec une solution.
https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs

Government Office for Science, Futures Toolkit (version HTML) : organiser
l'exploration et examiner les hypothèses plutôt que suivre seulement ses habitudes.
https://www.gov.uk/government/publications/futures-toolkit-for-policy-makers-and-analysts/the-futures-toolkit-html

Ces références motivent la méthode ; elles ne constituent PAS les recherches
spécifiques à tes repos, qui n'ont pas été effectuées pendant cette correction.

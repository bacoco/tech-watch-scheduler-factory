# UPDATE — évolution du projet et de la connaissance

## Préconditions

T0 terminé, baseline présente et empreintes vérifiées. Lire le dernier run abouti et les curseurs propres aux sources. Épingler le SHA courant du repo. La baseline est en lecture seule, même si une erreur ancienne est découverte.

## Recherche approfondie à chaque cycle

Relire les usages et appliquer RECHERCHE.md avec des recherches effectivement exécutées. Même repo inchangé : le domaine, les besoins et les solutions peuvent évoluer. Recherche ciblée et ouverte, sans refaire ni modifier le T0.

## Collecte à deux voies

**Suivi :** versions, publications, changements de code, incidents, réponses aux problèmes suivis et évolutions des produits pertinents.
**Découverte :** nouvelles sources, références bibliographiques et travaux anciens encore inconnus. Pas de filtre global « publié après T0 ».

Conserver `published_at`, `first_seen_at`, `source_version`, `repo_sha`. Un papier ancien découvert aujourd'hui est `newly_discovered_historical`. Autres catégories : `new_release`, `new_evidence`, `repo_change`, `correction`.

## Analyse de l'impact

Comparer aux acquis du T0, aux usages actuels et aux informations déjà livrées. Pour une proposition d’amélioration : vérifier aussi code, issues ouvertes ET fermées et PR. Une information de domaine ne nécessite aucune modification. Un problème peut avoir été résolu depuis le dernier run.
Ne pas reproposer un refus sans nommer la nouvelle preuve qui justifie de le rouvrir.

## Publication et état

Appliquer ISSUES.md. Un signal enrichit une issue existante lorsque possible. Écrire rapport, registre des décisions, références relues et receipt complet. En cas d'effet distant incertain, réconcilier l'identifiant avant nouvelle création.
Ne pas avancer la source bloquée. Utiliser recouvrement temporel et déduplication. Une découverte ancienne n'est jamais exclue par un watermark de publication.

`record-update` valide la baseline et un reçu complet puis avance l'état local avec contrôle du précédent run. Il ne réalise aucune publication GitHub. La Task ayant un accès GitHub seul doit respecter le même contrat d'état, avec parent Git attendu ; ne pas prétendre avoir exécuté le CLI.

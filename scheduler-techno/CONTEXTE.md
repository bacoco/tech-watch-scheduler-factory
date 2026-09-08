# bacoco/tech-watch-scheduler-factory

Type : Factory open source qui génère des contrats de veille repository-specific, des cadences adaptatives, un runtime dedicated/multiplexed et un site public GitHub Pages.
Objectif : Surveiller les évolutions de ChatGPT Tasks, GitHub, GitHub Pages et des patterns de scheduling fiables afin que la factory continue à générer des veilles simples à activer, sûres, adaptatives et publiables sur un site public séparé.
Profil : ready
SHA analysé : `de8ee50d79f7bc27e78fd8c259a983a27d4feb90`
Date : 2026-09-08T21:30:00+02:00

## Contraintes
- Le README utilisateur doit rester centré sur deux mini-prompts ; la logique détaillée reste versionnée dans prompts/.
- Aucune tâche, repo runtime ou repo website ne doit être déclaré créé sans preuve d'outil.
- Le repo source reste canonique ; le repo website ne reçoit que la projection publique.
- Le T0 est gelé une fois ; les corrections futures passent par UPDATE.

## Preuves de lecture
- **e1** / documentation : README — deux mini-prompts et website automatique.
- **e2** / documentation : docs/RUNTIME.md — dedicated/multiplexed, lease, retry, garde de migration.
- **e3** / documentation : docs/WEBSITE.md — projection publique séparée et GitHub Pages.
- **e4** / documentation : prompts/ACTIVATE.md — activation des tâches et mise à jour website après T0/UPDATE.

## Inconnues bloquantes
Aucune à la génération.

## Intégration
Mode : none
Aucun `scheduler-techno/` n'existait au SHA analysé.

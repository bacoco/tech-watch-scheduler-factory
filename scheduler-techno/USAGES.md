# Usages de cette veille

## Finalité
`product_improvement`

La factory doit rester simple à installer depuis ChatGPT tout en étant rigoureuse sur les preuves, permissions, T0, reprise et séparation repo source / website.

## u1 — Mainteneur
**But :** faire évoluer la factory sans casser T0, runtime ou publication.
**Parcours :** lire le repo → cadrer → générer → activer → observer → post-mortem.
**Risques :** capacités externes changeantes, permissions partielles, faux succès, doubles effets.
**Succès :** contrats cohérents, blocages nommés, reprise sûre.

## u2 — Utilisateur ChatGPT
**But :** installer une veille et son website avec deux mini-prompts.
**Parcours :** PREPARE → ACTIVATE → tâches → T0/UPDATE → site public.
**Risques :** prompts trop longs, repo non autorisé à l'app GitHub, Pages non activé.
**Succès :** deux prompts courts, repo website séparé, URL vérifiée.

## u3 — Opérateur multi-repos
**But :** gérer plusieurs veilles avec des slots bornés.
**Parcours :** choisir dedicated/multiplexed → réserver → exécuter → reprendre.
**Risques :** worker crash, slot bloqué, doublons.
**Succès :** dispatch déterministe, lease récupérable, retry borné.

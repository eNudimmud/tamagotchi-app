# Contrat HTTP — Backend v4

Jeton local obligatoire (`X-Enki-Token`, valeur dans `backend/enki_token.txt`)
sur toutes les routes sauf `GET /health`. Réponses JSON UTF-8. `user_id`
(défaut `demo-user`) isole chaque créature : corps dans `enki_state.json`,
esprit dans `enki_home/<user_id>/` (etat, souvenirs, faits, audit, .ics).

## Corps (v3, conservé)

`GET /creature` — état complet du corps + bloc `esprit` (humeur, confiance,
autonomie, mode système, compétences, promesses en attente, portrait ASCII).
`POST /interact {user_id, type}` — feed/pet/play/sleep/clean/train/talk/evolve ;
409 si `no_carrot`. `POST /grant {user_id, amount}` — carottes **gratuites**
(anti pay-to-love). `POST /iap/verify` — 403 en MVP, volontairement.
`POST /rename {user_id, name}` — renomme corps et esprit.

## Esprit (v0.4, loi ECOS)

`POST /talk {user_id, text}` → `{reply[], pending?, evenements[], promesses[],
esprit}`. Détecte les promesses (« rappelle-moi de… demain à 18h »), en mémoire
avec provenance ; si une promesse attend, **propose** l'outil calendrier :
`pending` contient `action_id`, la carte de permission, le niveau, `expire`
(600 s), `strong_required` (niveau ≥ 3). **Rien n'est exécuté.**

`POST /confirm {user_id, action_id, approve, strong?}` → exécution du pipeline
complet (politique → consentement → exécution → vérification → audit → XP).
Codes : 200 (exécuté ou refusé proprement), 410 (inconnue/expirée/déjà
consommée — usage unique), 428 (confirmation forte requise), 409 (hash des
paramètres invalidé). Réponse : `decision`, `evenement` (nomenclature ECOS),
`verifie`, `sortie` (chemin du .ics), `reply[]`.

`GET /audit?user_id&n` — les n dernières entrées append-only (jamais de
secrets : clés sensibles refusées et expurgées, SC-007).
`GET /promesses` · `GET /memoire` (épisodes avec `epistemique` + `provenance`,
faits avec historique de corrections) · `GET /reves` · `GET /export` — paquet
`seve-export-1` intégral (anti-lock-in).
`POST /mode {user_id, mode}` — NORMAL, NO_LLM, READ_ONLY, NO_EXTERNAL_TOOLS,
MEMORY_LIMITED, WORLD_PAUSED, SAFE_IDLE (Art. 23 : dégradation honnête,
READ_ONLY bloque toute écriture avec `PERMISSION.VIOLATION_BLOCKED`).

## Invariants tenus par le serveur

Le LLM/la bouche ne touche jamais un outil ; toute écriture passe par
carte → confirmation à usage unique liée au hash exact des paramètres ;
un succès non vérifié ne compte pas ; l'audit ne ment pas ; l'absence ne
punit jamais (rattrapage : rêves et maturation, pas de reproche).

# Backend v4 — corps v3 + esprit v0.4 (loi ECOS)

- `server.py` — couche HTTP fine (stdlib `http.server`), jeton local, verrou
  d'écriture unique. Ne contient aucune logique de créature.
- `moteur.py` — le moteur v0.4 : émotions, mémoire épistémique à provenance,
  promesses, registre d'outils N0–N4, confirmations par hash, modes système,
  audit append-only. **Référence exécutable** : `python3 moteur.py --selftest`
  (20 tests, invariants constitutionnels C1–C9).
- `tests/test_server.py` — 11 tests d'intégration HTTP (vrai serveur, vrai
  disque) : jeton, anti pay-to-love, pipeline /talk → /confirm à usage unique,
  READ_ONLY, provenance, export, isolation des identités.

Fichiers générés (ignorés par git) : `enki_token.txt`, `enki_state.json`,
`enki_events.jsonl`, `enki_home/<user_id>/`.

La hiérarchie d'autorité : `docs/foundation/` > `docs/ecos-alignment.md` >
ce code. En cas de doute sur un comportement, le selftest du moteur fait foi.

# ENKI Tamagotchi — Backend v4 (Termux, 100 % stdlib, zéro dépendance)

Corps v3 (jauges, stades, carottes gratuites) + esprit v0.4 sous loi ECOS
(mémoire à provenance, promesses, permissions, audit, modes honnêtes).
Voir `docs/foundation/` (la loi), `docs/ecos-alignment.md` (le pacte),
`docs/BACKEND_API.md` (le contrat HTTP).

## 1. Lancer le backend (Python système uniquement — aucun pip)

```
cd ~/tamagotchi-app/backend
pkill -f "server.py" 2>/dev/null; sleep 1
python server.py > ~/enki.log 2>&1 &
sleep 2
cat ~/enki.log
```

Le log affiche l'URL et **le jeton local** (aussi dans `backend/enki_token.txt`) :

```
ENKI Tamagotchi Backend v4 (corps v3 + esprit 0.4.0-ref, loi ECOS)
  http://127.0.0.1:8000
  jeton local (X-Enki-Token) : <JETON>
```

Sur Android, 127.0.0.1 est joignable par toutes les apps du téléphone :
le jeton ferme la porte. Toutes les routes l'exigent, sauf `/health`.

## 2. Tester depuis Termux

```
T=$(cat ~/tamagotchi-app/backend/enki_token.txt)
curl 127.0.0.1:8000/health
curl -H "X-Enki-Token: $T" 127.0.0.1:8000/creature
curl -H "X-Enki-Token: $T" -X POST 127.0.0.1:8000/grant \
  -H "Content-Type: application/json" -d '{"user_id":"demo-user","amount":5}'
```

La boucle des dix étapes, à la main :

```
curl -H "X-Enki-Token: $T" -X POST 127.0.0.1:8000/talk \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","text":"rappelle-moi d'"'"'appeler maman demain à 18h"}'
# → réponse avec "pending": la carte de permission + action_id. RIEN n'est écrit.

curl -H "X-Enki-Token: $T" -X POST 127.0.0.1:8000/confirm \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","action_id":"<ACTION_ID>","approve":true}'
# → "TOOL.RESULT_VERIFIED", le chemin du .ics, la promesse passe à "tenue".

curl -H "X-Enki-Token: $T" "127.0.0.1:8000/audit?user_id=demo-user&n=5"
```

## 3. Tests

```
cd ~/tamagotchi-app/backend
python moteur.py --selftest      # 20 tests, invariants C1–C9 de la loi
python tests/test_server.py      # 11 tests d'intégration HTTP
```

La CI (`.github/workflows/backend-tests.yml`) rejoue les deux à chaque push.

## 4. App Flutter (build externe recommandé)

L'app pointe sur `http://localhost:8000`. Compiler l'APK sur PC/CI :

```
flutter build apk --debug --dart-define=ENKI_TOKEN=<JETON>
adb install app/build/app/outputs/flutter-apk/app-debug.apk
```

Sans `--dart-define`, colle le jeton dans **Réglages → Jeton local**.
L'onglet **Parler** montre le pipeline complet : proposition → carte de
permission → refus/accord → « ✓ vérifié » avec le chemin du fichier.

## Notes

- Backend = stdlib Python 3.8+ (`http.server`). Aucune dépendance. Tourne partout.
- Aucune chaîne/portefeuille. `/iap/verify` refuse (anti pay-to-love, Art. 19).
- Les carottes se récoltent gratuitement via `/grant`.
- La créature s'exporte intégralement : `GET /export` (anti-lock-in, Art. 1 & 8).

# ENKI Tamagotchi — Backend (Termux, 100% stdlib, zéro dépendance)

## 1. Sur Termux (tel) — extraire le tarball reçu
```
cd ~
tar xzf enki-tamagotchi.tar.gz
cd tamagotchi/backend
```

## 2. Lancer le backend (Python système uniquement — aucun pip/uv needed)
```
cd /data/data/com.termux/files/home/tamagotchi/backend
pkill -f "app.main" 2>/dev/null; sleep 1
python app/main.py > ~/enki.log 2>&1 &
sleep 2
curl 127.0.0.1:8000/health
cat ~/enki.log
```

Tu dois voir : `{"status":"ok"}` et `ENKI Tamagotchi Backend on http://127.0.0.1:8000`

## 3. Tester les endpoints (depuis Termux)
```
curl 127.0.0.1:8000/creature
curl -X POST 127.0.0.1:8000/iap/verify -H "Content-Type: application/json" -d '{"user_id":"demo","store_receipt":"mock","carrot":5}'
curl -X POST 127.0.0.1:8000/interact -H "Content-Type: application/json" -d '{"user_id":"demo","type":"feed"}'
```

## 4. Flutter app (Option A recommandée : build externe)
L'app pointe sur `http://localhost:8000` (tel physique OK).
Compiler l'APK sur PC/CI (voir README_TERMUX.md section Flutter) :
```
flutter build apk --release
```
Puis `adb install build/app/outputs/flutter-apk/app-release.apk` sur le tel.
Le backend tourne déjà sur le tel (étape 2), l'app s'y connecte en local.

## Notes
- Backend = stdlib Python 3.8+ (urllib/http.server). Aucune dépendance. Tourne partout.
- Aucune chaîne/portefeuille dans le code app. Conformité store validée.
- Burn = mock (N4 hard-block). Aucune tx réelle sans validation utilisateur.

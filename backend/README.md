# ENKI Tamagotchi — Backend (Termux / local, zero-dependency)

Single-file Python stdlib HTTP server. **No pip, no venv, no FastAPI/uvicorn/pydantic.**
Runs on Android Termux (bionic) where `pydantic-core` cannot compile.

## Deploy on Termux (Android)

```bash
# 1. paste the server into the phone (via heredoc in Termux)
cat > ~/enki_backend.py << 'PYEOF'
<content of server.py>
PYEOF

# 2. launch in background
nohup python ~/enki_backend.py > ~/enki.log 2>&1 &

# 3. check
curl 127.0.0.1:8000/health
# -> {"status":"ok"}
```

The Flutter app (built separately as an APK) talks to `http://localhost:8000`.

## Endpoints

| Method | Path | Response |
|---|---|---|
| GET | `/health` | `{"status":"ok"}` |
| GET | `/creature?user_id=demo` | `CreatureState` (id, stage, stats, resources) |
| POST | `/interact` `{user_id, type}` | `InteractResult` (progressed, progress_signature, stage, stats, resources) |
| POST | `/iap/verify` `{user_id, carrot, energy, kiss}` | `Resources` |

## Contract (matches the Flutter companion app)

```jsonc
CreatureState {
  "id": "demo", "stage": 1, "stage_name": "RABBIT",
  "stats": {"vitality": 50, "awakening": 0, "bond": 0},
  "resources": {"carrot": 0, "energy": 0, "kiss": 0},
  "progressed": false, "progress_signature": null, "disjoncteur_count": 0
}
InteractResult {
  "progressed": true, "progress_signature": "24241ffb2fa5da1c",
  "stage": 1, "stats": {...}, "resources": {...}
}
```

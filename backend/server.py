"""ENKI Tamagotchi Backend - single-file stdlib server (Termux-safe, ZERO deps).

Emits the JSON contract expected by the Flutter companion app:
  GET  /creature?user_id=... -> CreatureState { id, stage, stats{vitality,awakening,bond}, resources{carrot,energy,kiss}, disjoncteur_count }
  POST /interact {user_id, type} -> InteractResult { progressed, progress_signature, stage, stats, resources }
  POST /iap/verify {user_id, carrot, energy, kiss} -> Resources { carrot, energy, kiss }
  GET  /health -> {status:"ok"}
"""
from enum import IntEnum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import urllib.parse
import time
import hashlib

STAGE_NAMES = {0: "EGG", 1: "RABBIT", 2: "APPRENTICE", 3: "GARDENER", 4: "GUARDIAN"}


class Stage(IntEnum):
    EGG = 0
    RABBIT = 1
    APPRENTICE = 2
    GARDENER = 3
    GUARDIAN = 4


class Creature:
    def __init__(self, user_id):
        self.user_id = user_id
        self.stage = Stage.RABBIT
        self.carrots = 0
        self.progress = 0
        self.last_interaction = time.time()

    def stats(self):
        return {
            "vitality": max(0, min(100, 50 + self.progress)),
            "awakening": self.progress,
            "bond": self.carrots,
        }

    def resources(self):
        return {"carrot": self.carrots, "energy": 0, "kiss": 0}

    def to_state(self):
        return {
            "id": self.user_id,
            "stage": int(self.stage),
            "stage_name": STAGE_NAMES[int(self.stage)],
            "stats": self.stats(),
            "resources": self.resources(),
            "progressed": False,
            "progress_signature": None,
            "disjoncteur_count": 0,
        }

    def to_interact(self, progressed):
        sig = (
            hashlib.sha256(
                f"{self.user_id}:{self.progress}:{time.time()}".encode()
            ).hexdigest()[:16]
            if progressed
            else None
        )
        return {
            "progressed": progressed,
            "progress_signature": sig,
            "stage": int(self.stage),
            "stats": self.stats(),
            "resources": self.resources(),
        }


CREATURES = {}


def get_creature(user_id):
    if user_id not in CREATURES:
        CREATURES[user_id] = Creature(user_id)
    return CREATURES[user_id]


def handle_interact(user_id, action):
    cr = get_creature(user_id)
    cr.last_interaction = time.time()
    before = cr.progress
    before_stage = int(cr.stage)
    if action == "feed":
        cr.carrots += 1
        cr.progress += 5
    elif action in ("pet", "play"):
        cr.progress += 2
    elif action in ("train", "evolve", "task"):
        cr.progress += 8
    while cr.progress >= 100 and int(cr.stage) < 4:
        cr.progress -= 100
        cr.stage = Stage(int(cr.stage) + 1)
    progressed = (cr.progress != before) or (int(cr.stage) != before_stage)
    return cr, progressed


def handle_iap(user_id, carrots, energy=0, kiss=0):
    cr = get_creature(user_id)
    cr.carrots += carrots
    return {"carrot": cr.carrots, "energy": energy, "kiss": kiss}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/health":
            self._send(200, {"status": "ok"})
        elif path == "/creature":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            uid = q.get("user_id", ["demo"])[0]
            self._send(200, get_creature(uid).to_state())
        else:
            self._send(404, {"error": "not_found"})

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw or b"{}")
        except Exception:
            data = {}
        if path == "/interact":
            uid = data.get("user_id", "demo")
            act = data.get("type", "feed")
            cr, progressed = handle_interact(uid, act)
            self._send(200, cr.to_interact(progressed))
        elif path == "/iap/verify":
            uid = data.get("user_id", "demo")
            carrots = int(data.get("carrot", 0))
            energy = int(data.get("energy", 0))
            kiss = int(data.get("kiss", 0))
            self._send(200, handle_iap(uid, carrots, energy, kiss))
        else:
            self._send(404, {"error": "not_found"})

    def log_message(self, *a):
        pass


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("ENKI Tamagotchi Backend on http://127.0.0.1:8000")
    srv.serve_forever()


if __name__ == "__main__":
    main()

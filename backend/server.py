"""ENKI Tamagotchi Backend v2 - single-file stdlib server (Termux-safe, ZERO deps).

Modèle de compagnon riche : besoins qui décroissent dans le temps (faim, energie,
hygiene, social, fun), humeur derivee, cycle jour/nuit + phase lunaire, stades
d'evolution (EGG -> RABBIT -> APPRENTICE -> GARDENER -> GUARDIAN).

Contrat JSON:
  GET  /creature?user_id=... -> CreatureState
  POST /interact {user_id, type} -> InteractResult
  POST /iap/verify {user_id, carrot, energy, kiss} -> Resources
  POST /rename {user_id, name} -> {name}
  GET  /health -> {status:"ok"}

Aucune dependance externe : http.server stdlib uniquement. Tourne sur Termux.
"""
from enum import IntEnum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import urllib.parse
import time
import hashlib

STAGE_NAMES = {0: "EGG", 1: "RABBIT", 2: "APPRENTICE", 3: "GARDENER", 4: "GUARDIAN"}

# Decroissance des besoins, points par minute (tel reste ouvert longtemps -> vivant).
DECAY = {
    "hunger": 0.30,   # faim : 0 = affame
    "energy": 0.22,   # energie : 0 = epuise
    "hygiene": 0.15,  # proprete : 0 = sale
    "social": 0.28,   # lien : 0 = ignore
    "fun": 0.36,      # amusement : 0 = ennuie
}

MOON_PHASES = [
    "new", "waxing_crescent", "first_quarter", "waxing_gibbous",
    "full", "waning_gibbous", "last_quarter", "waning_crescent",
]

# Une "journee" demo = 4 minutes (jour 60%, nuit 40%) pour voir le cycle vivre.
DAY_SECONDS = 240
DAY_FRACTION = 0.6
# Une lunaison demo = 8 journees.
MOON_PERIOD_DAYS = 8


class Stage(IntEnum):
    EGG = 0
    RABBIT = 1
    APPRENTICE = 2
    GARDENER = 3
    GUARDIAN = 4


class Creature:
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = "Enki"
        self.stage = Stage.RABBIT
        self.needs = {"hunger": 72, "energy": 70, "hygiene": 82, "social": 60, "fun": 62}
        self.awakening = 0
        self.bond = 0
        self.carrots = 0
        self.energy_res = 0
        self.kiss = 0
        self.born = time.time()
        self.last = time.time()
        self.disjoncteur = 0

    # --- dynamique temporelle ---
    def decay(self):
        now = time.time()
        dt = (now - self.last) / 60.0
        if dt > 0:
            for k, rate in DECAY.items():
                self.needs[k] = max(0, min(100, self.needs[k] - rate * dt))
            self.last = now

    def mood(self):
        n = self.needs
        if n["hygiene"] < 15:
            return "sick", int(n["hygiene"])
        if n["energy"] < 15:
            return "sleepy", int(n["energy"])
        if n["hunger"] < 15:
            return "hungry", int(n["hunger"])
        if n["fun"] < 20:
            return "bored", int(n["fun"])
        if n["social"] < 20:
            return "sad", int(n["social"])
        score = int(sum(n.values()) / len(n))
        return ("happy" if score > 70 else "content"), score

    def vitality(self):
        return max(0, min(100, int((self.needs["hunger"] + self.needs["energy"] + self.needs["hygiene"]) / 3)))

    def cycle(self):
        age = time.time() - self.born
        day_idx = int(age // DAY_SECONDS)
        into_day = age % DAY_SECONDS
        is_day = into_day < (DAY_SECONDS * DAY_FRACTION)
        moon_idx = int((day_idx % (MOON_PERIOD_DAYS * len(MOON_PHASES))) // MOON_PERIOD_DAYS) % len(MOON_PHASES)
        return {"is_day": is_day, "phase": MOON_PHASES[moon_idx], "day_count": day_idx}

    # --- actions ---
    def apply(self, action):
        before_stage = int(self.stage)
        before_awaken = self.awakening
        n = self.needs
        ok = True
        msg = ""
        if action == "feed":
            if self.carrots > 0:
                self.carrots -= 1
                n["hunger"] = min(100, n["hunger"] + 38)
                self.bond = min(100, self.bond + 1)
            else:
                ok = False
                msg = "no_carrot"
        elif action == "pet":
            n["social"] = min(100, n["social"] + 22)
            self.bond = min(100, self.bond + 4)
            self.kiss = min(999, self.kiss + 1)
        elif action == "play":
            n["fun"] = min(100, n["fun"] + 30)
            n["energy"] = max(0, n["energy"] - 12)
            if self.carrots > 0 and (self.bond % 3 == 0):
                self.carrots -= 1  # jouer coute parfois une carotte
        elif action == "sleep":
            n["energy"] = min(100, n["energy"] + 55)
            n["fun"] = min(100, n["fun"] + 8)
        elif action == "clean":
            n["hygiene"] = min(100, n["hygiene"] + 50)
        elif action == "train":
            self.awakening = min(100, self.awakening + 7)
            n["energy"] = max(0, n["energy"] - 10)
            n["fun"] = min(100, n["fun"] + 4)
        elif action == "talk":
            n["social"] = min(100, n["social"] + 16)
            n["fun"] = min(100, n["fun"] + 10)
            self.bond = min(100, self.bond + 2)
        elif action == "evolve":
            if int(self.stage) < 4:
                self.stage = Stage(int(self.stage) + 1)
                self.awakening = 0
                self.bond = min(100, self.bond + 10)
            else:
                ok = False
                msg = "max_stage"
        else:
            ok = False
            msg = "unknown_action"

        progressed = (self.awakening != before_awaken) or (int(self.stage) != before_stage)
        return ok, msg, progressed

    # --- serialisation ---
    def to_state(self):
        self.decay()
        mstate, mscore = self.mood()
        return {
            "id": self.user_id,
            "name": self.name,
            "stage": int(self.stage),
            "stage_name": STAGE_NAMES[int(self.stage)],
            "needs": {k: int(v) for k, v in self.needs.items()},
            "mood": {"state": mstate, "score": int(mscore)},
            "vitality": self.vitality(),
            "awakening": int(self.awakening),
            "bond": int(self.bond),
            "resources": {"carrot": int(self.carrots), "energy": int(self.energy_res), "kiss": int(self.kiss)},
            "cycle": self.cycle(),
            "disjoncteur_count": int(self.disjoncteur),
            "progressed": False,
            "progress_signature": None,
        }

    def to_interact(self, ok, msg, progressed):
        sig = (
            hashlib.sha256(f"{self.user_id}:{self.awakening}:{time.time()}".encode()).hexdigest()[:16]
            if progressed else None
        )
        body = {
            "ok": ok,
            "message": msg,
            "progressed": progressed,
            "progress_signature": sig,
            "stage": int(self.stage),
            "needs": {k: int(v) for k, v in self.needs.items()},
            "mood": {"state": self.mood()[0], "score": self.mood()[1]},
            "vitality": self.vitality(),
            "awakening": int(self.awakening),
            "bond": int(self.bond),
            "resources": {"carrot": int(self.carrots), "energy": int(self.energy_res), "kiss": int(self.kiss)},
        }
        return body


CREATURES = {}


def get_creature(user_id):
    if user_id not in CREATURES:
        CREATURES[user_id] = Creature(user_id)
    return CREATURES[user_id]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/health":
            self._send(200, {"status": "ok"})
        elif path == "/creature":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            uid = q.get("user_id", ["demo-user"])[0]
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
        uid = data.get("user_id", "demo-user")
        cr = get_creature(uid)
        if path == "/interact":
            act = data.get("type", "feed")
            cr.decay()
            ok, msg, progressed = cr.apply(act)
            code = 200 if ok else 409
            self._send(code, cr.to_interact(ok, msg, progressed))
        elif path == "/iap/verify":
            carrots = int(data.get("carrot", 0))
            energy = int(data.get("energy", 0))
            kiss = int(data.get("kiss", 0))
            cr.carrots += carrots
            cr.energy_res += energy
            cr.kiss += kiss
            self._send(200, {"carrot": cr.carrots, "energy": cr.energy_res, "kiss": cr.kiss})
        elif path == "/rename":
            name = str(data.get("name", "")).strip()[:24]
            if name:
                cr.name = name
            self._send(200, {"name": cr.name})
        else:
            self._send(404, {"error": "not_found"})

    def log_message(self, *a):
        pass


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("ENKI Tamagotchi Backend v2 on http://127.0.0.1:8000")
    srv.serve_forever()


if __name__ == "__main__":
    main()

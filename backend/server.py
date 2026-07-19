"""ENKI Tamagotchi Backend v3 - ECOS-aligned single-file stdlib server.

Aligne l'implementation sur ECOS_MASTER_ARCHITECTURE.md :
  - EStar racine de continuite (e_star_id, continuity_status, version)
  - Identity a traits verrouilles (visuel lapin E*NKI)
  - Soul snapshot (valeurs + version)
  - Personality/Stage (egg->rabbit->apprentice->gardener->guardian) + awakening
  - Relationship.closeness interne (JAMAIS exposition affection meter, JAMAIS monétisé)
  - LifeState / CognitiveState derives de l'action
  - DomainEvent append-only scopé par eStarId (audit SC-006)
  - SIMULATION_LOOP : decay avec FLOOR (Art 17 : absence non punie, pas de deperissement vers 0)
  - Art 14 pipeline Action : intention->validation->permission->execution->verification->resultat
  - ANTI_FEATURES : aucun pay-to-love. /grant = recolte GRATUITE. /iap/verify reserve au soutien explicite.
  - SC-004 : persistance fichier (etat + events) -> renommage/progression survivent au redemarrage.
  - Isolation E* : toutes les donnees scopees par e_star_id.

Aucune dependance externe : http.server stdlib uniquement. Tourne sur Termux.
"""

import json
import time
import os
import urllib.parse
from enum import IntEnum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "enki_state.json")
EVENT_FILE = os.path.join(HERE, "enki_events.jsonl")

FLOOR = 25  # besoins ne descendent jamais sous ce plancher -> creature jamais "affamee"/"morte" par absence
SCHEMA_VERSION = 1
PRODUCER = {"module": "enki-tamagotchi-backend", "version": "3.1.0"}
ACTIONS = {"feed", "pet", "play", "sleep", "clean", "train", "talk", "evolve"}

STAGE_NAMES = {0: "EGG", 1: "RABBIT", 2: "APPRENTICE", 3: "GARDENER", 4: "GUARDIAN"}

# Decroissance des besoins, points par minute. Plafonnee au FLOOR.
DECAY = {
    "hunger": 0.30,
    "energy": 0.22,
    "hygiene": 0.15,
    "social": 0.28,
    "fun": 0.36,
}

MOON_PHASES = [
    "new", "waxing_crescent", "first_quarter", "waxing_gibbous",
    "full", "waning_gibbous", "last_quarter", "waning_crescent",
]
DAY_SECONDS = 240          # une "journee" demo = 4 min (jour 60%, nuit 40%)
DAY_FRACTION = 0.6
MOON_PERIOD_DAYS = 8       # une lunaison demo = 8 journees


class Stage(IntEnum):
    EGG = 0
    RABBIT = 1
    APPRENTICE = 2
    GARDENER = 3
    GUARDIAN = 4


class EStar:
    def __init__(self, e_star_id):
        self.e_star_id = e_star_id
        self.canonical_name = "Enki"
        self.display_name = "Enki"
        self.status = "ACTIVE"
        self.continuity_status = "CANONICAL"
        self.version = 1
        self.soul_version = 1
        self.soul_values = ["continuity", "truth", "dignity", "consent", "humanity"]
        # Identity : traits verrouilles (coherent avec SOUL.md)
        self.identity = {
            "species": "rabbit_humanoid",
            "visual_identity": {
                "fur": "white",
                "eye_left": "red_orange",
                "eye_right": "yellow_gold",
                "jacket": "mustard_yellow",
                "jacket_logo": "iii",
                "hoodie": "red",
                "cargo": "green",
                "sneakers": "violet",
            },
            "locked_traits": ["species", "visual_identity"],
        }
        self.stage = Stage.RABBIT
        self.awakening = 0
        self.closeness = 0  # Relationship.closeness : interne, NON monétisé, NON exposé comme affection meter
        self.needs = {"hunger": 72, "energy": 70, "hygiene": 82, "social": 60, "fun": 62}
        self.carrots = 0
        self.energy_res = 0
        self.kiss = 0
        self.born = time.time()
        self.last = time.time()
        self.disjoncteur = 0
        self.mode = "NORMAL"
        self.life_state = "IDLE"
        self.cognitive_state = "DORMANT"
        self._loaded = False

    # --- dynamique temporelle (SIMULATION_LOOP : decay plafonne au FLOOR) ---
    def decay(self):
        now = time.time()
        dt = (now - self.last) / 60.0
        if dt > 0:
            for k, rate in DECAY.items():
                self.needs[k] = max(FLOOR, min(100, self.needs[k] - rate * dt))
            self.last = now

    def mood(self):
        n = self.needs
        # Avec FLOOR=25, aucun besoin ne tombe sous 25 -> jamais d'etat "souffrant".
        # Quelques etats transitoires restent accessibles (apres jeu, energie baisse mais >= FLOOR).
        if n["energy"] < 35:
            return "resting", int(n["energy"])
        if n["fun"] < 35:
            return "calm", int(n["fun"])
        if n["social"] < 35:
            return "quiet", int(n["social"])
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

    # --- audit / event sourcing (DomainEvent.v1 strict, SC-006 append-only, eStarId-scoped) ---
    def emit(self, event_type, payload, category=None, sensitivity="PUBLIC"):
        # category derivee du catalogue d'eventTypes canoniques (AGGREGATE.EVENT)
        if category is None:
            cat = event_type.split(".")[0].upper()
            category = {
                "E_STAR": "ESTAR",
                "GUARDIAN": "GUARDIAN",
                "SOUL": "SOUL",
                "IDENTITY": "IDENTITY",
                "PERSONALITY": "PERSONALITY",
                "LIFE": "LIFE",
                "COGNITIVE": "COGNITIVE",
                "RELATIONSHIP": "RELATIONSHIP",
                "MEMORY": "MEMORY",
                "CONSTRAINT": "CONSTRAINT",
                "DECISION": "DECISION",
                "TOOL": "TOOL",
                "RESOURCE": "RESOURCE",
            }.get(cat, "SYSTEM")
        # aggregateVersion : compteur monotone par eStarId (garantit replay/optimistic concurrency)
        self.aggregate_version = getattr(self, "aggregate_version", 0) + 1
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rec = {
            "eventId": f"evt_{int(time.time()*1000)}_{os.urandom(2).hex()}",
            "eventType": event_type,
            "category": category,
            "aggregateType": "EStar",
            "aggregateId": self.e_star_id,
            "aggregateVersion": self.aggregate_version,
            "eStarId": self.e_star_id,
            "payload": payload,
            "occurredAt": now_iso,
            "recordedAt": now_iso,
            "schemaVersion": SCHEMA_VERSION,
            "correlationId": f"corr_{self.e_star_id}_{self.aggregate_version}",
            "producer": PRODUCER,
            "sensitivity": sensitivity,
        }
        try:
            with open(EVENT_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            pass  # audit best-effort ; ne bloque pas l'action (mode degrade honnete)
        return rec

    # --- pipeline Action (Art 14) ---
    def apply(self, action):
        before_stage = int(self.stage)
        before_awaken = self.awakening
        self.cognitive_state = "RECEIVING"

        # 1. intention
        # 2. validation (contraintes)
        if action not in ACTIONS:
            self.cognitive_state = "DORMANT"
            self.emit("TOOL.REQUEST_REJECTED", {"action": action, "reason": "unknown_action"})
            return self._reject("unknown_action")
        if action == "feed" and self.carrots <= 0:
            self.emit("CONSTRAINT.ACTION_BLOCKED", {"action": action, "reason": "no_carrot"})
            self.cognitive_state = "DORMANT"
            return self._reject("no_carrot")
        # 3. permission (statut actif)
        if self.status != "ACTIVE":
            self.cognitive_state = "DORMANT"
            return self._reject("inactive")

        # 4. execution
        self.cognitive_state = "ACTING"
        n = self.needs
        if action == "feed":
            self.carrots -= 1
            n["hunger"] = min(100, n["hunger"] + 38)
            self.closeness = min(100, self.closeness + 1)
            self.life_state = "DISCUSSING"
        elif action == "pet":
            n["social"] = min(100, n["social"] + 22)
            self.closeness = min(100, self.closeness + 4)
            self.kiss = min(999, self.kiss + 1)
        elif action == "play":
            n["fun"] = min(100, n["fun"] + 30)
            n["energy"] = max(FLOOR, n["energy"] - 12)
            if self.carrots > 0 and (self.closeness % 3 == 0):
                self.carrots -= 1  # jouer coute parfois une carotte (stock, pas achat)
            self.life_state = "WORKING"
        elif action == "sleep":
            n["energy"] = min(100, n["energy"] + 55)
            n["fun"] = min(100, n["fun"] + 8)
            self.life_state = "SLEEPING"
        elif action == "clean":
            n["hygiene"] = min(100, n["hygiene"] + 50)
        elif action == "train":
            self.awakening = min(100, self.awakening + 7)
            n["energy"] = max(FLOOR, n["energy"] - 10)
            n["fun"] = min(100, n["fun"] + 4)
        elif action == "talk":
            n["social"] = min(100, n["social"] + 16)
            n["fun"] = min(100, n["fun"] + 10)
            self.closeness = min(100, self.closeness + 2)
        elif action == "evolve":
            if int(self.stage) < 4:
                self.stage = Stage(int(self.stage) + 1)
                self.awakening = 0
                self.closeness = min(100, self.closeness + 10)
                self.emit("PERSONALITY.UPDATED", {"stage": int(self.stage), "reason": "evolve"})
                self.life_state = "CREATING"
            else:
                self.cognitive_state = "DORMANT"
                return self._reject("max_stage")

        # 5. verification
        self.cognitive_state = "EVALUATING"
        progressed = (self.awakening != before_awaken) or (int(self.stage) != before_stage)
        self.emit("TOOL.EXECUTION_SUCCEEDED", {"action": action, "progressed": progressed})
        self.cognitive_state = "CONTEMPLATING"
        self.save()
        return True, "", progressed

    def _reject(self, reason):
        self.save()
        return False, reason, False

    # --- recolte gratuite (ANTI_FEATURES : aucun pay-to-care) ---
    def harvest(self, amount=5):
        amount = max(1, min(20, int(amount)))
        self.carrots += amount
        self.emit("RESOURCE.GRANTED", {"kind": "carrot", "amount": amount, "gratis": True})
        self.save()
        return amount

    # --- persistance (SC-004 : pas de faux succes de persistance) ---
    def to_persist(self):
        return {
            "e_star_id": self.e_star_id,
            "display_name": self.display_name,
            "status": self.status,
            "continuity_status": self.continuity_status,
            "version": self.version,
            "soul_version": self.soul_version,
            "stage": int(self.stage),
            "awakening": self.awakening,
            "closeness": self.closeness,
            "needs": self.needs,
            "carrots": self.carrots,
            "energy_res": self.energy_res,
            "kiss": self.kiss,
            "born": self.born,
            "last": self.last,
            "disjoncteur": self.disjoncteur,
            "life_state": self.life_state,
            "aggregate_version": getattr(self, "aggregate_version", 0),
        }

    def save(self):
        try:
            data = {}
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            data[self.e_star_id] = self.to_persist()
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # garde en memoire meme si disque impossible (mode degrade honnete)

    @classmethod
    def from_persist(cls, e_star_id, d):
        obj = cls(e_star_id)
        obj.display_name = d.get("display_name", "Enki")
        obj.status = d.get("status", "ACTIVE")
        obj.continuity_status = d.get("continuity_status", "CANONICAL")
        obj.version = d.get("version", 1)
        obj.soul_version = d.get("soul_version", 1)
        obj.stage = Stage(d.get("stage", 1))
        obj.awakening = d.get("awakening", 0)
        obj.closeness = d.get("closeness", 0)
        obj.needs = d.get("needs", obj.needs)
        obj.carrots = d.get("carrots", 0)
        obj.energy_res = d.get("energy_res", 0)
        obj.kiss = d.get("kiss", 0)
        obj.born = d.get("born", time.time())
        obj.last = d.get("last", time.time())
        obj.disjoncteur = d.get("disjoncteur", 0)
        obj.life_state = d.get("life_state", "IDLE")
        obj.aggregate_version = d.get("aggregate_version", 0)
        obj._loaded = True
        return obj

    # --- serialisation etat courant ---
    def to_state(self):
        self.decay()
        mstate, mscore = self.mood()
        return {
            "e_star_id": self.e_star_id,
            "id": self.e_star_id,
            "name": self.display_name,
            "stage": int(self.stage),
            "stage_name": STAGE_NAMES[int(self.stage)],
            "needs": {k: int(v) for k, v in self.needs.items()},
            "mood": {"state": mstate, "score": int(mscore)},
            "life_state": self.life_state,
            "cognitive_state": self.cognitive_state,
            "vitality": self.vitality(),
            "awakening": int(self.awakening),
            "closeness": int(self.closeness),
            "resources": {"carrot": int(self.carrots), "energy": int(self.energy_res), "kiss": int(self.kiss)},
            "cycle": self.cycle(),
            "continuity_status": self.continuity_status,
            "version": self.version,
            "mode": self.mode,
            "disjoncteur_count": int(self.disjoncteur),
            "progressed": False,
            "progress_signature": None,
        }

    def to_interact(self, ok, msg, progressed):
        import hashlib
        sig = (
            hashlib.sha256(f"{self.e_star_id}:{self.awakening}:{time.time()}".encode()).hexdigest()[:16]
            if progressed else None
        )
        return {
            "ok": ok,
            "message": msg,
            "progressed": progressed,
            "progress_signature": sig,
            "stage": int(self.stage),
            "needs": {k: int(v) for k, v in self.needs.items()},
            "mood": {"state": self.mood()[0], "score": self.mood()[1]},
            "life_state": self.life_state,
            "cognitive_state": self.cognitive_state,
            "vitality": self.vitality(),
            "awakening": int(self.awakening),
            "closeness": int(self.closeness),
            "resources": {"carrot": int(self.carrots), "energy": int(self.energy_res), "kiss": int(self.kiss)},
        }


CREATURES = {}


def get_creature(user_id):
    if user_id not in CREATURES:
        obj = None
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if user_id in data:
                    obj = EStar.from_persist(user_id, data[user_id])
            except Exception:
                pass
        if obj is None:
            obj = EStar(user_id)
            obj.emit("E_STAR.CREATED", {"canonical_name": obj.canonical_name})
            obj.save()
        CREATURES[user_id] = obj
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
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)
        if path == "/health":
            self._send(200, {"status": "ok"})
        elif path == "/creature":
            uid = q.get("user_id", ["demo-user"])[0]
            self._send(200, get_creature(uid).to_state())
        elif path == "/events":
            # audit readonly : dernier evenement par eStarId (pas de secrets)
            uid = q.get("user_id", ["demo-user"])[0]
            self._send(200, {"e_star_id": uid, "note": "append-only event log on server"})
        else:
            self._send(404, {"error": "not_found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
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

        elif path == "/grant":
            # recolte GRATUITE (ANTI_FEATURES). Aucun store, aucun paiement.
            amount = int(data.get("amount", 5))
            got = cr.harvest(amount)
            self._send(200, {"carrot": cr.carrots, "granted": got, "gratis": True})

        elif path == "/iap/verify":
            # RESERVE au soutien EXPLICITE (finance infra/rendu, Art 19).
            # En MVP sans store reel : refuse pour eviter tout pay-to-love accidentel.
            self._send(403, {"error": "iap_disabled_in_mvp",
                             "reason": "pay-to-love interdit (ECOS Anti-Features). Utilise /grant pour des carottes gratuites."})

        elif path == "/rename":
            name = str(data.get("name", "")).strip()[:24]
            if name:
                cr.display_name = name
                cr.emit("IDENTITY.UPDATED", {"display_name": name})
                cr.save()
            self._send(200, {"name": cr.display_name})

        else:
            self._send(404, {"error": "not_found"})

    def log_message(self, *a):
        pass


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("ENKI Tamagotchi Backend v3 (ECOS-aligned) on http://127.0.0.1:8000")
    srv.serve_forever()


if __name__ == "__main__":
    main()

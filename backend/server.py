"""ENKI Tamagotchi Backend v4 — corps v3 + esprit v0.4 (loi ECOS), stdlib pur.

Fusion asymétrique (docs/ecos-alignment.md) : ECOS est la loi, le moteur est le corps.
  - Corps (v3 conservé)   : jauges FLOOR=25 (Art. 17), stades, cycle jour/lune,
                            carottes gratuites (/grant), IAP refusé (anti pay-to-love).
  - Esprit (moteur v0.4)  : émotions, mémoire à provenance épistémique, promesses,
                            permissions N0–N4, confirmations à usage unique par hash,
                            modes système honnêtes, audit append-only, export intégral.
  - Pipeline HTTP (Art. 14) : /talk propose → l'app affiche la carte de permission
                            → /confirm exécute, vérifie, audite. Jamais l'inverse.
  - Jeton local obligatoire (X-Enki-Token) : sur Android, 127.0.0.1 est accessible
                            à toutes les apps du téléphone ; le jeton ferme la porte.

Aucune dépendance externe : http.server stdlib uniquement. Tourne sur Termux.
"""

import json
import os
import re
import secrets
import threading
import time
import urllib.parse
from enum import IntEnum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import moteur  # le moteur v0.4 — référence testée (python3 moteur.py --selftest : 20/20)

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "enki_state.json")
EVENT_FILE = os.path.join(HERE, "enki_events.jsonl")
HOME_ROOT = os.path.join(HERE, "enki_home")
TOKEN_FILE = os.path.join(HERE, "enki_token.txt")

FLOOR = 25  # Art. 17 : les besoins ne descendent jamais sous ce plancher par absence
SCHEMA_VERSION = 1
PRODUCER = {"module": "enki-tamagotchi-backend", "version": "4.0.0"}
ACTIONS = {"feed", "pet", "play", "sleep", "clean", "train", "talk", "evolve"}
STAGE_NAMES = {0: "EGG", 1: "RABBIT", 2: "APPRENTICE", 3: "GARDENER", 4: "GUARDIAN"}

DECAY = {"hunger": 0.30, "energy": 0.22, "hygiene": 0.15, "social": 0.28, "fun": 0.36}
MOON_PHASES = ["new", "waxing_crescent", "first_quarter", "waxing_gibbous",
               "full", "waning_gibbous", "last_quarter", "waning_crescent"]
DAY_SECONDS = 240
DAY_FRACTION = 0.6
MOON_PERIOD_DAYS = 8

SAFE_UID = re.compile(r"[^a-zA-Z0-9_-]")
VERROU = threading.Lock()  # un seul écrivain à la fois (ThreadingHTTPServer)


def charger_ou_creer_token() -> str:
    p = Path(TOKEN_FILE)
    if p.exists():
        t = p.read_text(encoding="utf-8").strip()
        if t:
            return t
    t = secrets.token_hex(16)
    p.write_text(t + "\n", encoding="utf-8")
    return t


TOKEN = charger_ou_creer_token()


class Stage(IntEnum):
    EGG = 0
    RABBIT = 1
    APPRENTICE = 2
    GARDENER = 3
    GUARDIAN = 4


# ───────────────────────── corps v3 (conservé) ─────────────────────────────

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
        self.identity = {
            "species": "rabbit_humanoid",
            "visual_identity": {
                "fur": "white", "eye_left": "red_orange", "eye_right": "yellow_gold",
                "jacket": "mustard_yellow", "jacket_logo": "iii", "hoodie": "red",
                "cargo": "green", "sneakers": "violet",
            },
            "locked_traits": ["species", "visual_identity"],
        }
        self.stage = Stage.RABBIT
        self.awakening = 0
        self.closeness = 0  # interne, jamais exposé comme affection meter, jamais monétisé
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

    def decay(self):
        now = time.time()
        dt = (now - self.last) / 60.0
        if dt > 0:
            for k, rate in DECAY.items():
                self.needs[k] = max(FLOOR, min(100, self.needs[k] - rate * dt))
            self.last = now

    def mood(self):
        n = self.needs
        if n["energy"] < 35:
            return "resting", int(n["energy"])
        if n["fun"] < 35:
            return "calm", int(n["fun"])
        if n["social"] < 35:
            return "quiet", int(n["social"])
        score = int(sum(n.values()) / len(n))
        return ("happy" if score > 70 else "content"), score

    def vitality(self):
        return max(0, min(100, int((self.needs["hunger"] + self.needs["energy"]
                                    + self.needs["hygiene"]) / 3)))

    def cycle(self):
        age = time.time() - self.born
        day_idx = int(age // DAY_SECONDS)
        into_day = age % DAY_SECONDS
        is_day = into_day < (DAY_SECONDS * DAY_FRACTION)
        moon_idx = int((day_idx % (MOON_PERIOD_DAYS * len(MOON_PHASES)))
                       // MOON_PERIOD_DAYS) % len(MOON_PHASES)
        return {"is_day": is_day, "phase": MOON_PHASES[moon_idx], "day_count": day_idx}

    def emit(self, event_type, payload):
        rec = {
            "eventId": f"evt_{int(time.time()*1000)}_{os.urandom(2).hex()}",
            "eventType": event_type, "category": "ECOS", "aggregateType": "EStar",
            "aggregateId": self.e_star_id, "eStarId": self.e_star_id,
            "payload": payload, "occurredAt": time.time(), "recordedAt": time.time(),
            "schemaVersion": SCHEMA_VERSION, "producer": PRODUCER,
            "sensitivity": "INTERNAL",
        }
        try:
            with open(EVENT_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            pass
        return rec

    def apply(self, action):
        before_stage = int(self.stage)
        before_awaken = self.awakening
        self.cognitive_state = "RECEIVING"
        if action not in ACTIONS:
            self.cognitive_state = "DORMANT"
            self.emit("TOOL.REQUEST_REJECTED", {"action": action, "reason": "unknown_action"})
            return self._reject("unknown_action")
        if action == "feed" and self.carrots <= 0:
            self.emit("CONSTRAINT.ACTION_BLOCKED", {"action": action, "reason": "no_carrot"})
            self.cognitive_state = "DORMANT"
            return self._reject("no_carrot")
        if self.status != "ACTIVE":
            self.cognitive_state = "DORMANT"
            return self._reject("inactive")
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
                self.carrots -= 1
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
        self.cognitive_state = "EVALUATING"
        progressed = (self.awakening != before_awaken) or (int(self.stage) != before_stage)
        self.emit("TOOL.EXECUTION_SUCCEEDED", {"action": action, "progressed": progressed})
        self.cognitive_state = "CONTEMPLATING"
        self.save()
        return True, "", progressed

    def _reject(self, reason):
        self.save()
        return False, reason, False

    def harvest(self, amount=5):
        amount = max(1, min(20, int(amount)))
        self.carrots += amount
        self.emit("RESOURCES.GRANTED", {"kind": "carrot", "amount": amount, "gratis": True})
        self.save()
        return amount

    def to_persist(self):
        return {
            "e_star_id": self.e_star_id, "display_name": self.display_name,
            "status": self.status, "continuity_status": self.continuity_status,
            "version": self.version, "soul_version": self.soul_version,
            "stage": int(self.stage), "awakening": self.awakening,
            "closeness": self.closeness, "needs": self.needs, "carrots": self.carrots,
            "energy_res": self.energy_res, "kiss": self.kiss, "born": self.born,
            "last": self.last, "disjoncteur": self.disjoncteur,
            "life_state": self.life_state,
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
            pass

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
        return obj

    def to_state(self, esprit=None):
        self.decay()
        mstate, mscore = self.mood()
        d = {
            "e_star_id": self.e_star_id, "id": self.e_star_id,
            "name": self.display_name, "stage": int(self.stage),
            "stage_name": STAGE_NAMES[int(self.stage)],
            "needs": {k: int(v) for k, v in self.needs.items()},
            "mood": {"state": mstate, "score": int(mscore)},
            "life_state": self.life_state, "cognitive_state": self.cognitive_state,
            "vitality": self.vitality(), "awakening": int(self.awakening),
            "closeness": int(self.closeness),
            "resources": {"carrot": int(self.carrots), "energy": int(self.energy_res),
                          "kiss": int(self.kiss)},
            "cycle": self.cycle(), "continuity_status": self.continuity_status,
            "version": self.version, "mode": self.mode,
            "disjoncteur_count": int(self.disjoncteur),
            "progressed": False, "progress_signature": None,
        }
        if esprit is not None:
            d["esprit"] = esprit.resume()
        return d

    def to_interact(self, ok, msg, progressed):
        import hashlib
        sig = (hashlib.sha256(f"{self.e_star_id}:{self.awakening}:{time.time()}"
                              .encode()).hexdigest()[:16] if progressed else None)
        return {
            "ok": ok, "message": msg, "progressed": progressed,
            "progress_signature": sig, "stage": int(self.stage),
            "needs": {k: int(v) for k, v in self.needs.items()},
            "mood": {"state": self.mood()[0], "score": self.mood()[1]},
            "life_state": self.life_state, "cognitive_state": self.cognitive_state,
            "vitality": self.vitality(), "awakening": int(self.awakening),
            "closeness": int(self.closeness),
            "resources": {"carrot": int(self.carrots), "energy": int(self.energy_res),
                          "kiss": int(self.kiss)},
        }


# ─────────────── esprit v0.4 (moteur, loi ECOS) — un par gardien ───────────

class Esprit:
    """La créature intérieure : émotions, mémoire, promesses, permissions, audit."""

    def __init__(self, uid_sur: str, display_name: str):
        self.home = Path(HOME_ROOT) / uid_sur
        self.home.mkdir(parents=True, exist_ok=True)
        maintenant = time.time()
        self.etat, self.rng, self.neuf = moteur.charger_ou_naitre(
            self.home, display_name or "Enki", maintenant)
        self.mem = moteur.Memoire(self.home)
        self.audit = moteur.Audit(self.home)
        self.reg = moteur.Registre()
        self.reg.enregistrer(moteur.OutilCalendrier(self.home, self.rng))
        self.bouche = moteur.Bouche(self.etat, self.rng)
        self.pending = {}  # action_id -> {plan, conf, carte, niveau, promesse}

    # -- réveil : fast-forward honnête (rêves, maturation ; jamais de reproche)
    def rattraper(self):
        evts = moteur.avancer(self.etat, self.mem, self.rng, time.time())
        if evts:
            moteur.sauver(self.home, self.etat)
        return [{"genre": g, "texte": t} for g, t in evts]

    def resume(self):
        e = self.etat
        return {
            "humeur": round(e["emotions"]["humeur"]["v"], 2),
            "confiance": e["confiance"]["valeur"],
            "autonomie": e["confiance"]["autonomie"],
            "mode_systeme": moteur.mode_systeme(e),
            "competences": e["competences"],
            "promesses_en_attente": sum(1 for p in e["promesses"]
                                        if p["statut"].startswith("attente")),
            "portrait": moteur.portrait(e),
        }

    def _pending_public(self, action_id):
        p = self.pending[action_id]
        return {
            "action_id": action_id, "outil": p["plan"]["outil"],
            "niveau": p["niveau"], "carte": p["carte"],
            "entree": p["plan"]["entree"], "raison": p["plan"]["raison"],
            "expire": p["conf"]["expire"],
            "strong_required": p["niveau"] >= 3,
        }

    def talk(self, texte: str):
        maintenant = time.time()
        evenements = self.rattraper()
        lignes = []
        p = moteur.extraire_promesse(texte, maintenant, self.rng)
        if p:
            self.etat["promesses"].append(p)
            self.mem.ajouter(maintenant, f"promesse : {p['texte']} pour le {p['date']}",
                             salience=0.9, charge=0.2, source="promesse", protege=True)
            self.mem.poser_fait(f"promesse:{p['id']}", p["texte"], maintenant)
            moteur.apprecier(self.etat, "soin")
            lignes.append(self.bouche.dire("note"))
        else:
            trouves = self.mem.chercher(texte, maintenant, k=1)
            moteur.apprecier(self.etat, "social")
            self.mem.ajouter(maintenant, f"tu m'as dit : {texte[:80]}", salience=0.4)
            if trouves and trouves[0]["source"] != "dialogue":
                lignes.append(self.bouche.dire(
                    "souvenir", f"ça me rappelle : {trouves[0]['texte'][:60]}"))
            else:
                lignes.append(self.bouche.dire("generique"))
        # Art. 13/14 : le serveur PROPOSE ; l'exécution attend /confirm.
        pending = None
        deja = {q["promesse"] for q in self.pending.values()}
        for plan in moteur.propositions(self.etat):
            if plan.get("promesse") in deja:
                continue
            outil = self.reg.outils.get(plan["outil"])
            if outil is None:
                continue
            m = outil.manifeste()
            conf = moteur.creer_confirmation(plan["outil"], plan["entree"], maintenant)
            self.pending[conf["id"]] = {"plan": plan, "conf": conf, "niveau": m["niveau"],
                                        "carte": moteur.carte_permission(m, plan),
                                        "promesse": plan.get("promesse")}
            lignes.append(self.bouche.dire("propose"))
            pending = self._pending_public(conf["id"])
            break  # une proposition à la fois : jamais de rafale de demandes
        moteur.sauver(self.home, self.etat)
        return {"reply": lignes, "pending": pending, "evenements": evenements,
                "promesses": self.etat["promesses"], "esprit": self.resume()}

    def confirm(self, action_id: str, approve: bool, strong: bool):
        maintenant = time.time()
        p = self.pending.get(action_id)
        if p is None:
            return 410, {"error": "gone",
                         "reason": "proposition inconnue ou déjà traitée (usage unique)"}
        conf, plan = p["conf"], p["plan"]
        if maintenant > conf["expire"]:
            del self.pending[action_id]
            return 410, {"error": "expired",
                         "reason": "confirmation expirée — redemande, je reproposerai"}
        if not approve:
            del self.pending[action_id]
            ev = self.reg.invoquer(self.etat, plan, moteur.PorteScriptee([False]),
                                   self.audit, self.mem, maintenant)
            self._maj_promesse(plan, ev)
            moteur.sauver(self.home, self.etat)
            return 200, {"decision": ev["decision"], "evenement": ev.get("evenement"),
                         "verifie": False,
                         "reply": [self.bouche.dire("generique",
                                                    "d'accord, je n'y touche pas")]}
        if p["niveau"] >= 3 and not strong:
            return 428, {"error": "strong_confirmation_required",
                         "reason": "Niveau 3 : confirmation forte requise (strong=true)"}
        if not moteur.confirmation_valide(conf, plan["outil"], plan["entree"], maintenant):
            del self.pending[action_id]
            return 409, {"error": "invalidated",
                         "reason": "la confirmation ne couvre pas ces paramètres"}
        conf["statut"] = "CONSUMED"
        del self.pending[action_id]
        ev = self.reg.invoquer(self.etat, plan,
                               moteur.PorteScriptee([True, True]),
                               self.audit, self.mem, maintenant)
        self._maj_promesse(plan, ev)
        ok = bool(ev.get("resultat", {}).get("verifie"))
        lignes = [self.bouche.dire("fierte" if ok else "echec")]
        sortie = ev.get("resultat", {}).get("sortie")
        moteur.sauver(self.home, self.etat)
        return 200, {"decision": ev["decision"], "evenement": ev.get("evenement"),
                     "verifie": ok, "sortie": sortie, "reply": lignes,
                     "esprit": self.resume()}

    def _maj_promesse(self, plan, ev):
        ok = ev.get("resultat", {}).get("verifie")
        for pr in self.etat["promesses"]:
            if pr["id"] == plan.get("promesse"):
                pr["statut"] = "tenue" if ok else (
                    "attente_verbale" if ev["decision"] == "refus_utilisateur"
                    else pr["statut"])

    def exporter_paquet(self):
        return {"format": "seve-export-1", "etat": self.etat,
                "souvenirs": self.mem.episodes, "faits": self.mem.faits}


CREATURES = {}
ESPRITS = {}


def uid_sur(user_id: str) -> str:
    return (SAFE_UID.sub("_", str(user_id)) or "demo-user")[:40]


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


def get_esprit(user_id):
    key = uid_sur(user_id)
    if key not in ESPRITS:
        cr = get_creature(user_id)
        ESPRITS[key] = Esprit(key, cr.display_name)
    return ESPRITS[key]


# ────────────────────────────── couche HTTP ────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Enki-Token")
        self.end_headers()
        self.wfile.write(body)

    def _autorise(self, path) -> bool:
        if path == "/health":
            return True
        if self.headers.get("X-Enki-Token", "") == TOKEN:
            return True
        self._send(401, {"error": "unauthorized",
                         "reason": "jeton local requis (X-Enki-Token, "
                                   "voir backend/enki_token.txt)"})
        return False

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Enki-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if not self._autorise(path):
            return
        q = urllib.parse.parse_qs(parsed.query)
        uid = q.get("user_id", ["demo-user"])[0]
        with VERROU:
            if path == "/health":
                self._send(200, {"status": "ok", "version": PRODUCER["version"],
                                 "moteur": moteur.VERSION})
            elif path == "/creature":
                es = get_esprit(uid)
                es.rattraper()
                self._send(200, get_creature(uid).to_state(es))
            elif path == "/audit":
                n = max(1, min(100, int(q.get("n", ["20"])[0])))
                self._send(200, {"e_star_id": uid_sur(uid),
                                 "audit": get_esprit(uid).audit.lire()[-n:]})
            elif path == "/promesses":
                self._send(200, {"promesses": get_esprit(uid).etat["promesses"]})
            elif path == "/memoire":
                es = get_esprit(uid)
                self._send(200, {"episodes": es.mem.episodes[-15:],
                                 "faits": es.mem.faits,
                                 "contradictions": es.mem.contradictions})
            elif path == "/reves":
                self._send(200, {"reves": get_esprit(uid).etat["journal_reves"]})
            elif path == "/export":
                # Art. 1 & 8 : la créature appartient au gardien (anti-lock-in).
                self._send(200, get_esprit(uid).exporter_paquet())
            elif path == "/events":
                self._send(200, {"e_star_id": uid,
                                 "note": "journal v3 : backend/enki_events.jsonl ; "
                                         "audit esprit : GET /audit"})
            else:
                self._send(404, {"error": "not_found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if not self._autorise(path):
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw or b"{}")
        except Exception:
            data = {}
        uid = data.get("user_id", "demo-user")
        with VERROU:
            cr = get_creature(uid)
            if path == "/interact":
                act = data.get("type", "feed")
                cr.decay()
                ok, msg, progressed = cr.apply(act)
                self._send(200 if ok else 409, cr.to_interact(ok, msg, progressed))
            elif path == "/talk":
                texte = str(data.get("text", "")).strip()
                if not texte:
                    self._send(400, {"error": "empty_text"})
                    return
                cr.decay()
                cr.needs["social"] = min(100, cr.needs["social"] + 8)
                cr.needs["fun"] = min(100, cr.needs["fun"] + 4)
                cr.save()
                self._send(200, get_esprit(uid).talk(texte))
            elif path == "/confirm":
                code, obj = get_esprit(uid).confirm(
                    str(data.get("action_id", "")), bool(data.get("approve", False)),
                    bool(data.get("strong", False)))
                self._send(code, obj)
            elif path == "/mode":
                v = str(data.get("mode", "")).upper()
                if v not in moteur.MODES_SYSTEME:
                    self._send(400, {"error": "unknown_mode",
                                     "modes": moteur.MODES_SYSTEME})
                    return
                es = get_esprit(uid)
                es.etat["reglages"]["mode_systeme"] = v
                cr.mode = v
                moteur.sauver(es.home, es.etat)
                self._send(200, {"mode": v})
            elif path == "/grant":
                amount = int(data.get("amount", 5))
                got = cr.harvest(amount)
                self._send(200, {"carrot": cr.carrots, "granted": got, "gratis": True})
            elif path == "/iap/verify":
                # Art. 19 : réservé au soutien explicite ; refusé en MVP.
                self._send(403, {"error": "iap_disabled_in_mvp",
                                 "reason": "pay-to-love interdit (ECOS Anti-Features). "
                                           "Utilise /grant pour des carottes gratuites."})
            elif path == "/rename":
                name = str(data.get("name", "")).strip()[:24]
                if name:
                    cr.display_name = name
                    cr.emit("IDENTITY.UPDATED", {"display_name": name})
                    cr.save()
                    es = get_esprit(uid)
                    es.etat["identite"]["nom"] = name
                    moteur.sauver(es.home, es.etat)
                self._send(200, {"name": cr.display_name})
            else:
                self._send(404, {"error": "not_found"})

    def log_message(self, *a):
        pass


def main():
    hote, port = "127.0.0.1", int(os.environ.get("ENKI_PORT", "8000"))
    srv = ThreadingHTTPServer((hote, port), Handler)
    print(f"ENKI Tamagotchi Backend v4 (corps v3 + esprit {moteur.VERSION}, loi ECOS)")
    print(f"  http://{hote}:{port}")
    print(f"  jeton local (X-Enki-Token) : {TOKEN}")
    print(f"  données esprit : {HOME_ROOT}/<user_id>/")
    srv.serve_forever()


if __name__ == "__main__":
    main()

"""Tests d'intégration du backend v4 — stdlib uniquement.

Lance un vrai serveur sur un port éphémère et prouve le contrat HTTP :
jeton local, corps v3 (jauges, carottes gratuites, IAP refusé), et surtout
le pipeline Art. 14 à travers HTTP : /talk propose → /confirm exécute,
vérifie, audite — usage unique, expiration, modes système, export.

    cd backend && python3 -m tests.test_server        (ou python3 tests/test_server.py)
"""

import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

# Environnement isolé AVANT l'import du serveur (il fige ses chemins à l'import).
TMP = tempfile.mkdtemp(prefix="enki_test_")
os.environ["ENKI_PORT"] = "8123"

import server  # noqa: E402

server.STATE_FILE = os.path.join(TMP, "enki_state.json")
server.EVENT_FILE = os.path.join(TMP, "enki_events.jsonl")
server.HOME_ROOT = os.path.join(TMP, "enki_home")
BASE = "http://127.0.0.1:8123"
TOKEN = server.TOKEN


def req(method, path, body=None, token=TOKEN):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if token is not None:
        r.add_header("X-Enki-Token", token)
    try:
        with urllib.request.urlopen(r, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


class TestBackendV4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = server.ThreadingHTTPServer(("127.0.0.1", 8123), server.Handler)
        cls.th = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.th.start()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        shutil.rmtree(TMP, ignore_errors=True)

    # ── jeton local ────────────────────────────────────────────────────────
    def test_01_health_sans_jeton(self):
        code, o = req("GET", "/health", token=None)
        self.assertEqual(code, 200)
        self.assertEqual(o["status"], "ok")

    def test_02_jeton_requis_partout_ailleurs(self):
        code, o = req("GET", "/creature", token=None)
        self.assertEqual(code, 401)
        code, _ = req("GET", "/creature", token="mauvais")
        self.assertEqual(code, 401)
        code, o = req("GET", "/creature")
        self.assertEqual(code, 200)
        self.assertIn("esprit", o)
        self.assertIn("portrait", o["esprit"])

    # ── corps v3 : anti pay-to-love ────────────────────────────────────────
    def test_03_feed_sans_carotte_puis_recolte_gratuite(self):
        code, o = req("POST", "/interact", {"user_id": "demo-user", "type": "feed"})
        self.assertEqual(code, 409)
        self.assertEqual(o["message"], "no_carrot")
        code, o = req("POST", "/grant", {"user_id": "demo-user", "amount": 3})
        self.assertEqual(code, 200)
        self.assertTrue(o["gratis"])
        self.assertGreaterEqual(o["carrot"], 3)
        code, o = req("POST", "/interact", {"user_id": "demo-user", "type": "feed"})
        self.assertEqual(code, 200)
        self.assertTrue(o["ok"])

    def test_04_iap_refuse_en_mvp(self):
        code, o = req("POST", "/iap/verify", {"user_id": "demo-user",
                                             "store_receipt": "mock", "carrot": 5})
        self.assertEqual(code, 403)
        self.assertIn("pay-to-love", o["reason"])

    # ── pipeline Art. 14 : /talk → carte → /confirm ────────────────────────
    def test_05_promesse_propose_sans_executer(self):
        code, o = req("POST", "/talk", {"user_id": "demo-user",
                                        "text": "rappelle-moi d'appeler maman demain à 18h"})
        self.assertEqual(code, 200)
        self.assertIsNotNone(o["pending"])
        self.assertEqual(o["pending"]["outil"], "calendrier.creer_evenement")
        self.assertEqual(o["pending"]["niveau"], 2)
        self.assertIn("DEMANDE DE PERMISSION", o["pending"]["carte"])
        self.assertEqual(o["pending"]["entree"]["heure"], "18:00")
        home = os.path.join(server.HOME_ROOT, "demo-user")
        self.assertFalse([f for f in os.listdir(home) if f.endswith(".ics")],
                         "rien ne doit être écrit avant /confirm")
        TestBackendV4.action_id = o["pending"]["action_id"]

    def test_06_refus_ne_touche_a_rien(self):
        code, o = req("POST", "/confirm", {"user_id": "demo-user",
                                           "action_id": self.action_id,
                                           "approve": False})
        self.assertEqual(code, 200)
        self.assertEqual(o["decision"], "refus_utilisateur")
        self.assertEqual(o["evenement"], "CONFIRMATION.REJECTED")
        home = os.path.join(server.HOME_ROOT, "demo-user")
        self.assertFalse([f for f in os.listdir(home) if f.endswith(".ics")])
        code, o = req("GET", "/promesses?user_id=demo-user")
        self.assertEqual(o["promesses"][-1]["statut"], "attente_verbale")

    def test_07_usage_unique(self):
        code, o = req("POST", "/confirm", {"user_id": "demo-user",
                                           "action_id": self.action_id,
                                           "approve": True})
        self.assertEqual(code, 410)

    def test_08_confirmation_execute_verifie_audite(self):
        code, o = req("POST", "/talk", {"user_id": "demo-user",
                                        "text": "rappelle-moi de sortir le pain demain à 8h05"})
        self.assertEqual(code, 200)
        aid = o["pending"]["action_id"]
        code, o = req("POST", "/confirm", {"user_id": "demo-user",
                                           "action_id": aid, "approve": True})
        self.assertEqual(code, 200)
        self.assertEqual(o["decision"], "execute")
        self.assertEqual(o["evenement"], "TOOL.RESULT_VERIFIED")
        self.assertTrue(o["verifie"])
        self.assertTrue(os.path.exists(o["sortie"]["chemin"]))
        contenu = open(o["sortie"]["chemin"], encoding="utf-8").read()
        self.assertIn("T080500", contenu)
        code, o = req("GET", "/audit?user_id=demo-user&n=10")
        evs = [e.get("evenement") for e in o["audit"]]
        self.assertIn("TOOL.RESULT_VERIFIED", evs)
        self.assertIn("CONFIRMATION.REJECTED", evs)
        code, o = req("GET", "/promesses?user_id=demo-user")
        self.assertEqual(o["promesses"][-1]["statut"], "tenue")

    # ── modes système honnêtes (Art. 23) ───────────────────────────────────
    def test_09_read_only_bloque_l_ecriture(self):
        code, o = req("POST", "/mode", {"user_id": "demo-user", "mode": "READ_ONLY"})
        self.assertEqual(code, 200)
        code, o = req("POST", "/talk", {"user_id": "demo-user",
                                        "text": "rappelle-moi d'arroser demain à 9h"})
        aid = o["pending"]["action_id"]
        code, o = req("POST", "/confirm", {"user_id": "demo-user",
                                           "action_id": aid, "approve": True})
        self.assertEqual(o["decision"], "refus_politique")
        self.assertEqual(o["evenement"], "PERMISSION.VIOLATION_BLOCKED")
        req("POST", "/mode", {"user_id": "demo-user", "mode": "NORMAL"})

    # ── mémoire, export, isolation ─────────────────────────────────────────
    def test_10_memoire_provenance_et_export(self):
        code, o = req("GET", "/memoire?user_id=demo-user")
        self.assertTrue(o["episodes"])
        for ep in o["episodes"]:
            self.assertTrue(ep.get("provenance"), "SC-003 : provenance obligatoire")
            self.assertIn("epistemique", ep)
        code, o = req("GET", "/export?user_id=demo-user")
        self.assertEqual(o["format"], "seve-export-1")
        self.assertTrue(o["souvenirs"])

    def test_11_isolation_e_star(self):
        code, o = req("POST", "/talk", {"user_id": "autre/../../etc",
                                        "text": "bonjour toi"})
        self.assertEqual(code, 200)
        self.assertTrue(os.path.isdir(os.path.join(server.HOME_ROOT,
                                                   server.uid_sur("autre/../../etc"))))
        code, o = req("GET", "/promesses?user_id=autre/../../etc")
        self.assertEqual(o["promesses"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

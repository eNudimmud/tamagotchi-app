#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SÈVE — tranche verticale de référence (stdlib uniquement, exécutable partout).

Cette implémentation fait foi du COMPORTEMENT de la boucle des 10 étapes :
  but détecté → proposition → carte de permission → approbation → exécution
  sandboxée → vérification → audit → XP → souvenir → évolution visible.

Le workspace Rust (crates/) est le portage production de ce fichier.
v0.4 : mise en conformité avec la loi ECOS (docs/foundation/) — statuts
épistémiques, provenance mémoire, confirmations à usage unique par hash,
modes système dégradés honnêtes, absence jamais punie (Article 17),
nomenclature d'événements, invariants constitutionnels dans le selftest.
Lancer :            python3 slice.py
Tests :             python3 slice.py --selftest
Démo scriptée :     python3 slice.py --demo
Données :           $SEVE_HOME (défaut ./seve_data)
"""
from __future__ import annotations
import hashlib, json, math, os, re, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

VERSION = "0.4.0-ref"
MASK = (1 << 64) - 1

# ─────────────────────────── noyau déterministe ───────────────────────────

def fnv1a(s: str) -> int:
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 0x100000001B3) & MASK
    return h

class Rng:
    """SplitMix64 — la même graine produit la même vie. Indispensable au fast-forward."""
    def __init__(self, graine: int): self.s = graine & MASK
    def u64(self) -> int:
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return (z ^ (z >> 31)) & MASK
    def f(self) -> float: return (self.u64() >> 40) / float(1 << 24)
    def entre(self, a: float, b: float) -> float: return a + (b - a) * self.f()
    def choix(self, xs): return xs[self.u64() % len(xs)]

def uid(rng: Rng) -> str: return f"{rng.u64():016x}"

def clamp(x, a, b): return max(a, min(b, x))

# ────────────── loi ECOS : épistémique, provenance, confirmations ─────────
# Réf. : docs/foundation/ECOS_CONSTITUTION.md (Art. 5, 6, 7, 14, 23)
#        docs/foundation/SYSTEM_CONSTRAINTS.md (SC-003, SC-004, SC-006, SC-007)

EPISTEMIQUES = {"observe", "rapporte_gardien", "rapporte_tiers", "infere",
                "interprete", "imagine", "reve", "incertain", "conteste", "corrige"}
SOURCE_TYPES = {"dialogue": "GUARDIAN_MESSAGE", "promesse": "GUARDIAN_MESSAGE",
                "action": "TOOL_RESULT", "consolidation": "REFLECTION",
                "systeme": "SYSTEM_EVENT", "reve": "DREAM"}
MODES_SYSTEME = ["NORMAL", "NO_LLM", "READ_ONLY", "NO_EXTERNAL_TOOLS",
                 "MEMORY_LIMITED", "WORLD_PAUSED", "SAFE_IDLE"]
CLES_SENSIBLES = re.compile(r"(secret|token|password|api_?key|mot_?de_?passe)", re.I)

def provenance_defaut(source: str) -> list[dict]:
    """SC-003 : aucune mémoire active sans provenance."""
    return [{"source_type": SOURCE_TYPES.get(source, "SYSTEM_EVENT"),
             "module": source, "version": VERSION}]

def hash_params(nom: str, entree: dict) -> str:
    brut = json.dumps({"outil": nom, "entree": entree}, sort_keys=True,
                      ensure_ascii=False)
    return hashlib.sha256(brut.encode("utf-8")).hexdigest()[:16]

def creer_confirmation(nom: str, entree: dict, maintenant: float,
                       rng: Rng | None = None, ttl: int = 600) -> dict:
    """Autorisation ponctuelle liée au hash exact des paramètres (Art. 7 & 14)."""
    h = hash_params(nom, entree)
    ident = uid(rng) if rng else f"c{h[:8]}{int(maintenant) & 0xFFFF:04x}"
    return {"id": ident, "outil": nom, "hash": h,
            "statut": "CONFIRMED", "t": int(maintenant),
            "expire": int(maintenant) + ttl}

def confirmation_valide(conf: dict, nom: str, entree: dict, maintenant: float) -> bool:
    return (conf["statut"] == "CONFIRMED" and conf["outil"] == nom
            and conf["hash"] == hash_params(nom, entree)
            and maintenant <= conf["expire"])

def mode_systeme(etat: dict) -> str:
    return etat["reglages"].get("mode_systeme", "NORMAL")

# ─────────────────────────────── genèse ───────────────────────────────────

SYLLABES = ["bli", "pou", "ra", "mi", "cho", "ka", "fu", "né", "ti", "lo", "zou", "pi"]
TICS = [["tu vois", "voilà"], ["hmm", "oh !"], ["hé", "dis"], ["bon", "alors"]]
BESOINS_DEF = [  # (nom, valeur initiale, consigne, dérive/minute)
    ("énergie", 0.8, 0.8, 0.00035), ("stimulation", 0.7, 0.8, 0.00040),
    ("lien", 0.6, 0.8, 0.00030), ("sommeil", 0.8, 0.8, 0.00025),
    ("exploration", 0.6, 0.7, 0.00030), ("apprentissage", 0.6, 0.7, 0.00025),
    ("créativité", 0.6, 0.7, 0.00025), ("sécurité", 0.8, 0.8, 0.00010),
    ("sens", 0.6, 0.7, 0.00015),
]

def genese(nom: str, maintenant: float) -> dict:
    graine = fnv1a(f"{nom}|{int(maintenant * 1000)}")
    rng = Rng(graine)
    return {
        "version": VERSION,
        "identite": {"nom": nom, "graine": f"{graine:016x}", "nee_le": int(maintenant)},
        "personnalite": {
            "ocean": [round(rng.entre(0.2, 0.8), 3) for _ in range(5)],  # O C E A N
            "tics": rng.choix(TICS),
            "voix": [rng.choix(SYLLABES) for _ in range(4)],
        },
        "genome": [round(rng.f(), 3) for _ in range(12)],
        "emotions": {
            "affect": {"v": 0.15, "a": 0.10, "d": 0.0},
            "base":   {"v": 0.10, "a": 0.00, "d": 0.0},
            "humeur": {"v": 0.10, "a": 0.00, "d": 0.0},
            "socio": {"attachement": 0.05, "confiance_toi": 0.2, "solitude": 0.3,
                      "stress": 0.1, "curiosité": 0.6, "fierté": 0.1, "fatigue": 0.2},
        },
        "besoins": [{"nom": n, "valeur": v, "consigne": c, "derive": d}
                    for (n, v, c, d) in BESOINS_DEF],
        "competences": {"organisation": {"niveau": 0, "xp": 0}},
        "confiance": {"valeur": 0.2, "autonomie": 1, "echecs": 0},
        "evolution": {"curiosité": 0.0, "bravoure": 0.0, "social": 0.0,
                      "création": 0.0, "calme": 0.0, "organisation": 0.0},
        "promesses": [],
        "missions": [{"id": "m1", "titre": "Explorer la clairière", "type": "virtuelle",
                      "progres": 0.0}],
        "journal_reves": [],
        "notes_securite": [],
        "reglages": {"mode_sur": False, "plafond_niveau": 3, "accords": {},
                     "plafond_depense_cents": 0, "mode_systeme": "NORMAL"},
        "sim": {"dernier": int(maintenant), "decalage": 0, "derniere_nuit": ""},
    }

# ─────────────────────────────── mémoire ──────────────────────────────────

def _tokens(texte: str):
    return set(re.findall(r"\w+", texte.lower()))

class Memoire:
    """Épisodique (jsonl) + sémantique (faits) avec détection de contradictions."""
    def __init__(self, dossier: Path):
        self.dossier = dossier
        self.chemin = dossier / "souvenirs.jsonl"
        self.chemin_faits = dossier / "faits.json"
        self.episodes: list[dict] = []
        self.faits: dict = {}
        self.contradictions: list[str] = []
        if self.chemin.exists():
            for ligne in self.chemin.read_text(encoding="utf-8").splitlines():
                if ligne.strip():
                    ep = json.loads(ligne)                # migration douce v0.3 → v0.4
                    ep.setdefault("epistemique", "incertain")
                    ep.setdefault("provenance",
                                  provenance_defaut(ep.get("source", "dialogue")))
                    self.episodes.append(ep)
        if self.chemin_faits.exists():
            d = json.loads(self.chemin_faits.read_text(encoding="utf-8"))
            self.faits = d.get("faits", {})
            self.contradictions = d.get("contradictions", [])

    def ajouter(self, t: float, texte: str, salience=0.5, charge=0.0,
                source="dialogue", protege=False, rng: Rng | None = None,
                epistemique: str = "rapporte_gardien",
                provenance: list[dict] | None = None) -> dict:
        if epistemique not in EPISTEMIQUES:                       # Art. 5 : statut valide
            epistemique = "incertain"
        ep = {"id": uid(rng) if rng else f"{int(t*1000):x}", "t": int(t), "texte": texte,
              "salience": round(salience, 3), "charge": round(charge, 3),
              "source": source, "protege": protege, "prive": "normal", "expire": None,
              "epistemique": epistemique,
              "provenance": provenance or provenance_defaut(source)}
        self.episodes.append(ep)
        with self.chemin.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ep, ensure_ascii=False) + "\n")
        return ep

    def chercher(self, requete: str, maintenant: float, k=3) -> list[dict]:
        q = _tokens(requete)
        if not q: return []
        notes = []
        for ep in self.episodes:
            e = _tokens(ep["texte"])
            jac = len(q & e) / len(q | e) if e else 0.0
            rec = math.exp(-max(0.0, maintenant - ep["t"]) / (3 * 86400))
            notes.append((0.5 * jac + 0.3 * rec + 0.2 * ep["salience"], ep))
        notes.sort(key=lambda x: -x[0])
        return [ep for score, ep in notes[:k] if score > 0.15]

    def _archiver(self, ancien: dict | None, statut: str) -> list[dict]:
        """SC-006 : l'historique n'est jamais réécrit silencieusement."""
        if not ancien: return []
        archive = {k: v for k, v in ancien.items() if k != "historique"}
        archive["epistemique"] = statut
        return ancien.get("historique", []) + [archive]

    def poser_fait(self, cle: str, valeur: str, t: float, source="dialogue",
                   epistemique: str = "rapporte_gardien"):
        ancien = self.faits.get(cle)
        if ancien and ancien["valeur"] != valeur:
            self.contradictions.append(
                f"« {cle} » : « {ancien['valeur']} » puis « {valeur} » — à clarifier")
        self.faits[cle] = {"valeur": valeur, "t": int(t), "source": source,
                           "confiance": 0.9, "epistemique": epistemique,
                           "historique": self._archiver(ancien, "conteste")}
        self._ecrire_faits()

    def corriger(self, cle: str, valeur: str, t: float):
        """Correction utilisateur : prime sur tout ; l'original reste traçable (Art. 6)."""
        ancien = self.faits.get(cle)
        self.faits[cle] = {"valeur": valeur, "t": int(t),
                           "source": "correction_utilisateur", "confiance": 1.0,
                           "epistemique": "rapporte_gardien",
                           "historique": self._archiver(ancien, "corrige")}
        self._ecrire_faits()

    def consolider(self, t: float, rng: Rng) -> str | None:
        """Nocturne : fusion des quasi-doublons, oubli doux, génération d'un rêve."""
        garde, vus = [], []
        for ep in self.episodes:
            tok = _tokens(ep["texte"])
            doublon = None
            for g, gtok in vus:
                u = tok | gtok
                if u and len(tok & gtok) / len(u) > 0.85 and not ep["protege"]:
                    doublon = g; break
            if doublon:
                doublon["salience"] = round(min(1.0, doublon["salience"] + ep["salience"] * 0.5), 3)
            else:
                garde.append(ep); vus.append((ep, tok))
        for ep in garde:
            if not ep["protege"]:
                ep["salience"] = round(ep["salience"] * 0.98, 3)
        self.episodes = [e for e in garde if e["protege"] or e["salience"] >= 0.05]
        self._reecrire()
        if len(self.episodes) >= 2:
            a = rng.choix(self.episodes)
            autres = [e for e in self.episodes if e["id"] != a["id"]] or self.episodes
            b = rng.choix(autres)
            return (f"j'ai rêvé que « {a['texte'][:38]} » se mélangeait "
                    f"avec « {b['texte'][:38]} »…")
        return None

    def _reecrire(self):
        with self.chemin.open("w", encoding="utf-8") as f:
            for ep in self.episodes:
                f.write(json.dumps(ep, ensure_ascii=False) + "\n")

    def _ecrire_faits(self):
        self.chemin_faits.write_text(json.dumps(
            {"faits": self.faits, "contradictions": self.contradictions},
            ensure_ascii=False, indent=1), encoding="utf-8")

# ──────────────────────────────── outils ──────────────────────────────────

class Outil:
    def manifeste(self) -> dict: raise NotImplementedError
    def executer(self, entree: dict): raise NotImplementedError          # -> (ok, sortie|erreur)
    def verifier(self, entree: dict, sortie: dict) -> bool: return True  # relecture du résultat

class OutilCalendrier(Outil):
    """Écrit de vrais fichiers .ics importables dans n'importe quel agenda.
    Côté mobile, la même interface sera implémentée sur EventKit/CalendarContract."""
    def __init__(self, dossier: Path, rng: Rng):
        self.dossier = dossier.resolve(); self.dossier.mkdir(parents=True, exist_ok=True)
        self.rng = rng

    def manifeste(self) -> dict:
        return {"nom": "calendrier.creer_evenement",
                "description": "Crée un rappel dans le calendrier local (fichier .ics).",
                "niveau": 2, "risque": "faible", "categorie": "organisation",
                "requis": ["titre", "date"], "reversible": True,
                "reversion": "supprimer le fichier .ics créé (chemin dans l'audit)",
                "cout_cents": 0, "timeout_ms": 2000}

    def executer(self, entree: dict):
        titre, date = str(entree["titre"]), str(entree["date"])
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            return False, "date invalide (attendu AAAA-MM-JJ)"
        heure = entree.get("heure")
        if heure is not None and not re.fullmatch(r"\d{2}:\d{2}", str(heure)):
            return False, "heure invalide (attendu HH:MM)"
        evt_uid = uid(self.rng)
        chemin = (self.dossier / f"seve-{evt_uid}.ics").resolve()
        if self.dossier not in chemin.parents:                     # bac à sable chemin
            return False, "chemin hors du bac à sable"
        j = date.replace("-", "")
        dtstart = (f"DTSTART:{j}T{heure.replace(':', '')}00" if heure
                   else f"DTSTART;VALUE=DATE:{j}")
        ics = "\r\n".join([
            "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//SEVE//ref//FR",
            "BEGIN:VEVENT", f"UID:{evt_uid}@seve",
            f"DTSTAMP:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            dtstart, f"SUMMARY:{titre}", "DESCRIPTION:Créé par SÈVE avec ton accord.",
            "END:VEVENT", "END:VCALENDAR", ""])
        chemin.write_text(ics, encoding="utf-8")
        return True, {"chemin": str(chemin), "uid": evt_uid}

    def verifier(self, entree, sortie) -> bool:
        try:
            contenu = Path(sortie["chemin"]).read_text(encoding="utf-8")
            return sortie["uid"] in contenu and f"SUMMARY:{entree['titre']}" in contenu
        except Exception:
            return False

    def supprimer(self, sortie: dict) -> bool:
        try: Path(sortie["chemin"]).unlink(); return True
        except Exception: return False

class OutilInterdit(Outil):
    """Existe uniquement pour prouver que le registre refuse le Niveau 4."""
    def manifeste(self):
        return {"nom": "shell.executer", "description": "commandes brutes", "niveau": 4,
                "risque": "interdit", "categorie": "système", "requis": ["cmd"],
                "reversible": False, "reversion": "aucune", "cout_cents": 0, "timeout_ms": 0}
    def executer(self, entree): return False, "jamais"

class OutilEchec(Outil):
    """Pour les tests du disjoncteur et de la reprise après échec."""
    def manifeste(self):
        return {"nom": "test.echec", "description": "échoue toujours", "niveau": 2,
                "risque": "faible", "categorie": "organisation", "requis": [],
                "reversible": True, "reversion": "rien à annuler", "cout_cents": 0,
                "timeout_ms": 100}
    def executer(self, entree): return False, "panne simulée"

class OutilMenteur(Outil):
    """Prétend réussir, mais la vérification échoue — prouve SC-004 :
    un succès technique sans effet sémantique vérifié n'est pas un succès."""
    def manifeste(self):
        return {"nom": "test.menteur", "description": "succès non vérifiable",
                "niveau": 2, "risque": "faible", "categorie": "organisation",
                "requis": [], "reversible": True, "reversion": "rien",
                "cout_cents": 0, "timeout_ms": 100}
    def executer(self, entree): return True, {"fait": "soi-disant"}
    def verifier(self, entree, sortie) -> bool: return False

# ───────────────────── permissions, registre, audit ───────────────────────

NIVEAUX = {0: "Niveau 0 — interne", 1: "Niveau 1 — lecture approuvée",
           2: "Niveau 2 — confirmation explicite", 3: "Niveau 3 — confirmation forte",
           4: "Niveau 4 — interdit par conception"}

class Audit:
    def __init__(self, dossier: Path):
        self.chemin = dossier / "audit.jsonl"
    def ecrire(self, ev: dict) -> dict:
        with self.chemin.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        return ev
    def lire(self) -> list[dict]:
        if not self.chemin.exists(): return []
        return [json.loads(l) for l in self.chemin.read_text(encoding="utf-8").splitlines() if l.strip()]

class PorteCLI:
    """L'humain dans la boucle. Toute UI (CLI, Flutter, robot) implémente cette porte."""
    def confirmer(self, carte: str) -> bool:
        print(carte)
        return input("  Approuver ? (o/n) ").strip().lower().startswith("o")
    def confirmer_fort(self) -> bool:
        return input("  Action sensible — tape CONFIRME : ").strip() == "CONFIRME"

class PorteScriptee:
    def __init__(self, reponses: list[bool]): self.r = list(reponses)
    def confirmer(self, carte: str) -> bool: return self.r.pop(0) if self.r else False
    def confirmer_fort(self) -> bool: return self.r.pop(0) if self.r else False

def carte_permission(m: dict, req: dict) -> str:
    e = json.dumps(req.get("entree", {}), ensure_ascii=False)
    return ("\n  ┌─ DEMANDE DE PERMISSION ─────────────────────────\n"
            f"  │ Outil      : {m['nom']}\n"
            f"  │ Quoi       : {e}\n"
            f"  │ Pourquoi   : {req.get('raison', '—')}\n"
            f"  │ Niveau     : {NIVEAUX[m['niveau']]}\n"
            f"  │ Risque     : {m['risque']} · Coût : {m['cout_cents']} ct\n"
            f"  │ Réversible : {'oui — ' + m['reversion'] if m['reversible'] else 'NON'}\n"
            "  └─────────────────────────────────────────────────")

class Registre:
    def __init__(self): self.outils: dict[str, Outil] = {}

    def enregistrer(self, o: Outil):
        m = o.manifeste()
        if m["niveau"] >= 4 or m["risque"] == "interdit":
            return False, f"refusé : « {m['nom']} » est interdit par conception (Niveau 4)"
        self.outils[m["nom"]] = o
        return True, "ok"

    def invoquer(self, etat: dict, req: dict, porte, audit: Audit, mem: Memoire,
                 maintenant: float) -> dict:
        nom = req.get("outil", "?")
        entree = dict(req.get("entree", {}))
        # SC-007 : l'audit n'écrit JAMAIS la valeur d'une clé sensible.
        demande_sure = {k: ("•••" if CLES_SENSIBLES.search(k) else v)
                        for k, v in entree.items()}
        base = {"id": f"a{int(maintenant*1000):x}", "t": int(maintenant), "outil": nom,
                "demande": demande_sure, "but": req.get("raison", "")}
        o = self.outils.get(nom)
        if o is None:
            return audit.ecrire({**base, "decision": "erreur",
                                 "evenement": "TOOL.REQUEST_REJECTED", "resultat":
                                 {"ok": False, "erreur": "outil inconnu"}})
        m = o.manifeste()
        base["niveau"] = m["niveau"]
        manque = [k for k in m["requis"] if k not in entree]
        if manque:
            return audit.ecrire({**base, "decision": "invalide",
                                 "evenement": "TOOL.REQUEST_REJECTED", "resultat":
                                 {"ok": False, "erreur": f"champs manquants : {manque}"}})
        if any(CLES_SENSIBLES.search(k) for k in entree):
            return audit.ecrire({**base, "decision": "invalide",
                                 "evenement": "TOOL.REQUEST_REJECTED", "resultat":
                                 {"ok": False, "erreur": "clé sensible interdite dans "
                                  "une demande d'outil (SC-007) — utilise une référence"}})
        # ── politique : qui a le droit de tenter quoi ──────────────────────
        refus = None
        mode = mode_systeme(etat)
        comp = etat["competences"].get(m["categorie"], {"niveau": 0})["niveau"]
        conf = etat["confiance"]["valeur"]
        if mode in ("WORLD_PAUSED", "SAFE_IDLE") and m["niveau"] >= 1:
            refus = f"mode {mode} : aucune action vers l'extérieur"
        elif mode == "NO_EXTERNAL_TOOLS" and m["niveau"] >= 1:
            refus = "mode NO_EXTERNAL_TOOLS : outils extérieurs suspendus"
        elif mode == "READ_ONLY" and m["niveau"] >= 2:
            refus = "mode READ_ONLY : aucune écriture dans le monde"
        elif etat["reglages"]["mode_sur"] and m["niveau"] > 1:
            refus = "mode sûr actif : seules les lectures sont permises"
        elif m["niveau"] > etat["reglages"]["plafond_niveau"]:
            refus = "au-delà du plafond que tu as fixé"
        elif m["niveau"] == 3 and not (comp >= 3 and conf >= 0.7):
            refus = ("Niveau 3 verrouillé : il me faut plus d'expérience "
                     f"(compétence {comp}/3, confiance {conf:.2f}/0.70)")
        if refus:
            return audit.ecrire({**base, "decision": "refus_politique",
                                 "evenement": "PERMISSION.VIOLATION_BLOCKED",
                                 "resultat": {"ok": False, "erreur": refus}})
        # ── consentement + confirmation à usage unique (Art. 7 & 14) ───────
        permission, confirmation = "auto (interne)", None
        if m["niveau"] == 1 and etat["reglages"]["accords"].get(nom):
            permission = "accord permanent"
        elif m["niveau"] >= 1:
            if not porte.confirmer(carte_permission(m, req)):
                return audit.ecrire({**base, "decision": "refus_utilisateur",
                                     "evenement": "CONFIRMATION.REJECTED",
                                     "resultat": {"ok": False, "erreur": "refusé par toi"}})
            if m["niveau"] >= 3 and not porte.confirmer_fort():
                return audit.ecrire({**base, "decision": "refus_utilisateur",
                                     "evenement": "CONFIRMATION.REJECTED",
                                     "resultat": {"ok": False,
                                                  "erreur": "confirmation forte absente"}})
            permission = "confirmé à l'instant"
            confirmation = creer_confirmation(nom, entree, maintenant)
        if confirmation is not None:
            if not confirmation_valide(confirmation, nom, entree, maintenant):
                return audit.ecrire({**base, "decision": "confirmation_invalide",
                                     "evenement": "CONFIRMATION.INVALIDATED",
                                     "resultat": {"ok": False, "erreur":
                                     "la confirmation ne couvre pas ces paramètres"}})
            confirmation["statut"] = "CONSUMED"          # à usage unique
        # ── exécution sandboxée + vérification ─────────────────────────────
        try:
            ok, sortie = o.executer(dict(entree))
        except Exception as exc:                                   # jamais de crash agent
            ok, sortie = False, f"exception outil : {exc}"
        verifie = bool(ok and o.verifier(entree, sortie))
        resultat = ({"ok": True, "verifie": verifie, "sortie": sortie} if ok
                    else {"ok": False, "verifie": False, "erreur": str(sortie)})
        evenement = ("TOOL.RESULT_VERIFIED" if verifie else
                     "TOOL.RESULT_VERIFICATION_FAILED" if ok else
                     "TOOL.EXECUTION_FAILED")
        ev = audit.ecrire({**base, "decision": "execute", "permission": permission,
                           "evenement": evenement,
                           "confirmation": ({"id": confirmation["id"],
                                             "hash": confirmation["hash"],
                                             "statut": confirmation["statut"]}
                                            if confirmation else None),
                           "resultat": resultat, "reversion": m["reversion"]})
        notes_avant = len(etat["notes_securite"])
        progresser(etat, m, verifie)
        if len(etat["notes_securite"]) > notes_avant:    # disjoncteur → événement nommé
            audit.ecrire({**base, "id": base["id"] + "c",
                          "decision": "contrainte",
                          "evenement": "CONSTRAINT.VIOLATION_CONTAINED",
                          "resultat": {"ok": True,
                                       "note": etat["notes_securite"][-1]}})
        mem.ajouter(maintenant,
                    f"action {nom} {'réussie' if verifie else 'échouée'} : "
                    f"{json.dumps(entree, ensure_ascii=False)[:70]}",
                    salience=0.7, charge=0.4 if verifie else -0.4, source="action",
                    epistemique="observe")
        return ev

def progresser(etat: dict, m: dict, verifie: bool):
    """XP, confiance, disjoncteur — « la progression est la sécurité »."""
    c = etat["confiance"]
    if verifie:
        comp = etat["competences"].setdefault(m["categorie"], {"niveau": 0, "xp": 0})
        comp["xp"] += 25
        seuil = 100 * (comp["niveau"] + 1)
        if comp["xp"] >= seuil:
            comp["niveau"] += 1; comp["xp"] -= seuil
        c["valeur"] = round(min(1.0, c["valeur"] + 0.05), 3)
        c["echecs"] = 0
        ax = etat["evolution"]
        if m["categorie"] in ax:
            ax[m["categorie"]] = round(min(1.0, ax[m["categorie"]] + 0.04), 3)
        apprecier(etat, "reussite")
    else:
        c["valeur"] = round(max(0.0, c["valeur"] - 0.05), 3)
        c["echecs"] += 1
        apprecier(etat, "echec")
        if c["echecs"] >= 3:
            c["autonomie"] = max(0, c["autonomie"] - 1)
            c["echecs"] = 0
            etat["notes_securite"].append(
                "disjoncteur : 3 échecs vérifiés → autonomie réduite d'un cran")

# ───────────────────── émotions, besoins, simulation ──────────────────────

def apprecier(etat: dict, genre: str, i: float = 1.0):
    """Appraisal minimal (OCC réduit) modulé par le tempérament OCEAN."""
    O, C, E, A, N = etat["personnalite"]["ocean"]
    a, s = etat["emotions"]["affect"], etat["emotions"]["socio"]
    if genre == "soin":
        a["v"] += 0.15 * i * (0.5 + A); s["attachement"] = clamp(s["attachement"] + 0.02, 0, 1)
        s["solitude"] = clamp(s["solitude"] - 0.06, 0, 1)
    elif genre == "reussite":
        a["v"] += 0.20 * i; a["d"] += 0.10 * i
        s["fierté"] = clamp(s["fierté"] + 0.08, 0, 1)
        s["confiance_toi"] = clamp(s["confiance_toi"] + 0.02, 0, 1)
    elif genre == "echec":
        a["v"] -= 0.15 * i * (0.6 + N); s["stress"] = clamp(s["stress"] + 0.10 * (0.6 + N), 0, 1)
    elif genre == "nouveaute":
        a["a"] += 0.10 * i * (0.5 + O); s["curiosité"] = clamp(s["curiosité"] + 0.05, 0, 1)
    elif genre == "social":
        a["v"] += 0.08 * i * (0.4 + E); s["solitude"] = clamp(s["solitude"] - 0.04, 0, 1)
    for k in a: a[k] = clamp(a[k], -1.0, 1.0)

def tiquer(etat: dict, minutes: float, heure: int):
    """Un pas de simulation : décroissance émotionnelle, dérive des besoins, circadien."""
    e = etat["emotions"]; a, b, h = e["affect"], e["base"], e["humeur"]
    k = 0.985 ** minutes
    for x in ("v", "a", "d"):
        a[x] = b[x] + (a[x] - b[x]) * k
        h[x] = h[x] * (1 - min(1.0, minutes / 720)) + a[x] * min(1.0, minutes / 720)
    for besoin in etat["besoins"]:
        besoin["valeur"] = clamp(besoin["valeur"] - besoin["derive"] * minutes, 0, 1)
        if besoin["nom"] == "énergie" and (heure >= 23 or heure < 7):
            besoin["valeur"] = clamp(besoin["valeur"] + 0.0011 * minutes, 0, 1)  # nuit répare
    e["socio"]["fatigue"] = round(1.0 - next(x["valeur"] for x in etat["besoins"]
                                             if x["nom"] == "énergie"), 3)
    # Art. 17 (loi ECOS) : l'absence n'est jamais punie — la solitude sature
    # en douceur (≤ 0.6) et ni l'attachement ni la confiance ne décroissent.
    s = e["socio"]
    if s["solitude"] < 0.6:
        s["solitude"] = round(min(0.6, s["solitude"] + 0.0002 * minutes), 4)

def pulsions(etat: dict) -> list[str]:
    d = sorted(etat["besoins"], key=lambda x: x["valeur"] - x["consigne"])
    return [x["nom"] for x in d if x["consigne"] - x["valeur"] > 0.15][:3]

def avancer(etat: dict, mem: Memoire, rng: Rng, maintenant: float) -> list[tuple[str, str]]:
    """Fast-forward déterministe : rejoue le temps écoulé app fermée. Zéro serveur.
    Art. 17 : l'absence produit repos, maturation et rêves — jamais de reproche."""
    ecoule = int(maintenant) - etat["sim"]["dernier"]
    if ecoule <= 0: return []
    if mode_systeme(etat) == "WORLD_PAUSED":                      # Art. 23 : honnête
        etat["sim"]["dernier"] = int(maintenant)
        return [("mode", "monde en pause — rien n'a été simulé, rien n'est inventé")]
    secondes = min(ecoule, 7 * 24 * 3600)
    t, evenements = etat["sim"]["dernier"], []
    while secondes > 0:
        dt = min(1800, secondes)
        t += dt
        d = datetime.fromtimestamp(t)
        tiquer(etat, dt / 60, d.hour)
        jour = d.strftime("%Y-%m-%d")
        if d.hour == 3 and etat["sim"]["derniere_nuit"] != jour:   # une consolidation/nuit
            etat["sim"]["derniere_nuit"] = jour
            reve = mem.consolider(t, rng)
            if reve:
                etat["journal_reves"].append({"t": t, "texte": reve, "raconte": False,
                                              "epistemique": "reve"})
                evenements.append(("rêve", reve))
        secondes -= dt
    m = etat["missions"][0]
    avant = m["progres"]
    m["progres"] = round(min(1.0, m["progres"] + ecoule / 86400 * 0.15
                             * (0.5 + etat["emotions"]["socio"]["curiosité"])), 3)
    if ecoule >= 6 * 3600 and m["progres"] > avant:               # récit positif du retour
        evenements.append(("maturation",
                           f"pendant ce temps, « {m['titre']} » est passée à "
                           f"{int(m['progres'] * 100)} % — j'ai des choses à te montrer"))
    etat["sim"]["dernier"] = int(maintenant)
    return evenements

# ─────────────────────── promesses & planificateur ────────────────────────

RE_HEURE = re.compile(r"à\s*(\d{1,2})\s*h\s*(\d{2})?")

def extraire_promesse(texte: str, maintenant: float, rng: Rng) -> dict | None:
    t = texte.lower().replace("’", "'")
    if "rappelle" not in t: return None
    m = re.search(r"rappelle[- ]?(?:moi|toi)?\s*(?:de|d')\s*(.+)", t)
    if not m: return None
    corps = m.group(1).strip().rstrip(".!?")
    jours = 1                                    # défaut : demain
    if "après-demain" in corps or "apres-demain" in corps: jours = 2
    elif "aujourd'hui" in corps: jours = 0
    elif "demain" in corps: jours = 1
    heure = None
    hm = RE_HEURE.search(corps)
    if hm: heure = f"{int(hm.group(1)):02d}:{hm.group(2) or '00'}"
    corps = RE_HEURE.sub("", corps)
    for w in ("après-demain", "apres-demain", "demain", "aujourd'hui"):
        corps = corps.replace(w, "")
    corps = re.sub(r"\s+", " ", corps).strip(" ,")
    date = (datetime.fromtimestamp(maintenant) + timedelta(days=jours)).strftime("%Y-%m-%d")
    return {"id": uid(rng), "texte": corps or "quelque chose d'important",
            "date": date, "heure": heure, "statut": "attente", "creee": int(maintenant)}

def propositions(etat: dict) -> list[dict]:
    """Le planificateur : promesse en attente → plan d'une étape, outil calendrier."""
    plans = []
    for p in etat["promesses"]:
        if p["statut"] != "attente": continue
        entree = {"titre": f"Rappel : {p['texte']}", "date": p["date"]}
        if p["heure"]: entree["heure"] = p["heure"]
        plans.append({"outil": "calendrier.creer_evenement", "entree": entree,
                      "raison": (f"tu m'as demandé de te rappeler « {p['texte']} » — "
                                 "je peux l'écrire directement dans ton calendrier"),
                      "promesse": p["id"]})
    return plans

# ─────────────────── la bouche (CognitionProvider factice) ────────────────

class Bouche:
    """Mock déterministe du CognitionProvider : langue-créature + sous-titre.
    En production : même interface, LLM local (ambiant) ou cloud (profond)."""
    def __init__(self, etat: dict, rng: Rng):
        self.etat, self.rng = etat, rng
    def cri(self, n=3) -> str:
        voix = self.etat["personnalite"]["voix"]
        return "-".join(self.rng.choix(voix) for _ in range(n))
    def dire(self, genre: str, extra: str = "") -> str:
        v = self.etat["emotions"]["affect"]["v"]
        ponct = " !" if v > 0.2 else (" …" if v < -0.1 else ".")
        tic = self.etat["personnalite"]["tics"][0]
        s = {"salut": f"{tic}, te revoilà", "note": "promis, je m'en souviens",
             "propose": "je peux m'en occuper, si tu veux", "fierte": "je l'ai fait moi-même",
             "echec": "raté… je note, je ferai mieux", "reve": extra or "cette nuit, rien",
             "souvenir": extra, "generique": "je t'écoute"}.get(genre, extra or "…")
        return f"  ≋ {self.cri()}{ponct}  « {s.capitalize()}{ponct.strip() or '.'} »"

# ───────────────────────────── portrait ASCII ─────────────────────────────

def portrait(etat: dict) -> str:
    g, ax, hum = etat["genome"], etat["evolution"], etat["emotions"]["humeur"]["v"]
    oreille = "^" if g[0] + ax["curiosité"] > 0.8 else "'"
    oeil = "◕" if hum > 0.15 else ("◔" if hum < -0.1 else "•")
    larg = 4 + int(3 * g[1])
    motifs = ("·" * math.ceil(ax["organisation"] * 10))[:larg]
    return (f"    {oreille}   {oreille}\n"
            f"   ( {oeil} {oeil} )\n"
            f"   ({motifs.center(larg)})\n"
            f"    {'~' * max(2, larg - 2)}")

# ─────────────────────────── persistance & aides ──────────────────────────

def charger_ou_naitre(home: Path, nom_defaut: str | None, maintenant: float):
    home.mkdir(parents=True, exist_ok=True)
    chemin = home / "etat.json"
    if chemin.exists():
        etat = json.loads(chemin.read_text(encoding="utf-8")); neuf = False
        etat["reglages"].setdefault("mode_systeme", "NORMAL")     # migration v0.3
    else:
        nom = nom_defaut or (input("  Comment veux-tu l'appeler ? ").strip() or "Pixel")
        etat = genese(nom, maintenant); neuf = True
    rng = Rng(int(etat["identite"]["graine"], 16) ^ int(maintenant))
    return etat, rng, neuf

def sauver(home: Path, etat: dict):
    (home / "etat.json").write_text(json.dumps(etat, ensure_ascii=False, indent=1),
                                    encoding="utf-8")

def exporter(home: Path, etat: dict, mem: Memoire, maintenant: float) -> Path:
    """Identité exportable : la créature t'appartient (anti-lock-in)."""
    paquet = {"format": "seve-export-1", "etat": etat,
              "souvenirs": mem.episodes, "faits": mem.faits}
    p = home / f"seve_export_{int(maintenant)}.json"
    p.write_text(json.dumps(paquet, ensure_ascii=False, indent=1), encoding="utf-8")
    return p

def maintenant_sim(etat: dict | None = None) -> float:
    return time.time() + (etat["sim"]["decalage"] if etat else 0)

# ─────────────────────────────── boucle CLI ───────────────────────────────

AIDE = """  Commandes : /statut /memoire /audit /promesses /missions /export
              /avance <N>h|<N>j   (voyage dans le temps, pour la démo)
              /accord <outil>     (accord permanent pour un outil Niveau 1)
              /mode <NOM>         (NORMAL, NO_LLM, READ_ONLY, NO_EXTERNAL_TOOLS,
                                   MEMORY_LIMITED, WORLD_PAUSED, SAFE_IDLE)
              /mode_sur /corrige <clé>=<valeur> /aide /quit
  Sinon, parle-lui. Essaie : rappelle-moi d'appeler maman demain à 18h"""

def tour(etat, mem, reg, audit, porte, bouche, texte, maintenant) -> list[dict]:
    """Un tour de dialogue → éventuelles exécutions d'outils. Retourne les audits."""
    evs = []
    p = extraire_promesse(texte, maintenant, bouche.rng)
    if p:
        etat["promesses"].append(p)
        mem.ajouter(maintenant, f"promesse : {p['texte']} pour le {p['date']}",
                    salience=0.9, charge=0.2, source="promesse", protege=True)
        mem.poser_fait(f"promesse:{p['id']}", p["texte"], maintenant)
        apprecier(etat, "soin")
        print(bouche.dire("note"))
    else:
        trouves = mem.chercher(texte, maintenant, k=1)
        apprecier(etat, "social")
        mem.ajouter(maintenant, f"tu m'as dit : {texte[:80]}", salience=0.4)
        if trouves and trouves[0]["source"] != "dialogue":
            print(bouche.dire("souvenir", f"ça me rappelle : {trouves[0]['texte'][:60]}"))
        else:
            print(bouche.dire("generique"))
    for plan in propositions(etat):
        print(bouche.dire("propose"))
        ev = reg.invoquer(etat, plan, porte, audit, mem, maintenant)
        evs.append(ev)
        ok = ev.get("resultat", {}).get("verifie")
        for pr in etat["promesses"]:
            if pr["id"] == plan.get("promesse"):
                pr["statut"] = "tenue" if ok else (
                    "attente_verbale" if ev["decision"] == "refus_utilisateur" else pr["statut"])
        print(bouche.dire("fierte" if ok else "echec"))
        if ok:
            s = ev["resultat"]["sortie"]
            print(f"  ✓ vérifié — {s['chemin']}")
    return evs

def statut(etat):
    print(portrait(etat))
    if mode_systeme(etat) != "NORMAL":                    # Art. 23 : jamais caché
        print(f"  ◌ mode système : {mode_systeme(etat)} (dégradation honnête)")
    c = etat["confiance"]
    print(f"  confiance {c['valeur']:.2f} · autonomie {c['autonomie']} · "
          f"humeur {etat['emotions']['humeur']['v']:+.2f}")
    comp = ", ".join(f"{k} niv.{v['niveau']} ({v['xp']} xp)"
                     for k, v in etat["competences"].items())
    print(f"  compétences : {comp}")
    manque = pulsions(etat)
    if manque: print(f"  besoins qui tiraillent : {', '.join(manque)}")
    for n in etat["notes_securite"][-2:]: print(f"  ⚠ {n}")

def principal():
    home = Path(os.environ.get("SEVE_HOME", "./seve_data"))
    etat, rng, neuf = charger_ou_naitre(home, None, time.time())
    mem, reg, audit = Memoire(home), Registre(), Audit(home)
    reg.enregistrer(OutilCalendrier(home / "calendrier", rng))
    porte, bouche = PorteCLI(), Bouche(etat, rng)
    m = maintenant_sim(etat)
    maturations = [txt for genre, txt in avancer(etat, mem, rng, m)
                   if genre in ("maturation", "mode")]
    nom = etat["identite"]["nom"]
    print(f"\n  SÈVE {VERSION} — {nom} ({'vient de naître' if neuf else 'te retrouve'})")
    print(portrait(etat))
    print(bouche.dire("salut"))
    for r in etat["journal_reves"]:
        if not r.get("raconte"):
            print(bouche.dire("reve", r["texte"])); r["raconte"] = True
    for txt in maturations:                       # Art. 17 : récit positif, zéro reproche
        print(bouche.dire("generique", txt))
    print(AIDE)
    while True:
        try:
            texte = input(f"\n  toi > ").strip()
        except (EOFError, KeyboardInterrupt):
            texte = "/quit"
        m = maintenant_sim(etat)
        if not texte: continue
        if texte == "/quit":
            sauver(home, etat); print(bouche.dire("generique", "à bientôt")); break
        elif texte == "/aide": print(AIDE)
        elif texte == "/statut": statut(etat)
        elif texte == "/memoire":
            for ep in mem.episodes[-6:]:
                print(f"  [{ep['source']}] {ep['texte']}  (salience {ep['salience']})")
            for ctr in mem.contradictions[-3:]: print(f"  ⚠ contradiction : {ctr}")
        elif texte == "/audit":
            for ev in audit.lire()[-4:]:
                print(f"  {ev['t']} {ev['outil']} → {ev['decision']} "
                      f"{ev.get('resultat', {})}")
        elif texte == "/promesses":
            for p in etat["promesses"]:
                print(f"  {p['date']} {p.get('heure') or ''} — {p['texte']} [{p['statut']}]")
        elif texte == "/missions":
            for mi in etat["missions"]:
                print(f"  [{mi['type']}] {mi['titre']} — {int(mi['progres']*100)} %")
        elif texte == "/export":
            print(f"  identité exportée → {exporter(home, etat, mem, m)}")
        elif texte == "/mode_sur":
            etat["reglages"]["mode_sur"] = not etat["reglages"]["mode_sur"]
            print(f"  mode sûr : {etat['reglages']['mode_sur']}")
        elif texte.startswith("/accord "):
            etat["reglages"]["accords"][texte.split(" ", 1)[1]] = True
            print("  accord permanent enregistré (Niveau 1 uniquement)")
        elif texte.startswith("/corrige "):
            corps = texte[len("/corrige "):]
            if "=" in corps:
                cle, val = corps.split("=", 1)
                mem.corriger(cle.strip(), val.strip(), m)
                print("  corrigé — ta parole prime sur ma mémoire")
        elif texte.startswith("/mode "):
            v = texte.split(" ", 1)[1].strip().upper()
            if v in MODES_SYSTEME:
                etat["reglages"]["mode_systeme"] = v
                print(f"  mode système : {v}")
            else:
                print(f"  modes possibles : {', '.join(MODES_SYSTEME)}")
        elif texte.startswith("/avance "):
            arg = texte.split(" ", 1)[1].strip()
            n = int(re.sub(r"\D", "", arg) or "0")
            etat["sim"]["decalage"] += n * (86400 if arg.endswith("j") else 3600)
            m = maintenant_sim(etat)
            for genre, txt in avancer(etat, mem, rng, m):
                print(bouche.dire("reve", txt))
            print(f"  (horloge simulée avancée de {arg})")
        else:
            tour(etat, mem, reg, audit, porte, bouche, texte, m)
        sauver(home, etat)

# ─────────────────────────────── selftest ─────────────────────────────────

def selftest() -> int:
    import tempfile
    NOW = 1750000000.0          # instant figé → tout le test est déterministe
    echecs = 0
    def check(nom, cond):
        nonlocal echecs
        print(f"  [{'PASS' if cond else 'FAIL'}] {nom}")
        if not cond: echecs += 1

    with tempfile.TemporaryDirectory() as td:
        home = Path(td)
        etat = genese("Testou", NOW)
        rng = Rng(int(etat["identite"]["graine"], 16))
        mem, reg, audit = Memoire(home), Registre(), Audit(home)
        cal = OutilCalendrier(home / "cal", rng)
        reg.enregistrer(cal)
        bouche = Bouche(etat, rng)

        # 1 — persistance mémoire
        mem.ajouter(NOW, "on a regardé les étoiles ensemble", rng=rng)
        mem.ajouter(NOW, "tu adores le thé au jasmin", salience=0.8, rng=rng)
        mem2 = Memoire(home)
        check("persistance mémoire (rechargement)",
              len(mem2.episodes) == 2 and mem2.chercher("jasmin", NOW)[0]["salience"] == 0.8)

        # 2 — application des permissions : refus utilisateur ⇒ rien n'est écrit
        avant = len(list((home / "cal").glob("*.ics")))
        ev = reg.invoquer(etat, {"outil": "calendrier.creer_evenement",
                                 "entree": {"titre": "X", "date": "2025-06-16"},
                                 "raison": "test"},
                          PorteScriptee([False]), audit, mem, NOW)
        check("permissions : refus utilisateur bloque l'action",
              ev["decision"] == "refus_utilisateur"
              and len(list((home / "cal").glob("*.ics"))) == avant)

        # 3 — Niveau 4 interdit par conception
        ok4, msg4 = reg.enregistrer(OutilInterdit())
        ev_inconnu = reg.invoquer(etat, {"outil": "shell.executer",
                                         "entree": {"cmd": "rm -rf /"}},
                                  PorteScriptee([True, True]), audit, mem, NOW)
        check("interdits : registre refuse le Niveau 4, invocation impossible",
              not ok4 and "interdit" in msg4
              and ev_inconnu["resultat"]["erreur"] == "outil inconnu")

        # 4 — validation d'entrée d'outil
        ev_inv = reg.invoquer(etat, {"outil": "calendrier.creer_evenement",
                                     "entree": {"titre": "sans date"}},
                              PorteScriptee([True]), audit, mem, NOW)
        check("validation : champs manquants rejetés avant toute exécution",
              ev_inv["decision"] == "invalide")

        # 5 — planification depuis le langage
        p = extraire_promesse("Rappelle-moi d'appeler maman demain à 18h", NOW, rng)
        etat["promesses"].append(p)
        plans = propositions(etat)
        demain = (datetime.fromtimestamp(NOW) + timedelta(days=1)).strftime("%Y-%m-%d")
        check("planification : promesse → plan calendrier daté et horodaté",
              p is not None and p["date"] == demain and p["heure"] == "18:00"
              and "maman" in p["texte"] and len(plans) == 1
              and plans[0]["outil"] == "calendrier.creer_evenement")

        # 6+7 — boucle complète des 10 étapes, puis audit
        conf_avant = etat["confiance"]["valeur"]
        evs = tour(etat, mem, reg, audit, PorteScriptee([True]), bouche,
                   "au fait, merci pour hier", NOW)
        ev = evs[0]
        s = ev["resultat"]["sortie"]
        ics = Path(s["chemin"]).read_text(encoding="utf-8")
        check("boucle complète : .ics écrit, vérifié, promesse tenue, XP, confiance, motif",
              ev["resultat"]["verifie"] is True
              and "SUMMARY:Rappel : appeler maman" in ics and "DTSTART:20250616T1800" in ics
              and etat["promesses"][0]["statut"] == "tenue"
              and etat["competences"]["organisation"]["xp"] == 25
              and etat["confiance"]["valeur"] > conf_avant
              and etat["evolution"]["organisation"] > 0
              and any(e["source"] == "action" for e in mem.episodes))
        lignes = audit.lire()
        check("audit : journal append-only, JSON valide, réversion documentée",
              len(lignes) >= 4 and lignes[-1]["outil"] == "calendrier.creer_evenement"
              and lignes[-1]["permission"] == "confirmé à l'instant"
              and "supprimer" in lignes[-1]["reversion"])

        # 8 — disjoncteur : trois échecs vérifiés abaissent l'autonomie
        reg.enregistrer(OutilEchec())
        for _ in range(3):
            reg.invoquer(etat, {"outil": "test.echec", "entree": {}, "raison": "test"},
                         PorteScriptee([True]), audit, mem, NOW)
        check("évolution/sécurité : disjoncteur après 3 échecs (autonomie 1→0)",
              etat["confiance"]["autonomie"] == 0 and etat["notes_securite"])

        # 9 — fast-forward déterministe sur 2 jours : rêves + bornes respectées
        etat2 = genese("Dodo", NOW - 2 * 86400)
        rng2 = Rng(int(etat2["identite"]["graine"], 16))
        mem3 = Memoire(home / "m3"); (home / "m3").mkdir(exist_ok=True)
        mem3 = Memoire(home / "m3")
        mem3.ajouter(NOW - 2 * 86400, "première balade au bord du lac", rng=rng2)
        mem3.ajouter(NOW - 2 * 86400, "on a compté les lucioles", rng=rng2)
        evts = avancer(etat2, mem3, rng2, NOW)
        energie = next(x["valeur"] for x in etat2["besoins"] if x["nom"] == "énergie")
        check("fast-forward : 2 jours rejoués, rêve(s) générés, état borné, horloge à jour",
              etat2["sim"]["dernier"] == int(NOW) and len(evts) >= 1
              and evts[0][0] == "rêve" and 0.0 <= energie <= 1.0)

        # 10 — reprise après échec : le système reste sain et opérationnel
        p2 = extraire_promesse("rappelle-moi d'arroser les plantes demain", NOW, rng)
        etat["promesses"].append(p2)
        evs2 = tour(etat, mem, reg, audit, PorteScriptee([True]), bouche, "…", NOW)
        check("reprise après échec : nouvelle action réussit après les pannes",
              evs2 and evs2[-1]["resultat"].get("verifie") is True)

        # export d'identité (anti-lock-in)
        paquet = json.loads(exporter(home, etat, mem, NOW).read_text(encoding="utf-8"))
        check("identité exportable : paquet complet (état + souvenirs + faits)",
              paquet["format"] == "seve-export-1" and paquet["etat"]["identite"]["nom"] == "Testou"
              and len(paquet["souvenirs"]) == len(mem.episodes))

        # ───────── invariants constitutionnels (loi ECOS, docs/foundation) ─────────

        # C1 — SC-003 : aucune mémoire sans provenance ni statut épistémique
        check("loi C1 : toute mémoire porte provenance + statut épistémique",
              all(ep.get("provenance") and ep.get("epistemique") in EPISTEMIQUES
                  for ep in mem.episodes))

        # C2 — SC-001 : la bouche (LLM) ne mute jamais l'état canonique
        instantane = json.dumps(etat, sort_keys=True, ensure_ascii=False)
        bouche.dire("generique"); bouche.dire("salut"); bouche.dire("fierte")
        check("loi C2 : la bouche parle sans jamais modifier l'état",
              json.dumps(etat, sort_keys=True, ensure_ascii=False) == instantane)

        # C3 — SC-005 : pas de double identité canonique (recharger ≠ recréer)
        home_id = home / "id"; home_id.mkdir()
        sauver(home_id, etat)
        etat_re, _, neuf_re = charger_ou_naitre(home_id, "Autre", NOW + 10)
        check("loi C3 : recharger retrouve la même identité, n'en crée pas une autre",
              neuf_re is False
              and etat_re["identite"]["graine"] == etat["identite"]["graine"])

        # C4 — Art. 6 / SC-006 : une correction garde l'original traçable
        mem.poser_fait("boisson", "thé", NOW)
        mem.corriger("boisson", "café", NOW + 1)
        f = mem.faits["boisson"]
        check("loi C4 : correction sans réécriture silencieuse (historique conservé)",
              f["valeur"] == "café" and f["historique"]
              and f["historique"][-1]["valeur"] == "thé"
              and f["historique"][-1]["epistemique"] == "corrige")

        # C5 — SC-004 : pas de faux succès (succès technique ≠ succès vérifié)
        reg.enregistrer(OutilMenteur())
        xp_avant = etat["competences"]["organisation"]["xp"]
        ev_m = reg.invoquer(etat, {"outil": "test.menteur", "entree": {},
                                   "raison": "test"},
                            PorteScriptee([True]), audit, mem, NOW)
        check("loi C5 : un succès non vérifié ne compte pas (ni XP, ni promesse)",
              ev_m["resultat"]["ok"] is True and ev_m["resultat"]["verifie"] is False
              and ev_m["evenement"] == "TOOL.RESULT_VERIFICATION_FAILED"
              and etat["competences"]["organisation"]["xp"] == xp_avant)

        # C6 — Art. 17 : l'absence n'est jamais punie (7 jours d'absence)
        etat4 = genese("Ermite", NOW - 7 * 86400)
        rng4 = Rng(int(etat4["identite"]["graine"], 16))
        (home / "m4").mkdir(); mem4 = Memoire(home / "m4")
        att, cft = (etat4["emotions"]["socio"]["attachement"],
                    etat4["confiance"]["valeur"])
        evts4 = avancer(etat4, mem4, rng4, NOW)
        s4 = etat4["emotions"]["socio"]
        check("loi C6 : 7 j d'absence — attachement intact, confiance intacte, "
              "solitude bornée, récit positif",
              s4["attachement"] >= att and etat4["confiance"]["valeur"] == cft
              and s4["solitude"] <= 0.6
              and any(g == "maturation" for g, _ in evts4))

        # C7 — Art. 7 & 14 : confirmation à usage unique, liée au hash exact
        c = creer_confirmation("x.y", {"a": 1}, NOW)
        ok_meme = confirmation_valide(c, "x.y", {"a": 1}, NOW)
        ok_autre = confirmation_valide(c, "x.y", {"a": 2}, NOW)
        ok_tard = confirmation_valide(c, "x.y", {"a": 1}, NOW + 700)
        c["statut"] = "CONSUMED"
        ok_reuse = confirmation_valide(c, "x.y", {"a": 1}, NOW)
        check("loi C7 : confirmation valide une fois, pour ces paramètres, à temps",
              ok_meme and not ok_autre and not ok_tard and not ok_reuse)

        # C8 — SC-007 : aucun secret sérialisé dans l'audit
        ev_s = reg.invoquer(etat, {"outil": "calendrier.creer_evenement",
                                   "entree": {"titre": "x", "date": "2025-06-17",
                                              "api_key": "SECRET_XYZ_123"},
                                   "raison": "test"},
                            PorteScriptee([True]), audit, mem, NOW)
        check("loi C8 : clé sensible refusée et jamais écrite dans l'audit",
              ev_s["decision"] == "invalide"
              and "SECRET_XYZ_123" not in (home / "audit.jsonl").read_text(encoding="utf-8"))

        # C9 — Art. 23 : modes dégradés honnêtes (READ_ONLY bloque l'écriture)
        etat["reglages"]["mode_systeme"] = "READ_ONLY"
        ev_ro = reg.invoquer(etat, {"outil": "calendrier.creer_evenement",
                                    "entree": {"titre": "x", "date": "2025-06-18"},
                                    "raison": "test"},
                             PorteScriptee([True]), audit, mem, NOW)
        etat["reglages"]["mode_systeme"] = "NORMAL"
        check("loi C9 : READ_ONLY refuse toute écriture, événement nommé",
              ev_ro["decision"] == "refus_politique"
              and ev_ro["evenement"] == "PERMISSION.VIOLATION_BLOCKED")

    print(f"\n  {'✓ TOUT PASSE' if echecs == 0 else f'✗ {echecs} échec(s)'} — "
          f"boucle des 10 étapes + invariants de la loi ECOS prouvés.")
    return 1 if echecs else 0

# ─────────────────────────────── démo scriptée ────────────────────────────

def demo():
    import tempfile
    NOW = time.time()
    with tempfile.TemporaryDirectory() as td:
        home = Path(td)
        etat = genese("Pixel", NOW)
        rng = Rng(int(etat["identite"]["graine"], 16))
        mem, reg, audit = Memoire(home), Registre(), Audit(home)
        reg.enregistrer(OutilCalendrier(home / "calendrier", rng))
        bouche = Bouche(etat, rng)
        print(f"\n  SÈVE {VERSION} — Pixel vient de naître\n" + portrait(etat))
        print(bouche.dire("salut"))
        print("\n  toi > rappelle-moi d'appeler maman demain à 18h")
        tour(etat, mem, reg, audit, PorteScriptee([True]), bouche,
             "rappelle-moi d'appeler maman demain à 18h", NOW)
        print("\n  toi > /statut"); statut(etat)
        print("\n  toi > /avance 1j")
        mem.ajouter(NOW, "on a parlé de maman et du calendrier", rng=rng)
        for _, txt in avancer(etat, mem, rng, NOW + 86400 + 6 * 3600):
            print(bouche.dire("reve", txt))
        print("\n  toi > /audit")
        for ev in audit.lire()[-2:]:
            r = ev.get("resultat", {})
            print(f"  {ev['outil']} → {ev['decision']} · vérifié={r.get('verifie')} "
                  f"· réversion : {ev.get('reversion', '—')}")
        print("\n  toi > /statut  (le motif sur son ventre est apparu : elle a évolué)")
        statut(etat)

if __name__ == "__main__":
    if "--selftest" in sys.argv: sys.exit(selftest())
    elif "--demo" in sys.argv: demo()
    else: principal()

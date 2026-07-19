# Alignement ECOS ↔ SÈVE — v0.4

## Le pacte

Fusion asymétrique, décidée le 19 juillet 2026 : **ECOS est la loi, SÈVE est le corps.** Les documents de `docs/foundation/` (Constitution, contraintes système, anti-features) ont autorité sur l'architecture, qui a autorité sur le code. En cas de contradiction, le document de rang supérieur prévaut ; le code se corrige, jamais l'inverse. La stack d'implémentation ECOS (TypeScript, event sourcing serveur) n'est *pas* adoptée : le runtime reste le monorepo Rust local-first, avec la référence Python `reference/slice.py` qui fait foi du comportement — désormais 20 tests, dont 9 invariants constitutionnels.

Légende des verdicts : **✓** conforme avant v0.4 · **✚** mis en conformité par v0.4 · **◐** partiel (reste documenté) · **◇** hors périmètre actuel, prévu à la roadmap.

## Constitution — les 26 articles

| Art. | Sujet | Verdict | Où dans SÈVE |
|---|---|---|---|
| 1 | Le modèle n'est pas l'identité | ✓ | Doctrine 3 de la bible ; identité dans `etat.json`, bouche interchangeable (`FournisseurCognition`) |
| 2 | Continuité lors des migrations | ✓ | Migration v0.3→v0.4 non destructive démontrée (`charger_ou_naitre`, `Memoire.__init__`) |
| 3 | Unicité canonique | ◐ | Recharger ≠ recréer (invariant C3) ; le statut formel de fork/héritage sera porté avec le multi-appareils |
| 4 | Vérité (jamais prétendre) | ✓ | `verifie` sémantique ; invariant C5 « pas de faux succès » |
| 5 | Statuts épistémiques distincts | ✚ | `EPISTEMIQUES` (10 statuts) sur épisodes, faits et rêves ; jamais transformés silencieusement |
| 6 | Mémoire avec provenance, correction traçable | ✚ | `provenance` obligatoire (C1) ; `corriger()` archive l'original avec statut `corrige` (C4) |
| 7 | Consentement explicite, contextuel, révocable | ✚ | Carte de permission + confirmation à usage unique liée au hash exact des paramètres (C7) ; accords permanents limités au Niveau 1, révocables |
| 8 | Vie privée, contrôle du gardien | ✓ | Local-first, `/export` intégral, `/corrige` ; la *redaction* ciblée d'épisodes reste à outiller (◐) |
| 9 | Dignité (jamais une marchandise affective) | ✓ | Modèle économique bible v0.2 : on finance calcul, outils, matériel — jamais l'affection |
| 10 | Guardianship, pas propriété | ✓ | Vocabulaire adopté : le gardien |
| 11 | Autonomie dans les limites | ✓ | La créature propose, peut ne rien proposer ; plafonds compétence × confiance × politique |
| 12 | SOUL immuable, versionné | ◇ | Équivalents actuels : `personnalite` + `genome` (immuables de fait) ; le SOUL formel avec procédure d'amendement est au jalon v0.5 |
| 13 | Le LLM propose, ECOS valide | ✓ | Doctrine fondatrice ; invariant C2 (la bouche ne mute jamais l'état) |
| 14 | Pipeline d'action en 7 temps | ✓ | Intention → validation → permission → confirmation → exécution → vérification → résultat : c'est `Registre.invoquer` |
| 15 | Sécurité physique ; jamais LLM → robot | ✓ | Niveau 4 inexistant par construction ; `docs/robotics.md` (contrôleur déterministe embarqué) |
| 16 | Transparence des mutations | ✓✚ | Audit append-only ; v0.4 ajoute la nomenclature d'événements (`TOOL.RESULT_VERIFIED`…) |
| 17 | L'absence n'est jamais punie | ✚ | Solitude saturée douce (≤ 0.6), attachement et confiance intacts, récit de retour positif (« maturation ») — invariant C6 |
| 18 | Pas d'optimisation de la dépendance | ✓ | Aucun streak, aucun scroll ; re-vérifié à chaque feature par le test de constitutionnalité |
| 19 | Économie : interdits | ✓ | Anti-features adoptées telles quelles (`docs/foundation/ANTI_FEATURES.md`) |
| 20 | Bloc Network | ◇ | Aucun réseau social au périmètre actuel |
| 21 | Héritage ≠ clonage | ◇ | Prévu avec le multi-créatures |
| 22 | Évolution avec rollback | ✓ | L'export est un snapshot rejouable ; migration non destructive prouvée |
| 23 | Dégradation honnête | ✚ | 7 modes système (`/mode`), `WORLD_PAUSED` ne simule rien et le dit, `READ_ONLY` testé (C9), mode affiché dans `/statut` |
| 24 | Le texte généré n'est jamais canonique | ✓ | Les mots de la bouche n'entrent jamais en mémoire comme faits ; seuls messages du gardien et actions vérifiées le deviennent |
| 25 | Hiérarchie des priorités | ✓ | Adoptée comme référence normative pour tout arbitrage |
| 26 | Amendements versionnés | ✓ | `docs/foundation/` vit dans le dépôt, versionné par git |

## Contraintes système SC-001 → SC-008

| SC | Contrainte | Verdict | Preuve |
|---|---|---|---|
| 001 | Pas de mutation canonique par le LLM | ✓ | Invariant C2 ; en Rust, `dire(&CreatureState, …)` est immuable par le compilateur |
| 002 | Pas de contrôle robotique direct | ✓ | `docs/robotics.md` : intentions bornées, contrôleur déterministe, arrêt réflexe |
| 003 | Pas de mémoire sans provenance | ✚ | Invariant C1 ; migration douce des épisodes v0.3 |
| 004 | Pas de faux succès | ✓✚ | `verifie` depuis v0.3 ; v0.4 le *prouve* avec `OutilMenteur` (C5) et l'événement `TOOL.RESULT_VERIFICATION_FAILED` |
| 005 | Pas de double identité canonique | ◐ | Invariant C3 (recharger ≠ recréer) ; verrouillage formel multi-appareils à venir |
| 006 | Pas de réécriture silencieuse | ✚ | Audit append-only + historique des faits corrigés (C4) |
| 007 | Pas de secret sérialisé | ✚ | Clés sensibles refusées *et* expurgées de l'audit (C8) |
| 008 | Isolation E* | ◇ | Isolation physique : une créature = un dossier `SEVE_HOME` ; l'identifiant explicite arrivera avec le multi-créatures |

## Ce que la v0.4 a changé, concrètement

Dans `reference/slice.py` (référence testée, 20/20) : statuts épistémiques et provenance sur toute mémoire, avec migration douce des données v0.3 ; corrections et contradictions qui archivent l'original au lieu de l'écraser ; confirmations à usage unique liées au hash SHA-256 des paramètres exacts, avec expiration ; sept modes système honnêtes appliqués dans le pipeline de politique et affichés au statut ; l'absence recadrée en maturation (solitude bornée, attachement intact, récit positif au retour) ; la nomenclature d'événements ECOS dans chaque entrée d'audit, y compris `CONSTRAINT.VIOLATION_CONTAINED` quand le disjoncteur se déclenche ; une garde anti-secrets qui refuse la demande *et* expurge l'audit ; et neuf invariants constitutionnels exécutables ajoutés au selftest.

## Traductions assumées (pourquoi pas l'event sourcing complet)

ECOS spécifie event store, outbox, optimistic concurrency et idempotence des commandes — des mécanismes de *système distribué*. SÈVE est local-first mono-gardien : un seul écrivain, zéro réseau, zéro concurrence. Ce qui en tient lieu, à garanties équivalentes pour ce contexte : l'audit append-only est notre journal d'événements (jamais réécrit, rejouable pour comprendre) ; `etat.json` réécrit atomiquement à chaque tour est notre agrégat versionné (champ `version` du format) ; l'export intégral est notre snapshot. Le jour où le multi-appareils arrive (sync chiffrée, tier Complice), l'outbox et les versions d'agrégat deviendront nécessaires — c'est écrit à la roadmap, pas oublié.

## Le test de constitutionnalité, adopté

Toute nouvelle fonctionnalité (et toute proposition d'outil de la future marketplace) devra répondre aux neuf questions du test avant d'entrer dans le code : continuité, vérité, dignité, consentement, SOUL, sécurité, explicabilité, réversibilité, et « resterait-elle acceptable si son fonctionnement était entièrement visible ? ». Une fonction rentable peut et doit être rejetée — c'était déjà la dernière ligne de notre roadmap, c'est désormais la loi.

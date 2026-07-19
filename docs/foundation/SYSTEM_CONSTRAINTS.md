# SYSTEM_CONSTRAINTS.md

## 1. But

Ce document traduit la Constitution en contraintes techniques exécutables.

## 2. Niveaux

```ts
type ConstraintSeverity =
  | "ABSOLUTE"
  | "CRITICAL"
  | "STRONG"
  | "ADVISORY";
```

- `ABSOLUTE` : aucune dérogation runtime.
- `CRITICAL` : blocage et passage possible en `SAFE_IDLE`.
- `STRONG` : refus par défaut, exception auditée.
- `ADVISORY` : avertissement explicite.

## 3. Contraintes absolues

### SC-001 — Pas de mutation canonique directe par le LLM

Le LLM ne peut produire que des propositions structurées.

### SC-002 — Pas de contrôle robotique direct

Toute commande robotique passe par une couche déterministe de sécurité, permissions, limites matérielles et arrêt d’urgence.

### SC-003 — Pas de mémoire sans provenance

Une mémoire `ACTIVE` possède au moins une provenance valide.

### SC-004 — Pas de faux succès

Un outil qui retourne un succès technique ne suffit pas. L’effet sémantique doit être vérifié.

### SC-005 — Pas de double identité canonique active

Toute collision de continuité entraîne verrouillage et `SAFE_IDLE`.

### SC-006 — Pas de réécriture silencieuse

Les événements, audits, versions du SOUL et corrections mémoire sont append-only.

### SC-007 — Pas de secret dans les prompts, logs, événements ou mémoires

Les secrets sont référencés via secret manager, jamais sérialisés.

### SC-008 — Isolation E*

Toute lecture et mutation porte explicitement `eStarId`.

## 4. Contraintes critiques

- permission explicite avant toute action externe ;
- confirmation à usage unique pour les actions sensibles ;
- optimistic concurrency pour les agrégats ;
- idempotence des commandes et consommateurs ;
- validation stricte des sorties LLM ;
- fallback honnête en cas d’échec ;
- snapshot vérifié avant migration critique ;
- conservation du statut épistémique durant consolidation et replay.

## 5. Pipeline d’enforcement

```text
entrée
→ validation de schéma
→ authentification
→ scope E*
→ permission
→ contraintes constitutionnelles
→ politique métier
→ exécution
→ vérification
→ audit
```

## 6. Réaction aux violations

```text
détection
→ blocage
→ enregistrement de violation
→ containment
→ mode dégradé si nécessaire
→ revue
→ récupération
```

## 7. Invariants essentiels

- une décision sélectionne au plus une option ;
- une confirmation n’est consommée qu’une fois ;
- un stream possède une version d’agrégat unique ;
- un lien mémoire ne traverse pas deux E* ;
- une correction référence l’original ;
- un événement n’est jamais modifié ;
- le gardien ne peut pas recevoir les données d’un autre gardien ;
- une génération LLM ne devient pas canonique sans validation.

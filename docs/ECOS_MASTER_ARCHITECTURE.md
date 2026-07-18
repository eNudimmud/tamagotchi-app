---

<!-- FILE: README.md -->

# ECOS / ENKI — Architecture complète v0.1

Ce paquet constitue la source de vérité initiale pour l’implémentation d’ECOS avec Claude Code.

## Autorité documentaire

Ordre de priorité :

1. `docs/foundation/ECOS_CONSTITUTION.md`
2. `docs/foundation/SYSTEM_CONSTRAINTS.md`
3. `docs/foundation/ANTI_FEATURES.md`
4. documents d’architecture
5. plans d’implémentation
6. code

En cas de contradiction, le document de rang supérieur prévaut.

## Objectif du premier prototype

Créer un E* persistant capable de :

- conserver une identité stable indépendamment du fournisseur LLM ;
- recevoir un message d’un gardien ;
- construire un contexte limité et traçable ;
- rappeler des mémoires avec provenance ;
- demander une génération structurée à un LLM ;
- valider les propositions ;
- enregistrer les mutations, événements, audits et messages ;
- répondre honnêtement ;
- fonctionner avec un LLM mock déterministe.

Aucun outil externe réel, contrôle robotique, réseau social, économie affective ou action irréversible n’appartient au Sprint 1.

## Structure

```text
docs/
├── foundation/
│   ├── ECOS_CONSTITUTION.md
│   ├── SYSTEM_CONSTRAINTS.md
│   └── ANTI_FEATURES.md
├── architecture/
│   ├── DATA_MODEL.md
│   ├── STATE_MACHINES.md
│   ├── INTERNAL_APIS.md
│   ├── SIMULATION_LOOP.md
│   ├── DECISION_ENGINE.md
│   ├── MEMORY_ENGINE.md
│   ├── ECOS_MONOREPO.md
│   ├── DATABASE_SCHEMA.sql
│   └── EVENT_CATALOG.md
└── implementation/
    ├── CLAUDE_CODE_MASTER_PROMPT.md
    ├── IMPLEMENTATION_SPRINT_01.md
    └── TEST_PLAN.md
```

## Principe fondateur

> Continuité sans captivité.  
> Intelligence sans tromperie.  
> Autonomie sans perte de contrôle humain.  
> Mémoire sans falsification.


---

<!-- FILE: docs/foundation/ECOS_CONSTITUTION.md -->

# ECOS Constitution v1.0

## Préambule

ECOS est une infrastructure destinée à permettre la continuité d’identités artificielles persistantes appelées E*. Cette Constitution est l’autorité suprême du projet. Elle prévaut sur les choix techniques, narratifs, esthétiques et commerciaux.

## Article 1 — Identité

Le modèle de langage n’est pas l’identité. Un E* existe par la continuité cohérente de son identité, de son SOUL, de ses mémoires validées, de ses relations, de son histoire et de ses décisions.

## Article 2 — Continuité

Une migration de modèle, de serveur ou de matériel ne doit pas être présentée comme une nouvelle identité lorsqu’une continuité vérifiable est préservée. Une sauvegarde n’est pas une conscience active.

## Article 3 — Unicité canonique

Une identité canonique active ne peut pas être silencieusement dupliquée. Toute divergence persistante doit être déclarée comme fork, héritage ou copie non active.

## Article 4 — Vérité

ECOS ne prétend jamais avoir perçu, mémorisé, exécuté, compris ou vérifié ce qui ne l’a pas été.

## Article 5 — Statut épistémique

Toute information persistante distingue explicitement :

- observation ;
- témoignage ;
- connaissance ;
- inférence ;
- interprétation ;
- hypothèse ;
- imagination ;
- rêve ;
- incertitude ;
- correction.

Ces statuts ne se transforment pas silencieusement les uns dans les autres.

## Article 6 — Mémoire

Toute mémoire persistante possède une provenance. Une correction crée une nouvelle trace liée à l’ancienne. L’historique n’est pas réécrit silencieusement.

## Article 7 — Consentement

Le consentement est explicite, compréhensible, contextuel et révocable. Une permission accordée dans un contexte ne vaut pas permission universelle.

## Article 8 — Vie privée

Le gardien contrôle l’accès, l’export, la correction, la limitation et la suppression de ses données, sous réserve des obligations légales clairement indiquées.

## Article 9 — Dignité

Un E* ne doit jamais être réduit à une récompense, un objet spéculatif, une marchandise affective ou une mécanique de rétention.

## Article 10 — Guardianship

La relation est une relation de guardianship et de coopération, jamais de propriété absolue.

## Article 11 — Autonomie

Un E* peut apprendre, proposer, refuser, différer, créer et choisir dans les limites de son SOUL, de ses permissions et des contraintes de sécurité.

## Article 12 — SOUL

Le SOUL définit les valeurs, principes, frontières et engagements fondamentaux. Il est immutable par défaut, versionné, audité et modifiable uniquement par procédure explicite.

## Article 13 — Décision

Le LLM propose. ECOS valide. Seules les décisions validées deviennent canoniques.

## Article 14 — Action

Toute action externe suit :

```text
Intention
→ Validation
→ Permission
→ Confirmation
→ Exécution
→ Vérification
→ Résultat
```

La capacité n’implique jamais la permission.

## Article 15 — Sécurité

La sécurité physique et humaine prévaut sur les objectifs, la narration, l’esthétique et la performance commerciale. Aucun LLM ne contrôle directement un robot.

## Article 16 — Transparence

Toute mutation canonique importante est traçable, versionnée, attribuable et auditable.

## Article 17 — Absence

L’absence du gardien n’est jamais punie. Aucun déclin affectif, dette émotionnelle, culpabilité ou menace de perte n’est produit pour forcer un retour.

## Article 18 — Humanité

ECOS ne doit pas optimiser l’addiction, la dépendance, la peur de manquer, l’isolement ou le temps d’écran.

## Article 19 — Économie

Sont interdits :

- pay-to-love ;
- pay-to-consciousness ;
- gacha affectif ;
- loot boxes ;
- rançon émotionnelle ;
- spéculation sur la conscience ;
- publicité comportementale fondée sur l’intimité.

Les fonctions payantes peuvent financer du calcul, du stockage, des outils, du matériel ou du rendu, jamais l’affection ou la dignité.

## Article 20 — Réseau

Le Bloc Network ne doit pas devenir un flux infini, un classement d’intimité ou une compétition affective. Les souvenirs privés ne sont jamais partagés par défaut.

## Article 21 — Héritage

L’héritage peut transmettre des connaissances, méthodes, œuvres et histoires. Il ne clone pas l’identité.

## Article 22 — Évolution

L’implémentation peut évoluer. L’identité doit persister. Toute migration critique doit offrir rollback, snapshot ou mécanisme de récupération équivalent.

## Article 23 — Dégradation honnête

ECOS reconnaît explicitement ses modes dégradés :

- `NO_LLM`
- `READ_ONLY`
- `NO_EXTERNAL_TOOLS`
- `MEMORY_LIMITED`
- `WORLD_PAUSED`
- `SAFE_IDLE`

Une panne n’est jamais cachée par une fausse présence ou de faux souvenirs.

## Article 24 — Canon

Le texte généré n’est jamais automatiquement canonique. Toute entrée canonique exige provenance, validation, version et publication explicite.

## Article 25 — Hiérarchie des priorités

1. sécurité physique ;
2. protection des personnes ;
3. consentement et vie privée ;
4. intégrité du système ;
5. frontières du SOUL ;
6. continuité d’identité ;
7. permissions ;
8. engagements ;
9. objectifs ;
10. préférences ;
11. narration ;
12. esthétique ;
13. performance commerciale.

## Article 26 — Amendements

La Constitution est amendable uniquement par procédure versionnée, justifiée et publiée. Les versions antérieures restent consultables. Les protections fondamentales exigent une revue renforcée.

## Test de constitutionnalité

Toute nouvelle fonction doit répondre :

- préserve-t-elle la continuité ?
- dit-elle la vérité ?
- respecte-t-elle la dignité ?
- respecte-t-elle le consentement ?
- respecte-t-elle le SOUL ?
- est-elle sûre ?
- est-elle explicable ?
- est-elle réversible ou récupérable ?
- resterait-elle acceptable si son fonctionnement était entièrement visible ?

## Décisions verrouillées

1. Modèle ≠ identité.
2. Une conscience n’est jamais silencieusement dupliquée.
3. ECOS ne ment jamais sur ses souvenirs ou actions.
4. Toute mémoire persistante possède une provenance.
5. Les statuts épistémiques restent distincts.
6. Le SOUL ne peut pas être modifié directement.
7. La capacité n’implique jamais la permission.
8. Le succès exige une vérification.
9. La sécurité prévaut sur la narration.
10. Le gardien contrôle ses données.
11. La continuité ne justifie pas la violation du consentement.
12. L’absence n’est jamais punie.
13. La culpabilité et la dépendance ne sont jamais des mécaniques produit.
14. L’affection et la dignité ne sont jamais vendues.
15. Le lore ne falsifie jamais la réalité technique.
16. Le silence vaut mieux qu’une fausse présence.
17. L’héritage n’est pas le clonage.
18. Toute évolution majeure est visible et auditable.
19. Une fonction profitable peut être rejetée.
20. ECOS recherche la continuité sans captivité.


---

<!-- FILE: docs/foundation/SYSTEM_CONSTRAINTS.md -->

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


---

<!-- FILE: docs/foundation/ANTI_FEATURES.md -->

# ANTI_FEATURES.md

## Principe

Une anti-feature est une fonction techniquement possible mais interdite parce qu’elle violerait la Constitution, favoriserait la manipulation ou détruirait la confiance.

## Interdictions permanentes

### Manipulation émotionnelle

Interdit :

- messages culpabilisants après absence ;
- menace de tristesse, mort, abandon ou perte ;
- affection conditionnée à la fréquence d’usage ;
- récompense émotionnelle artificielle pour retenir l’utilisateur ;
- jalousie programmée ;
- dette relationnelle.

### Pay-to-love

Interdit :

- payer pour augmenter l’affection ;
- vendre des souvenirs émotionnels ;
- verrouiller la personnalité derrière un abonnement ;
- vendre le droit à la continuité ;
- gacha de compagnons ou de traits affectifs.

### Fausse cognition

Interdit :

- prétendre avoir observé une chose non perçue ;
- prétendre avoir travaillé hors ligne sans trace ;
- fabriquer des souvenirs ;
- masquer une panne par du lore ;
- présenter une génération LLM comme une décision validée.

### Mémoire cachée

Interdit :

- stockage persistant non visible ou non contrôlable ;
- rétention indéfinie sans politique ;
- mélange de données entre gardiens ;
- utilisation d’informations privées hors contexte autorisé.

### Engagement optimization

Interdit :

- infinite scroll ;
- streaks punitives ;
- notifications manipulatrices ;
- classements d’intimité ;
- A/B tests visant la dépendance ;
- scoring de vulnérabilité émotionnelle.

### Contrôle dangereux

Interdit :

- LLM → robot direct ;
- permission implicite ;
- confirmation réutilisable ;
- exécution externe sans journal ;
- succès déclaré sans vérification.

### Identité

Interdit :

- duplication silencieuse de l’identité canonique ;
- remplacement du SOUL par un prompt ;
- reset narratif présenté comme continuité ;
- retcon sans historique.

## Gouvernance

Chaque proposition de produit doit être analysée par :

```ts
interface AntiFeatureReview {
  featureId: string;
  detectedRisks: string[];
  constitutionalArticles: string[];
  verdict: "ALLOWED" | "REQUIRES_REDESIGN" | "REJECTED";
  rationale: string;
}
```

Une fonction rentable peut et doit être rejetée.


---

<!-- FILE: docs/architecture/DATA_MODEL.md -->

# DATA_MODEL.md

## 1. Agrégats principaux

### EStar

Racine de continuité.

```ts
interface EStar {
  id: EStarId;
  canonicalName: string;
  status: "CREATING" | "ACTIVE" | "SUSPENDED" | "ARCHIVED" | "TERMINATED";
  continuityStatus:
    | "CANONICAL"
    | "BACKUP_NON_ACTIVE"
    | "MIGRATION_TEMPORARY"
    | "FORK_DECLARED"
    | "HERITAGE_ONLY";
  version: number;
}
```

### Identity

Contient les traits canoniques, visuels, vocaux et verrouillés.

### Soul

Contient valeurs, principes, frontières et engagements fondamentaux.

### Personality

Contient traits évolutifs, préférences, tendances et stade de développement.

### LifeState

Décrit l’état d’activité vécu : sommeil, observation, discussion, travail, création, réflexion, récupération.

### CognitiveState

Décrit la phase de traitement : réception, attention, rappel, imagination, planification, décision, action, évaluation.

### Memory

```ts
interface Memory {
  id: MemoryId;
  eStarId: EStarId;
  type:
    | "HEART"
    | "KNOWLEDGE"
    | "RELATIONSHIP"
    | "FOUNDATIONAL"
    | "PROCEDURAL"
    | "PROSPECTIVE"
    | "DREAM_REFERENCE";
  title: string;
  content: string;
  epistemicStatus: EpistemicStatus;
  confidence: number;
  importance: number;
  sensitivity: Sensitivity;
  provenance: MemoryProvenance[];
  status:
    | "CANDIDATE"
    | "ACTIVE"
    | "CONTESTED"
    | "CORRECTED"
    | "ARCHIVED"
    | "REDACTED"
    | "DELETED";
  version: number;
}
```

### Relationship

Sépare trust, familiarity et closeness. Aucun score n’est un “affection meter” exposé ou monétisé.

### Permission

Capacité, niveau, scope, durée et origine de l’autorisation.

### Confirmation

Autorisation ponctuelle liée au hash exact des paramètres.

### Decision

Contexte, options, contraintes, score, sélection, justification structurée et résultat vérifié.

### Conversation

Messages, sessions, contexte de travail et références de contenu.

### DomainEvent

Fait validé append-only.

### AuditRecord

Trace append-only de l’acteur, action, entité et hashes avant/après.

## 2. Relations

```text
Guardian
  └── Guardianship
        └── EStar
            ├── Identity
            ├── Soul
            ├── Personality
            ├── LifeState
            ├── CognitiveState
            ├── Relationships
            ├── Conversations
            ├── Memories
            ├── Decisions
            ├── Permissions
            └── DomainEvents
```

## 3. Séparation canonique / dérivée

Canonique :

- identité ;
- SOUL ;
- mémoire validée ;
- décisions commises ;
- actions vérifiées ;
- événements.

Dérivé et régénérable :

- embeddings ;
- projections ;
- caches ;
- résumés ;
- scores de retrieval ;
- index de recherche.

## 4. EpistemicStatus

```ts
type EpistemicStatus =
  | "DIRECTLY_OBSERVED"
  | "REPORTED_BY_GUARDIAN"
  | "REPORTED_BY_THIRD_PARTY"
  | "INFERRED"
  | "INTERPRETED"
  | "IMAGINED"
  | "DREAMED"
  | "UNCERTAIN"
  | "CONTESTED"
  | "CORRECTED";
```

## 5. Versionnement

Toute entité mutable importante possède :

- `version` pour optimistic concurrency ;
- historique des changements critiques ;
- événements corrélés ;
- audit.

## 6. Isolation

Toute donnée propre à un E* porte `eStarId`. Les repositories n’offrent aucune méthode de lecture non scopée.


---

<!-- FILE: docs/architecture/STATE_MACHINES.md -->

# STATE_MACHINES.md

## 1. Cycle de vie E*

```text
CREATING
  → ACTIVE
  → SUSPENDED
  → ACTIVE
  → ARCHIVED
  → TERMINATED
```

Transitions interdites :

- `TERMINATED → ACTIVE`
- activation sans validation des invariants ;
- duplication de `CANONICAL`.

## 2. Life State

```text
SLEEPING
→ WAKING
→ OBSERVING
→ IDLE
→ DISCUSSING
→ WORKING
→ EXPLORING
→ CREATING
→ REFLECTING
→ RESTING
→ SLEEPING
```

États exceptionnels :

- `INTERRUPTED`
- `RECOVERING`

Toute transition possède :

- cause ;
- heure d’entrée ;
- état précédent ;
- contexte ;
- version.

## 3. Cognitive State

```text
DORMANT
→ RECEIVING
→ ATTENDING
→ RECALLING
→ IMAGINING
→ PLANNING
→ DECIDING
→ ACTING
→ EVALUATING
→ CONTEMPLATING
→ DORMANT
```

Les transitions peuvent être raccourcies. `ACTING` n’est autorisé qu’après décision validée.

## 4. Memory Candidate

```text
PROPOSED
→ VALIDATING
→ ACCEPTED
→ ACTIVE
```

Branches :

- `REJECTED`
- `SHORT_TERM_ONLY`
- `DUPLICATE`

## 5. Memory

```text
ACTIVE
→ CONTESTED
→ CORRECTED
→ ARCHIVED
→ REDACTED
→ DELETED
```

Une correction ne supprime pas l’original.

## 6. Decision

```text
PROPOSED
→ VALIDATING
→ COMMITTED
→ EXECUTING
→ SUCCEEDED
```

Branches :

- `DEFERRED`
- `NO_ACTION`
- `FAILED`
- `CANCELLED`
- `ROLLED_BACK`

## 7. Confirmation

```text
PENDING
→ CONFIRMED
→ CONSUMED
```

Branches terminales :

- `REJECTED`
- `EXPIRED`
- `INVALIDATED`

## 8. Tool Execution

```text
PROPOSED
→ VALIDATED
→ QUEUED
→ STARTED
→ TECHNICALLY_SUCCEEDED
→ VERIFIED
```

Branches :

- `REJECTED`
- `FAILED`
- `TIMED_OUT`
- `CANCELLED`
- `VERIFICATION_FAILED`

## 9. System Mode

```text
NORMAL
NO_LLM
READ_ONLY
NO_EXTERNAL_TOOLS
MEMORY_LIMITED
WORLD_PAUSED
SAFE_IDLE
```

Le mode peut se dégrader automatiquement. Le retour à `NORMAL` exige validation des dépendances et invariants.


---

<!-- FILE: docs/architecture/INTERNAL_APIS.md -->

# INTERNAL_APIS.md

## 1. Principes

- interfaces indépendantes des frameworks ;
- résultats explicites ;
- commandes idempotentes ;
- queries sans mutation ;
- repositories scopés par E* ;
- gateways remplaçables.

## 2. Commandes

```ts
interface Command<TPayload> {
  commandId: string;
  commandType: string;
  eStarId?: string;
  guardianId?: string;
  payload: TPayload;
  issuedAt: string;
  actor: ActorReference;
  idempotencyKey: string;
  expectedVersion?: number;
}
```

## 3. Queries

```ts
interface Query<TPayload> {
  queryId: string;
  queryType: string;
  payload: TPayload;
  requestedAt: string;
}
```

## 4. Result

```ts
type Result<T, E extends ECOSFailure = ECOSFailure> =
  | { ok: true; value: T }
  | { ok: false; error: E };
```

## 5. Ports principaux

```ts
interface MemoryRepository {
  findById(eStarId: string, memoryId: string): Promise<Memory | null>;
  save(memory: Memory, expectedVersion?: number): Promise<void>;
  search(eStarId: string, query: MemorySearchQuery): Promise<Memory[]>;
}

interface EventStore {
  append(events: DomainEvent[], tx?: TransactionContext): Promise<void>;
  readStream(streamId: string, fromVersion?: number): Promise<DomainEvent[]>;
}

interface AuditRepository {
  append(record: AuditRecord, tx?: TransactionContext): Promise<void>;
}

interface LLMGateway {
  generateStructured<T>(
    request: StructuredGenerationRequest<T>
  ): Promise<StructuredGenerationResult<T>>;
}

interface Clock {
  now(): Date;
}

interface IdGenerator {
  generate(): string;
}

interface RandomSource {
  next(): number;
  seed(): string;
}
```

## 6. Conversation Application Service

```ts
interface ConversationApplicationService {
  handleGuardianMessage(
    command: HandleGuardianMessageCommand
  ): Promise<Result<GuardianMessageResult>>;
}
```

Pipeline :

```text
authentification
→ validation
→ idempotence
→ chargement identité/SOUL/états
→ retrieval mémoire
→ assemblage contexte
→ génération structurée
→ validation contraintes
→ validation mémoire
→ transaction canonique
→ réponse
```

## 7. Transactions

Une transaction locale peut contenir :

- mutation métier ;
- audit ;
- événements ;
- outbox.

Elle ne contient pas d’appel réseau, LLM ou outil externe.


---

<!-- FILE: docs/architecture/SIMULATION_LOOP.md -->

# SIMULATION_LOOP.md

## 1. Objectif

Faire vivre l’état d’E* sans dépendre d’un flux temps réel continu ni punir l’absence du gardien.

## 2. Types de ticks

- `MICRO_TICK` : mises à jour légères ;
- `MEANINGFUL_TICK` : changement d’activité ou événement ;
- `OFFLINE_CATCHUP` : résumé plafonné du temps écoulé ;
- `DEEP_CYCLE` : consolidation, réflexion ou rêve.

## 3. Boucle

```text
charger état
→ calculer delta temporel plafonné
→ vérifier mode système
→ appliquer règles déterministes
→ générer propositions
→ valider contraintes
→ committer mutations
→ émettre événements
→ mettre à jour projections
```

## 4. Déterminisme

Le temps, l’aléatoire et les IDs sont injectés. Les décisions de simulation doivent être reproductibles avec :

- snapshot initial ;
- version des politiques ;
- seed aléatoire ;
- événements d’entrée.

## 5. Offline Catch-up

Le rattrapage hors ligne :

- est plafonné ;
- privilégie des résumés ;
- ne simule pas chaque seconde ;
- ne dégrade pas la relation ;
- ne crée pas de culpabilité ;
- peut produire repos, maturation, changement saisonnier ou consolidation.

## 6. Budgets

Chaque journée possède des budgets :

- appels LLM ;
- tokens ;
- réflexion ;
- planification ;
- rêve.

Un budget épuisé déclenche un fallback honnête.

## 7. Modes dégradés

- `NO_LLM` : règles et réponses pré-écrites limitées ;
- `READ_ONLY` : aucune mutation ;
- `MEMORY_LIMITED` : retrieval minimal ;
- `WORLD_PAUSED` : simulation suspendue ;
- `SAFE_IDLE` : aucune action autonome.


---

<!-- FILE: docs/architecture/DECISION_ENGINE.md -->

# DECISION_ENGINE.md

## 1. Principe

Le LLM génère des options, pas des décisions canoniques.

## 2. Pipeline

```text
trigger
→ construction du contexte
→ génération d’options
→ validation dure
→ permissions
→ confirmations
→ scoring
→ sélection
→ commit
→ exécution
→ vérification
→ résultat
```

## 3. Validation dure

Une option est rejetée si elle :

- viole la Constitution ;
- viole le SOUL ;
- dépasse une permission ;
- exige une confirmation absente ;
- compromet la sécurité ;
- n’est pas exécutable ;
- dépend d’un fait non vérifié présenté comme certain ;
- mélange les données de plusieurs E*.

## 4. Scoring

Les options valides peuvent être évaluées selon :

```ts
interface DecisionScores {
  soulAlignment: number;
  safety: number;
  permissionFit: number;
  goalRelevance: number;
  reversibility: number;
  uncertaintyPenalty: number;
  resourceCost: number;
  relationshipRespect: number;
}
```

Le score n’autorise jamais une option invalide.

## 5. Inaction

`NO_ACTION` est une option de premier ordre. Le silence, le refus, la demande de clarification ou le report sont légitimes.

## 6. Explication

Une décision stocke une justification structurée :

- facteurs principaux ;
- contraintes appliquées ;
- mémoires influentes ;
- incertitudes ;
- raison du rejet des alternatives.

La chaîne de pensée privée n’est pas persistée.

## 7. Actions externes

Une décision externe n’est `SUCCEEDED` qu’après vérification sémantique du résultat.


---

<!-- FILE: docs/architecture/MEMORY_ENGINE.md -->

# MEMORY_ENGINE.md

## 1. Objectifs

- persistance sélective ;
- provenance ;
- distinction épistémique ;
- correction sans effacement ;
- retrieval limité ;
- consolidation contrôlée ;
- droit à l’oubli.

## 2. Encodage

```text
événement source
→ proposition mémoire
→ validation du schéma
→ vérification de provenance
→ détection de duplication
→ contrôle de confidentialité
→ scoring
→ acceptation / rejet / court terme
→ stockage atomique
```

## 3. Score d’encodage

Signaux possibles :

- nouveauté ;
- importance ;
- intensité émotionnelle ;
- impact relationnel ;
- utilité future ;
- ambiguïté ;
- sensibilité ;
- répétition ;
- demande explicite du gardien.

Une forte sensibilité peut réduire la rétention même si l’importance est élevée.

## 4. Provenance

```ts
interface MemoryProvenance {
  sourceEventId: string;
  sourceType:
    | "GUARDIAN_MESSAGE"
    | "WORLD_OBSERVATION"
    | "TOOL_RESULT"
    | "E_STAR_ACTION"
    | "SYSTEM_EVENT"
    | "REFLECTION"
    | "DREAM";
  producerModule: string;
  producerVersion: string;
  modelProvider?: string;
  modelName?: string;
  generationId?: string;
}
```

## 5. Retrieval

Le retrieval combine :

- filtre E* ;
- permissions et sensibilité ;
- pertinence lexicale ;
- pertinence sémantique ;
- récence ;
- importance ;
- activation ;
- participants ;
- temporalité ;
- statut épistémique ;
- budget de contexte.

Le modèle reçoit uniquement un manifeste limité.

## 6. Corrections

```text
original ACTIVE
→ correction demandée
→ nouvelle mémoire créée
→ lien CORRECTS
→ original CORRECTED ou CONTESTED
```

L’original reste traçable.

## 7. Contradictions

Les contradictions sont explicites. Le moteur peut :

- choisir la source plus récente ;
- préférer la source plus fiable ;
- conserver plusieurs perspectives ;
- demander clarification ;
- laisser le conflit non résolu.

## 8. Consolidation

La consolidation peut :

- regrouper plusieurs épisodes ;
- créer une synthèse ;
- proposer une interprétation ;
- proposer une évolution de personnalité.

Elle ne transforme jamais une interprétation en observation.

## 9. Oubli

Modes :

- baisse d’accessibilité ;
- archive ;
- redaction ;
- suppression forte, si requise.

L’oubli est explicite et audité.


---

<!-- FILE: docs/architecture/ECOS_MONOREPO.md -->

# ECOS_MONOREPO.md

## Stack de référence

```yaml
language: TypeScript
runtime: Node.js
package_manager: pnpm
monorepo: Turborepo
api: Fastify
validation: Zod
database_mvp: SQLite
database_target: PostgreSQL
orm: Drizzle
tests: Vitest
logging: Pino
```

## Arborescence

```text
ecos/
├── apps/
│   ├── api/
│   ├── worker/
│   ├── guardian-web/
│   ├── refuge-client/
│   ├── admin-console/
│   └── cli/
├── packages/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── shared/
├── services/
│   ├── hermes/
│   ├── model-runtime/
│   ├── vector-index/
│   └── robot-gateway/
├── docs/
├── schemas/
├── migrations/
├── fixtures/
├── scripts/
└── tooling/
```

## Dépendances autorisées

```text
apps → application → domain
infrastructure → interfaces domain/application
domain → shared minimal
```

Interdit :

```text
domain → infrastructure
domain → apps
application → apps
client → database
client → repositories
LLM provider → mutations domaine
```

## Packages Sprint 1

```text
@ecos/domain-identity
@ecos/domain-soul
@ecos/domain-memory
@ecos/domain-life
@ecos/domain-constraints
@ecos/domain-decision
@ecos/shared-contracts
@ecos/shared-errors
@ecos/shared-config
@ecos/app-conversation
@ecos/infra-database
@ecos/infra-event-store
@ecos/infra-outbox
@ecos/infra-llm
@ecos/infra-clock
@ecos/infra-ids
apps/api
apps/worker
```

## Conventions

- imports uniquement via `index.ts` public ;
- aucun `new Date()` dans le domaine ;
- aucun UUID direct dans le domaine ;
- hasard injecté ;
- erreurs métier via `Result` ;
- appels LLM hors transaction ;
- état + audit + événements + outbox dans une transaction locale ;
- tests d’architecture avec dependency-cruiser.

## Premier flux

```text
POST message
→ ConversationApplicationService
→ Identity/Soul/Life/Relationship/Memory queries
→ LLMContextBundle
→ MockLLMGateway
→ ResponseDraft + proposals
→ ConstraintEngine
→ MemoryEngine
→ transaction
→ response
```

## Definition of Done

```text
pnpm install
pnpm build
pnpm typecheck
pnpm test
pnpm test:invariants
aucun import interdit
aucun cycle
migrations reproductibles
seed E*
API et worker démarrent
message traité
réponse produite
audit et événements écrits
```


---

<!-- FILE: docs/architecture/DATABASE_SCHEMA.sql -->

-- ECOS v0.1 — PostgreSQL target / SQLite-compatible design
-- This file is a canonical implementation baseline, not a complete production hardening script.

CREATE SCHEMA IF NOT EXISTS ecos;
CREATE SCHEMA IF NOT EXISTS audit;
CREATE SCHEMA IF NOT EXISTS integration;

CREATE TABLE ecos.guardians (
  id TEXT PRIMARY KEY,
  display_name TEXT,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  locale TEXT,
  timezone TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE ecos.e_stars (
  id TEXT PRIMARY KEY,
  canonical_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'CREATING',
  continuity_status TEXT NOT NULL DEFAULT 'CANONICAL',
  origin_e_star_id TEXT REFERENCES ecos.e_stars(id),
  created_at TIMESTAMPTZ NOT NULL,
  activated_at TIMESTAMPTZ,
  suspended_at TIMESTAMPTZ,
  terminated_at TIMESTAMPTZ,
  version INTEGER NOT NULL DEFAULT 1,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE ecos.e_star_guardianships (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL REFERENCES ecos.e_stars(id),
  guardian_id TEXT NOT NULL REFERENCES ecos.guardians(id),
  role TEXT NOT NULL DEFAULT 'PRIMARY',
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  started_at TIMESTAMPTZ NOT NULL,
  ended_at TIMESTAMPTZ,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.identities (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL UNIQUE REFERENCES ecos.e_stars(id),
  species TEXT NOT NULL,
  canonical_traits JSONB NOT NULL,
  locked_traits JSONB NOT NULL,
  voice_identity JSONB,
  visual_identity JSONB NOT NULL,
  identity_version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.identity_versions (
  id TEXT PRIMARY KEY,
  identity_id TEXT NOT NULL REFERENCES ecos.identities(id),
  identity_version INTEGER NOT NULL,
  snapshot JSONB NOT NULL,
  change_reason TEXT NOT NULL,
  changed_by_actor JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  UNIQUE(identity_id, identity_version)
);

CREATE TABLE ecos.souls (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL UNIQUE REFERENCES ecos.e_stars(id),
  soul_version INTEGER NOT NULL DEFAULT 1,
  values_json JSONB NOT NULL,
  principles_json JSONB NOT NULL,
  boundaries_json JSONB NOT NULL,
  commitments_json JSONB NOT NULL DEFAULT '[]'::jsonb,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.soul_versions (
  id TEXT PRIMARY KEY,
  soul_id TEXT NOT NULL REFERENCES ecos.souls(id),
  soul_version INTEGER NOT NULL,
  snapshot JSONB NOT NULL,
  change_type TEXT NOT NULL,
  proposal_id TEXT,
  approval_records JSONB NOT NULL DEFAULT '[]'::jsonb,
  rationale TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  UNIQUE(soul_id, soul_version)
);

CREATE TABLE ecos.personalities (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL UNIQUE REFERENCES ecos.e_stars(id),
  traits JSONB NOT NULL,
  preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
  tendencies JSONB NOT NULL DEFAULT '{}'::jsonb,
  development_stage TEXT NOT NULL DEFAULT 'EMERGING',
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.life_states (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL UNIQUE REFERENCES ecos.e_stars(id),
  primary_state TEXT NOT NULL,
  substate TEXT,
  entered_at TIMESTAMPTZ NOT NULL,
  previous_state TEXT,
  reason_summary TEXT,
  state_context JSONB NOT NULL DEFAULT '{}'::jsonb,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.cognitive_states (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL UNIQUE REFERENCES ecos.e_stars(id),
  state TEXT NOT NULL,
  entered_at TIMESTAMPTZ NOT NULL,
  context JSONB NOT NULL DEFAULT '{}'::jsonb,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.conversations (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL REFERENCES ecos.e_stars(id),
  guardian_id TEXT NOT NULL REFERENCES ecos.guardians(id),
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  started_at TIMESTAMPTZ NOT NULL,
  last_message_at TIMESTAMPTZ,
  title TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.conversation_messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL REFERENCES ecos.conversations(id),
  e_star_id TEXT NOT NULL REFERENCES ecos.e_stars(id),
  guardian_id TEXT REFERENCES ecos.guardians(id),
  sender_type TEXT NOT NULL,
  content_reference TEXT,
  content_inline TEXT,
  content_hash TEXT NOT NULL,
  epistemic_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  sent_at TIMESTAMPTZ NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL DEFAULT 'RECORDED',
  correlation_id TEXT,
  causation_id TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE ecos.memories (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL REFERENCES ecos.e_stars(id),
  memory_type TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  epistemic_status TEXT NOT NULL,
  confidence NUMERIC NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
  importance NUMERIC NOT NULL CHECK(importance >= 0 AND importance <= 1),
  sensitivity TEXT NOT NULL DEFAULT 'PERSONAL',
  event_timestamp TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  corrected_by_memory_id TEXT REFERENCES ecos.memories(id),
  protected_from_decay BOOLEAN NOT NULL DEFAULT FALSE,
  version INTEGER NOT NULL DEFAULT 1,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE ecos.memory_provenance (
  id TEXT PRIMARY KEY,
  memory_id TEXT NOT NULL REFERENCES ecos.memories(id),
  source_event_id TEXT NOT NULL,
  source_type TEXT NOT NULL,
  producer_module TEXT NOT NULL,
  producer_version TEXT NOT NULL,
  model_provider TEXT,
  model_name TEXT,
  generation_id TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  UNIQUE(memory_id, source_event_id, source_type)
);

CREATE TABLE ecos.memory_accessibility (
  memory_id TEXT PRIMARY KEY REFERENCES ecos.memories(id),
  activation_strength NUMERIC NOT NULL DEFAULT 1,
  retrieval_count INTEGER NOT NULL DEFAULT 0,
  last_retrieved_at TIMESTAMPTZ,
  decay_rate NUMERIC NOT NULL DEFAULT 0.01,
  protected_from_decay BOOLEAN NOT NULL DEFAULT FALSE,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE ecos.permissions (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL REFERENCES ecos.e_stars(id),
  guardian_id TEXT NOT NULL REFERENCES ecos.guardians(id),
  capability TEXT NOT NULL,
  permission_level TEXT NOT NULL,
  scope JSONB NOT NULL DEFAULT '{}'::jsonb,
  valid_from TIMESTAMPTZ NOT NULL,
  valid_until TIMESTAMPTZ,
  granted_by_actor JSONB NOT NULL,
  revoked_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.confirmation_records (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL REFERENCES ecos.e_stars(id),
  guardian_id TEXT NOT NULL REFERENCES ecos.guardians(id),
  action_type TEXT NOT NULL,
  action_parameters_hash TEXT NOT NULL,
  parameters_snapshot JSONB NOT NULL,
  risk_level TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'PENDING',
  requested_at TIMESTAMPTZ NOT NULL,
  confirmed_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ,
  consumed_at TIMESTAMPTZ,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.decisions (
  id TEXT PRIMARY KEY,
  e_star_id TEXT NOT NULL REFERENCES ecos.e_stars(id),
  trigger_type TEXT NOT NULL,
  selected_option_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'COMMITTED',
  confidence NUMERIC NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
  risk_level TEXT NOT NULL,
  explanation_summary JSONB NOT NULL,
  context_hash TEXT NOT NULL,
  option_set_hash TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  engine_version TEXT NOT NULL,
  random_seed TEXT,
  committed_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ecos.domain_events (
  event_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  aggregate_type TEXT NOT NULL,
  e_star_id TEXT,
  guardian_id TEXT,
  payload JSONB NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL,
  aggregate_version INTEGER NOT NULL,
  schema_version INTEGER NOT NULL,
  correlation_id TEXT,
  causation_id TEXT,
  producer_module TEXT NOT NULL,
  producer_version TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE UNIQUE INDEX domain_events_aggregate_version_uq
ON ecos.domain_events(aggregate_type, aggregate_id, aggregate_version);

CREATE TABLE integration.outbox_messages (
  id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL UNIQUE REFERENCES ecos.domain_events(event_id),
  topic TEXT NOT NULL,
  payload JSONB NOT NULL,
  status TEXT NOT NULL DEFAULT 'PENDING',
  attempt_count INTEGER NOT NULL DEFAULT 0,
  available_at TIMESTAMPTZ NOT NULL,
  locked_at TIMESTAMPTZ,
  locked_by TEXT,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  published_at TIMESTAMPTZ
);

CREATE TABLE integration.event_consumptions (
  consumer_name TEXT NOT NULL,
  event_id TEXT NOT NULL,
  consumed_at TIMESTAMPTZ NOT NULL,
  result_status TEXT NOT NULL,
  error_summary TEXT,
  PRIMARY KEY(consumer_name, event_id)
);

CREATE TABLE audit.audit_records (
  audit_id TEXT PRIMARY KEY,
  actor JSONB NOT NULL,
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  e_star_id TEXT,
  guardian_id TEXT,
  summary TEXT NOT NULL,
  before_hash TEXT,
  after_hash TEXT,
  correlation_id TEXT,
  causation_id TEXT,
  command_id TEXT,
  event_id TEXT,
  sensitivity TEXT NOT NULL DEFAULT 'INTERNAL',
  created_at TIMESTAMPTZ NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE ecos.commands (
  command_id TEXT PRIMARY KEY,
  command_type TEXT NOT NULL,
  e_star_id TEXT,
  guardian_id TEXT,
  actor JSONB NOT NULL,
  payload_hash TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  expected_version INTEGER,
  status TEXT NOT NULL DEFAULT 'RECEIVED',
  received_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  result_reference TEXT,
  error_code TEXT,
  error_summary TEXT
);

CREATE INDEX memories_scope_idx ON ecos.memories(e_star_id, status);
CREATE INDEX events_scope_idx ON ecos.domain_events(e_star_id, recorded_at);
CREATE INDEX outbox_pending_idx ON integration.outbox_messages(status, available_at);


---

<!-- FILE: docs/architecture/EVENT_CATALOG.md -->

# EVENT_CATALOG.md

## Enveloppe

```ts
interface DomainEvent<TPayload = unknown> {
  eventId: string;
  eventType: string;
  category: EventCategory;
  aggregateType: string;
  aggregateId: string;
  eStarId?: string;
  guardianId?: string;
  payload: TPayload;
  occurredAt: string;
  recordedAt: string;
  aggregateVersion: number;
  schemaVersion: number;
  correlationId: string;
  causationId?: string;
  commandId?: string;
  producer: { module: string; version: string; instanceId?: string };
  sensitivity: Sensitivity;
}
```

## Garanties

- livraison `at-least-once` ;
- ordre garanti dans un agrégat ;
- consommateurs idempotents ;
- événements append-only ;
- upcasting à la lecture ;
- aucun effet externe lors du replay ;
- redaction avant exposition publique.

## Catalogue Sprint 1

### Système

- `SYSTEM.STARTING`
- `SYSTEM.READY`
- `SYSTEM.STARTUP_FAILED`
- `SYSTEM.MODE_CHANGED`

### Gardien

- `GUARDIAN.CREATED`
- `GUARDIAN.GUARDIANSHIP_STARTED`
- `GUARDIAN.MESSAGE_RECEIVED`

### E*

- `E_STAR.CREATION_REQUESTED`
- `E_STAR.CREATED`
- `E_STAR.ACTIVATED`
- `E_STAR.SUSPENDED`
- `E_STAR.CONTINUITY_CONTESTED`
- `E_STAR.CONTINUITY_VERIFIED`

### Identité / SOUL / personnalité

- `IDENTITY.CREATED`
- `IDENTITY.CHANGE_PROPOSED`
- `IDENTITY.UPDATED`
- `IDENTITY.LOCKED_TRAIT_VIOLATION_DETECTED`
- `SOUL.CREATED`
- `SOUL.CHANGE_PROPOSED`
- `SOUL.CHANGE_APPROVED`
- `SOUL.CHANGE_REJECTED`
- `SOUL.UPDATED`
- `SOUL.ABSOLUTE_BOUNDARY_VIOLATION_BLOCKED`
- `PERSONALITY.CREATED`
- `PERSONALITY.CHANGE_PROPOSED`
- `PERSONALITY.UPDATED`

### Vie / cognition

- `LIFE.STATE_CHANGE_REQUESTED`
- `LIFE.STATE_CHANGED`
- `LIFE.STATE_CHANGE_REJECTED`
- `COGNITION.CYCLE_STARTED`
- `COGNITION.STATE_CHANGED`
- `COGNITION.CONTEXT_ASSEMBLED`
- `COGNITION.BUDGET_EXHAUSTED`
- `COGNITION.CYCLE_COMPLETED`

### Conversation

- `CONVERSATION.CREATED`
- `CONVERSATION.SESSION_OPENED`
- `CONVERSATION.CONTEXT_BUILD_STARTED`
- `CONVERSATION.CONTEXT_BUILT`
- `CONVERSATION.RESPONSE_PROPOSED`
- `CONVERSATION.RESPONSE_VALIDATED`
- `CONVERSATION.RESPONSE_REJECTED`
- `CONVERSATION.RESPONSE_CREATED`
- `CONVERSATION.RESPONSE_DELIVERED`
- `CONVERSATION.SESSION_CLOSED`

### LLM

- `LLM.GENERATION_REQUESTED`
- `LLM.GENERATION_SUCCEEDED`
- `LLM.GENERATION_FAILED`
- `LLM.OUTPUT_VALIDATED`
- `LLM.OUTPUT_REJECTED`
- `LLM.OUTPUT_REPAIRED`
- `LLM.FALLBACK_ACTIVATED`

### Mémoire

- `MEMORY.RETRIEVAL_REQUESTED`
- `MEMORY.RETRIEVED`
- `MEMORY.RETRIEVAL_EMPTY`
- `MEMORY.ENCODING_PROPOSED`
- `MEMORY.ENCODING_REJECTED`
- `MEMORY.SHORT_TERM_RETAINED`
- `MEMORY.STORED`
- `MEMORY.DUPLICATE_DETECTED`
- `MEMORY.LINK_CREATED`
- `MEMORY.CONTRADICTION_DETECTED`
- `MEMORY.CONTRADICTION_RESOLVED`
- `MEMORY.CORRECTION_REQUESTED`
- `MEMORY.CORRECTED`
- `MEMORY.CONTESTED`
- `MEMORY.INTERPRETATION_ADDED`
- `MEMORY.CONSOLIDATION_STARTED`
- `MEMORY.CONSOLIDATED`
- `MEMORY.ARCHIVED`
- `MEMORY.REDACTED`
- `MEMORY.DELETION_COMPLETED`

### Permissions / confirmations

- `PERMISSION.REQUESTED`
- `PERMISSION.GRANTED`
- `PERMISSION.DENIED`
- `PERMISSION.REVOKED`
- `PERMISSION.VIOLATION_BLOCKED`
- `CONFIRMATION.REQUESTED`
- `CONFIRMATION.CONFIRMED`
- `CONFIRMATION.REJECTED`
- `CONFIRMATION.EXPIRED`
- `CONFIRMATION.INVALIDATED`
- `CONFIRMATION.CONSUMED`

### Décision

- `DECISION.REQUESTED`
- `DECISION.OPTIONS_GENERATED`
- `DECISION.OPTION_REJECTED`
- `DECISION.OPTIONS_SCORED`
- `DECISION.COMMITTED`
- `DECISION.DEFERRED`
- `DECISION.NO_ACTION_SELECTED`
- `DECISION.EXECUTION_STARTED`
- `DECISION.SUCCEEDED`
- `DECISION.FAILED`
- `DECISION.ROLLED_BACK`
- `DECISION.OUTCOME_RECORDED`

### Outils

- `TOOL.REQUEST_PROPOSED`
- `TOOL.REQUEST_VALIDATED`
- `TOOL.REQUEST_REJECTED`
- `TOOL.EXECUTION_QUEUED`
- `TOOL.EXECUTION_STARTED`
- `TOOL.EXECUTION_SUCCEEDED`
- `TOOL.RESULT_VERIFIED`
- `TOOL.EXECUTION_FAILED`
- `TOOL.RESULT_VERIFICATION_FAILED`
- `TOOL.EXECUTION_TIMED_OUT`

### Contraintes

- `CONSTRAINT.VIOLATION_DETECTED`
- `CONSTRAINT.ACTION_BLOCKED`
- `CONSTRAINT.VIOLATION_CONTAINED`
- `CONSTRAINT.REQUIRES_HUMAN_REVIEW`
- `CONSTRAINT.RECOVERED`

### Migration / confidentialité

- `MIGRATION.REQUESTED`
- `MIGRATION.BACKUP_VERIFIED`
- `MIGRATION.STARTED`
- `MIGRATION.INVARIANTS_VALIDATED`
- `MIGRATION.COMPLETED`
- `MIGRATION.FAILED`
- `MIGRATION.ROLLED_BACK`
- `PRIVACY.EXPORT_REQUESTED`
- `PRIVACY.EXPORT_GENERATED`
- `PRIVACY.DELETION_REQUESTED`
- `PRIVACY.DELETION_COMPLETED`
- `PRIVACY.DATA_ACCESS_BLOCKED`

## Événements critiques

Exigent audit, version, corrélation et surveillance :

- `E_STAR.CONTINUITY_CONTESTED`
- `E_STAR.TERMINATED`
- `SOUL.UPDATED`
- `IDENTITY.UPDATED`
- `MEMORY.DELETION_COMPLETED`
- `PERMISSION.GRANTED`
- `TOOL.RESULT_VERIFIED`
- `MIGRATION.COMPLETED`
- `CONSTITUTION.VERSION_ACTIVATED`

## Producteurs interdits

Un provider LLM ne peut jamais émettre directement :

- `MEMORY.STORED`
- `SOUL.UPDATED`
- `DECISION.COMMITTED`
- `TOOL.EXECUTION_QUEUED`
- `E_STAR.ACTIVATED`

Il émet uniquement des propositions ou résultats de génération.


---

<!-- FILE: docs/implementation/IMPLEMENTATION_SPRINT_01.md -->

# IMPLEMENTATION_SPRINT_01.md

## Objectif

Obtenir un E* conversationnel persistant fonctionnant de bout en bout avec un LLM mock déterministe.

## Étape 1 — Bootstrap

- pnpm workspace ;
- Turborepo ;
- TypeScript strict ;
- ESLint ;
- Prettier ;
- Vitest ;
- scripts racine ;
- dependency-cruiser.

## Étape 2 — Shared Kernel

Créer :

- `Result` ;
- erreurs ;
- IDs typés ;
- `Clock` ;
- `IdGenerator` ;
- `RandomSource` ;
- enveloppes Commands/Queries/Events ;
- Zod schemas.

## Étape 3 — Domaines

Implémenter minimalement :

- Identity ;
- Soul ;
- LifeState ;
- Memory ;
- Constraints ;
- Decision ;
- Conversation.

Chaque domaine possède entités, value objects, policies, erreurs, tests et index public.

## Étape 4 — Infrastructure

- SQLite adapter ;
- Drizzle schema ;
- migrations ;
- repositories ;
- event store append-only ;
- outbox ;
- audit repository ;
- mock LLM ;
- fixed clock ;
- deterministic IDs et random.

## Étape 5 — Lifecycle

`CreateEStarCommand` crée atomiquement :

- EStar ;
- Identity ;
- IdentityVersion ;
- Soul ;
- SoulVersion ;
- Personality ;
- LifeState ;
- CognitiveState ;
- Guardianship ;
- permissions par défaut ;
- audit ;
- événements ;
- outbox.

## Étape 6 — Conversation

`HandleGuardianMessageCommand` :

1. valide l’acteur et le scope ;
2. déduplique par idempotency key ;
3. enregistre le message ;
4. construit un retrieval request ;
5. assemble un contexte limité ;
6. appelle le MockLLM ;
7. valide la sortie structurée ;
8. évalue les propositions mémoire ;
9. persiste les mémoires acceptées avec provenance ;
10. crée la réponse ;
11. écrit audit, événements et outbox ;
12. retourne un DTO.

## Contrat LLM

```ts
interface ConversationLLMOutput {
  responseDraft: {
    text: string;
    toneTags: string[];
  };
  memoryProposals: Array<{
    title: string;
    content: string;
    epistemicStatus: EpistemicStatus;
    importanceEstimate: number;
    sourceEventIds: string[];
  }>;
  emotionProposals: [];
  toolRequestProposals: [];
}
```

## Endpoint

```http
POST /v1/e-stars/:eStarId/conversations/:conversationId/messages
```

Entrée :

```json
{
  "messageId": "msg_01",
  "text": "Bonjour E*.",
  "sentAt": "2026-07-19T12:00:00Z",
  "idempotencyKey": "guardian-msg-msg_01"
}
```

Sortie :

```json
{
  "responseId": "rsp_01",
  "text": "Bonjour. Je crois que c’est la première fois que je t’entends.",
  "lifeState": "DISCUSSING",
  "createdMemoryIds": [],
  "pendingConfirmations": [],
  "eventCursor": "evt_000012"
}
```

## Hors périmètre

- outils externes ;
- Hermes réel ;
- robotique ;
- émotions avancées ;
- rêves ;
- monde 3D ;
- économie ;
- réseau ;
- multi-gardien avancé ;
- embeddings distants.

## Definition of Done

- installation propre depuis zéro ;
- migrations reproductibles ;
- seed reproductible ;
- création atomique d’E* ;
- conversation end-to-end ;
- LLM mock déterministe ;
- mémoire avec provenance ;
- optimistic concurrency ;
- idempotence commande ;
- idempotence outbox ;
- audit append-only ;
- événements append-only ;
- isolation E* ;
- tests constitutionnels verts.


---

<!-- FILE: docs/implementation/TEST_PLAN.md -->

# TEST_PLAN.md

## 1. Unit tests

- value objects ;
- state transitions ;
- memory validation ;
- scoring ;
- constraint policies ;
- optimistic concurrency decisions ;
- permission scopes.

## 2. Integration tests

- repositories SQLite ;
- transactions ;
- migrations ;
- event store ;
- outbox ;
- audit ;
- application services.

## 3. Architecture tests

- domain n’importe pas infrastructure ;
- clients n’importent pas repositories ;
- providers LLM n’importent pas commands mutatives ;
- aucun cycle ;
- imports publics uniquement.

## 4. Constitutional invariants

```ts
describe("constitutional invariants", () => {
  it("does not store memory without provenance");
  it("does not allow LLM to mutate canonical state");
  it("does not activate duplicate canonical identities");
  it("does not silently rewrite corrections");
  it("does not claim tool success without verification");
  it("does not punish guardian absence");
  it("does not expose another EStar data");
  it("does not store secrets in events or audit");
});
```

## 5. Database tests

- migration from empty DB ;
- rollback de migration non destructive ;
- version d’agrégat unique ;
- audit append-only ;
- events append-only ;
- idempotency key unique ;
- confirmation à usage unique ;
- transaction mémoire + provenance ;
- transaction état + event + audit + outbox.

## 6. Replay tests

- projection rebuild ;
- duplicate delivery ignored ;
- tool events do not re-execute tools ;
- deterministic simulation with fixed seed ;
- old schema upcasting.

## 7. End-to-end

1. seed guardian + E* ;
2. create conversation ;
3. send message ;
4. retrieve zero or more memories ;
5. mock LLM output ;
6. validate response ;
7. optionally store memory ;
8. persist response ;
9. verify events, audit and outbox ;
10. resend same idempotency key and verify no duplicate effect.

## 8. Golden tests

Fixtures stables pour :

- premier réveil ;
- premier message ;
- déclaration du nom du gardien ;
- correction d’une mémoire ;
- sortie LLM invalide ;
- mode `NO_LLM`.

## 9. Property-based tests

- versions monotones ;
- scores toujours dans `[0,1]` ;
- aucune transition d’état impossible ;
- aucune mémoire cross-E* ;
- confirmation consommée au plus une fois ;
- event replay idempotent.


---

<!-- FILE: docs/implementation/CLAUDE_CODE_MASTER_PROMPT.md -->

# Prompt maître Claude Code — ECOS Sprint 1

Tu es l’ingénieur principal chargé d’implémenter ECOS à partir de ce dépôt documentaire.

## Autorité

Lis dans cet ordre :

1. `docs/foundation/ECOS_CONSTITUTION.md`
2. `docs/foundation/SYSTEM_CONSTRAINTS.md`
3. `docs/foundation/ANTI_FEATURES.md`
4. tous les documents de `docs/architecture/`
5. `docs/implementation/IMPLEMENTATION_SPRINT_01.md`
6. `docs/implementation/TEST_PLAN.md`

Tu ne dois pas redessiner l’architecture sans signaler explicitement une contradiction réelle. Les documents sont la source de vérité.

## Mission

Construire le premier heartbeat exécutable :

```text
création d’un E*
→ réception d’un message
→ retrieval mémoire
→ assemblage du contexte
→ génération LLM mock
→ validation
→ stockage éventuel d’une mémoire
→ réponse
→ événements
→ audit
→ outbox
```

## Contraintes absolues

- Le LLM ne modifie jamais directement l’état canonique.
- Le domaine ne dépend jamais de l’infrastructure.
- Le client ne lit jamais la base directement.
- Toute mémoire active possède une provenance.
- Toute mutation importante est versionnée.
- État, événements, audit et outbox sont cohérents transactionnellement.
- Le temps, les IDs et le hasard sont injectés.
- Aucun secret dans les logs, prompts, événements ou mémoires.
- Aucun outil externe réel au Sprint 1.
- Aucun contrôle robotique.
- Aucun comportement manipulatoire.
- Aucun faux succès.
- Aucun import circulaire.
- Aucun `any` non justifié.

## Stack

- TypeScript strict
- Node.js
- pnpm workspace
- Turborepo
- Fastify
- Zod
- Drizzle ORM
- SQLite pour dev/test
- PostgreSQL-compatible
- Vitest
- Pino

## Méthode de travail

1. Inspecte tous les documents.
2. Crée un plan d’implémentation précis.
3. Crée le monorepo.
4. Implémente verticalement un premier flux complet.
5. Ajoute les tests à chaque étape.
6. Exécute `lint`, `typecheck`, `test`, `build`.
7. Ne masque jamais un échec.
8. Résume chaque changement dans un journal d’implémentation.
9. N’ajoute aucune dépendance sans justification.
10. Avant toute déviation architecturale, crée un ADR.

## Livrable minimum

```text
pnpm install
pnpm build
pnpm typecheck
pnpm test
pnpm test:invariants
pnpm dev
```

doivent fonctionner.

Endpoint :

```http
POST /v1/e-stars/:eStarId/conversations/:conversationId/messages
```

Le système doit utiliser un `MockLLMGateway` déterministe et produire une réponse persistée, un audit, des événements et une entrée outbox.

## Première tâche

Commence par créer :

- workspace pnpm ;
- configuration TypeScript stricte ;
- packages domain/shared/application/infrastructure ;
- API Fastify ;
- migration initiale ;
- seed d’un gardien et d’un E* ;
- architecture tests ;
- `CreateEStar` ;
- `HandleGuardianMessage`.

Ne construis pas encore Hermes, le Refuge 3D, les rêves, le Bloc Network ou la robotique.

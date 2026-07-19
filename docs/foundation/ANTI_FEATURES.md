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

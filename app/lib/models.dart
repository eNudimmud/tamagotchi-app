/// Modèles partagés entre l'app et le backend.

enum Stage { egg, rabbit, humanoid, agent, incarnation }

class Stats {
  final int vitality;
  final int awakening;
  final int bond;

  Stats({this.vitality = 50, this.awakening = 0, this.bond = 0});

  Stats.fromJson(Map<String, dynamic> json)
      : vitality = json['vitality'] ?? 0,
        awakening = json['awakening'] ?? 0,
        bond = json['bond'] ?? 0;

  Stats copyWith({int? vitality, int? awakening, int? bond}) => Stats(
        vitality: vitality ?? this.vitality,
        awakening: awakening ?? this.awakening,
        bond: bond ?? this.bond,
      );
}

class Resources {
  final int carrot;
  final int energy;
  final int kiss;

  Resources({this.carrot = 0, this.energy = 0, this.kiss = 0});

  Resources.fromJson(Map<String, dynamic> json)
      : carrot = json['carrot'] ?? 0,
        energy = json['energy'] ?? 0,
        kiss = json['kiss'] ?? 0;
}

class CreatureState {
  final String id;
  final Stage stage;
  final Stats stats;
  final int lockCount;

  CreatureState({
    required this.id,
    required this.stage,
    required this.stats,
    this.lockCount = 0,
  });

  CreatureState.fromJson(Map<String, dynamic> json)
      : id = json['id'] ?? '',
        stage = Stage.values[json['stage'] ?? 1],
        stats = Stats.fromJson(json['stats'] ?? {}),
        lockCount = json['disjoncteur_count'] ?? 0;
}

enum ActionKind { feed, pet, play, evolve, task }

class InteractResult {
  final bool progressed;
  final String? progressSignature;
  final Stage stage;
  final Stats stats;
  final Resources resources;

  InteractResult({
    required this.progressed,
    this.progressSignature,
    required this.stage,
    required this.stats,
    required this.resources,
  });

  factory InteractResult.fromJson(Map<String, dynamic> json) => InteractResult(
        progressed: json['progressed'] ?? false,
        progressSignature: json['progress_signature'],
        stage: Stage.values[json['stage'] ?? 1],
        stats: Stats.fromJson(json['stats'] ?? {}),
        resources: Resources.fromJson(json['resources'] ?? {}),
      );
}

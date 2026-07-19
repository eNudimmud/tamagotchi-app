/// Modèles partagés entre l'app et le backend ENKI Tamagotchi v2.

enum Stage { egg, rabbit, apprentice, gardener, guardian }

extension StageName on Stage {
  String get label {
    switch (this) {
      case Stage.egg:
        return 'Egg';
      case Stage.rabbit:
        return 'Rabbit';
      case Stage.apprentice:
        return 'Apprentice';
      case Stage.gardener:
        return 'Gardener';
      case Stage.guardian:
        return 'Guardian';
    }
  }
}

class Needs {
  final int hunger;
  final int energy;
  final int hygiene;
  final int social;
  final int fun;

  Needs({this.hunger = 70, this.energy = 70, this.hygiene = 80, this.social = 60, this.fun = 60});

  Needs.fromJson(Map<String, dynamic> json)
      : hunger = json['hunger'] ?? 0,
        energy = json['energy'] ?? 0,
        hygiene = json['hygiene'] ?? 0,
        social = json['social'] ?? 0,
        fun = json['fun'] ?? 0;
}

class Mood {
  final String state;
  final int score;

  Mood({this.state = 'content', this.score = 50});

  Mood.fromJson(Map<String, dynamic> json)
      : state = json['state'] ?? 'content',
        score = json['score'] ?? 0;

  String get label {
    switch (state) {
      case 'happy':
        return 'Joyeux';
      case 'content':
        return 'Paisible';
      case 'hungry':
        return 'Affamé';
      case 'sleepy':
        return 'Sommeil';
      case 'sick':
        return 'Patraque';
      case 'bored':
        return 'Ennuyé';
      case 'sad':
        return 'Morose';
      default:
        return state;
    }
  }
}

class Cycle {
  final bool isDay;
  final String phase;
  final int dayCount;

  Cycle({this.isDay = true, this.phase = 'new', this.dayCount = 0});

  Cycle.fromJson(Map<String, dynamic> json)
      : isDay = json['is_day'] ?? true,
        phase = json['phase'] ?? 'new',
        dayCount = json['day_count'] ?? 0;

  String get phaseLabel {
    const m = {
      'new': 'Nouvelle lune',
      'waxing_crescent': 'Croissant ascendant',
      'first_quarter': 'Premier quartier',
      'waxing_gibbous': 'Gibbeuse ascendante',
      'full': 'Pleine lune',
      'waning_gibbous': 'Gibbeuse descendante',
      'last_quarter': 'Dernier quartier',
      'waning_crescent': 'Croissant descendant',
    };
    return m[phase] ?? phase;
  }
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
  final String name;
  final Stage stage;
  final Needs needs;
  final Mood mood;
  final int vitality;
  final int awakening;
  final int closeness;
  final Resources resources;
  final Cycle cycle;
  final int lockCount;

  CreatureState({
    required this.id,
    required this.name,
    required this.stage,
    required this.needs,
    required this.mood,
    required this.vitality,
    required this.awakening,
    required this.closeness,
    required this.resources,
    required this.cycle,
    this.lockCount = 0,
  });

  CreatureState.fromJson(Map<String, dynamic> json)
      : id = json['id'] ?? '',
        name = json['name'] ?? 'Enki',
        stage = Stage.values[json['stage'] ?? 1],
        needs = Needs.fromJson(json['needs'] ?? {}),
        mood = Mood.fromJson(json['mood'] ?? {}),
        vitality = json['vitality'] ?? 0,
        awakening = json['awakening'] ?? 0,
        closeness = json['closeness'] ?? 0,
        resources = Resources.fromJson(json['resources'] ?? {}),
        cycle = Cycle.fromJson(json['cycle'] ?? {}),
        lockCount = json['disjoncteur_count'] ?? 0;
}

enum ActionKind { feed, pet, play, sleep, clean, train, talk, evolve }

class InteractResult {
  final bool ok;
  final String message;
  final bool progressed;
  final String? progressSignature;
  final Stage stage;
  final Needs needs;
  final Mood mood;
  final int vitality;
  final int awakening;
  final int closeness;
  final Resources resources;

  InteractResult({
    required this.ok,
    this.message = '',
    required this.progressed,
    this.progressSignature,
    required this.stage,
    required this.needs,
    required this.mood,
    required this.vitality,
    required this.awakening,
    required this.closeness,
    required this.resources,
  });

  factory InteractResult.fromJson(Map<String, dynamic> json) => InteractResult(
        ok: json['ok'] ?? true,
        message: json['message'] ?? '',
        progressed: json['progressed'] ?? false,
        progressSignature: json['progress_signature'],
        stage: Stage.values[json['stage'] ?? 1],
        needs: Needs.fromJson(json['needs'] ?? {}),
        mood: Mood.fromJson(json['mood'] ?? {}),
        vitality: json['vitality'] ?? 0,
        awakening: json['awakening'] ?? 0,
        closeness: json['closeness'] ?? 0,
        resources: Resources.fromJson(json['resources'] ?? {}),
      );
}


/// ── Esprit v0.4 (loi ECOS) : conversation & cartes de permission ──────────

class PendingAction {
  final String actionId;
  final String outil;
  final int niveau;
  final String carte;
  final String raison;
  final bool strongRequired;
  final int expire;

  PendingAction.fromJson(Map<String, dynamic> json)
      : actionId = json['action_id'] ?? '',
        outil = json['outil'] ?? '',
        niveau = json['niveau'] ?? 0,
        carte = json['carte'] ?? '',
        raison = json['raison'] ?? '',
        strongRequired = json['strong_required'] ?? false,
        expire = json['expire'] ?? 0;
}

class TalkReply {
  final List<String> reply;
  final PendingAction? pending;
  final List<Map<String, dynamic>> evenements;

  TalkReply.fromJson(Map<String, dynamic> json)
      : reply = (json['reply'] as List? ?? const []).cast<String>(),
        pending = json['pending'] == null
            ? null
            : PendingAction.fromJson(json['pending']),
        evenements = (json['evenements'] as List? ?? const [])
            .cast<Map<String, dynamic>>();
}

class ConfirmResult {
  final int statusCode;
  final String decision;
  final String? evenement;
  final bool verifie;
  final Map<String, dynamic>? sortie;
  final List<String> reply;
  final String? reason;

  ConfirmResult.fromJson(Map<String, dynamic> json, this.statusCode)
      : decision = json['decision'] ?? '',
        evenement = json['evenement'],
        verifie = json['verifie'] ?? false,
        sortie = json['sortie'] as Map<String, dynamic>?,
        reply = (json['reply'] as List? ?? const []).cast<String>(),
        reason = json['reason'];
}

import 'package:flutter/material.dart';
import 'api_service.dart';
import 'iap_service.dart';
import 'models.dart';

class CompanionProvider extends ChangeNotifier {
  final IapService _iap;
  final ApiService _api;

  CompanionProvider(this._api) : _iap = IapService(_api);

  CreatureState? creature;
  Resources resources = Resources();
  bool loading = false;
  String? error;
  bool facingBack = false;

  static const String _userId = 'demo-user';

  ApiService get api => _api;
  String get userId => _userId;

  Future<void> refresh() async {
    loading = true;
    error = null;
    notifyListeners();
    try {
      creature = await _api.getCreature();
      resources = creature!.resources;
    } catch (e) {
      error = 'companion unavailable';
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  Future<void> act(ActionKind kind) async {
    error = null;
    notifyListeners();
    try {
      final result = await _api.interact(_userId, kind);
      if (!result.ok) {
        error = _messageFor(result.message);
        notifyListeners();
        return;
      }
      // reconstruit l'etat a partir du resultat d'interaction
      creature = CreatureState(
        id: creature?.id ?? _userId,
        name: creature?.name ?? 'Enki',
        stage: result.stage,
        needs: result.needs,
        mood: result.mood,
        vitality: result.vitality,
        awakening: result.awakening,
        closeness: result.closeness,
        resources: result.resources,
        cycle: creature?.cycle ?? Cycle(),
      );
      resources = result.resources;
    } catch (e) {
      error = e.toString().replaceFirst('Exception: ', '');
    }
    notifyListeners();
  }

  Future<void> rename(String name) async {
    try {
      await _api.rename(_userId, name);
      if (creature != null) {
        creature = CreatureState(
          id: creature!.id,
          name: name,
          stage: creature!.stage,
          needs: creature!.needs,
          mood: creature!.mood,
          vitality: creature!.vitality,
          awakening: creature!.awakening,
          closeness: creature!.closeness,
          resources: creature!.resources,
          cycle: creature!.cycle,
        );
      }
    } catch (e) {
      error = e.toString().replaceFirst('Exception: ', '');
    }
    notifyListeners();
  }

  void toggleFacing() {
    facingBack = !facingBack;
    notifyListeners();
  }

  Future<void> buyCarrots(int amount) async {
    // Recolte gratuite (ECOS Anti-Features : pas de pay-to-care).
    try {
      resources = await _iap.grantCarrots(_userId, amount);
    } catch (e) {
      error = e.toString().replaceFirst('Exception: ', '');
    }
    notifyListeners();
  }

  String _messageFor(String m) {
    switch (m) {
      case 'no_carrot':
        return 'Plus de carottes. Appuie sur Récolter.';
      case 'max_stage':
        return 'Stade maximal atteint.';
      case 'unknown_action':
        return 'Action inconnue.';
      default:
        return '';
    }
  }
}

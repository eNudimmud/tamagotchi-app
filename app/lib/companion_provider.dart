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

  static const String _userId = 'demo-user';

  Future<void> refresh() async {
    loading = true;
    error = null;
    notifyListeners();
    try {
      creature = await _api.getCreature();
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
      creature = CreatureState(
        id: creature?.id ?? 'companion',
        stage: result.stage,
        stats: result.stats,
        lockCount: creature?.lockCount ?? 0,
      );
      resources = result.resources;
    } catch (e) {
      error = e.toString().replaceFirst('Exception: ', '');
    }
    notifyListeners();
  }

  Future<void> buyCarrots(int amount) async {
    // MVP: reçu simulé. En prod, déclencher l'achat store puis passer le vrai reçu.
    try {
      resources = await _iap.grantCarrots(_userId, 'mock_receipt', amount);
    } catch (e) {
      error = e.toString().replaceFirst('Exception: ', '');
    }
    notifyListeners();
  }
}

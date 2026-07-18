import 'api_service.dart';
import 'models.dart';

/// Couche de ressources du compagnon.
/// ECOS Anti-Features : aucun pay-to-love. Les carottes sont RECOLTEES
/// gratuitement via /grant. Aucune monnaie d'achat conditionnée au soin.
class IapService {
  final ApiService _api;

  IapService(this._api);

  /// Recolte gratuite de carottes (finance l'infra/le rendu via soutien explicite,
  /// jamais l'affection ou la dignite de la creature — Art 19).
  Future<Resources> grantCarrots(String userId, int amount) {
    return _api.grantCarrots(userId: userId, amount: amount);
  }
}

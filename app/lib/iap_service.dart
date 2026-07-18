import 'api_service.dart';
import 'models.dart';

/// Couche d'achat in-app.
/// En MVP : le reçu est envoyé au backend qui crédite les ressources de jeu.
/// Aucune référence à une chaîne ou à un actif numérique ici : les stores
/// voient uniquement des "carrots / energy / kiss" (monnaie de jeu).
class IapService {
  final ApiService _api;

  IapService(this._api);

  /// Appelé après validation du reçu par le store (logique store réelle à brancher ici).
  /// Le backend fait le lien avec la progression de la créature.
  Future<Resources> grantCarrots(String userId, String storeReceipt, int amount) {
    return _api.verifyPurchase(
      userId: userId,
      storeReceipt: storeReceipt,
      carrot: amount,
    );
  }
}

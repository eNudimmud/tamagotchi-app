import 'dart:convert';
import 'package:http/http.dart' as http;
import 'models.dart';

/// Point d'entrée unique vers le backend.
/// Sur Termux, le backend tourne en local : http://10.0.2.2:8000 depuis l'émulateur,
/// ou http://localhost:8000 si l'app tourne aussi sur le tel via Termux.
/// En dev sur machine différente, remplacer par l'IP locale du tel qui héberge le backend.
const String kBaseUrl = String.fromEnvironment(
  'BACKEND_URL',
  defaultValue: 'http://localhost:8000',
);

class ApiService {
  final http.Client _client;

  ApiService([http.Client? client]) : _client = client ?? http.Client();

  Future<CreatureState> getCreature() async {
    final res = await _client.get(Uri.parse('$kBaseUrl/creature'));
    if (res.statusCode != 200) {
      throw Exception('companion unavailable');
    }
    return CreatureState.fromJson(jsonDecode(res.body));
  }

  Future<InteractResult> interact(String userId, ActionKind kind) async {
    final res = await _client.post(
      Uri.parse('$kBaseUrl/interact'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'user_id': userId, 'type': kind.name}),
    );
    if (res.statusCode == 423) {
      throw Exception('companion is resting, try later');
    }
    if (res.statusCode != 200) {
      throw Exception('action not possible right now');
    }
    return InteractResult.fromJson(jsonDecode(res.body));
  }

  Future<Resources> verifyPurchase({
    required String userId,
    required String storeReceipt,
    int carrot = 0,
    int energy = 0,
    int kiss = 0,
  }) async {
    final res = await _client.post(
      Uri.parse('$kBaseUrl/iap/verify'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'store_receipt': storeReceipt,
        'carrot': carrot,
        'energy': energy,
        'kiss': kiss,
      }),
    );
    if (res.statusCode != 200) {
      throw Exception('purchase could not be applied');
    }
    return Resources.fromJson(jsonDecode(res.body));
  }
}

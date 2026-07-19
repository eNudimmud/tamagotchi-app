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

  /// Jeton local du backend (backend/enki_token.txt).
  /// Sur Android, 127.0.0.1 est accessible à toutes les apps : le jeton ferme la porte.
  /// Fourni au build (--dart-define=ENKI_TOKEN=...) ou saisi dans Réglages.
  static String token = const String.fromEnvironment('ENKI_TOKEN', defaultValue: '');

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'X-Enki-Token': token,
      };

  Future<CreatureState> getCreature() async {
    final res =
        await _client.get(Uri.parse('$kBaseUrl/creature'), headers: _headers);
    if (res.statusCode != 200) {
      throw Exception('companion unavailable');
    }
    return CreatureState.fromJson(jsonDecode(res.body));
  }

  Future<InteractResult> interact(String userId, ActionKind kind) async {
    final res = await _client.post(
      Uri.parse('$kBaseUrl/interact'),
      headers: _headers,
      body: jsonEncode({'user_id': userId, 'type': kind.name}),
    );
    if (res.statusCode == 423) {
      throw Exception('companion is resting, try later');
    }
    if (res.statusCode != 200 && res.statusCode != 409) {
      throw Exception('action not possible right now');
    }
    return InteractResult.fromJson(jsonDecode(res.body));
  }

  Future<Resources> grantCarrots({
    required String userId,
    int amount = 5,
  }) async {
    // Recolte GRATUITE (ECOS Anti-Features : aucun pay-to-care).
    final res = await _client.post(
      Uri.parse('$kBaseUrl/grant'),
      headers: _headers,
      body: jsonEncode({'user_id': userId, 'amount': amount}),
    );
    if (res.statusCode != 200) {
      throw Exception('recolte impossible');
    }
    return Resources.fromJson(jsonDecode(res.body));
  }

  /// Un tour de conversation : l'esprit répond et peut PROPOSER une action.
  /// Rien n'est exécuté ici — l'exécution attend confirm() (loi ECOS, Art. 14).
  Future<TalkReply> talk(String userId, String text) async {
    final res = await _client.post(
      Uri.parse('$kBaseUrl/talk'),
      headers: _headers,
      body: jsonEncode({'user_id': userId, 'text': text}),
    );
    if (res.statusCode != 200) {
      throw Exception('conversation impossible (${res.statusCode})');
    }
    return TalkReply.fromJson(jsonDecode(res.body));
  }

  /// Réponse du gardien à une carte de permission. Usage unique, expirable.
  Future<ConfirmResult> confirm(String userId, String actionId, bool approve,
      {bool strong = false}) async {
    final res = await _client.post(
      Uri.parse('$kBaseUrl/confirm'),
      headers: _headers,
      body: jsonEncode({
        'user_id': userId,
        'action_id': actionId,
        'approve': approve,
        'strong': strong,
      }),
    );
    return ConfirmResult.fromJson(jsonDecode(res.body), res.statusCode);
  }

  Future<Map<String, dynamic>> rename(String userId, String name) async {
    final res = await _client.post(
      Uri.parse('$kBaseUrl/rename'),
      headers: _headers,
      body: jsonEncode({'user_id': userId, 'name': name}),
    );
    if (res.statusCode != 200) {
      throw Exception('rename failed');
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }
}

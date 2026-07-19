import 'package:flutter/material.dart';
import 'api_service.dart';
import 'models.dart';

/// Ecran Reglages : nom du compagnon, pronoms, notifications, theme.
/// MVP : reflete l'etat local ; le backend ne persiste pas encore ces champs
/// (hors nom via /rename).
class SettingsScreen extends StatelessWidget {
  final CreatureState? creature;
  final void Function(String) onRename;
  const SettingsScreen({this.creature, required this.onRename, super.key});

  @override
  Widget build(BuildContext context) {
    final nameCtrl = TextEditingController(text: creature?.name ?? 'Enki');
    return Scaffold(
      appBar: AppBar(title: const Text('Réglages')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            controller: nameCtrl,
            maxLength: 24,
            decoration: const InputDecoration(
              labelText: 'Nom du compagnon',
              border: OutlineInputBorder(),
            ),
          ),
          ElevatedButton.icon(
            onPressed: () => onRename(nameCtrl.text.trim()),
            icon: const Icon(Icons.save),
            label: const Text('Enregistrer le nom'),
          ),
          const Divider(height: 28),
          TextField(
            controller: TextEditingController(text: ApiService.token),
            obscureText: true,
            onChanged: (v) => ApiService.token = v.trim(),
            decoration: const InputDecoration(
              labelText: 'Jeton local (X-Enki-Token)',
              helperText:
                  'Affiché au démarrage du backend (backend/enki_token.txt). '
                  'Ferme l\'API locale aux autres apps du téléphone.',
              border: OutlineInputBorder(),
            ),
          ),
          const Divider(height: 28),
          SwitchListTile(
            title: const Text('Notifications'),
            subtitle: const Text('Rappels si le compagnon décline'),
            value: true,
            onChanged: (_) {},
          ),
          ListTile(
            title: const Text('Thème'),
            subtitle: const Text('Clair (ENKI crème / vert)'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          ListTile(
            title: const Text('Pronoms'),
            subtitle: const Text('Non défini'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          const Divider(height: 28),
          const ListTile(
            title: Text('À propos'),
            subtitle: Text('E*NKI Tamagotchi — compagnon souverain'),
          ),
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'models.dart';

/// Ecran Jardin : relie les besoins du compagnon a la lune et au temps.
/// MVP : affiche la phase lunaire courante et une grille de plantations
/// symboliques (pas encore reliees au backend de culture).
class GardenScreen extends StatelessWidget {
  final Cycle? cycle;
  const GardenScreen({this.cycle, super.key});

  @override
  Widget build(BuildContext context) {
    final phase = cycle?.phaseLabel ?? 'Nouvelle lune';
    final isDay = cycle?.isDay ?? true;
    return Scaffold(
      appBar: AppBar(title: const Text('Jardin')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    Icon(
                      isDay ? Icons.wb_sunny : Icons.nights_stay,
                      size: 40,
                      color: isDay ? Colors.amber : Colors.indigo,
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(phase, style: Theme.of(context).textTheme.titleLarge),
                          Text('Jour ${cycle?.dayCount ?? 0} · ${isDay ? 'Jour' : 'Nuit'}'),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Text('Cycle lunaire', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 10),
            Wrap(
              spacing: 10,
              runSpacing: 10,
              children: const [
                _LuneChip(label: 'Nouvelle lune', emoji: '🌑', active: true),
                _LuneChip(label: 'Premier quartier', emoji: '🌓'),
                _LuneChip(label: 'Pleine lune', emoji: '🌕'),
                _LuneChip(label: 'Dernier quartier', emoji: '🌗'),
              ],
            ),
            const SizedBox(height: 20),
            Text('Plantations', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 10),
            Expanded(
              child: GridView.count(
                crossAxisCount: 3,
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
                children: const [
                  _Plot(label: 'Carotte', emoji: '🥕'),
                  _Plot(label: 'Basilic', emoji: '🌿'),
                  _Plot(label: 'Laitue', emoji: '🥬'),
                  _Plot(label: 'Tomate', emoji: '🍅'),
                  _Plot(label: 'Menthe', emoji: '🌱'),
                  _Plot(label: 'Flo', emoji: '🌸'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _LuneChip extends StatelessWidget {
  final String label;
  final String emoji;
  final bool active;
  const _LuneChip({required this.label, required this.emoji, this.active = false});

  @override
  Widget build(BuildContext context) => Chip(
        avatar: Text(emoji, style: const TextStyle(fontSize: 18)),
        label: Text(label),
        backgroundColor: active ? Colors.green.shade200 : null,
      );
}

class _Plot extends StatelessWidget {
  final String label;
  final String emoji;
  const _Plot({required this.label, required this.emoji});

  @override
  Widget build(BuildContext context) => Container(
        decoration: BoxDecoration(
          color: Colors.green.shade50,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: Colors.green.shade200),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(emoji, style: const TextStyle(fontSize: 30)),
            const SizedBox(height: 6),
            Text(label, style: const TextStyle(fontSize: 12)),
          ],
        ),
      );
}

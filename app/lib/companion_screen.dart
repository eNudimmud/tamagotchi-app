import 'package:flutter/material.dart';
import 'companion_provider.dart';
import 'models.dart';

class CompanionScreen extends StatelessWidget {
  final CompanionProvider provider;

  const CompanionScreen(this.provider, {super.key});

  @override
  Widget build(BuildContext context) {
    final creature = provider.creature;
    return Scaffold(
      appBar: AppBar(title: const Text('Companion')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (provider.error != null)
              Container(
                padding: const EdgeInsets.all(10),
                color: Colors.amber.shade100,
                child: Text(provider.error!, textAlign: TextAlign.center),
              ),
            const SizedBox(height: 16),
            Center(
              child: Text(
                _stageName(creature?.stage ?? Stage.rabbit),
                style: Theme.of(context).textTheme.headlineSmall,
              ),
            ),
            const SizedBox(height: 8),
            if (creature != null) _StatsRow(stats: creature.stats),
            const SizedBox(height: 20),
            _ResourceRow(resources: provider.resources),
            const SizedBox(height: 24),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              alignment: WrapAlignment.center,
              children: [
                _ActionButton(label: 'Feed', onTap: () => provider.act(ActionKind.feed)),
                _ActionButton(label: 'Pet', onTap: () => provider.act(ActionKind.pet)),
                _ActionButton(label: 'Play', onTap: () => provider.act(ActionKind.play)),
                _ActionButton(label: 'Evolve', onTap: () => provider.act(ActionKind.evolve)),
              ],
            ),
            const Spacer(),
            ElevatedButton.icon(
              onPressed: () => provider.buyCarrots(5),
              icon: const Icon(Icons.shopping_basket),
              label: const Text('Get 5 carrots'),
            ),
          ],
        ),
      ),
    );
  }

  String _stageName(Stage s) {
    switch (s) {
      case Stage.egg:
        return 'Egg';
      case Stage.rabbit:
        return 'Rabbit';
      case Stage.humanoid:
        return 'Companion';
      case Stage.agent:
        return 'Helper';
      case Stage.incarnation:
        return 'Incarnate';
    }
  }
}

class _StatsRow extends StatelessWidget {
  final Stats stats;
  const _StatsRow({required this.stats});

  @override
  Widget build(BuildContext context) => Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _Stat(label: 'Vitality', value: stats.vitality),
          _Stat(label: 'Awakening', value: stats.awakening),
          _Stat(label: 'Bond', value: stats.bond),
        ],
      );
}

class _Stat extends StatelessWidget {
  final String label;
  final int value;
  const _Stat({required this.label, required this.value});

  @override
  Widget build(BuildContext context) => Column(
        children: [
          Text('$value', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
        ],
      );
}

class _ResourceRow extends StatelessWidget {
  final Resources resources;
  const _ResourceRow({required this.resources});

  @override
  Widget build(BuildContext context) => Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          Text('🥕 ${resources.carrot}'),
          Text('⚡ ${resources.energy}'),
          Text('💛 ${resources.kiss}'),
        ],
      );
}

class _ActionButton extends StatelessWidget {
  final String label;
  final VoidCallback onTap;
  const _ActionButton({required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) => ElevatedButton(
        onPressed: onTap,
        child: Text(label),
      );
}

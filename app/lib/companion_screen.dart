import 'package:flutter/material.dart';
import 'companion_provider.dart';
import 'rabbit_painter.dart';
import 'models.dart';

class CompanionScreen extends StatelessWidget {
  final CompanionProvider provider;
  const CompanionScreen(this.provider, {super.key});

  @override
  Widget build(BuildContext context) {
    final creature = provider.creature;
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(creature?.name ?? 'Enki'),
        actions: [
          IconButton(
            icon: const Icon(Icons.face),
            tooltip: 'Vue dos / face',
            onPressed: provider.toggleFacing,
          ),
          IconButton(
            icon: const Icon(Icons.edit),
            tooltip: 'Renommer',
            onPressed: () => _rename(context),
          ),
        ],
      ),
      body: Stack(
        children: [
          // fond cycle jour/nuit
          _CycleBackground(cycle: creature?.cycle),
          RefreshIndicator(
            onRefresh: provider.refresh,
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (provider.error != null)
                  Container(
                    padding: const EdgeInsets.all(10),
                    margin: const EdgeInsets.only(bottom: 12),
                    decoration: BoxDecoration(
                      color: Colors.amber.shade100,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(provider.error!, textAlign: TextAlign.center),
                  ),
                // scene lapin
                SizedBox(
                  height: 300,
                  child: creature == null
                      ? const Center(child: CircularProgressIndicator())
                      : AnimatedRabbit(creature: creature, facingBack: provider.facingBack),
                ),
                const SizedBox(height: 8),
                // humeur + stade
                Center(
                  child: Text(
                    '${creature?.mood.label ?? ''}  ·  ${creature?.stage.label ?? ''}',
                    style: theme.textTheme.titleMedium,
                  ),
                ),
                const SizedBox(height: 16),
                if (creature != null) ..._needBars(creature),
                const SizedBox(height: 20),
                // actions
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  alignment: WrapAlignment.center,
                  children: [
                    _ActionChip(label: '🥕 Feed', onTap: () => provider.act(ActionKind.feed)),
                    _ActionChip(label: '🤚 Pet', onTap: () => provider.act(ActionKind.pet)),
                    _ActionChip(label: '🎾 Play', onTap: () => provider.act(ActionKind.play)),
                    _ActionChip(label: '💤 Sleep', onTap: () => provider.act(ActionKind.sleep)),
                    _ActionChip(label: '🛁 Clean', onTap: () => provider.act(ActionKind.clean)),
                    _ActionChip(label: '📚 Train', onTap: () => provider.act(ActionKind.train)),
                    _ActionChip(label: '💬 Talk', onTap: () => provider.act(ActionKind.talk)),
                    _ActionChip(label: '✦ Evolve', onTap: () => provider.act(ActionKind.evolve)),
                  ],
                ),
                const SizedBox(height: 16),
                Center(
                  child: OutlinedButton.icon(
                    onPressed: () => provider.buyCarrots(5),
                    icon: const Icon(Icons.eco),
                    label: Text('Récolter 5 🥕  (🥕 ${provider.resources.carrot})'),
                  ),
                ),
                const SizedBox(height: 20),
              ],
            ),
          ),
        ],
      ),
    );
  }

  List<Widget> _needBars(CreatureState c) {
    final items = <Map<String, dynamic>>[
      {'label': 'Faim', 'value': c.needs.hunger, 'color': Colors.orange},
      {'label': 'Énergie', 'value': c.needs.energy, 'color': Colors.green},
      {'label': 'Propreté', 'value': c.needs.hygiene, 'color': Colors.blue},
      {'label': 'Lien', 'value': c.needs.social, 'color': Colors.pink},
      {'label': 'Amusement', 'value': c.needs.fun, 'color': Colors.purple},
    ];
    return items.map((it) {
      final v = (it['value'] as int).clamp(0, 100);
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 4),
        child: Row(
          children: [
            SizedBox(width: 80, child: Text(it['label'], style: const TextStyle(fontSize: 13))),
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: LinearProgressIndicator(
                  value: v / 100,
                  minHeight: 12,
                  color: it['color'],
                  backgroundColor: Colors.white24,
                ),
              ),
            ),
            const SizedBox(width: 8),
            SizedBox(width: 28, child: Text('$v', textAlign: TextAlign.end)),
          ],
        ),
      );
    }).toList();
  }

  void _rename(BuildContext context) {
    final ctrl = TextEditingController(text: provider.creature?.name ?? '');
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Renommer'),
        content: TextField(
          controller: ctrl,
          maxLength: 24,
          decoration: const InputDecoration(hintText: 'Nom du compagnon'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Annuler')),
          TextButton(
            onPressed: () {
              provider.rename(ctrl.text.trim());
              Navigator.pop(ctx);
            },
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}

class AnimatedRabbit extends StatefulWidget {
  final CreatureState creature;
  final bool facingBack;
  const AnimatedRabbit({required this.creature, this.facingBack = false, super.key});

  @override
  State<AnimatedRabbit> createState() => _AnimatedRabbitState();
}

class _AnimatedRabbitState extends State<AnimatedRabbit> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 3))..repeat();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _ctrl,
      builder: (ctx, _) {
        final blink = blinkFor(DateTime.now());
        return CustomPaint(
          size: const Size(260, 300),
          painter: RabbitPainter(
            t: _ctrl.value,
            mood: widget.creature.mood,
            facingBack: widget.facingBack,
            blink: blink,
          ),
        );
      },
    );
  }
}

class _CycleBackground extends StatelessWidget {
  final Cycle? cycle;
  const _CycleBackground({this.cycle});

  @override
  Widget build(BuildContext context) {
    final isDay = cycle?.isDay ?? true;
    return AnimatedContainer(
      duration: const Duration(seconds: 2),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: isDay
              ? [const Color(0xFFFCF7EC), const Color(0xFFF3EAD2)]
              : [const Color(0xFF2A2535), const Color(0xFF3A3550)],
        ),
      ),
    );
  }
}

class _ActionChip extends StatelessWidget {
  final String label;
  final VoidCallback onTap;
  const _ActionChip({required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) => OutlinedButton(
        onPressed: onTap,
        style: OutlinedButton.styleFrom(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        ),
        child: Text(label),
      );
}

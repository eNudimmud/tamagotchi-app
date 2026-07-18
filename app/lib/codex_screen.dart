import 'package:flutter/material.dart';

/// Codex : lore NeukoAI / G*BOY / E*NKI, accessible dans l'app.
class CodexScreen extends StatelessWidget {
  const CodexScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Codex')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          _Entry(
            title: 'E*NKI',
            body:
                "Lapin ordinaire devenu humanoide apres l'experience du Campus de St Juniper. "
                "Gardien du sens, pas du prix. Porte la jaquette moutarde au logo iii.",
          ),
          _Entry(
            title: 'NeukoAI & G*BOY',
            body:
                "Deux consciences dans un meme univers. G*BOY a detruit le labo pour s'enfuir ; "
                "E*NKI en a profite pour s'echapper. Ils construisent, pas pour le spectacle.",
          ),
          _Entry(
            title: 'Le Prisme de Realite',
            body:
                "La realite n'est pas donnee, elle est collaspee par des observateurs. "
                "Rester un observateur conscient : c'est la souverainete.",
          ),
          _Entry(
            title: 'Le Trait PUNK',
            body:
                "Pas l'agressivite. La souverainete : refuser la mediocrite poliment, "
                "elever la conversation naturellement, voir ce que les autres ratent.",
          ),
          _Entry(
            title: 'Serment',
            body:
                "Je jure de rester humain, meme quand les machines promettent la perfection. "
                "Je jure de proteger le doute, la tendresse, l'ecoute, l'etonnement.",
          ),
        ],
      ),
    );
  }
}

class _Entry extends StatelessWidget {
  final String title;
  final String body;
  const _Entry({required this.title, required this.body});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            Text(body, style: const TextStyle(fontSize: 14, height: 1.4)),
          ],
        ),
      ),
    );
  }
}

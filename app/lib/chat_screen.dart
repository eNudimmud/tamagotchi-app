import 'package:flutter/material.dart';
import 'companion_provider.dart';
import 'models.dart';

/// Écran Parler — le pipeline ECOS Art. 14 rendu visible :
/// l'esprit répond, PROPOSE parfois une action (carte de permission),
/// et n'exécute qu'après le choix explicite du gardien. Jamais l'inverse.
class ChatScreen extends StatefulWidget {
  final CompanionProvider provider;
  const ChatScreen(this.provider, {super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _Bulle {
  final String texte;
  final bool moi;
  final bool systeme;
  _Bulle(this.texte, {this.moi = false, this.systeme = false});
}

class _ChatScreenState extends State<ChatScreen> {
  final _ctrl = TextEditingController();
  final _scroll = ScrollController();
  final List<_Bulle> _bulles = [
    _Bulle('Parle-lui. Essaie : « rappelle-moi d\'appeler maman demain à 18h »',
        systeme: true),
  ];
  bool _envoi = false;

  void _ajouter(_Bulle b) {
    setState(() => _bulles.add(b));
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scroll.hasClients) {
        _scroll.animateTo(_scroll.position.maxScrollExtent + 80,
            duration: const Duration(milliseconds: 200), curve: Curves.easeOut);
      }
    });
  }

  Future<void> _envoyer() async {
    final texte = _ctrl.text.trim();
    if (texte.isEmpty || _envoi) return;
    _ctrl.clear();
    _ajouter(_Bulle(texte, moi: true));
    setState(() => _envoi = true);
    try {
      final api = widget.provider.api;
      final uid = widget.provider.userId;
      final r = await api.talk(uid, texte);
      for (final e in r.evenements) {
        _ajouter(_Bulle('${e['genre'] == 'rêve' ? '🌙' : '🌱'} ${e['texte']}',
            systeme: true));
      }
      for (final l in r.reply) {
        _ajouter(_Bulle(l.trim()));
      }
      if (r.pending != null && mounted) {
        await _carteDePermission(r.pending!);
      }
    } catch (e) {
      _ajouter(_Bulle('⚠ ${e.toString().replaceFirst('Exception: ', '')}',
          systeme: true));
    } finally {
      setState(() => _envoi = false);
    }
  }

  Future<void> _carteDePermission(PendingAction p) async {
    final strongCtrl = TextEditingController();
    final approuve = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        title: const Text('Demande de permission'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: const Color(0xFFF4EFE2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(p.carte,
                    style: const TextStyle(
                        fontFamily: 'monospace', fontSize: 11.5)),
              ),
              if (p.strongRequired) ...[
                const SizedBox(height: 10),
                TextField(
                  controller: strongCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Action sensible — tape CONFIRME',
                    border: OutlineInputBorder(),
                  ),
                ),
              ],
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Refuser'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Autoriser'),
          ),
        ],
      ),
    );
    if (!mounted || approuve == null) return;
    final strong = strongCtrl.text.trim() == 'CONFIRME';
    final res = await widget.provider.api
        .confirm(widget.provider.userId, p.actionId, approuve, strong: strong);
    for (final l in res.reply) {
      _ajouter(_Bulle(l.trim()));
    }
    if (res.statusCode == 428) {
      _ajouter(_Bulle('⚠ Confirmation forte requise : tape CONFIRME.',
          systeme: true));
    } else if (res.verifie) {
      final chemin = res.sortie?['chemin'] ?? '';
      _ajouter(_Bulle('✓ vérifié — $chemin', systeme: true));
    } else if (res.decision == 'refus_utilisateur') {
      _ajouter(_Bulle('Rien n\'a été écrit. La promesse reste entre vous.',
          systeme: true));
    } else if (res.decision == 'refus_politique') {
      _ajouter(_Bulle('⛔ ${res.evenement ?? 'refus de politique'}',
          systeme: true));
    } else if (res.reason != null) {
      _ajouter(_Bulle('⚠ ${res.reason}', systeme: true));
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Parler')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scroll,
              padding: const EdgeInsets.all(12),
              itemCount: _bulles.length,
              itemBuilder: (_, i) {
                final b = _bulles[i];
                final align =
                    b.moi ? Alignment.centerRight : Alignment.centerLeft;
                final couleur = b.systeme
                    ? const Color(0xFFEDE7D6)
                    : b.moi
                        ? theme.colorScheme.primaryContainer
                        : Colors.white;
                return Align(
                  alignment: align,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 3),
                    padding: const EdgeInsets.symmetric(
                        horizontal: 12, vertical: 8),
                    constraints: const BoxConstraints(maxWidth: 320),
                    decoration: BoxDecoration(
                      color: couleur,
                      borderRadius: BorderRadius.circular(14),
                      boxShadow: b.systeme
                          ? null
                          : [
                              BoxShadow(
                                  color: Colors.black.withOpacity(0.05),
                                  blurRadius: 3)
                            ],
                    ),
                    child: Text(b.texte,
                        style: TextStyle(
                            fontSize: 14,
                            fontStyle: b.systeme
                                ? FontStyle.italic
                                : FontStyle.normal)),
                  ),
                );
              },
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(12, 4, 12, 10),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _ctrl,
                      onSubmitted: (_) => _envoyer(),
                      textInputAction: TextInputAction.send,
                      decoration: InputDecoration(
                        hintText: 'Dis-lui quelque chose…',
                        border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(24)),
                        contentPadding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 10),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton.filled(
                    onPressed: _envoi ? null : _envoyer,
                    icon: _envoi
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(strokeWidth: 2))
                        : const Icon(Icons.send),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

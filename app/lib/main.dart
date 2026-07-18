import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_service.dart';
import 'companion_provider.dart';
import 'companion_screen.dart';

void main() {
  final api = ApiService();
  final provider = CompanionProvider(api);
  provider.refresh();
  runApp(
    ChangeNotifierProvider.value(
      value: provider,
      child: MaterialApp(
        title: 'Companion',
        theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.green),
        home: const _Home(),
      ),
    ),
  );
}

class _Home extends StatelessWidget {
  const _Home();

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<CompanionProvider>(context);
    return CompanionScreen(provider);
  }
}

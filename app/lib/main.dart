import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_service.dart';
import 'companion_provider.dart';
import 'companion_screen.dart';
import 'garden_screen.dart';
import 'codex_screen.dart';
import 'settings_screen.dart';
import 'models.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => CompanionProvider(ApiService())..refresh(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'E*NKI Tamagotchi',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF4B5320),
          background: const Color(0xFFFCF7EC),
        ),
        scaffoldBackgroundColor: const Color(0xFFFCF7EC),
      ),
      home: const Home(),
    );
  }
}

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<CompanionProvider>(context);
    final cycle = provider.creature?.cycle;
    final body = [
      CompanionScreen(provider),
      GardenScreen(cycle: cycle),
      const CodexScreen(),
      SettingsScreen(
        creature: provider.creature,
        onRename: (n) => provider.rename(n),
      ),
    ];
    return Scaffold(
      body: body[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.pets), label: 'Compagnon'),
          NavigationDestination(icon: Icon(Icons.local_florist), label: 'Jardin'),
          NavigationDestination(icon: Icon(Icons.auto_stories), label: 'Codex'),
          NavigationDestination(icon: Icon(Icons.settings), label: 'Réglages'),
        ],
      ),
    );
  }
}

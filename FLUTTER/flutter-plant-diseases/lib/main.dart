import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ai_detection/core/theme/app_theme.dart';
import 'package:ai_detection/core/routes/app_router.dart';
import 'package:ai_detection/core/services/storage_service.dart';
import 'package:ai_detection/core/services/auth_service.dart';
import 'package:ai_detection/core/services/detection_service.dart';
import 'package:ai_detection/core/services/farm_service.dart';
import 'package:ai_detection/core/services/firebase_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await StorageService.instance.init();
  try {
    await FirebaseService.initialize();
  } catch (e) {
    debugPrint('Firebase initialization error: $e');
  }
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthService()),
        ChangeNotifierProvider(create: (_) => DetectionService()),
        ChangeNotifierProvider(create: (_) => FarmService()),
      ],
      child: MaterialApp(
        title: 'LeafCare',
        theme: AppTheme.lightTheme,
        themeMode: ThemeMode.light,
        debugShowCheckedModeBanner: false,
        initialRoute: AppRouter.login,
        routes: AppRouter.routes,
        onGenerateRoute: AppRouter.onGenerateRoute,
      ),
    );
  }
}


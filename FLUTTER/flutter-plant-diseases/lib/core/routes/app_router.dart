import 'package:flutter/material.dart';
import 'package:ai_detection/features/auth/presentation/login_screen.dart';
import 'package:ai_detection/features/auth/presentation/register_screen.dart';
import 'package:ai_detection/features/dashboard/presentation/dashboard_screen.dart';
import 'package:ai_detection/features/detection/presentation/detection_screen.dart';
import 'package:ai_detection/features/farm/presentation/farm_list_screen.dart';
import 'package:ai_detection/features/farm/presentation/farm_detail_screen.dart';
import 'package:ai_detection/features/profile/presentation/profile_screen.dart';

class AppRouter {
  static const String login = '/login';
  static const String register = '/register';
  static const String dashboard = '/dashboard';
  static const String detection = '/detection';
  static const String farmList = '/farm-list';
  static const String farmDetail = '/farm-detail';
  static const String profile = '/profile';

  static Map<String, WidgetBuilder> get routes => {
        login: (context) => const LoginScreen(),
        register: (context) => const RegisterScreen(),
        dashboard: (context) => const DashboardScreen(),
        detection: (context) => const DetectionScreen(),
        farmList: (context) => const FarmListScreen(),
        profile: (context) => const ProfileScreen(),
      };

  static Route<dynamic>? onGenerateRoute(RouteSettings settings) {
    if (settings.name == farmDetail) {
      final farmId = settings.arguments as String;
      return MaterialPageRoute(
        builder: (context) => FarmDetailScreen(farmId: farmId),
      );
    }
    return null;
  }
}


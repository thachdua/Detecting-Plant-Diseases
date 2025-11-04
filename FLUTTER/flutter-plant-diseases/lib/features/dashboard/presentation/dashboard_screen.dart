import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:ai_detection/core/routes/app_router.dart';
import 'package:ai_detection/core/services/auth_service.dart';
import 'package:ai_detection/core/services/detection_service.dart';
import 'package:ai_detection/core/services/storage_service.dart';
import 'package:ai_detection/core/theme/app_theme.dart';
import 'package:ai_detection/core/widgets/modern_card.dart';
import 'package:ai_detection/core/widgets/stats_summary_card.dart';
import 'package:ai_detection/features/dashboard/widgets/recent_detection_card.dart';
import 'package:ai_detection/features/dashboard/widgets/plants_chart.dart';
import 'package:ai_detection/core/widgets/bottom_nav_bar.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentNavIndex = 0;
  File? _avatarImage;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadAvatar();
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _loadAvatar();
  }

  void _loadAvatar() {
    final authService = context.read<AuthService>();
    final userId = authService.currentUser?.id;
    if (userId != null) {
      final avatarPath = StorageService.instance.getAvatarPath(userId);
      if (avatarPath != null && File(avatarPath).existsSync()) {
        setState(() {
          _avatarImage = File(avatarPath);
        });
      } else {
        setState(() {
          _avatarImage = null;
        });
      }
    }
  }

  void _onNavTap(int index) {
    setState(() => _currentNavIndex = index);
    switch (index) {
      case 0:
        // Already on dashboard
        break;
      case 1:
        Navigator.pushNamed(context, AppRouter.detection);
        break;
      case 2:
        Navigator.pushNamed(context, AppRouter.farmList);
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    final authService = context.watch<AuthService>();
    final detectionService = context.watch<DetectionService>();
    final recentDetections = detectionService.recentDetections.take(5).toList();
    final weeklyStats = detectionService.getWeeklyStats();

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: Text(
          'Dashboard',
          style: GoogleFonts.inter(
            fontSize: 28,
            fontWeight: FontWeight.w700,
            color: AppTheme.textPrimary,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
            tooltip: 'Notifications',
          ),
          PopupMenuButton(
            icon: CircleAvatar(
              radius: 16,
              backgroundColor: AppTheme.accentGreen,
              backgroundImage: _avatarImage != null ? FileImage(_avatarImage!) : null,
              child: _avatarImage == null
                  ? Text(
                      authService.currentUser?.username[0].toUpperCase() ?? 'U',
                      style: GoogleFonts.inter(
                        color: AppTheme.primaryGreen,
                        fontWeight: FontWeight.w600,
                      ),
                    )
                  : null,
            ),
            itemBuilder: (context) => [
              PopupMenuItem(
                child: ListTile(
                  leading: const Icon(Icons.person_outline),
                  title: Text(
                    authService.currentUser?.username ?? 'User',
                    style: GoogleFonts.inter(),
                  ),
                  contentPadding: EdgeInsets.zero,
                  onTap: () async {
                    final result = await Navigator.pushNamed(context, AppRouter.profile);
                    if (mounted) {
                      _loadAvatar();
                    }
                  },
                ),
              ),
              PopupMenuItem(
                child: ListTile(
                  leading: const Icon(Icons.logout),
                  title: Text('Logout', style: GoogleFonts.inter()),
                  contentPadding: EdgeInsets.zero,
                  onTap: () async {
                    await authService.logout();
                    if (context.mounted) {
                      Navigator.pushReplacementNamed(context, AppRouter.login);
                    }
                  },
                ),
              ),
            ],
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          await Future.delayed(const Duration(milliseconds: 500));
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (authService.currentUser != null)
                AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: AppTheme.accentBlue,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: Icon(
                          Icons.waving_hand,
                          color: AppTheme.warningOrange,
                          size: 28,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              'Welcome back,',
                              style: GoogleFonts.inter(
                                fontSize: 14,
                                color: AppTheme.textSecondary,
                                fontWeight: FontWeight.w500,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              authService.currentUser!.username,
                              style: GoogleFonts.inter(
                                fontSize: 20,
                                fontWeight: FontWeight.w700,
                                color: AppTheme.textPrimary,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              const SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: StatsSummaryCard(
                      title: 'Infected',
                      value: detectionService.totalInfected.toString(),
                      icon: Icons.warning_rounded,
                      color: AppTheme.errorRed,
                      backgroundColor: const Color(0xFFFFEBEE),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: StatsSummaryCard(
                      title: 'Healthy',
                      value: detectionService.totalHealthy.toString(),
                      icon: Icons.check_circle_rounded,
                      color: AppTheme.successGreen,
                      backgroundColor: AppTheme.accentGreen,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              ModernCard(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Weekly Statistics',
                          style: GoogleFonts.inter(
                            fontSize: 18,
                            fontWeight: FontWeight.w600,
                            color: AppTheme.textPrimary,
                          ),
                        ),
                        Icon(
                          Icons.insights_outlined,
                          color: AppTheme.primaryGreen,
                          size: 20,
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    PlantsChart(stats: weeklyStats),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Recent Detections',
                    style: GoogleFonts.inter(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: AppTheme.textPrimary,
                    ),
                  ),
                  TextButton(
                    onPressed: () {},
                    child: Text(
                      'View All',
                      style: GoogleFonts.inter(
                        fontWeight: FontWeight.w600,
                        color: AppTheme.primaryGreen,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              if (recentDetections.isEmpty)
                ModernCard(
                  padding: const EdgeInsets.all(40),
                  child: Column(
                    children: [
                      Icon(
                        Icons.search_off_outlined,
                        size: 64,
                        color: AppTheme.textSecondary.withOpacity(0.5),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No detections yet',
                        style: GoogleFonts.inter(
                          fontSize: 16,
                          color: AppTheme.textSecondary,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Start detecting plant diseases',
                        style: GoogleFonts.inter(
                          fontSize: 14,
                          color: AppTheme.textSecondary.withOpacity(0.7),
                        ),
                      ),
                    ],
                  ),
                )
              else
                ...recentDetections.map((detection) => RecentDetectionCard(detection: detection)),
              const SizedBox(height: 100),
            ],
          ),
        ),
      ),
      bottomNavigationBar: ModernBottomNavBar(
        currentIndex: _currentNavIndex,
        onTap: _onNavTap,
      ),
    );
  }
}

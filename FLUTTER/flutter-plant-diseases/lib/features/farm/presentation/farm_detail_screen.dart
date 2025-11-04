import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:image_picker/image_picker.dart';
import 'package:ai_detection/core/models/farm_model.dart';
import 'package:ai_detection/core/services/farm_service.dart';
import 'package:ai_detection/core/services/detection_service.dart';
import 'package:ai_detection/core/theme/app_theme.dart';
import 'package:ai_detection/features/farm/widgets/add_plant_dialog.dart';
import 'package:ai_detection/core/widgets/modern_card.dart';
import 'package:ai_detection/core/widgets/modern_button.dart';

class FarmDetailScreen extends StatelessWidget {
  final String farmId;

  const FarmDetailScreen({super.key, required this.farmId});

  @override
  Widget build(BuildContext context) {
    final farmService = context.watch<FarmService>();
    final farm = farmService.getFarmById(farmId);

    if (farm == null) {
      return Scaffold(
        backgroundColor: AppTheme.background,
        appBar: AppBar(
          automaticallyImplyLeading: false,
          title: Text(
            'Farm Details',
            style: GoogleFonts.inter(
              fontSize: 28,
              fontWeight: FontWeight.w700,
              color: AppTheme.textPrimary,
            ),
          ),
        ),
        body: Center(
          child: Text(
            'Farm not found',
            style: GoogleFonts.inter(color: AppTheme.textSecondary),
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: Text(
          farm.name,
          style: GoogleFonts.inter(
            fontSize: 28,
            fontWeight: FontWeight.w700,
            color: AppTheme.textPrimary,
          ),
        ),
      ),
      body: Column(
        children: [
          ModernCard(
            margin: const EdgeInsets.all(20),
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppTheme.accentGreen,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Icon(
                        Icons.agriculture_rounded,
                        color: AppTheme.primaryGreen,
                        size: 32,
                      ),
                    ),
                    const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(
                                farm.name,
                                style: GoogleFonts.inter(
                                  fontSize: 22,
                                  fontWeight: FontWeight.w700,
                                  color: AppTheme.textPrimary,
                                ),
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                              ),
                              const SizedBox(height: 4),
                              Row(
                                children: [
                                  Icon(
                                    Icons.location_on_outlined,
                                    size: 14,
                                    color: AppTheme.textSecondary,
                                  ),
                                  const SizedBox(width: 4),
                                  Expanded(
                                    child: Text(
                                      farm.location,
                                      style: GoogleFonts.inter(
                                        fontSize: 14,
                                        color: AppTheme.textSecondary,
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 4),
                              Text(
                                farm.cropType,
                                style: GoogleFonts.inter(
                                  fontSize: 14,
                                  color: AppTheme.textSecondary,
                                ),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ],
                          ),
                        ),
                  ],
                ),
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _buildStat(
                      context,
                      'Total',
                      farm.totalPlants.toString(),
                      Icons.eco_rounded,
                      AppTheme.primaryGreen,
                    ),
                    _buildStat(
                      context,
                      'Healthy',
                      farm.healthyPlants.toString(),
                      Icons.check_circle_rounded,
                      AppTheme.successGreen,
                    ),
                    _buildStat(
                      context,
                      'Infected',
                      farm.infectedPlants.toString(),
                      Icons.warning_rounded,
                      AppTheme.errorRed,
                    ),
                  ],
                ),
              ],
            ),
          ),
          Expanded(
            child: farm.plants.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.eco_outlined,
                          size: 80,
                          color: AppTheme.textSecondary.withOpacity(0.5),
                        ),
                        const SizedBox(height: 24),
                        Text(
                          'No plants added yet',
                          style: GoogleFonts.inter(
                            fontSize: 18,
                            fontWeight: FontWeight.w600,
                            color: AppTheme.textPrimary,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Add your first plant to get started',
                          style: GoogleFonts.inter(
                            fontSize: 14,
                            color: AppTheme.textSecondary,
                          ),
                        ),
                      ],
                    ),
                  )
                : GridView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      crossAxisSpacing: 12,
                      mainAxisSpacing: 12,
                      childAspectRatio: 0.85,
                    ),
                    itemCount: farm.plants.length,
                    itemBuilder: (context, index) {
                      final plant = farm.plants[index];
                      return Hero(
                        tag: 'plant_${plant.id}',
                        child: ModernCard(
                          padding: EdgeInsets.zero,
                          onLongPress: () {
                            showDialog(
                              context: context,
                              builder: (context) => _PlantOptionsDialog(
                                farmId: farmId,
                                plant: plant,
                              ),
                            );
                          },
                          child: Column(
                            children: [
                              Expanded(
                                child: plant.imagePath.isNotEmpty
                                    ? ClipRRect(
                                        borderRadius: const BorderRadius.vertical(
                                          top: Radius.circular(20),
                                        ),
                                        child: Image.file(
                                          File(plant.imagePath),
                                          fit: BoxFit.contain,
                                          width: double.infinity,
                                          height: double.infinity,
                                        ),
                                      )
                                    : Container(
                                        decoration: BoxDecoration(
                                          color: AppTheme.accentBlue,
                                          borderRadius: const BorderRadius.vertical(
                                            top: Radius.circular(20),
                                          ),
                                        ),
                                        child: Center(
                                          child: Icon(
                                            Icons.image_outlined,
                                            size: 48,
                                            color: AppTheme.textSecondary
                                                .withOpacity(0.5),
                                          ),
                                        ),
                                      ),
                              ),
                              Padding(
                                padding: const EdgeInsets.all(12),
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Text(
                                      plant.name,
                                      style: GoogleFonts.inter(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w600,
                                        color: AppTheme.textPrimary,
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                      textAlign: TextAlign.center,
                                    ),
                                    const SizedBox(height: 4),
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(
                                          plant.status == PlantStatus.healthy
                                              ? Icons.check_circle_rounded
                                              : Icons.warning_rounded,
                                          color: plant.status == PlantStatus.healthy
                                              ? AppTheme.successGreen
                                              : AppTheme.errorRed,
                                          size: 18,
                                        ),
                                        const SizedBox(width: 6),
                                        Text(
                                          plant.status == PlantStatus.healthy
                                              ? 'Healthy'
                                              : 'Infected',
                                          style: GoogleFonts.inter(
                                            fontSize: 12,
                                            fontWeight: FontWeight.w600,
                                            color: plant.status ==
                                                    PlantStatus.healthy
                                                ? AppTheme.successGreen
                                                : AppTheme.errorRed,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          showDialog(
            context: context,
            builder: (context) => AddPlantDialog(farmId: farmId),
          );
        },
        icon: const Icon(Icons.add_rounded),
        label: Text(
          'Add Plant',
          style: GoogleFonts.inter(fontWeight: FontWeight.w600),
        ),
      ),
    );
  }

  Widget _buildStat(
    BuildContext context,
    String label,
    String value,
    IconData icon,
    Color color,
  ) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color, size: 24),
        ),
        const SizedBox(height: 8),
        Text(
          value,
          style: GoogleFonts.inter(
            fontSize: 24,
            fontWeight: FontWeight.w700,
            color: color,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: GoogleFonts.inter(
            fontSize: 12,
            color: AppTheme.textSecondary,
          ),
        ),
      ],
    );
  }
}

class _PlantOptionsDialog extends StatelessWidget {
  final String farmId;
  final PlantModel plant;

  const _PlantOptionsDialog({
    required this.farmId,
    required this.plant,
  });

  Future<void> _redetectPlant(BuildContext context) async {
    Navigator.pop(context); // Close options dialog first
    
    final imagePicker = ImagePicker();
    final image = await showDialog<XFile>(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        title: Text(
          'Select Image for Re-detection',
          style: GoogleFonts.inter(fontWeight: FontWeight.w700),
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt_outlined),
              title: Text('Take Photo', style: GoogleFonts.inter()),
              onTap: () async {
                final photo = await imagePicker.pickImage(source: ImageSource.camera);
                if (photo != null && context.mounted) {
                  Navigator.pop(context, photo);
                }
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library_outlined),
              title: Text('Choose from Gallery', style: GoogleFonts.inter()),
              onTap: () async {
                final photo = await imagePicker.pickImage(source: ImageSource.gallery);
                if (photo != null && context.mounted) {
                  Navigator.pop(context, photo);
                }
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel', style: GoogleFonts.inter()),
          ),
        ],
      ),
    );

    if (image == null || !context.mounted) return;

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(
        child: CircularProgressIndicator(),
      ),
    );

    try {
      final detectionService = context.read<DetectionService>();
      final detection = await detectionService.detectDisease(image.path);
      final newStatus = PlantStatus.infected;
      await detectionService.saveDetection(detection);
      
      final farmService = context.read<FarmService>();
      await farmService.updatePlantStatus(farmId, plant.id, newStatus);
      
      if (context.mounted) {
        Navigator.pop(context); // Close loading
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Re-detection completed: ${detection.diseaseName}',
              style: GoogleFonts.inter(),
            ),
            backgroundColor: AppTheme.successGreen,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        Navigator.pop(context); // Close loading
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Error during re-detection: $e',
              style: GoogleFonts.inter(),
            ),
            backgroundColor: AppTheme.errorRed,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        );
      }
    }
  }

  Future<void> _deletePlant(BuildContext context) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        title: Text(
          'Delete Plant',
          style: GoogleFonts.inter(fontWeight: FontWeight.w700),
        ),
        content: Text(
          'Are you sure you want to delete "${plant.name}"?',
          style: GoogleFonts.inter(),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('Cancel', style: GoogleFonts.inter()),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text(
              'Delete',
              style: GoogleFonts.inter(color: AppTheme.errorRed),
            ),
          ),
        ],
      ),
    );

    if (confirm == true && context.mounted) {
      final farmService = context.read<FarmService>();
      await farmService.deletePlant(farmId, plant.id);
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Plant deleted successfully',
            style: GoogleFonts.inter(),
          ),
          backgroundColor: AppTheme.successGreen,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(24),
      ),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              plant.name,
              style: GoogleFonts.inter(
                fontSize: 20,
                fontWeight: FontWeight.w700,
                color: AppTheme.textPrimary,
              ),
            ),
            const SizedBox(height: 24),
            ModernButton(
              label: 'Re-detect Disease',
              icon: Icons.search_rounded,
              onPressed: () => _redetectPlant(context),
            ),
            const SizedBox(height: 12),
            ModernButton(
              label: 'Delete Plant',
              icon: Icons.delete_outlined,
              isPrimary: false,
              onPressed: () => _deletePlant(context),
            ),
            const SizedBox(height: 12),
            OutlinedButton(
              onPressed: () => Navigator.pop(context),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: Text(
                'Cancel',
                style: GoogleFonts.inter(fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:ai_detection/core/models/farm_model.dart';
import 'package:ai_detection/core/services/farm_service.dart';
import 'package:ai_detection/core/services/detection_service.dart';
import 'package:ai_detection/core/theme/app_theme.dart';
import 'package:ai_detection/core/widgets/modern_button.dart';
import 'package:ai_detection/core/widgets/modern_card.dart';

class AddPlantDialog extends StatefulWidget {
  final String farmId;

  const AddPlantDialog({super.key, required this.farmId});

  @override
  State<AddPlantDialog> createState() => _AddPlantDialogState();
}

class _AddPlantDialogState extends State<AddPlantDialog> {
  final ImagePicker _picker = ImagePicker();
  final TextEditingController _nameController = TextEditingController();
  XFile? _pickedImage;
  PlantStatus _selectedStatus = PlantStatus.healthy;
  bool _isLoading = false;
  bool _useDetection = false;

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    try {
      final image = await _picker.pickImage(source: ImageSource.gallery);
      if (image != null) {
        setState(() => _pickedImage = image);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Error picking image: $e',
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

  Future<void> _handleAdd() async {
    if (_pickedImage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Please select an image',
            style: GoogleFonts.inter(),
          ),
          backgroundColor: AppTheme.errorRed,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      );
      return;
    }
    if (_nameController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Please enter plant name',
            style: GoogleFonts.inter(),
          ),
          backgroundColor: AppTheme.errorRed,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      );
      return;
    }
    setState(() => _isLoading = true);
    PlantStatus finalStatus = _selectedStatus;
    if (_useDetection) {
      final detectionService = context.read<DetectionService>();
      final detection = await detectionService.detectDisease(_pickedImage!.path);
      finalStatus = PlantStatus.infected;
      await detectionService.saveDetection(detection);
    }
    final farmService = context.read<FarmService>();
    await farmService.addPlantToFarm(
      widget.farmId,
      _nameController.text.trim(),
      _pickedImage!.path,
      finalStatus,
    );
    setState(() => _isLoading = false);
    if (mounted) {
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            _useDetection
                ? 'Plant added and disease detected'
                : 'Plant added successfully',
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
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.85,
        ),
        child: Container(
          padding: const EdgeInsets.all(24),
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.accentGreen,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Icon(
                      Icons.eco_rounded,
                      color: AppTheme.primaryGreen,
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Text(
                      'Add New Plant',
                      style: GoogleFonts.inter(
                        fontSize: 24,
                        fontWeight: FontWeight.w700,
                        color: AppTheme.textPrimary,
                      ),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                height: _pickedImage != null ? 200 : 150,
                decoration: BoxDecoration(
                  color: AppTheme.accentBlue,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: _pickedImage != null
                    ? Stack(
                        children: [
                          ClipRRect(
                            borderRadius: BorderRadius.circular(20),
                            child: Image.file(
                              File(_pickedImage!.path),
                              width: double.infinity,
                              fit: BoxFit.cover,
                            ),
                          ),
                          Positioned(
                            top: 8,
                            right: 8,
                            child: IconButton(
                              icon: Container(
                                padding: const EdgeInsets.all(6),
                                decoration: BoxDecoration(
                                  color: Colors.white,
                                  shape: BoxShape.circle,
                                ),
                                child: Icon(
                                  Icons.close,
                                  size: 16,
                                  color: AppTheme.errorRed,
                                ),
                              ),
                              onPressed: () {
                                setState(() => _pickedImage = null);
                              },
                            ),
                          ),
                        ],
                      )
                    : Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.image_outlined,
                              size: 48,
                              color: AppTheme.textSecondary.withOpacity(0.5),
                            ),
                            const SizedBox(height: 12),
                            Text(
                              'No image selected',
                              style: GoogleFonts.inter(
                                fontSize: 14,
                                color: AppTheme.textSecondary,
                              ),
                            ),
                          ],
                        ),
                      ),
              ),
              const SizedBox(height: 20),
              OutlinedButton.icon(
                onPressed: _pickImage,
                icon: const Icon(Icons.photo_library_outlined),
                label: Text(
                  'Select Image',
                  style: GoogleFonts.inter(fontWeight: FontWeight.w600),
                ),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
              const SizedBox(height: 24),
              TextFormField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: 'Plant Name',
                  prefixIcon: const Icon(Icons.eco_outlined),
                  labelStyle: GoogleFonts.inter(),
                ),
                style: GoogleFonts.inter(),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter plant name';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              ModernCard(
                padding: const EdgeInsets.all(16),
                color: AppTheme.accentBlue,
                child: Row(
                  children: [
                    Icon(
                      Icons.bug_report_outlined,
                      color: AppTheme.primaryGreen,
                      size: 20,
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Use AI Detection',
                        style: GoogleFonts.inter(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                          color: AppTheme.textPrimary,
                        ),
                      ),
                    ),
                    Switch(
                      value: _useDetection,
                      onChanged: (value) {
                        setState(() => _useDetection = value);
                      },
                      activeColor: AppTheme.primaryGreen,
                    ),
                  ],
                ),
              ),
              if (!_useDetection) ...[
                const SizedBox(height: 24),
                Text(
                  'Health Status',
                  style: GoogleFonts.inter(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: AppTheme.textPrimary,
                  ),
                ),
                const SizedBox(height: 12),
                SegmentedButton<PlantStatus>(
                  segments: [
                    ButtonSegment(
                      value: PlantStatus.healthy,
                      label: Text(
                        'Healthy',
                        style: GoogleFonts.inter(),
                      ),
                      icon: const Icon(
                        Icons.check_circle_outline,
                        size: 18,
                      ),
                    ),
                    ButtonSegment(
                      value: PlantStatus.infected,
                      label: Text(
                        'Infected',
                        style: GoogleFonts.inter(),
                      ),
                      icon: const Icon(
                        Icons.warning_outlined,
                        size: 18,
                      ),
                    ),
                  ],
                  selected: {_selectedStatus},
                  onSelectionChanged: (Set<PlantStatus> selected) {
                    setState(() => _selectedStatus = selected.first);
                  },
                ),
              ],
              const SizedBox(height: 32),
                Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _isLoading
                          ? null
                          : () => Navigator.pop(context),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: Text(
                        'Cancel',
                        style: GoogleFonts.inter(fontWeight: FontWeight.w600),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    flex: 2,
                    child: ModernButton(
                      label: _useDetection ? 'Detect & Add' : 'Add Plant',
                      icon: _useDetection ? Icons.search_rounded : Icons.add_rounded,
                      onPressed: _isLoading ? null : _handleAdd,
                      isLoading: _isLoading,
                    ),
                  ),
                ],
              ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

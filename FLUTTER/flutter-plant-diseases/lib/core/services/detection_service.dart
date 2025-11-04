import 'package:flutter/foundation.dart';
import 'dart:convert';
import 'package:ai_detection/core/models/detection_model.dart';
import 'package:ai_detection/core/services/storage_service.dart';

class DetectionService extends ChangeNotifier {
  final List<DetectionModel> _detections = [];

  List<DetectionModel> get detections => List.unmodifiable(_detections);
  List<DetectionModel> get recentDetections => List.unmodifiable(
        _detections.toList()..sort((a, b) => b.date.compareTo(a.date)),
      );

  int get totalInfected => _detections.length;
  int get totalHealthy => 0;

  DetectionService() {
    _loadDetections();
  }

  Future<void> _loadDetections() async {
    final detectionsJson = StorageService.instance.getString('detections');
    if (detectionsJson != null) {
      final List<dynamic> decoded = jsonDecode(detectionsJson);
      _detections.clear();
      _detections.addAll(
        decoded.map((d) => DetectionModel.fromJson(d as Map<String, dynamic>)),
      );
      notifyListeners();
    }
  }

  Future<void> _saveDetections() async {
    final encoded = jsonEncode(_detections.map((d) => d.toJson()).toList());
    await StorageService.instance.saveString('detections', encoded);
    notifyListeners();
  }

  Future<DetectionModel> detectDisease(String imagePath) async {
    await Future.delayed(const Duration(seconds: 1));
    final mockDiseases = [
      'Leaf Blight',
      'Powdery Mildew',
      'Rust',
      'Bacterial Spot',
      'Fungal Infection',
    ];
    final mockTreatments = [
      'Spray fungicide ABC once a week for 2 weeks.',
      'Apply copper-based fungicide every 10 days.',
      'Remove infected leaves and apply neem oil.',
      'Use systemic fungicide and improve air circulation.',
      'Apply sulfur-based treatment and reduce humidity.',
    ];
    final random = DateTime.now().millisecondsSinceEpoch % mockDiseases.length;
    final detection = DetectionModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      diseaseName: mockDiseases[random],
      confidence: 0.75 + (random * 0.15),
      treatment: mockTreatments[random],
      date: DateTime.now(),
      imagePath: imagePath,
    );
    return detection;
  }

  Future<void> saveDetection(DetectionModel detection, {String? farmId}) async {
    final updated = DetectionModel(
      id: detection.id,
      diseaseName: detection.diseaseName,
      confidence: detection.confidence,
      treatment: detection.treatment,
      date: detection.date,
      imagePath: detection.imagePath,
      farmId: farmId,
    );
    _detections.add(updated);
    await _saveDetections();
  }

  List<Map<String, dynamic>> getWeeklyStats() {
    final now = DateTime.now();
    final stats = <Map<String, dynamic>>[];
    for (int i = 6; i >= 0; i--) {
      final date = now.subtract(Duration(days: i));
      final dayDetections = _detections.where((d) {
        return d.date.year == date.year &&
            d.date.month == date.month &&
            d.date.day == date.day;
      }).length;
      stats.add({
        'date': date,
        'infected': dayDetections,
        'healthy': 0,
      });
    }
    return stats;
  }
}


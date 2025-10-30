class DiseaseDiagnosis {
  DiseaseDiagnosis({
    required this.disease,
    required this.confidence,
    required this.description,
    required this.recommendations,
    required this.label,
  });

  final String disease;
  final double confidence;
  final String description;
  final List<String> recommendations;
  final String label;

  factory DiseaseDiagnosis.fromJson(Map<String, dynamic> json) {
    final recommendations = (json['recommendations'] as List?)
            ?.map((entry) => entry.toString())
            .toList() ??
        <String>[];

    return DiseaseDiagnosis(
      disease: (json['disease'] ?? json['prediction'] ?? json['label'] ?? 'Unknown disease').toString(),
      confidence: _parseConfidence(json['confidence'] ?? json['probability']),
      description: (json['description'] ?? json['details'] ?? 'Không có mô tả chi tiết cho bệnh này.').toString(),
      recommendations: recommendations,
      label: (json['label'] ?? json['class'] ?? json['disease']).toString(),
    );
  }

  static double _parseConfidence(dynamic value) {
    if (value == null) {
      return 0.0;
    }
    if (value is num) {
      final num confidence = value;
      return confidence.toDouble();
    }
    final parsed = double.tryParse(value.toString());
    return parsed ?? 0.0;
  }
}

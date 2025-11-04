class DetectionModel {
  final String id;
  final String diseaseName;
  final double confidence;
  final String treatment;
  final DateTime date;
  final String? imagePath;
  final String? farmId;

  DetectionModel({
    required this.id,
    required this.diseaseName,
    required this.confidence,
    required this.treatment,
    required this.date,
    this.imagePath,
    this.farmId,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'diseaseName': diseaseName,
        'confidence': confidence,
        'treatment': treatment,
        'date': date.toIso8601String(),
        'imagePath': imagePath,
        'farmId': farmId,
      };

  factory DetectionModel.fromJson(Map<String, dynamic> json) => DetectionModel(
        id: json['id'] as String,
        diseaseName: json['diseaseName'] as String,
        confidence: (json['confidence'] as num).toDouble(),
        treatment: json['treatment'] as String,
        date: DateTime.parse(json['date'] as String),
        imagePath: json['imagePath'] as String?,
        farmId: json['farmId'] as String?,
      );
}


class FarmModel {
  final String id;
  final String name;
  final String location;
  final String cropType;
  final List<PlantModel> plants;

  FarmModel({
    required this.id,
    required this.name,
    required this.location,
    required this.cropType,
    required this.plants,
  });

  int get totalPlants => plants.length;
  int get infectedPlants => plants.where((p) => p.status == PlantStatus.infected).length;
  int get healthyPlants => plants.where((p) => p.status == PlantStatus.healthy).length;

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'location': location,
        'cropType': cropType,
        'plants': plants.map((p) => p.toJson()).toList(),
      };

  factory FarmModel.fromJson(Map<String, dynamic> json) => FarmModel(
        id: json['id'] as String,
        name: json['name'] as String,
        location: json['location'] as String,
        cropType: json['cropType'] as String,
        plants: (json['plants'] as List<dynamic>)
            .map((p) => PlantModel.fromJson(p as Map<String, dynamic>))
            .toList(),
      );
}

enum PlantStatus { healthy, infected }

class PlantModel {
  final String id;
  final String name;
  final String imagePath;
  final PlantStatus status;
  final DateTime createdAt;

  PlantModel({
    required this.id,
    required this.name,
    required this.imagePath,
    required this.status,
    required this.createdAt,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'imagePath': imagePath,
        'status': status.name,
        'createdAt': createdAt.toIso8601String(),
      };

  factory PlantModel.fromJson(Map<String, dynamic> json) => PlantModel(
        id: json['id'] as String,
        name: json['name'] as String? ?? 'Plant ${json['id']}',
        imagePath: json['imagePath'] as String,
        status: PlantStatus.values.firstWhere(
          (e) => e.name == json['status'],
          orElse: () => PlantStatus.healthy,
        ),
        createdAt: DateTime.parse(json['createdAt'] as String),
      );
}


import 'package:flutter/foundation.dart';
import 'dart:convert';
import 'package:ai_detection/core/models/farm_model.dart';
import 'package:ai_detection/core/services/storage_service.dart';

class FarmService extends ChangeNotifier {
  final List<FarmModel> _farms = [];

  List<FarmModel> get farms => List.unmodifiable(_farms);

  FarmService() {
    _loadFarms();
    if (_farms.isEmpty) {
      _initializeMockData();
    }
  }

  Future<void> _loadFarms() async {
    final farmsJson = StorageService.instance.getString('farms');
    if (farmsJson != null) {
      final List<dynamic> decoded = jsonDecode(farmsJson);
      _farms.clear();
      _farms.addAll(
        decoded.map((f) => FarmModel.fromJson(f as Map<String, dynamic>)),
      );
      notifyListeners();
    }
  }

  Future<void> _saveFarms() async {
    final encoded = jsonEncode(_farms.map((f) => f.toJson()).toList());
    await StorageService.instance.saveString('farms', encoded);
    notifyListeners();
  }

  void _initializeMockData() {
    _farms.addAll([
      FarmModel(
        id: '1',
        name: 'Rice Field A',
        location: 'Northern Region',
        cropType: 'Rice',
        plants: List.generate(120, (i) => PlantModel(
          id: 'p1_$i',
          name: 'Rice Plant ${i + 1}',
          imagePath: '',
          status: i < 8 ? PlantStatus.infected : PlantStatus.healthy,
          createdAt: DateTime.now().subtract(Duration(days: i % 30)),
        )),
      ),
      FarmModel(
        id: '2',
        name: 'Strawberry Field',
        location: 'Western Region',
        cropType: 'Strawberry',
        plants: List.generate(75, (i) => PlantModel(
          id: 'p2_$i',
          name: 'Strawberry Plant ${i + 1}',
          imagePath: '',
          status: i < 3 ? PlantStatus.infected : PlantStatus.healthy,
          createdAt: DateTime.now().subtract(Duration(days: i % 20)),
        )),
      ),
    ]);
    _saveFarms();
  }

  Future<void> addFarm(String name, String location, String cropType) async {
    final farm = FarmModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: name,
      location: location,
      cropType: cropType,
      plants: [],
    );
    _farms.add(farm);
    await _saveFarms();
  }

  FarmModel? getFarmById(String id) {
    try {
      return _farms.firstWhere((f) => f.id == id);
    } catch (_) {
      return null;
    }
  }

  Future<void> addPlantToFarm(String farmId, String name, String imagePath, PlantStatus status) async {
    final farmIndex = _farms.indexWhere((f) => f.id == farmId);
    if (farmIndex == -1) return;
    final farm = _farms[farmIndex];
    final plant = PlantModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: name,
      imagePath: imagePath,
      status: status,
      createdAt: DateTime.now(),
    );
    final updatedPlants = [...farm.plants, plant];
    _farms[farmIndex] = FarmModel(
      id: farm.id,
      name: farm.name,
      location: farm.location,
      cropType: farm.cropType,
      plants: updatedPlants,
    );
    await _saveFarms();
  }

  Future<void> deletePlant(String farmId, String plantId) async {
    final farmIndex = _farms.indexWhere((f) => f.id == farmId);
    if (farmIndex == -1) return;
    final farm = _farms[farmIndex];
    final updatedPlants = farm.plants.where((p) => p.id != plantId).toList();
    _farms[farmIndex] = FarmModel(
      id: farm.id,
      name: farm.name,
      location: farm.location,
      cropType: farm.cropType,
      plants: updatedPlants,
    );
    await _saveFarms();
  }

  Future<void> deleteFarm(String farmId) async {
    _farms.removeWhere((f) => f.id == farmId);
    await _saveFarms();
  }

  Future<void> updatePlantStatus(String farmId, String plantId, PlantStatus newStatus) async {
    final farmIndex = _farms.indexWhere((f) => f.id == farmId);
    if (farmIndex == -1) return;
    final farm = _farms[farmIndex];
    final updatedPlants = farm.plants.map((p) {
      if (p.id == plantId) {
        return PlantModel(
          id: p.id,
          name: p.name,
          imagePath: p.imagePath,
          status: newStatus,
          createdAt: p.createdAt,
        );
      }
      return p;
    }).toList();
    _farms[farmIndex] = FarmModel(
      id: farm.id,
      name: farm.name,
      location: farm.location,
      cropType: farm.cropType,
      plants: updatedPlants,
    );
    await _saveFarms();
  }
}


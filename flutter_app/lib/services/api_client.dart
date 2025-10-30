import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../models/disease_diagnosis.dart';

class ApiClient {
  ApiClient({
    http.Client? client,
    String? baseUrl,
    this.diagnosisPath = '/predict',
  })  : _client = client ?? http.Client(),
        baseUrl = baseUrl ?? const String.fromEnvironment(
          'API_BASE_URL',
          defaultValue: 'http://localhost:8000',
        );

  final http.Client _client;
  final String baseUrl;
  final String diagnosisPath;

  Uri get _diagnosisUri => Uri.parse(baseUrl + diagnosisPath);

  Future<DiseaseDiagnosis> diagnosePlant(File imageFile) async {
    final request = http.MultipartRequest('POST', _diagnosisUri)
      ..files.add(await http.MultipartFile.fromPath('image', imageFile.path));

    final streamedResponse = await _client.send(request);

    if (streamedResponse.statusCode < 200 || streamedResponse.statusCode >= 300) {
      final responseBody = await streamedResponse.stream.bytesToString();
      throw HttpException(
        'API trả về lỗi: ${streamedResponse.statusCode} - $responseBody',
        uri: _diagnosisUri,
      );
    }

    final response = await http.Response.fromStream(streamedResponse);
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return DiseaseDiagnosis.fromJson(data);
  }

  void close() {
    _client.close();
  }
}

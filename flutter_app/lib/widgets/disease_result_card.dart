import 'package:flutter/material.dart';

import '../models/disease_diagnosis.dart';

class DiseaseResultCard extends StatelessWidget {
  const DiseaseResultCard({super.key, required this.result});

  final DiseaseDiagnosis result;

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      elevation: 4,
      margin: const EdgeInsets.symmetric(vertical: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              result.disease,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Icon(Icons.verified, color: Colors.green),
                const SizedBox(width: 8),
                Text('Độ tin cậy: ${(result.confidence * 100).toStringAsFixed(1)}%'),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              result.description,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            if (result.recommendations.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(
                'Khuyến nghị xử lý',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 8),
              ...result.recommendations.map(
                (recommendation) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('• '),
                      Expanded(child: Text(recommendation)),
                    ],
                  ),
                ),
              ),
            ] else ...[
              const SizedBox(height: 16),
              Text(
                'Chưa có khuyến nghị cụ thể. Vui lòng tham khảo chuyên gia nông nghiệp.',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ],
          ],
        ),
      ),
    );
  }
}

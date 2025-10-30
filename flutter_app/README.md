# Plant Disease Doctor (Flutter)

Ứng dụng Flutter nhỏ giúp kết nối tới server API hiện có để nhận diện bệnh trên cây trồng.

## Tính năng chính
- Chọn ảnh từ thư viện hoặc chụp trực tiếp bằng camera.
- Gửi ảnh lên API `/predict` để nhận kết quả phân loại bệnh.
- Hiển thị mô tả bệnh, độ tin cậy và danh sách khuyến nghị xử lý/thuốc bảo vệ thực vật.

## Cấu hình
Mặc định ứng dụng gọi tới `http://localhost:8000/predict`. Để đổi URL hãy cung cấp biến biên dịch:

```sh
flutter run --dart-define=API_BASE_URL=https://your-domain.com
```

Nếu backend sử dụng đường dẫn khác, truyền thêm tham số `diagnosisPath` khi khởi tạo `ApiClient`.

## Chạy ứng dụng
1. Cài đặt Flutter SDK và cấu hình thiết bị ảo/thật.
2. Cài đặt dependencies:
   ```sh
   flutter pub get
   ```
3. Chạy ứng dụng:
   ```sh
   flutter run
   ```

## Cấu trúc thư mục
```
flutter_app/
 ├─ lib/
 │   ├─ main.dart                # UI chính
 │   ├─ models/disease_diagnosis.dart
 │   ├─ services/api_client.dart
 │   └─ widgets/disease_result_card.dart
 ├─ pubspec.yaml
 └─ README.md
```

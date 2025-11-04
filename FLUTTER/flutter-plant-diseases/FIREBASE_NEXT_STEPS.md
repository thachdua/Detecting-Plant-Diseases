# Firebase Next Steps - Đã hoàn thành các bước cấu hình

## ✅ Đã hoàn thành:

1. ✅ **Cấu hình Android build.gradle**
   - Đã thêm Google Services plugin vào `android/build.gradle.kts`
   - Đã thêm Firebase dependencies vào `android/app/build.gradle.kts`
   - Đã thêm plugin `com.google.gms.google-services` vào app

2. ✅ **Cấu hình Permissions**
   - Đã thêm location permissions vào `AndroidManifest.xml`
   - Đã thêm Google Maps API key vào `AndroidManifest.xml`

3. ✅ **Dependencies đã được cài đặt**
   - Đã chạy `flutter pub get` thành công

## 🔧 Bước tiếp theo (cần làm thủ công):

### 1. Enable Firebase Services trong Firebase Console

Truy cập [Firebase Console](https://console.firebase.google.com/) và enable các services sau:

#### Authentication:
1. Vào **Authentication** > **Get started**
2. Enable **Email/Password** provider
3. Click **Save**

#### Firestore Database:
1. Vào **Firestore Database** > **Create database**
2. Chọn **Start in test mode** (hoặc production mode nếu muốn)
3. Chọn location gần bạn nhất
4. Click **Enable**

#### Storage:
1. Vào **Storage** > **Get started**
2. Chọn **Start in test mode** (hoặc production mode)
3. Click **Next** và chọn location
4. Click **Done**

### 2. Kiểm tra google-services.json

Đảm bảo file `android/app/google-services.json` đã được đặt đúng vị trí và có nội dung hợp lệ.

### 3. Test app

Sau khi enable các services, chạy app:
```bash
flutter clean
flutter pub get
flutter run
```

## 📝 Lưu ý:

- Nếu gặp lỗi về Firebase initialization, kiểm tra lại:
  - File `google-services.json` đã đặt đúng chưa
  - Package name trong Firebase Console khớp với `applicationId` trong `build.gradle.kts`
  - Đã enable đủ các services cần thiết

- Code hiện tại đã được cấu hình để sử dụng Firebase, nhưng vẫn có thể chạy với mock data nếu Firebase chưa được enable.


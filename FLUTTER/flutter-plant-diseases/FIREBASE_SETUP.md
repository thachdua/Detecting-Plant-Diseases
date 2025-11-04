# Firebase Setup Guide

## 1. Tạo Firebase Project

1. Truy cập [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Nhập tên project và làm theo hướng dẫn
4. Enable Google Analytics (optional)

## 2. Thêm Android App vào Firebase

1. Trong Firebase Console, click "Add app" > Android
2. Nhập package name: `com.example.ai_detection` (hoặc package name của bạn)
3. Download file `google-services.json`
4. Đặt file vào `android/app/google-services.json`

## 3. Cấu hình Android

Thêm vào `android/build.gradle` (project level):

```gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
    }
}
```

Thêm vào `android/app/build.gradle` (app level):

```gradle
plugins {
    id 'com.android.application'
    id 'com.google.gms.google-services'
}

dependencies {
    implementation platform('com.google.firebase:firebase-bom:32.7.0')
}
```

## 3. Cấu hình Google Maps

1. Trong Firebase Console, vào "APIs & Services" > "Credentials"
2. Tạo API Key cho Google Maps
3. Thêm vào `android/app/src/main/AndroidManifest.xml`:

```xml
<application>
    <meta-data
        android:name="com.google.android.geo.API_KEY"
        android:value="YOUR_API_KEY_HERE"/>
</application>
```

## 4. Cấu hình Permissions

Thêm vào `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
```

## 5. Enable Firebase Services

Trong Firebase Console, enable:
- Authentication (Email/Password)
- Firestore Database
- Storage

## 6. Chạy lệnh

```bash
flutter pub get
flutter run
```


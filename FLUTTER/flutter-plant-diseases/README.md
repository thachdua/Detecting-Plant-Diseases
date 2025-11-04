# AI Plant Disease Detection App

A Flutter application for detecting plant diseases using AI technology.

## Features

- **Authentication**: Login and Register screens
- **Dashboard**: Overall statistics with charts showing infected vs healthy plants
- **Disease Detection**: Capture or upload plant images for AI-powered disease detection
- **Farm Management**: Manage multiple farms and track plant health status
- **Local Storage**: All data persists using SharedPreferences

## Getting Started

### Prerequisites

- Flutter SDK (>=3.0.0)
- Dart SDK

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Run the app:
   ```bash
   flutter run
   ```

## Project Structure

```
lib/
├── core/
│   ├── models/          # Data models
│   ├── routes/          # Navigation routes
│   ├── services/        # Business logic services
│   └── theme/           # App theming
├── features/
│   ├── auth/            # Authentication screens
│   ├── dashboard/       # Dashboard screen and widgets
│   ├── detection/       # Disease detection screen
│   └── farm/            # Farm management screens
```

## Usage

1. Register a new account or login
2. View dashboard statistics
3. Use the Detection screen to analyze plant images
4. Manage farms and track plant health in Farm Management

## Mock API

The app uses mock AI detection service that simulates:
- POST /api/detect - Returns disease name, confidence score, and treatment recommendation

## Technologies Used

- Flutter
- Provider (State Management)
- SharedPreferences (Local Storage)
- Image Picker
- FL Chart (Charts)
- Material Design 3


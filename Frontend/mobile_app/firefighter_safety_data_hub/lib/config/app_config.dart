import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

class AppConfig {
  static const String port = String.fromEnvironment(
    'API_PORT',
    defaultValue: '8000',
  );

  /// Override for a physical phone or remote developer backend:
  /// flutter run --dart-define=API_BASE_URL=http://192.168.1.10:8000
  static const String configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );

  /// Android **emulator** → backend on your dev machine (not localhost from the emulator).
  static const String baseUrlAndroidEmulator = 'http://10.0.2.2:$port';

  /// iOS **simulator** / desktop → backend on same machine.
  static const String baseUrlLoopback = 'http://127.0.0.1:$port';

  /// Local-first runtime URL with a dart-define escape hatch.
  ///
  /// - Local Flutter Web (localhost) talks to the local FastAPI backend on 8000.
  /// - A hosted Flutter Web build talks to the API on the same public origin.
  /// - `API_BASE_URL` can always override either behavior.
  static String get baseUrl {
    final override = configuredBaseUrl.trim().replaceAll(RegExp(r'/$'), '');
    if (override.isNotEmpty) return override;

    if (kIsWeb) {
      final host = Uri.base.host.toLowerCase();
      if (host == 'localhost' || host == '127.0.0.1') {
        return baseUrlLoopback;
      }
      return Uri.base.origin;
    }

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return baseUrlAndroidEmulator;
      case TargetPlatform.iOS:
        return baseUrlLoopback;
      default:
        return baseUrlLoopback;
    }
  }

  static String get authEndpoint => '$baseUrl/api/v1/auth';
  static String get loginUrl => '$authEndpoint/login';
  static String get signupUrl => '$authEndpoint/register';
  static String get passwordResetUrl => '$authEndpoint/password-reset';

  static String get forgotPasswordRequestUrl =>
      '$authEndpoint/forgot-password/request';

  static String get forgotPasswordConfirmUrl =>
      '$authEndpoint/forgot-password/confirm';

  static String get verifyEmailUrl => '$authEndpoint/verify-email';
  static String get resendVerificationUrl => '$authEndpoint/resend-verification';
  static String get deleteAccountUrl => '$authEndpoint/delete-account';

  static String get locationUploadUrl => '$baseUrl/api/v1/locationEntries/';
  static String get locationHistoryUrl => '$baseUrl/api/v1/locationEntries/last';
  static String get smokeSamplerUrl => '$baseUrl/api/v1/smokeSampler/';
  static String get dataTransferBaseUrl => '$baseUrl/api/v1/data-transfer';
  static String get ppeSubmitUrl => '$dataTransferBaseUrl/ppe';
  static String get logEventSubmitUrl => '$dataTransferBaseUrl/logevent';
}

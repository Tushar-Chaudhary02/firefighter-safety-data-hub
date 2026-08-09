import 'dart:convert';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:logger/logger.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite/sqflite.dart';

import '../debug/debug.dart';
import '../models/location_entry_model.dart';

/// Stores location entries locally.
///
/// Native/mobile builds use SQLite. Chrome/web builds use SharedPreferences,
/// so `flutter run -d chrome` can exercise location-history flows without a
/// separate web SQLite plugin.
class LocationStorageService {
  static final LocationStorageService _instance =
      LocationStorageService._internal();

  factory LocationStorageService() => _instance;

  LocationStorageService._internal();

  Database? _database;
  final logger = Logger();

  String _webStorageKey(String userKey) => 'location_entries_$userKey';

  Future<List<LocationEntry>> _getWebEntries(String userKey) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_webStorageKey(userKey));
    if (raw == null || raw.isEmpty) return [];

    try {
      final decoded = jsonDecode(raw);
      if (decoded is! List) return [];

      final entries = decoded
          .whereType<Map<String, dynamic>>()
          .map(LocationEntry.fromMap)
          .toList();
      entries.sort((a, b) => a.timestamp.compareTo(b.timestamp));
      return entries;
    } catch (_) {
      return [];
    }
  }

  Future<void> _setWebEntries(
    String userKey,
    List<LocationEntry> entries,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(
      _webStorageKey(userKey),
      jsonEncode(entries.map((entry) => entry.toMap()).toList()),
    );
  }

  Future<Database> _initDb() async {
    final dir = await getApplicationDocumentsDirectory();
    final dbPath = p.join(dir.path, 'location_entries.db');

    Log.success('Initialized database!');

    return openDatabase(
      dbPath,
      version: 2,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE locations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TEXT NOT NULL,
            accuracy REAL,
            altitude REAL
          )
        ''');
      },
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await db.execute('ALTER TABLE locations ADD COLUMN user_key TEXT;');
          await db.execute(
            "UPDATE locations SET user_key = 'unknown' WHERE user_key IS NULL;",
          );
        }
      },
    );
  }

  Future<Database> get _db async {
    if (_database != null) return _database!;
    _database = await _initDb();
    return _database!;
  }

  Future<void> insert(LocationEntry entry, {required String userKey}) async {
    if (kIsWeb) {
      final entries = await _getWebEntries(userKey);
      entries.add(entry);
      await _setWebEntries(userKey, entries);
      return;
    }

    final db = await _db;
    await db.insert(
      'locations',
      entry.toMap()
        ..remove('id')
        ..['user_key'] = userKey,
    );
  }

  Future<List<LocationEntry>> getLastEntries(
    int limit, {
    required String userKey,
  }) async {
    if (kIsWeb) {
      final entries = await _getWebEntries(userKey);
      return entries.reversed.take(limit).toList();
    }

    final db = await _db;
    final rows = await db.query(
      'locations',
      where: 'user_key = ?',
      whereArgs: [userKey],
      orderBy: 'timestamp DESC',
      limit: limit,
    );

    Log.info('Retrieved last ${rows.length} location entries.');
    return rows.map(LocationEntry.fromMap).toList();
  }

  Future<List<LocationEntry>> getAllEntries({required String userKey}) async {
    if (kIsWeb) {
      return _getWebEntries(userKey);
    }

    final db = await _db;
    final rows = await db.query(
      'locations',
      where: 'user_key = ?',
      whereArgs: [userKey],
      orderBy: 'timestamp ASC',
    );
    return rows.map(LocationEntry.fromMap).toList();
  }

  Future<void> clearAll({required String userKey}) async {
    if (kIsWeb) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_webStorageKey(userKey));
      return;
    }

    final db = await _db;
    await db.delete(
      'locations',
      where: 'user_key = ?',
      whereArgs: [userKey],
    );
    Log.info('Cleared all location entries from the database.');
  }
}

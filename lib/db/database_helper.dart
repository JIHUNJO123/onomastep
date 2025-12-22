import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/word.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('onomatopoeia.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 2,
      onCreate: _createDB,
      onUpgrade: _upgradeDB,
    );
  }

  Future _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE words (
        id INTEGER PRIMARY KEY,
        word TEXT NOT NULL,
        kanji TEXT,
        hiragana TEXT,
        level TEXT NOT NULL,
        partOfSpeech TEXT NOT NULL,
        definition TEXT NOT NULL,
        example TEXT NOT NULL,
        category TEXT DEFAULT 'Others',
        isFavorite INTEGER DEFAULT 0,
        translations TEXT
      )
    ''');

    await db.execute('''
      CREATE TABLE translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wordId INTEGER NOT NULL,
        languageCode TEXT NOT NULL,
        fieldType TEXT NOT NULL,
        translatedText TEXT NOT NULL,
        createdAt INTEGER NOT NULL,
        UNIQUE(wordId, languageCode, fieldType)
      )
    ''');

    await db.execute('''
      CREATE INDEX idx_translations_lookup
      ON translations(wordId, languageCode, fieldType)
    ''');

    await _loadInitialData(db);
  }

  Future _upgradeDB(Database db, int oldVersion, int newVersion) async {
    await db.execute('DROP TABLE IF EXISTS words');
    await db.execute('DROP TABLE IF EXISTS translations');
    await _createDB(db, newVersion);
  }

  Future<void> _loadInitialData(Database db) async {
    try {
      final jsonFiles = ['assets/data/onomatopoeia.json'];

      int totalWords = 0;
      for (final filePath in jsonFiles) {
        try {
          final String response = await rootBundle.loadString(filePath);
          final List<dynamic> data = json.decode(response);

          for (var wordJson in data) {
            Map<String, dynamic>? translationsMap;

            // Format 1: translations object
            if (wordJson['translations'] != null) {
              translationsMap = Map<String, dynamic>.from(
                wordJson['translations'],
              );
            }

            // Format 2: definition_ko, example_ko format
            final langCodes = ['ko', 'zh', 'es', 'fr', 'de', 'pt', 'vi', 'ar', 'th', 'ru'];
            for (final lang in langCodes) {
              final defKey = 'definition_$lang';
              final exKey = 'example_$lang';
              if (wordJson[defKey] != null || wordJson[exKey] != null) {
                translationsMap ??= {};
                translationsMap[lang] = {
                  'definition': wordJson[defKey]?.toString() ?? '',
                  'example': wordJson[exKey]?.toString() ?? '',
                };
              }
            }

            // Format 3: korean, chinese, spanish fields (Onomatopoeia JSON format)
            if (wordJson['korean'] != null) {
              translationsMap ??= {};
              translationsMap['ko'] = {
                'definition': wordJson['korean']?.toString() ?? '',
                'example': wordJson['example_ko']?.toString() ?? '',
              };
            }
            if (wordJson['chinese'] != null) {
              translationsMap ??= {};
              translationsMap['zh'] = {
                'definition': wordJson['chinese']?.toString() ?? '',
                'example': wordJson['example_zh']?.toString() ?? '',
              };
            }
            if (wordJson['spanish'] != null) {
              translationsMap ??= {};
              translationsMap['es'] = {
                'definition': wordJson['spanish']?.toString() ?? '',
                'example': wordJson['example_es']?.toString() ?? '',
              };
            }

            String? translationsJson;
            if (translationsMap != null && translationsMap.isNotEmpty) {
              translationsJson = json.encode(translationsMap);
            }

            await db.insert('words', {
              'id': wordJson['id'],
              'word': wordJson['word'] ?? '',
              'kanji': wordJson['kanji'] ?? wordJson['word'] ?? '',
              'hiragana': wordJson['hiragana'] ?? wordJson['reading'] ?? '',
              'level': wordJson['category'] ?? 'Others',
              'partOfSpeech': wordJson['partOfSpeech'] ?? 'onomatopoeia',
              'definition': wordJson['definition'] ?? '',
              'example': wordJson['example'] ?? '',
              'category': wordJson['category'] ?? 'Others',
              'isFavorite': 0,
              'translations': translationsJson,
            });
          }
          totalWords += data.length;
          print('Loaded $totalWords words with translations from $filePath');
        } catch (e) {
          print('Error loading $filePath: $e');
        }
      }
      print('Loaded total $totalWords onomatopoeia words');
    } catch (e) {
      print('Error loading initial data: $e');
    }
  }

  Future<String?> getTranslation(
    int wordId,
    String languageCode,
    String fieldType,
  ) async {
    final db = await instance.database;
    final result = await db.query(
      'translations',
      columns: ['translatedText'],
      where: 'wordId = ? AND languageCode = ? AND fieldType = ?',
      whereArgs: [wordId, languageCode, fieldType],
    );
    if (result.isNotEmpty) {
      return result.first['translatedText'] as String;
    }
    return null;
  }

  Future<void> saveTranslation(
    int wordId,
    String languageCode,
    String fieldType,
    String translatedText,
  ) async {
    final db = await instance.database;
    await db.insert('translations', {
      'wordId': wordId,
      'languageCode': languageCode,
      'fieldType': fieldType,
      'translatedText': translatedText,
      'createdAt': DateTime.now().millisecondsSinceEpoch,
    }, conflictAlgorithm: ConflictAlgorithm.replace);
  }

  Future<void> clearTranslations(String languageCode) async {
    final db = await instance.database;
    await db.delete(
      'translations',
      where: 'languageCode = ?',
      whereArgs: [languageCode],
    );
  }

  Future<void> clearAllTranslations() async {
    final db = await instance.database;
    await db.delete('translations');
  }

  Future<List<Word>> getAllWords() async {
    final db = await instance.database;
    final result = await db.query('words', orderBy: 'word ASC');
    return result.map((json) => Word.fromDb(json)).toList();
  }

  Future<List<Word>> getWordsByLevel(String level) async {
    final db = await instance.database;
    final result = await db.query(
      'words',
      where: 'category = ?',
      whereArgs: [level],
      orderBy: 'word ASC',
    );
    return result.map((json) => Word.fromDb(json)).toList();
  }

  Future<List<Word>> getWordsByCategory(String category) async {
    final db = await instance.database;
    final result = await db.query(
      'words',
      where: 'category = ?',
      whereArgs: [category],
      orderBy: 'word ASC',
    );
    return result.map((json) => Word.fromDb(json)).toList();
  }

  Future<List<String>> getAllCategories() async {
    final db = await instance.database;
    final result = await db.rawQuery(
      'SELECT DISTINCT category FROM words ORDER BY category ASC',
    );
    return result.map((row) => row['category'] as String).toList();
  }

  Future<List<Word>> getFavorites() async {
    final db = await instance.database;
    final result = await db.query(
      'words',
      where: 'isFavorite = ?',
      whereArgs: [1],
      orderBy: 'word ASC',
    );
    return result.map((json) => Word.fromDb(json)).toList();
  }

  Future<List<Word>> searchWords(String query) async {
    final db = await instance.database;
    final result = await db.query(
      'words',
      where: 'word LIKE ? OR definition LIKE ? OR hiragana LIKE ?',
      whereArgs: ['%$query%', '%$query%', '%$query%'],
      orderBy: 'word ASC',
    );
    return result.map((json) => Word.fromDb(json)).toList();
  }

  Future<void> toggleFavorite(int id, bool isFavorite) async {
    final db = await instance.database;
    await db.update(
      'words',
      {'isFavorite': isFavorite ? 1 : 0},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<Word?> getWordById(int id) async {
    final db = await instance.database;
    final result = await db.query('words', where: 'id = ?', whereArgs: [id]);
    if (result.isEmpty) return null;
    return Word.fromDb(result.first);
  }

  Future<Word?> getRandomWord() async {
    final db = await instance.database;
    final result = await db.rawQuery(
      'SELECT * FROM words ORDER BY RANDOM() LIMIT 1',
    );
    if (result.isEmpty) return null;
    return Word.fromDb(result.first);
  }

  List<Word>? _jsonWordsCache;

  void clearJsonCache() {
    _jsonWordsCache = null;
  }

  Future<List<Word>> _loadWordsFromJson() async {
    try {
      final List<Word> allWords = [];
      final jsonFiles = ['assets/data/onomatopoeia.json'];

      for (final file in jsonFiles) {
        try {
          print('Loading JSON file: $file');
          final String response = await rootBundle.loadString(file);
          final List<dynamic> data = json.decode(response);
          final words = data.map((json) => Word.fromJson(json)).toList();
          print('  Loaded ${words.length} words from $file');
          allWords.addAll(words);
        } catch (e) {
          print('Error loading $file: $e');
        }
      }

      print('Total JSON words loaded: ${allWords.length}');
      _jsonWordsCache = allWords;
      return allWords;
    } catch (e) {
      print('Error loading JSON words: $e');
      return [];
    }
  }

  Word? _findWordWithTranslation(List<Word> jsonWords, Word dbWord) {
    final matches =
        jsonWords
            .where((w) => w.word.toLowerCase() == dbWord.word.toLowerCase())
            .toList();

    if (matches.isEmpty) return null;

    for (final word in matches) {
      if (word.translations != null && word.translations!.isNotEmpty) {
        return word;
      }
    }
    return matches.first;
  }

  Future<List<Word>> getWordsWithTranslations() async {
    final db = await instance.database;
    final dbResult = await db.query('words', orderBy: 'word ASC');
    final dbWords = dbResult.map((json) => Word.fromDb(json)).toList();
    final jsonWords = await _loadWordsFromJson();
    return dbWords.map((dbWord) {
      final jsonWord = _findWordWithTranslation(jsonWords, dbWord) ?? dbWord;
      return dbWord.copyWith(translations: jsonWord.translations);
    }).toList();
  }

  Future<Word?> getTodayWord() async {
    try {
      final db = await instance.database;
      final today = DateTime.now();
      final seed = today.year * 10000 + today.month * 100 + today.day;
      final count =
          Sqflite.firstIntValue(
            await db.rawQuery('SELECT COUNT(*) FROM words'),
          ) ??
          0;

      if (count == 0) {
        print('No words in database');
        return null;
      }

      final index = seed % count;

      final result = await db.rawQuery('SELECT * FROM words LIMIT 1 OFFSET ?', [
        index,
      ]);
      if (result.isEmpty) return null;

      final dbWord = Word.fromDb(result.first);
      final jsonWords = await _loadWordsFromJson();
      final jsonWord = _findWordWithTranslation(jsonWords, dbWord);
      final finalWord = jsonWord ?? dbWord;
      return dbWord.copyWith(translations: finalWord.translations);
    } catch (e) {
      print('Error getting today word: $e');
      return null;
    }
  }

  Future<Map<String, int>> getWordCountByLevel() async {
    final db = await instance.database;
    final result = await db.rawQuery(
      'SELECT category, COUNT(*) as count FROM words GROUP BY category',
    );
    final Map<String, int> counts = {};
    for (var row in result) {
      counts[row['category'] as String] = row['count'] as int;
    }
    return counts;
  }

  Future<Word> applyTranslations(Word word, String languageCode) async {
    if (languageCode == 'en') return word;

    final translatedDef = await getTranslation(
      word.id,
      languageCode,
      'definition',
    );
    final translatedEx = await getTranslation(word.id, languageCode, 'example');

    return word.copyWith(
      translatedDefinition: translatedDef,
      translatedExample: translatedEx,
    );
  }

  Future<List<Word>> applyTranslationsToList(
    List<Word> words,
    String languageCode,
  ) async {
    if (languageCode == 'en') return words;

    final result = <Word>[];
    for (final word in words) {
      result.add(await applyTranslations(word, languageCode));
    }
    return result;
  }

  Future close() async {
    final db = await instance.database;
    db.close();
  }
}

import sqlite3
import json

# Load words from JSON
with open('assets/data/words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print(f"Loaded {len(words)} words from JSON")

# Check level distribution in JSON
levels = {}
for word in words:
    level = word.get('level', 'Unknown')
    levels[level] = levels.get(level, 0) + 1
print(f"JSON level distribution: {levels}")

# Create database
conn = sqlite3.connect('assets/data/prebuilt_words.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        definition TEXT NOT NULL,
        example TEXT NOT NULL,
        partOfSpeech TEXT NOT NULL,
        level TEXT NOT NULL,
        isFavorite INTEGER DEFAULT 0,
        translations TEXT
    )
''')

# Insert words
for word in words:
    cursor.execute('''
        INSERT INTO words (word, definition, example, partOfSpeech, level, isFavorite, translations)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        word['word'],
        word['definition'],
        word['example'],
        word['partOfSpeech'],
        word['level'],
        0,
        json.dumps(word.get('translations', {}))
    ))

conn.commit()

# Verify
cursor.execute("SELECT level, COUNT(*) FROM words GROUP BY level")
print(f"DB level distribution: {cursor.fetchall()}")

cursor.execute("SELECT COUNT(*) FROM words")
print(f"Total words in DB: {cursor.fetchone()[0]}")

conn.close()
print("Database created successfully!")

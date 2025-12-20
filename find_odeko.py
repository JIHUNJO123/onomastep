import json

with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print("=== 凸 또는 forehead 관련 단어 ===")
for w in words:
    word = w.get('word', '')
    defn = w.get('definition', '').lower()
    if '凸' in word or 'forehead' in defn or 'おでこ' in word or 'オデコ' in word:
        print(f"ID: {w['id']}, Word: {w['word']}, Level: {w['level']}, Def: {w['definition']}")

import json

with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

n5 = [w for w in words if w['level'] == 'N5']
print(f"N5 단어 수: {len(n5)}개\n")

print("=== N5 단어 전체 목록 (알파벳순) ===")
n5_sorted = sorted(n5, key=lambda x: x.get('hiragana', x.get('word', '')))

for i, w in enumerate(n5_sorted[:100], 1):
    word = w.get('word', '')
    defn = w.get('definition', '')[:40]
    print(f"{i}. {word} - {defn}...")

print(f"\n... 외 {len(n5_sorted) - 100}개")

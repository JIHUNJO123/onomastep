import json

with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

# alpha, beta, gamma 정의로 검색
print("=== alpha/beta/gamma 정의를 가진 단어 ===")
found = []
for w in words:
    defn = w.get('definition', '').lower()
    if 'alpha' in defn or 'beta' in defn or 'gamma' in defn:
        found.append(w)
        print(f"ID: {w['id']}, Word: {w['word']}, Def: {w['definition']}, Level: {w['level']}")

print(f"\n총 {len(found)}개 발견")

# 삭제
if found:
    for item in found:
        # alphabet은 유지
        if 'alphabet' not in item.get('definition', '').lower():
            words.remove(item)
            print(f"삭제됨: {item['word']}")
    
    with open('assets/data/words_n5_n3.json', 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print("저장 완료!")

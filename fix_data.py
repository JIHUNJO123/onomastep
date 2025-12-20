import json
import re

# JSON 파일 로드
with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print(f"총 단어 수: {len(words)}")

# 1. 삭제할 단어 패턴 (JLPT에 안나오는 단어들)
remove_patterns = [
    r'^アルファ$',  # alpha
    r'^ベータ$',    # beta
    r'^ガンマ$',    # gamma
    r'^デルタ$',    # delta
    r'^オメガ$',    # omega
]

# 삭제 대상 확인
to_remove = []
for word in words:
    for pattern in remove_patterns:
        if re.match(pattern, word.get('word', '')):
            to_remove.append(word)
            print(f"삭제: {word['word']} (id: {word['id']}, level: {word['level']})")

# 삭제 실행
for item in to_remove:
    words.remove(item)

print(f"\n삭제 후 단어 수: {len(words)}")

# 2. N5 단어 확인 (어려운 단어 목록)
print("\n=== N5 단어 목록 (처음 50개) ===")
n5_words = [w for w in words if w['level'] == 'N5']
print(f"N5 단어 수: {len(n5_words)}")

for i, word in enumerate(n5_words[:50]):
    print(f"{i+1}. {word['word']} - {word['definition']}")

# 저장
with open('assets/data/words_n5_n3.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

print("\n저장 완료!")

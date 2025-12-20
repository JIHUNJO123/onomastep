import json

with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print(f"삭제 전: {len(words)}개")

# お凸 삭제 (ID: 570)
words = [w for w in words if w.get('id') != 570]

print(f"삭제 후: {len(words)}개")

# 다른 이상한 단어도 확인
print("\n=== N5에서 의심스러운 단어 추가 검색 ===")
n5 = [w for w in words if w['level'] == 'N5']

# 특수문자나 이상한 한자 포함 단어
suspicious = []
for w in n5:
    word = w.get('word', '')
    # 凸, 凹 등 특수한 한자
    if '凸' in word or '凹' in word:
        suspicious.append(w)
        print(f"특수한자: {word} - {w['definition']}")
    # 이모지나 특수문자
    for c in word:
        if ord(c) > 0x1F000:
            suspicious.append(w)
            print(f"특수문자: {word}")
            break

with open('assets/data/words_n5_n3.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

print("\n저장 완료!")

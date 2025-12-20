import json

with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

n5 = [w for w in words if w['level'] == 'N5']

# 오데코 검색
print("=== 오데코/額 검색 ===")
for w in n5:
    word = w.get('word', '')
    if 'おでこ' in word or 'オデコ' in word or '額' in word:
        print(f"{w['word']} - {w['definition']} (Level: {w['level']})")

# N5에 있으면 이상한 고급 단어들 검색
print("\n=== N5에서 의심스러운 단어 검색 ===")
suspicious_words = [
    "概念", "抽象", "具体", "論理", "暗黙", "示唆", "本質",
    "傾向", "課題", "価値", "方針", "見解", "影響", "状況",
]

for w in n5:
    word = w.get('word', '')
    for sus in suspicious_words:
        if sus in word:
            print(f"발견: {word} - {w['definition']}")

# 실제 N5 단어인지 확인할 의심 단어 (영어 정의 기준)
print("\n=== 영어 정의에 고급 단어 포함 ===")
advanced_eng = ["abstract", "concept", "philosophy", "theory", "hypothesis", 
                "metaphor", "ideology", "principle", "doctrine"]

count = 0
for w in n5:
    defn = w.get('definition', '').lower()
    for adv in advanced_eng:
        if adv in defn:
            print(f"{w['word']} - {w['definition']}")
            count += 1
            break

print(f"\n고급 영어 정의 포함: {count}개")

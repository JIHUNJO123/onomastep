import json

with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

# ========== N5 추가 검토 ==========
print("=== N5 남은 단어 중 의심스러운 것들 ===")

n5_words = [w for w in words if w['level'] == 'N5']

# 실제 JLPT N5 단어가 아닌 것들 (추가 검토)
suspicious_n5 = []

for w in n5_words:
    word = w.get('word', '')
    defn = w.get('definition', '').lower()
    hiragana = w.get('hiragana', '')
    
    # 1. 복잡한 문법 패턴
    grammar_patterns = ['という', 'ている', 'ておく', 'てしまう', 'ようにする', 
                       'ことができる', 'なければならない', 'かもしれない']
    
    # 2. 고급 의미를 가진 단어
    advanced_meanings = ['philosophy', 'theory', 'abstract', 'metaphor', 
                        'hypothesis', 'concept', 'ideol', 'doctrine',
                        'paradox', 'contradiction', 'phenomenon']
    
    # 3. 의성어/의태어 (대부분 N3-N4)
    onomatopoeia = ['っと', 'りと', 'んと']
    
    is_suspicious = False
    reason = ""
    
    # 고급 의미 체크
    for adv in advanced_meanings:
        if adv in defn:
            is_suspicious = True
            reason = f"고급의미: {adv}"
            break
    
    # 카타카나 외래어 중 어려운 것
    if not is_suspicious and len(word) > 6 and all('\u30A0' <= c <= '\u30FF' or c in 'ー・' for c in word):
        # 긴 카타카나 외래어는 N4 이상
        is_suspicious = True
        reason = "긴 카타카나"
    
    # 정의에 여러 의미가 있는 복잡한 단어
    if not is_suspicious and defn.count(';') >= 4:
        is_suspicious = True
        reason = "복잡한 정의"
    
    if is_suspicious:
        suspicious_n5.append((w, reason))
        print(f"{reason}: {word} - {defn[:50]}...")

print(f"\n의심스러운 N5 단어: {len(suspicious_n5)}개")

# 이동
move_count = 0
for w, reason in suspicious_n5:
    if '긴 카타카나' in reason or '복잡한 정의' in reason:
        w['level'] = 'N4'
        move_count += 1

print(f"N4로 이동: {move_count}개")

# ========== 한자 표기 오류 수정 ==========
print("\n=== 한자 표기 오류 수정 ===")

# word와 kanji가 다른데 kanji가 비정상인 경우
for w in words:
    word = w.get('word', '')
    kanji = w.get('kanji', '')
    hiragana = w.get('hiragana', '')
    
    # 특수 한자가 word에 있는 경우 히라가나로 대체
    special = ['凸', '凹', '々々', '〃']
    for sp in special:
        if sp in word and hiragana:
            print(f"특수문자 대체: {word} → {hiragana}")
            w['word'] = hiragana
            w['kanji'] = ''
            break

# ========== 저장 ==========
with open('assets/data/words_n5_n3.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

# 최종 통계
levels = {}
for w in words:
    lvl = w.get('level', 'Unknown')
    levels[lvl] = levels.get(lvl, 0) + 1

print("\n=== 최종 레벨별 단어 수 ===")
for k, v in sorted(levels.items()):
    print(f"  {k}: {v}개")

print("\n저장 완료!")

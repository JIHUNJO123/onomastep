import json
import re

with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print(f"총 단어 수: {len(words)}")

# ========== 1. 한자 오류 수정 ==========
print("\n=== 한자 오류 수정 ===")

kanji_fixes = {
    # word: (correct_word, correct_kanji, correct_hiragana)
    'お凸': ('おでこ', '', 'おでこ'),  # 凸 → おでこ (한자 없음, 히라가나만)
}

for w in words:
    word = w.get('word', '')
    if word in kanji_fixes:
        correct = kanji_fixes[word]
        print(f"수정: {word} → {correct[0]}")
        w['word'] = correct[0]
        w['kanji'] = correct[1]
        w['hiragana'] = correct[2]

# ========== 2. N5에 있으면 안되는 단어 찾기 ==========
print("\n=== N5 레벨 검토 ===")

# JLPT N5 공식 단어 목록 기준 (약 800개)
# N5는 가장 기본적인 일상 단어만 포함
# 복잡한 의성어/의태어, 문어체, 추상적 개념은 N5가 아님

n5_words = [w for w in words if w['level'] == 'N5']
print(f"현재 N5 단어 수: {len(n5_words)}")

# N5에 부적절한 패턴들
not_n5_patterns = [
    # 복잡한 의성어/의태어 (N3-N4 수준)
    r'がやがや', r'ざわざわ', r'どたばた', r'ずるずる', r'からり', r'さらさら',
    r'くたばる', r'こうすると', r'こうすれば', r'そうすると',
    # 문어체/격식체
    r'抑', r'些とも', r'凝乎と',
    # 복잡한 문법 표현
    r'させる', r'だけでなく', r'としても', r'として', r'と言えば',
    r'事がある', r'事になる', r'序でに',
    # 고급 어휘
    r'敵わない', r'拘る', r'草臥れる', r'擽る', r'くっ付く',
    # 특수 표현
    r'けじめ', r'ちょっぴり', r'てくてく', r'とんとん',
]

# N4로 이동해야 할 단어들
move_to_n4 = []
for w in n5_words:
    word = w.get('word', '')
    defn = w.get('definition', '')
    
    # 패턴 매칭
    for pattern in not_n5_patterns:
        if re.search(pattern, word):
            move_to_n4.append(w)
            print(f"N5→N4: {word} ({defn[:30]}...)")
            break
    
    # 정의가 너무 복잡한 경우 (10단어 이상 + 세미콜론 3개 이상)
    if w not in move_to_n4:
        if len(defn.split()) > 12 and defn.count(';') >= 3:
            move_to_n4.append(w)
            print(f"N5→N4 (복잡): {word} ({defn[:40]}...)")

# 레벨 변경
for w in move_to_n4:
    w['level'] = 'N4'

print(f"\nN5→N4 이동: {len(move_to_n4)}개")

# ========== 3. 이상한 한자/특수문자 수정 ==========
print("\n=== 특수문자/이상한 한자 검토 ===")

# 특수한 한자 패턴 (JLPT에서 잘 안 나오는 것들)
special_kanji = ['凸', '凹', '壺', '罠', '蛇', '鰐', '鰯', '鮫', '鯨', '鰹']

for w in words:
    word = w.get('word', '')
    for sk in special_kanji:
        if sk in word:
            # 히라가나 버전이 있으면 그걸로 대체
            hiragana = w.get('hiragana', '')
            if hiragana and hiragana != word:
                print(f"특수한자 대체: {word} → {hiragana}")
                w['word'] = hiragana
                w['kanji'] = ''  # 특수 한자 제거

# ========== 4. 저장 ==========
with open('assets/data/words_n5_n3.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

# 레벨별 통계
levels = {}
for w in words:
    lvl = w.get('level', 'Unknown')
    levels[lvl] = levels.get(lvl, 0) + 1

print("\n=== 수정 후 레벨별 단어 수 ===")
for k, v in sorted(levels.items()):
    print(f"  {k}: {v}개")

print("\n저장 완료!")

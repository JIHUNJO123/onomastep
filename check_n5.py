import json

# JSON 파일 로드
with open('assets/data/words_n5_n3.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print("=== N5 단어 전체 목록 ===")
n5_words = [w for w in words if w['level'] == 'N5']
print(f"총 N5 단어: {len(n5_words)}개\n")

# N5 표준 단어 목록 (JLPT 공식 기준)
# 기본적인 일상 단어: 사람, 시간, 장소, 숫자, 가족, 음식, 기본 동사
n5_should_be = set([
    # 기본 명사
    "人", "男", "女", "子", "母", "父", "友達", "先生", "学生",
    "水", "お茶", "ご飯", "魚", "肉", "野菜", "果物",
    "家", "部屋", "台所", "駅", "学校", "病院", "店",
    "本", "新聞", "手紙", "電話", "テレビ", "ラジオ",
    "目", "耳", "口", "手", "足", "頭",
    # 기본 동사
    "行く", "来る", "帰る", "食べる", "飲む", "見る", "聞く",
    "話す", "読む", "書く", "買う", "売る", "作る",
    "あげる", "もらう", "くれる",
    # 기본 형용사
    "大きい", "小さい", "高い", "安い", "新しい", "古い",
    "暑い", "寒い", "熱い", "冷たい",
    # 숫자, 시간
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
    "今日", "明日", "昨日", "朝", "昼", "夜",
])

# N5에 있으면 안되는 어려운 단어 패턴
hard_patterns = [
    "影響", "状況", "判断", "利用", "増える", "減る",
    "傾向", "課題", "価値", "方針", "見解", "概念",
    "本質", "示唆", "暗黙", "抽象", "具体", "論理",
]

print("=== N5에 포함된 잠재적으로 어려운 단어 ===")
suspicious = []
for w in n5_words:
    word = w.get('word', '')
    defn = w.get('definition', '')
    # 한자가 3개 이상이면 의심
    kanji_count = sum(1 for c in word if '\u4e00' <= c <= '\u9fff')
    if kanji_count >= 3:
        suspicious.append(w)
        print(f"한자 많음: {word} - {defn}")

print(f"\n한자 3개 이상 단어: {len(suspicious)}개")

# 정의가 복잡한 단어 (10단어 이상)
print("\n=== 정의가 복잡한 N5 단어 ===")
complex_def = []
for w in n5_words:
    defn = w.get('definition', '')
    if len(defn.split()) > 8:
        complex_def.append(w)
        print(f"{w['word']} - {defn[:50]}...")

print(f"\n복잡한 정의: {len(complex_def)}개")

import json
import re

path = r'C:\Users\hooni\Desktop\jlpt_vocab_app\assets\data\words_n5_n3.json'
data = json.load(open(path, encoding='utf-8'))

# 한국어 번역에서 " - 영어" 부분 제거
pattern = re.compile(r'^([가-힣\s,]+)\s*-\s*[a-zA-Z].*$')
fixed = 0
for w in data:
    ko = w.get('translations', {}).get('ko', {})
    if isinstance(ko, dict):
        ko_def = ko.get('definition', '')
        match = pattern.match(ko_def)
        if match:
            new_def = match.group(1).strip()
            ko['definition'] = new_def
            fixed += 1
            if fixed <= 5:
                print(f"Fixed: {w.get('word')} | {ko_def} -> {new_def}")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'N5-N3: 총 {fixed}개 수정 완료!')

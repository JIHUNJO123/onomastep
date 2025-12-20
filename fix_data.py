import json
import re

# 1. 정의에서 (noun), (verb) 등 품사 표시 제거
# 2. 빈 정의 단어 제거
# 3. 가짜 번역 정리

def clean_pos_tags(definition):
    """괄호 안 품사 표시 제거: (noun), (verb), (adj), (adv), (int) 등"""
    if not definition:
        return definition
    # (noun), (verb) 등 제거
    cleaned = re.sub(r'\s*\((noun|verb|adj|adv|int|suf|pref|exp)\)\s*', ' ', definition, flags=re.IGNORECASE)
    return cleaned.strip()

def process_file(path, output_path, remove_empty=True):
    """JSON 파일 처리"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data)
    removed = []
    modified = []
    
    new_data = []
    for w in data:
        # 빈 정의 단어 제거
        defn = w.get('definition', '').strip()
        if remove_empty and not defn:
            removed.append(w.get('word'))
            continue
        
        # 품사 태그 정리
        original_def = w.get('definition', '')
        cleaned_def = clean_pos_tags(original_def)
        if original_def != cleaned_def:
            modified.append((w.get('word'), original_def, cleaned_def))
            w['definition'] = cleaned_def
            # translations.en.definition도 업데이트
            if w.get('translations', {}).get('en', {}).get('definition'):
                w['translations']['en']['definition'] = cleaned_def
        
        new_data.append(w)
    
    # 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    return {
        'original_count': original_count,
        'new_count': len(new_data),
        'removed': removed,
        'modified': modified
    }

# 각 레벨 처리
files = [
    ('N5-N3', r'assets\data\words_n5_n3.json', r'assets\data\words_n5_n3.json'),
    ('N2', r'C:\Users\hooni\Desktop\jlpt_vocab_app_n2\assets\data\words_n2.json', r'C:\Users\hooni\Desktop\jlpt_vocab_app_n2\assets\data\words_n2.json'),
    ('N1', r'C:\Users\hooni\Desktop\jlpt_vocab_app_n1\assets\data\words_n1.json', r'C:\Users\hooni\Desktop\jlpt_vocab_app_n1\assets\data\words_n1.json'),
]

for level, in_path, out_path in files:
    print(f"\n=== {level} ===")
    result = process_file(in_path, out_path)
    print(f"원본: {result['original_count']}개 -> 결과: {result['new_count']}개")
    if result['removed']:
        print(f"제거됨: {result['removed']}")
    if result['modified']:
        print(f"수정됨: {len(result['modified'])}개")
        for m in result['modified'][:5]:
            print(f"  {m[0]}: '{m[1]}' -> '{m[2]}'")
        if len(result['modified']) > 5:
            print(f"  ... 외 {len(result['modified'])-5}개")

print("\n완료!")

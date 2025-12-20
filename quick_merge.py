#!/usr/bin/env python3
"""
N5-N3 앱용 데이터 병합 및 저장 (동기 실행)
"""

import json
import os

# 작업 디렉토리
os.chdir(r"C:\Users\hooni\Desktop\jlpt_vocab_app")

print("=== N5-N3 앱 데이터 병합 ===\n")

n5_n3_words = []
word_id = 1

for level in ['N5', 'N4', 'N3']:
    filepath = f"words_{level.lower()}_final.json"
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for entry in data:
            new_entry = {
                'id': word_id,
                'word': entry.get('word', ''),
                'reading': entry.get('reading', entry.get('hiragana', '')),
                'definition': entry.get('definition', ''),
                'level': level,
                'korean': entry.get('korean', entry.get('translations', {}).get('ko', {}).get('definition', '')),
                'chinese': entry.get('chinese', entry.get('translations', {}).get('zh', {}).get('definition', '')),
                'example': entry.get('example', ''),
                'example_reading': entry.get('example_reading', ''),
                'example_meaning': entry.get('example_meaning', ''),
                'source': 'Bluskyo/Tanos'
            }
            word_id += 1
            n5_n3_words.append(new_entry)
        
        print(f"{level}: {len(data)} words")

# 통계
with_def = sum(1 for w in n5_n3_words if w.get('definition'))
print(f"\n총 {len(n5_n3_words)} words")
print(f"정의가 있는 단어: {with_def}/{len(n5_n3_words)}")

# assets/data에 저장
os.makedirs("assets/data", exist_ok=True)
output_file = "assets/data/words_n5_n3.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
print(f"\n저장: {output_file}")

# lib/data에도 저장
os.makedirs("lib/data", exist_ok=True)
lib_output = "lib/data/words_n5_n3.json"
with open(lib_output, 'w', encoding='utf-8') as f:
    json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
print(f"저장: {lib_output}")

print("\n=== 완료 ===")

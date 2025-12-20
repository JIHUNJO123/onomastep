#!/usr/bin/env python3
"""
N5-N3 앱용 데이터 준비 (독립 실행)
"""

import json
import os

def main():
    print("=== N5-N3 앱 데이터 준비 ===\n")
    
    # N5-N3 앱용 데이터 병합
    n5_n3_words = []
    word_id = 1
    
    for level in ['N5', 'N4', 'N3']:
        # final 파일 먼저 시도
        for suffix in ['final', 'merged']:
            filepath = f"words_{level.lower()}_{suffix}.json"
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for entry in data:
                    # 기존 데이터와 호환되는 형식으로 변환
                    new_entry = {
                        'id': word_id,
                        'word': entry.get('word', ''),
                        'reading': entry.get('reading', entry.get('hiragana', '')),
                        'definition': entry.get('definition', ''),
                        'level': level,
                        'korean': entry.get('korean', ''),
                        'chinese': entry.get('chinese', ''),
                        'example': entry.get('example', ''),
                        'example_reading': entry.get('example_reading', ''),
                        'example_meaning': entry.get('example_meaning', ''),
                        'source': 'Bluskyo/Tanos'
                    }
                    word_id += 1
                    n5_n3_words.append(new_entry)
                
                print(f"{level}: {len(data)} words from {filepath}")
                break
    
    # 정의가 있는 단어 수 확인
    with_def = sum(1 for w in n5_n3_words if w.get('definition'))
    print(f"\n총 {len(n5_n3_words)} words")
    print(f"정의가 있는 단어: {with_def}/{len(n5_n3_words)}")
    
    # 저장
    output_file = "assets/data/words_n5_n3.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
    print(f"\n저장: {output_file}")
    
    # lib/data에도 복사
    lib_output = "lib/data/words_n5_n3.json"
    if os.path.exists("lib/data"):
        with open(lib_output, 'w', encoding='utf-8') as f:
            json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
        print(f"저장: {lib_output}")

if __name__ == '__main__':
    main()

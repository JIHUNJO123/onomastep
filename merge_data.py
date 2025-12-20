#!/usr/bin/env python3
"""
기존 앱 데이터와 Bluskyo 데이터 병합
- 기존 데이터에서 정의 가져오기
- 없는 것만 Jisho API로 보충
"""

import json
import os

def load_existing_data():
    """기존 앱 데이터 로드"""
    existing = {}
    
    # assets/data 폴더의 기존 JSON 파일들
    data_files = [
        'assets/data/words_n5_n3.json',
        'lib/data/words_n5_n3.json',
    ]
    
    for filepath in data_files:
        if os.path.exists(filepath):
            print(f"  Loading {filepath}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry in data:
                    word = entry.get('word', '')
                    if word:
                        existing[word] = entry
            print(f"    Loaded {len(existing)} words")
            break
    
    return existing

def main():
    print("=== 데이터 병합 ===\n")
    
    # 기존 데이터 로드
    print("1. 기존 앱 데이터 로드...")
    existing = load_existing_data()
    print(f"   총 {len(existing)} entries in existing data")
    
    # Bluskyo 데이터 로드
    print("\n2. Bluskyo 데이터 로드...")
    bluskyo = {}
    with open('bluskyo_words.json', 'r', encoding='utf-8') as f:
        bluskyo = json.load(f)
    print(f"   총 {len(bluskyo)} entries in Bluskyo data")
    
    # 레벨별 분리 및 기존 데이터 병합
    print("\n3. 레벨별 분리 및 병합...")
    
    levels = {'N5': [], 'N4': [], 'N3': [], 'N2': [], 'N1': []}
    
    found_count = 0
    not_found_count = 0
    
    for word, level in bluskyo.items():
        if level not in levels:
            continue
        
        if word in existing:
            # 기존 데이터에서 가져오기
            entry = existing[word].copy()
            entry['level'] = level  # Bluskyo의 레벨 사용
            entry['source'] = 'Bluskyo+Existing'
            levels[level].append(entry)
            found_count += 1
        else:
            # 새 엔트리 생성
            entry = {
                'word': word,
                'reading': '',
                'definition': '',
                'level': level,
                'korean': '',
                'chinese': '',
                'example': '',
                'example_reading': '',
                'example_meaning': '',
                'source': 'Bluskyo'
            }
            levels[level].append(entry)
            not_found_count += 1
    
    print(f"   기존 데이터 활용: {found_count}")
    print(f"   새 데이터: {not_found_count}")
    
    # ID 재할당 및 저장
    print("\n4. 저장...")
    
    for level, words in levels.items():
        # ID 재할당
        for i, entry in enumerate(words):
            entry['id'] = i + 1
        
        # 저장
        filename = f"words_{level.lower()}_merged.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        
        # 정의가 있는 단어 수 계산
        with_def = sum(1 for w in words if w.get('definition'))
        print(f"   {level}: {len(words)} words ({with_def} with definitions) -> {filename}")
    
    print("\n=== 요약 ===")
    total = sum(len(w) for w in levels.values())
    total_with_def = sum(sum(1 for w in words if w.get('definition')) for words in levels.values())
    print(f"총 {total} 단어")
    print(f"정의가 있는 단어: {total_with_def}")
    print(f"정의가 없는 단어: {total - total_with_def} (Jisho API로 채워야 함)")

if __name__ == '__main__':
    main()

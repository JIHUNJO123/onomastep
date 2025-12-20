#!/usr/bin/env python3
"""
최종 데이터를 앱 형식으로 변환하고 assets/data에 복사
- N5-N3 앱: words_n5_n3.json
- N2 앱: words_n2.json  
- N1 앱: words_n1.json
"""

import json
import os
import shutil

def prepare_app_data():
    """앱용 데이터 준비"""
    print("=== 앱 데이터 준비 ===\n")
    
    # N5-N3 앱용 데이터 병합
    print("1. N5-N3 앱 데이터 병합...")
    
    n5_n3_words = []
    word_id = 1
    
    for level in ['N5', 'N4', 'N3']:
        # final 파일 먼저 시도, 없으면 merged 파일
        for suffix in ['final', 'merged']:
            filepath = f"words_{level.lower()}_{suffix}.json"
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 정의가 있는 것만 (없으면 일단 포함)
                for entry in data:
                    entry['id'] = word_id
                    word_id += 1
                    n5_n3_words.append(entry)
                
                print(f"   {level}: {len(data)} words from {filepath}")
                break
    
    # 저장
    output_file = "words_n5_n3_new.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
    print(f"   총 {len(n5_n3_words)} words -> {output_file}")
    
    # 정의가 있는 단어 수
    with_def = sum(1 for w in n5_n3_words if w.get('definition'))
    print(f"   정의가 있는 단어: {with_def}/{len(n5_n3_words)}")
    
    # N2 앱용 데이터
    print("\n2. N2 앱 데이터...")
    for suffix in ['final', 'merged']:
        filepath = f"words_n2_{suffix}.json"
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                n2_data = json.load(f)
            
            # ID 재할당
            for i, entry in enumerate(n2_data):
                entry['id'] = i + 1
            
            output_file = "words_n2_new.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(n2_data, f, ensure_ascii=False, indent=2)
            
            with_def = sum(1 for w in n2_data if w.get('definition'))
            print(f"   {len(n2_data)} words -> {output_file}")
            print(f"   정의가 있는 단어: {with_def}/{len(n2_data)}")
            break
    
    # N1 앱용 데이터
    print("\n3. N1 앱 데이터...")
    for suffix in ['final', 'merged']:
        filepath = f"words_n1_{suffix}.json"
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                n1_data = json.load(f)
            
            # ID 재할당
            for i, entry in enumerate(n1_data):
                entry['id'] = i + 1
            
            output_file = "words_n1_new.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(n1_data, f, ensure_ascii=False, indent=2)
            
            with_def = sum(1 for w in n1_data if w.get('definition'))
            print(f"   {len(n1_data)} words -> {output_file}")
            print(f"   정의가 있는 단어: {with_def}/{len(n1_data)}")
            break
    
    print("\n=== 완료 ===")
    print("\n다음 단계:")
    print("1. N3, N2, N1의 정의가 없는 단어들은 fill_definitions.py로 채우기")
    print("2. 완료되면 words_*_new.json을 assets/data/로 복사")

if __name__ == '__main__':
    prepare_app_data()

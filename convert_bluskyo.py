#!/usr/bin/env python3
"""
Bluskyo JLPT 데이터를 앱 형식으로 변환
- 레벨별로 분리
- 앱에서 사용하는 형식으로 변환
- Jisho API에서 세부 정보 가져오기
"""

import json
import urllib.request
import urllib.parse
import time
import re
from urllib.error import HTTPError, URLError

def load_bluskyo_data():
    """Bluskyo 데이터 로드"""
    with open('bluskyo_words.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 레벨별로 분리
    levels = {'N5': [], 'N4': [], 'N3': [], 'N2': [], 'N1': []}
    
    for word, level in data.items():
        if level in levels:
            levels[level].append(word)
    
    return levels

def fetch_jisho_word(word):
    """Jisho API에서 단어 정보 가져오기"""
    url = f"https://jisho.org/api/v1/search/words?keyword={urllib.parse.quote(word)}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data['data']:
                entry = data['data'][0]
                
                # 단어 (한자)
                word_text = entry['japanese'][0].get('word', '')
                
                # 읽기 (히라가나)
                reading = entry['japanese'][0].get('reading', '')
                
                # 의미 (영어)
                meanings = []
                for sense in entry['senses'][:3]:  # 최대 3개 의미
                    for gloss in sense.get('english_definitions', [])[:2]:
                        meanings.append(gloss)
                
                definition = '; '.join(meanings[:5]) if meanings else ''
                
                # 품사
                pos = []
                for sense in entry['senses'][:1]:
                    pos.extend(sense.get('parts_of_speech', []))
                
                return {
                    'word': word_text if word_text else word,
                    'reading': reading,
                    'definition': definition,
                    'pos': ', '.join(pos[:2]) if pos else ''
                }
    except Exception as e:
        print(f"    Error fetching {word}: {e}")
    
    return None

def main():
    print("=== Bluskyo JLPT 데이터 변환 ===\n")
    
    levels = load_bluskyo_data()
    
    print("원본 데이터:")
    for level, words in levels.items():
        print(f"  {level}: {len(words)} words")
    
    print("\n레벨별 데이터 저장 중...")
    
    # 각 레벨별로 저장
    for level, words in levels.items():
        output = []
        
        for i, word in enumerate(words):
            entry = {
                'id': i + 1,
                'word': word,
                'reading': '',  # 추후 채워질 수 있음
                'definition': '',  # 추후 채워질 수 있음
                'level': level,
                'korean': '',
                'chinese': '',
                'example': '',
                'example_reading': '',
                'example_meaning': '',
                'source': 'Bluskyo/Tanos'
            }
            output.append(entry)
        
        # 저장
        filename = f"words_{level.lower()}_bluskyo.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  {level}: {len(output)} words -> {filename}")
    
    print("\n=== 요약 ===")
    print(f"총 {sum(len(w) for w in levels.values())} 단어 (중복 없음)")
    print("\n참고: 이 데이터에는 definition(영어 의미)이 없습니다.")
    print("Jisho API를 사용하여 의미를 채워야 합니다.")

if __name__ == '__main__':
    main()

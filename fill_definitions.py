#!/usr/bin/env python3
"""
병합된 데이터에서 빈 정의를 Jisho API로 채우기
"""

import json
import urllib.request
import urllib.parse
import time
import sys
from urllib.error import HTTPError, URLError

def fetch_jisho_word(word):
    """Jisho API에서 단어 정보 가져오기"""
    url = f"https://jisho.org/api/v1/search/words?keyword={urllib.parse.quote(word)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data['data']:
                # 정확히 일치하는 항목 찾기
                for entry in data['data'][:3]:
                    for jp in entry['japanese']:
                        if jp.get('word') == word or jp.get('reading') == word:
                            word_text = jp.get('word', '')
                            reading = jp.get('reading', '')
                            
                            meanings = []
                            for sense in entry['senses'][:3]:
                                for gloss in sense.get('english_definitions', [])[:3]:
                                    if gloss not in meanings:
                                        meanings.append(gloss)
                            
                            definition = '; '.join(meanings[:6]) if meanings else ''
                            
                            return {
                                'word': word_text if word_text else word,
                                'reading': reading,
                                'definition': definition
                            }
                
                # 첫 번째 결과 사용
                entry = data['data'][0]
                word_text = entry['japanese'][0].get('word', '')
                reading = entry['japanese'][0].get('reading', '')
                
                meanings = []
                for sense in entry['senses'][:3]:
                    for gloss in sense.get('english_definitions', [])[:3]:
                        if gloss not in meanings:
                            meanings.append(gloss)
                
                definition = '; '.join(meanings[:6]) if meanings else ''
                
                return {
                    'word': word_text if word_text else word,
                    'reading': reading,
                    'definition': definition
                }
    except Exception as e:
        pass
    
    return None

def process_level(level):
    """특정 레벨의 단어들 처리"""
    input_file = f"words_{level.lower()}_merged.json"
    output_file = f"words_{level.lower()}_final.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        words = json.load(f)
    
    print(f"\n=== {level} 처리 중 ({len(words)} words) ===")
    
    # 정의가 없는 단어만 처리
    to_process = [w for w in words if not w.get('definition')]
    print(f"   정의가 필요한 단어: {len(to_process)}")
    
    if not to_process:
        print("   모든 단어에 정의가 있습니다!")
        # 그래도 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        return
    
    success_count = 0
    fail_count = 0
    
    for i, entry in enumerate(to_process):
        word = entry['word']
        
        result = fetch_jisho_word(word)
        
        if result and result['definition']:
            entry['reading'] = result['reading']
            entry['definition'] = result['definition']
            success_count += 1
        else:
            fail_count += 1
        
        if (i + 1) % 50 == 0:
            print(f"   {i + 1}/{len(to_process)} (success: {success_count}, fail: {fail_count})")
        
        time.sleep(0.15)
    
    # 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    # 통계
    with_def = sum(1 for w in words if w.get('definition'))
    print(f"   완료: success={success_count}, fail={fail_count}")
    print(f"   최종: {with_def}/{len(words)} words with definitions")
    print(f"   저장: {output_file}")

def main():
    if len(sys.argv) > 1:
        levels = [sys.argv[1].upper()]
    else:
        levels = ['N5', 'N4', 'N3', 'N2', 'N1']
    
    print("=== Jisho API로 정의 채우기 ===")
    
    for level in levels:
        try:
            process_level(level)
        except FileNotFoundError:
            print(f"   {level} 파일 없음")
    
    print("\n완료!")

if __name__ == '__main__':
    main()

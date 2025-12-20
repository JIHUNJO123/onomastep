#!/usr/bin/env python3
"""
Bluskyo JLPT 데이터에 Jisho API로 세부 정보 추가
- 영어 정의
- 읽기 (히라가나)
- 품사
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
                for entry in data['data']:
                    for jp in entry['japanese']:
                        if jp.get('word') == word or jp.get('reading') == word:
                            # 단어 (한자)
                            word_text = jp.get('word', '')
                            # 읽기 (히라가나)
                            reading = jp.get('reading', '')
                            
                            # 의미 (영어)
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
                
                # 정확히 일치하는 것이 없으면 첫 번째 결과 사용
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

def process_level(level, batch_size=50):
    """특정 레벨의 단어들 처리"""
    input_file = f"words_{level.lower()}_bluskyo.json"
    output_file = f"words_{level.lower()}_complete.json"
    
    # 기존 데이터 로드
    with open(input_file, 'r', encoding='utf-8') as f:
        words = json.load(f)
    
    print(f"\n=== {level} 처리 중 ({len(words)} words) ===")
    
    # 진행 상황 저장 파일 확인
    progress_file = f"progress_{level.lower()}.json"
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress = json.load(f)
            processed_ids = set(progress.get('processed', []))
            print(f"  이전 진행 상황 로드: {len(processed_ids)} processed")
    except:
        processed_ids = set()
    
    success_count = 0
    fail_count = 0
    
    for i, entry in enumerate(words):
        word_id = entry['id']
        
        # 이미 처리된 경우 스킵
        if word_id in processed_ids and entry.get('definition'):
            continue
        
        word = entry['word']
        
        # Jisho API 호출
        result = fetch_jisho_word(word)
        
        if result:
            entry['reading'] = result['reading']
            entry['definition'] = result['definition']
            if result['word'] != word:
                entry['kanji'] = result['word']
            success_count += 1
        else:
            fail_count += 1
        
        processed_ids.add(word_id)
        
        # 진행 상황 출력 (100개마다)
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{len(words)} processed (success: {success_count}, fail: {fail_count})")
        
        # API 호출 간격
        time.sleep(0.2)
        
        # 500개마다 저장
        if (i + 1) % 500 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump({'processed': list(processed_ids)}, f)
            print(f"  중간 저장 완료")
    
    # 최종 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"  완료: {success_count} success, {fail_count} fail")
    print(f"  저장: {output_file}")
    
    return words

def main():
    print("=== JLPT 단어 데이터 완성 ===")
    print("Jisho API를 사용하여 영어 정의와 읽기를 추가합니다.")
    
    # 인자로 레벨 지정 가능
    if len(sys.argv) > 1:
        levels = [sys.argv[1].upper()]
    else:
        levels = ['N5', 'N4', 'N3', 'N2', 'N1']
    
    for level in levels:
        try:
            process_level(level)
        except FileNotFoundError:
            print(f"  {level} 파일 없음, 스킵")
    
    print("\n=== 완료 ===")

if __name__ == '__main__':
    main()

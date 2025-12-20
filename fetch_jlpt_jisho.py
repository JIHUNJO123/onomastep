"""
JLPT 단어 데이터 생성
소스: JMdict (JLPT 태그 포함) + 기존 Tanos 데이터 활용
출처 표기: tanos.co.uk (CC BY) + 日本語能力試験出題基準
"""

import json
import urllib.request
import time

def fetch_jisho_jlpt(level):
    """Jisho.org API로 JLPT 레벨별 단어 가져오기"""
    words = []
    page = 1
    
    while True:
        url = f"https://jisho.org/api/v1/search/words?keyword=%23jlpt-{level.lower()}&page={page}"
        print(f"  Fetching {level} page {page}...")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if not data.get('data'):
                break
                
            for item in data['data']:
                # 첫 번째 일본어 표기
                japanese = item.get('japanese', [{}])[0]
                word = japanese.get('word', japanese.get('reading', ''))
                reading = japanese.get('reading', '')
                
                # 첫 번째 영어 정의
                senses = item.get('senses', [{}])
                definitions = []
                pos = []
                for sense in senses[:2]:  # 최대 2개 의미
                    defs = sense.get('english_definitions', [])
                    if defs:
                        definitions.extend(defs[:3])
                    parts = sense.get('parts_of_speech', [])
                    if parts:
                        pos.extend(parts)
                
                if word and definitions:
                    words.append({
                        'word': word,
                        'reading': reading,
                        'definition': '; '.join(definitions[:4]),
                        'pos': pos[0] if pos else 'unknown',
                        'level': level.upper()
                    })
            
            if len(data['data']) < 20:  # 마지막 페이지
                break
                
            page += 1
            time.sleep(0.5)  # API 부하 방지
            
            if page > 50:  # 안전장치
                break
                
        except Exception as e:
            print(f"    Error: {e}")
            break
    
    return words

def remove_duplicates(all_words):
    """중복 제거 (하위 레벨 우선)"""
    seen = set()
    result = {level: [] for level in ['N5', 'N4', 'N3', 'N2', 'N1']}
    
    # N5부터 처리 (하위 레벨 우선)
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        for word in all_words.get(level, []):
            key = word['word']
            if key not in seen:
                seen.add(key)
                result[level].append(word)
    
    return result

def main():
    print("=== JLPT 단어 데이터 생성 ===\n")
    
    all_words = {}
    
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        print(f"\nFetching {level}...")
        words = fetch_jisho_jlpt(level)
        all_words[level] = words
        print(f"  {level}: {len(words)} words")
    
    # 중복 제거
    print("\n중복 제거 중...")
    unique_words = remove_duplicates(all_words)
    
    # 결과 출력
    print("\n=== 결과 (중복 제거 후) ===")
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        print(f"  {level}: {len(unique_words[level])} words")
    
    total = sum(len(v) for v in unique_words.values())
    print(f"  총합: {total} words")
    
    # 저장
    with open('jlpt_all_levels.json', 'w', encoding='utf-8') as f:
        json.dump(unique_words, f, ensure_ascii=False, indent=2)
    print("\nSaved to jlpt_all_levels.json")

if __name__ == "__main__":
    main()

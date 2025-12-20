"""
Tanos.co.uk JLPT 단어 목록 수집
출처: tanos.co.uk + 日本語能力試験出題基準 (구 JLPT 공식 목록)
"""

import json
import urllib.request
import re
from html.parser import HTMLParser

# Tanos 단어 목록 URL (Anki deck export 형식)
TANOS_URLS = {
    'N5': 'https://www.tanos.co.uk/jlpt/jlpt5/vocab/VocabList.N5.json',
    'N4': 'https://www.tanos.co.uk/jlpt/jlpt4/vocab/VocabList.N4.json',
    'N3': 'https://www.tanos.co.uk/jlpt/jlpt3/vocab/VocabList.N3.json',
    'N2': 'https://www.tanos.co.uk/jlpt/jlpt2/vocab/VocabList.N2.json',
    'N1': 'https://www.tanos.co.uk/jlpt/jlpt1/vocab/VocabList.N1.json',
}

def fetch_tanos_data():
    """Tanos에서 JLPT 단어 데이터 가져오기"""
    all_words = {}
    
    for level, url in TANOS_URLS.items():
        print(f"Fetching {level}...")
        try:
            # JSON 직접 접근이 안되면 HTML 파싱 필요
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                all_words[level] = data
                print(f"  {level}: {len(data)} words")
        except Exception as e:
            print(f"  Error fetching {level}: {e}")
            all_words[level] = []
    
    return all_words

def fetch_tanos_html(level):
    """HTML 페이지에서 단어 추출"""
    urls = {
        'N5': 'https://www.tanos.co.uk/jlpt/jlpt5/vocab/',
        'N4': 'https://www.tanos.co.uk/jlpt/jlpt4/vocab/',
        'N3': 'https://www.tanos.co.uk/jlpt/jlpt3/vocab/',
        'N2': 'https://www.tanos.co.uk/jlpt/jlpt2/vocab/',
        'N1': 'https://www.tanos.co.uk/jlpt/jlpt1/vocab/',
    }
    
    url = urls.get(level)
    if not url:
        return []
    
    print(f"Fetching {level} from HTML...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            
        # 간단한 테이블 파싱
        # <tr><td>word</td><td>reading</td><td>meaning</td></tr>
        words = []
        # 테이블 행 패턴
        pattern = r'<tr[^>]*>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]*)</td>\s*<td[^>]*>([^<]+)</td>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        for match in matches:
            word, reading, meaning = match
            word = word.strip()
            reading = reading.strip()
            meaning = meaning.strip()
            
            if word and meaning and not word.startswith('Kanji'):
                words.append({
                    'word': word,
                    'reading': reading,
                    'meaning': meaning
                })
        
        print(f"  {level}: {len(words)} words from HTML")
        return words
        
    except Exception as e:
        print(f"  Error: {e}")
        return []

if __name__ == "__main__":
    # 먼저 JSON 시도
    print("Trying JSON endpoints...")
    data = fetch_tanos_data()
    
    # JSON이 안되면 HTML 파싱
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        if not data.get(level):
            data[level] = fetch_tanos_html(level)
    
    # 결과 저장
    total = sum(len(v) for v in data.values())
    print(f"\nTotal: {total} words")
    
    with open('tanos_raw.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved to tanos_raw.json")

#!/usr/bin/env python3
"""
Tanos JLPT 단어 데이터 가져오기 (웹 스크래핑)
출처: tanos.co.uk - Jonathan Waller's JLPT Resources (CC BY)
"""

import json
import re
import time
import urllib.request
from urllib.error import HTTPError, URLError

# Tanos 단어 목록을 직접 파싱
TANOS_URLS = {
    'N5': 'https://www.tanos.co.uk/jlpt/jlpt5/vocab/',
    'N4': 'https://www.tanos.co.uk/jlpt/jlpt4/vocab/',
    'N3': 'https://www.tanos.co.uk/jlpt/jlpt3/vocab/',
    'N2': 'https://www.tanos.co.uk/jlpt/jlpt2/vocab/',
    'N1': 'https://www.tanos.co.uk/jlpt/jlpt1/vocab/',
}

def fetch_html(url):
    """HTML 가져오기"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except (HTTPError, URLError) as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_vocab_html(html, level):
    """HTML에서 단어 추출"""
    words = []
    
    # 테이블 패턴: <tr><td>kanji</td><td>kana</td><td>meaning</td></tr>
    # Tanos 구조에 맞게 파싱
    
    # 방법 1: 테이블 행 찾기
    row_pattern = r'<tr[^>]*>.*?</tr>'
    rows = re.findall(row_pattern, html, re.DOTALL | re.IGNORECASE)
    
    for row in rows:
        # td 태그 내용 추출
        td_pattern = r'<td[^>]*>(.*?)</td>'
        cells = re.findall(td_pattern, row, re.DOTALL | re.IGNORECASE)
        
        if len(cells) >= 3:
            # HTML 태그 제거
            kanji = re.sub(r'<[^>]+>', '', cells[0]).strip()
            kana = re.sub(r'<[^>]+>', '', cells[1]).strip()
            meaning = re.sub(r'<[^>]+>', '', cells[2]).strip()
            
            # 유효한 단어인지 확인
            if kanji and meaning and not kanji.startswith('Kanji'):
                word = {
                    'word': kanji,
                    'reading': kana if kana != kanji else '',
                    'meaning': meaning,
                    'level': level,
                    'source': 'Tanos'
                }
                words.append(word)
    
    return words

def main():
    print("=== Tanos JLPT 단어 데이터 가져오기 ===\n")
    
    all_words = {}
    
    for level, url in TANOS_URLS.items():
        print(f"Fetching {level}...")
        html = fetch_html(url)
        
        if html:
            words = parse_vocab_html(html, level)
            all_words[level] = words
            print(f"  {level}: {len(words)} words")
        else:
            print(f"  {level}: Failed to fetch")
            all_words[level] = []
        
        time.sleep(1)  # 서버 부하 방지
    
    # 결과 저장
    output_file = 'tanos_words.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 결과 ===")
    total = 0
    for level, words in all_words.items():
        print(f"  {level}: {len(words)} words")
        total += len(words)
    print(f"  총합: {total} words")
    print(f"\nSaved to {output_file}")

if __name__ == '__main__':
    main()

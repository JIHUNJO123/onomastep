#!/usr/bin/env python3
"""Bluskyo/JLPT_Vocabulary data 폴더에서 JLPT 단어 가져오기"""

import json
import urllib.request
from urllib.error import HTTPError, URLError

def fetch_url(url):
    """URL 가져오기"""
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/vnd.github.v3+json',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except (HTTPError, URLError) as e:
        print(f"Error: {e}")
        return None

def fetch_raw(url):
    """Raw content 가져오기"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except (HTTPError, URLError) as e:
        print(f"Error: {e}")
        return None

def main():
    print("=== Bluskyo/JLPT_Vocabulary/data 탐색 ===\n")
    
    # data 폴더 내용
    data_url = "https://api.github.com/repos/Bluskyo/JLPT_Vocabulary/contents/data"
    contents = fetch_url(data_url)
    
    if not contents:
        print("data 폴더 접근 실패")
        return
    
    print("data 폴더 파일:")
    for item in contents:
        print(f"  - {item['name']} ({item['type']})")
    
    print("\n=== JSON 파일 다운로드 ===")
    
    all_words = {}
    
    for item in contents:
        if item['type'] == 'file' and item['name'].endswith('.json'):
            print(f"\n다운로드: {item['name']}")
            content = fetch_raw(item['download_url'])
            
            if content:
                try:
                    data = json.loads(content)
                    if isinstance(data, list):
                        print(f"  {len(data)} entries")
                        # 레벨 추출
                        level = item['name'].replace('.json', '').upper()
                        if level.startswith('JLPT_'):
                            level = level.replace('JLPT_', '')
                        elif level.startswith('JLPT'):
                            level = level.replace('JLPT', '')
                        
                        all_words[level] = data
                        
                        # 샘플 데이터 출력
                        if data:
                            print(f"  샘플: {data[0]}")
                except json.JSONDecodeError as e:
                    print(f"  JSON 파싱 오류: {e}")
    
    # 결과 저장
    if all_words:
        with open('bluskyo_jlpt_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_words, f, ensure_ascii=False, indent=2)
        
        print("\n=== 요약 ===")
        total = 0
        for key, data in sorted(all_words.items()):
            count = len(data) if isinstance(data, list) else 0
            print(f"  {key}: {count} words")
            total += count
        print(f"  총합: {total} words")
        print(f"\n저장됨: bluskyo_jlpt_data.json")

if __name__ == '__main__':
    main()

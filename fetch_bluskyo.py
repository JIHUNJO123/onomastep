#!/usr/bin/env python3
"""Bluskyo/JLPT_Vocabulary에서 JLPT 단어 가져오기"""

import json
import urllib.request
from urllib.error import HTTPError, URLError

# Bluskyo/JLPT_Vocabulary 저장소 확인
BASE_URL = "https://api.github.com/repos/Bluskyo/JLPT_Vocabulary/contents"

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
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except (HTTPError, URLError) as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    print("=== Bluskyo/JLPT_Vocabulary 저장소 탐색 ===\n")
    
    # 저장소 내용 확인
    contents = fetch_url(BASE_URL)
    
    if not contents:
        print("저장소 접근 실패")
        return
    
    print("저장소 파일 목록:")
    for item in contents:
        print(f"  - {item['name']} ({item['type']})")
        if item['type'] == 'file' and item['name'].endswith('.json'):
            print(f"    Download URL: {item['download_url']}")
    
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
                        # 레벨 추출 시도
                        level = item['name'].replace('.json', '').upper()
                        if level in ['N5', 'N4', 'N3', 'N2', 'N1']:
                            all_words[level] = data
                        else:
                            # 파일 내용에서 레벨 확인
                            if data and 'level' in data[0]:
                                level = data[0]['level']
                            all_words[item['name']] = data
                    elif isinstance(data, dict):
                        print(f"  Dict with keys: {list(data.keys())[:5]}")
                        all_words[item['name']] = data
                except json.JSONDecodeError as e:
                    print(f"  JSON 파싱 오류: {e}")
    
    # 결과 저장
    if all_words:
        with open('bluskyo_jlpt.json', 'w', encoding='utf-8') as f:
            json.dump(all_words, f, ensure_ascii=False, indent=2)
        print(f"\n저장됨: bluskyo_jlpt.json")
        
        print("\n=== 요약 ===")
        for key, data in all_words.items():
            if isinstance(data, list):
                print(f"  {key}: {len(data)} words")

if __name__ == '__main__':
    main()

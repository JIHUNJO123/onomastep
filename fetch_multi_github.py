#!/usr/bin/env python3
"""
다양한 GitHub 저장소에서 JLPT 단어 데이터 가져오기
"""

import json
import urllib.request
from urllib.error import HTTPError, URLError

# 여러 공개 저장소 목록
SOURCES = [
    # https://github.com/psgganern/jlpt-vocab-lists
    {
        'N5': 'https://raw.githubusercontent.com/psgganern/jlpt-vocab-lists/master/N5.json',
        'N4': 'https://raw.githubusercontent.com/psgganern/jlpt-vocab-lists/master/N4.json',
        'N3': 'https://raw.githubusercontent.com/psgganern/jlpt-vocab-lists/master/N3.json',
        'N2': 'https://raw.githubusercontent.com/psgganern/jlpt-vocab-lists/master/N2.json',
        'N1': 'https://raw.githubusercontent.com/psgganern/jlpt-vocab-lists/master/N1.json',
        'name': 'psgganern/jlpt-vocab-lists'
    },
    # https://github.com/hexenq/kuroshiro (might have vocab)
    # https://github.com/davidluzgouveia/jlpt-vocabulary
    {
        'N5': 'https://raw.githubusercontent.com/davidluzgouveia/jlpt-vocabulary/master/data/n5.json',
        'N4': 'https://raw.githubusercontent.com/davidluzgouveia/jlpt-vocabulary/master/data/n4.json',
        'N3': 'https://raw.githubusercontent.com/davidluzgouveia/jlpt-vocabulary/master/data/n3.json',
        'N2': 'https://raw.githubusercontent.com/davidluzgouveia/jlpt-vocabulary/master/data/n2.json',
        'N1': 'https://raw.githubusercontent.com/davidluzgouveia/jlpt-vocabulary/master/data/n1.json',
        'name': 'davidluzgouveia/jlpt-vocabulary'
    },
    # https://github.com/TehSomeLuigi/jlpt-vocab
    {
        'N5': 'https://raw.githubusercontent.com/TehSomeLuigi/jlpt-vocab/main/n5.json',
        'N4': 'https://raw.githubusercontent.com/TehSomeLuigi/jlpt-vocab/main/n4.json',
        'N3': 'https://raw.githubusercontent.com/TehSomeLuigi/jlpt-vocab/main/n3.json',
        'N2': 'https://raw.githubusercontent.com/TehSomeLuigi/jlpt-vocab/main/n2.json',
        'N1': 'https://raw.githubusercontent.com/TehSomeLuigi/jlpt-vocab/main/n1.json',
        'name': 'TehSomeLuigi/jlpt-vocab'
    },
]

def fetch_url(url):
    """URL 가져오기"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # CSV나 다른 형식일 수 있음
                return content
    except (HTTPError, URLError) as e:
        return None

def main():
    print("=== 다양한 GitHub JLPT 데이터 소스 시도 ===\n")
    
    for source in SOURCES:
        name = source.pop('name')
        print(f"=== {name} ===")
        
        all_data = {}
        total = 0
        
        for level, url in source.items():
            if level == 'name':
                continue
            print(f"  {level}: ", end="")
            data = fetch_url(url)
            
            if data:
                if isinstance(data, list):
                    count = len(data)
                elif isinstance(data, dict):
                    count = len(data.get('words', data.get('data', [])))
                else:
                    count = len(data.split('\n'))
                print(f"{count} items")
                all_data[level] = data
                total += count
            else:
                print("Failed")
        
        if total > 0:
            # 저장
            filename = f"jlpt_data_{name.replace('/', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            print(f"  => Total: {total} words, saved to {filename}\n")
        else:
            print(f"  => No data found\n")
        
        source['name'] = name  # restore

if __name__ == '__main__':
    main()

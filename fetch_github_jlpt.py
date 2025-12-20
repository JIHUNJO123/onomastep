#!/usr/bin/env python3
"""
GitHub에서 JLPT 단어 데이터셋 가져오기
공개된 JLPT 단어 목록을 사용
"""

import json
import urllib.request
from urllib.error import HTTPError, URLError

# 공개 JLPT 데이터셋 (GitHub raw files)
DATASETS = [
    # jisho-api/jlpt-vocab
    {
        'name': 'jlpt-vocab-N5',
        'url': 'https://raw.githubusercontent.com/jisho-api/jlpt-vocab/main/N5.json',
        'level': 'N5'
    },
    {
        'name': 'jlpt-vocab-N4',
        'url': 'https://raw.githubusercontent.com/jisho-api/jlpt-vocab/main/N4.json',
        'level': 'N4'
    },
    {
        'name': 'jlpt-vocab-N3',
        'url': 'https://raw.githubusercontent.com/jisho-api/jlpt-vocab/main/N3.json',
        'level': 'N3'
    },
    {
        'name': 'jlpt-vocab-N2',
        'url': 'https://raw.githubusercontent.com/jisho-api/jlpt-vocab/main/N2.json',
        'level': 'N2'
    },
    {
        'name': 'jlpt-vocab-N1',
        'url': 'https://raw.githubusercontent.com/jisho-api/jlpt-vocab/main/N1.json',
        'level': 'N1'
    },
]

# 대안: stephenmk/yomitan-jlpt-vocab (Tanos 기반)
YOMITAN_DATASETS = [
    {
        'name': 'yomitan-N5',
        'url': 'https://raw.githubusercontent.com/stephenmk/yomitan-jlpt-vocab/main/jlpt_n5.json',
        'level': 'N5'
    },
    {
        'name': 'yomitan-N4', 
        'url': 'https://raw.githubusercontent.com/stephenmk/yomitan-jlpt-vocab/main/jlpt_n4.json',
        'level': 'N4'
    },
    {
        'name': 'yomitan-N3',
        'url': 'https://raw.githubusercontent.com/stephenmk/yomitan-jlpt-vocab/main/jlpt_n3.json',
        'level': 'N3'
    },
    {
        'name': 'yomitan-N2',
        'url': 'https://raw.githubusercontent.com/stephenmk/yomitan-jlpt-vocab/main/jlpt_n2.json',
        'level': 'N2'
    },
    {
        'name': 'yomitan-N1',
        'url': 'https://raw.githubusercontent.com/stephenmk/yomitan-jlpt-vocab/main/jlpt_n1.json',
        'level': 'N1'
    },
]

def fetch_json(url):
    """JSON 가져오기"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except (HTTPError, URLError) as e:
        print(f"  Error: {e}")
        return None

def try_dataset(datasets, name):
    """데이터셋 시도"""
    print(f"\n=== {name} 시도 중 ===")
    all_words = {}
    
    for ds in datasets:
        print(f"  Fetching {ds['level']}...")
        data = fetch_json(ds['url'])
        
        if data:
            print(f"    Success: {len(data)} items")
            all_words[ds['level']] = data
        else:
            all_words[ds['level']] = []
    
    total = sum(len(w) for w in all_words.values())
    return all_words, total

def main():
    print("=== GitHub에서 JLPT 단어 데이터 가져오기 ===")
    
    # 여러 데이터셋 시도
    results = {}
    
    # 첫 번째 데이터셋 시도
    data1, total1 = try_dataset(DATASETS, "jisho-api/jlpt-vocab")
    if total1 > 0:
        results['jlpt-vocab'] = (data1, total1)
    
    # 두 번째 데이터셋 시도
    data2, total2 = try_dataset(YOMITAN_DATASETS, "stephenmk/yomitan-jlpt-vocab")
    if total2 > 0:
        results['yomitan'] = (data2, total2)
    
    # 가장 많은 데이터를 가진 것 선택
    if results:
        best_name = max(results, key=lambda x: results[x][1])
        best_data, best_total = results[best_name]
        
        print(f"\n=== 최종 결과: {best_name} ({best_total} words) ===")
        for level, words in best_data.items():
            print(f"  {level}: {len(words)} words")
        
        # 저장
        with open('github_jlpt_data.json', 'w', encoding='utf-8') as f:
            json.dump(best_data, f, ensure_ascii=False, indent=2)
        print("\nSaved to github_jlpt_data.json")
    else:
        print("\n모든 데이터셋 가져오기 실패")

if __name__ == '__main__':
    main()

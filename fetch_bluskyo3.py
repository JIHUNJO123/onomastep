#!/usr/bin/env python3
"""Bluskyo/JLPT_Vocabulary data/results 폴더에서 JLPT 단어 가져오기"""

import json
import urllib.request
from urllib.error import HTTPError, URLError

def fetch_url(url):
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except (HTTPError, URLError) as e:
        print(f"Error: {e}")
        return None

def fetch_raw(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return response.read().decode('utf-8')
    except (HTTPError, URLError) as e:
        print(f"Error: {e}")
        return None

def explore_dir(path, depth=0):
    """디렉토리 재귀 탐색"""
    url = f"https://api.github.com/repos/Bluskyo/JLPT_Vocabulary/contents/{path}"
    contents = fetch_url(url)
    
    if not contents:
        return {}
    
    indent = "  " * depth
    all_data = {}
    
    for item in contents:
        print(f"{indent}- {item['name']} ({item['type']})")
        
        if item['type'] == 'dir':
            sub_data = explore_dir(f"{path}/{item['name']}", depth + 1)
            all_data.update(sub_data)
        elif item['type'] == 'file' and (item['name'].endswith('.json') or item['name'].endswith('.csv')):
            print(f"{indent}  Download: {item['download_url']}")
            content = fetch_raw(item['download_url'])
            
            if content and item['name'].endswith('.json'):
                try:
                    data = json.loads(content)
                    count = len(data) if isinstance(data, list) else 1
                    print(f"{indent}  => {count} items")
                    
                    # 파일명에서 레벨 추출
                    name = item['name'].replace('.json', '')
                    all_data[name] = data
                    
                    if isinstance(data, list) and data:
                        print(f"{indent}  샘플: {str(data[0])[:100]}")
                except:
                    pass
    
    return all_data

def main():
    print("=== Bluskyo/JLPT_Vocabulary 전체 탐색 ===\n")
    
    all_data = explore_dir("data")
    
    if all_data:
        with open('bluskyo_full.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print("\n=== 최종 요약 ===")
        total = 0
        for key, data in sorted(all_data.items()):
            count = len(data) if isinstance(data, list) else 1
            print(f"  {key}: {count} items")
            total += count
        print(f"  총합: {total}")
        print(f"\n저장됨: bluskyo_full.json")

if __name__ == '__main__':
    main()

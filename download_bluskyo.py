#!/usr/bin/env python3
"""Bluskyo JLPTWords.json 다운로드 및 분석"""

import json
import urllib.request

url = "https://raw.githubusercontent.com/Bluskyo/JLPT_Vocabulary/main/data/results/JLPTWords.json"

print("Downloading JLPTWords.json...")
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(req, timeout=60) as response:
    content = response.read().decode('utf-8')

# 저장
with open('bluskyo_words.json', 'w', encoding='utf-8') as f:
    f.write(content)

# 분석
data = json.loads(content)
print(f"Type: {type(data)}")

if isinstance(data, dict):
    print(f"Keys: {list(data.keys())}")
    for key, value in data.items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} items")
            if value:
                print(f"    Sample: {value[0]}")
elif isinstance(data, list):
    print(f"Length: {len(data)}")
    if data:
        print(f"Sample: {data[0]}")

print("\nSaved to bluskyo_words.json")

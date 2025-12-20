#!/usr/bin/env python3
"""GitHub에서 JLPT 관련 저장소 검색"""

import json
import urllib.request

url = "https://api.github.com/search/repositories?q=jlpt+vocabulary+json&sort=stars&per_page=20"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/vnd.github.v3+json',
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=30) as response:
    data = json.loads(response.read().decode('utf-8'))

print("=== JLPT Vocabulary 관련 GitHub 저장소 ===\n")
for item in data.get('items', []):
    print(f"- {item['full_name']} ({item['stargazers_count']} stars)")
    print(f"  URL: {item['html_url']}")
    if item.get('description'):
        print(f"  설명: {item['description'][:80]}")
    print()

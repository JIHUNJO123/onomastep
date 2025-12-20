import json
import os
import sys

# 버퍼 비활성화
sys.stdout.reconfigure(line_buffering=True)

def load_json(filepath):
    """JSON 파일을 로드합니다."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_word(word_data, new_id, level):
    """단어 데이터를 통일된 형식으로 변환합니다."""
    # reading 필드 추출 (hiragana 또는 reading 필드에서)
    reading = word_data.get('reading', '') or word_data.get('hiragana', '')
    
    return {
        "id": new_id,
        "word": word_data.get('word', ''),
        "reading": reading,
        "definition": word_data.get('definition', ''),
        "level": level,
        "korean": word_data.get('korean', ''),
        "chinese": word_data.get('chinese', ''),
        "example": word_data.get('example', ''),
        "example_reading": word_data.get('example_reading', ''),
        "example_meaning": word_data.get('example_meaning', ''),
        "source": "Bluskyo/Tanos"
    }

def main():
    base_dir = r"C:\Users\hooni\Desktop\jlpt_vocab_app"
    
    # 파일 경로 정의
    files = {
        "N5": os.path.join(base_dir, "words_n5_final.json"),
        "N4": os.path.join(base_dir, "words_n4_final.json"),
        "N3": os.path.join(base_dir, "words_n3_final.json"),
    }
    
    merged_words = []
    level_counts = {}
    current_id = 1
    
    # 각 레벨별로 데이터 로드 및 변환
    for level in ["N5", "N4", "N3"]:
        filepath = files[level]
        print(f"Loading {level} from {filepath}...")
        
        words = load_json(filepath)
        level_counts[level] = len(words)
        
        for word in words:
            converted = convert_word(word, current_id, level)
            merged_words.append(converted)
            current_id += 1
    
    # 출력 디렉토리 확인 및 생성
    output_paths = [
        os.path.join(base_dir, "assets", "data", "words_n5_n3.json"),
        os.path.join(base_dir, "lib", "data", "words_n5_n3.json"),
    ]
    
    for output_path in output_paths:
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged_words, f, ensure_ascii=False, indent=2)
        
        print(f"Saved to {output_path}")
    
    # 결과 보고
    print("\n" + "=" * 50)
    print("병합 완료 보고서")
    print("=" * 50)
    for level, count in level_counts.items():
        print(f"{level}: {count}개 단어")
    print("-" * 50)
    print(f"총 단어 수: {len(merged_words)}개")
    print("=" * 50)
    
    # 샘플 데이터 출력
    print("\n샘플 데이터 (처음 3개):")
    for word in merged_words[:3]:
        print(json.dumps(word, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

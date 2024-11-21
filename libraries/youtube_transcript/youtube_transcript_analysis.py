#유튜브 자막 재일 자주 쓰는 단어수 조회를 json 파일로 불러오기
from youtube_transcript_api import YouTubeTranscriptApi
from collections import Counter
import re
import json

def get_transcript(video_id, language='ko'):
    """
    유튜브 동영상의 스크립트를 가져옵니다.

    Args:
        video_id (str): 유튜브 동영상 ID
        language (str): 자막 언어 (기본값: 'ko' - 한국어)

    Returns:
        transcript_text (str): 동영상의 전체 자막 텍스트
    """
    try:
        # 자막을 가져옴
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # 자막 텍스트를 하나의 문자열로 결합
        transcript_text = " ".join([entry['text'] for entry in transcript])

        return transcript_text

    except Exception as e:
        print(f"자막을 가져오지 못했습니다: {e}")
        return None

def analyze_transcript(transcript_text):
    """
    스크립트를 분석합니다.

    Args:
        transcript_text (str): 자막 텍스트

    Returns:
        analysis (dict): 분석 결과
    """
    # 텍스트를 소문자로 변환하고 특수 문자 제거
    clean_text = re.sub(r'\W+', ' ', transcript_text.lower())

    # 단어별로 분할
    words = clean_text.split()

    # 단어 빈도 계산
    word_count = Counter(words)

    # 자막의 총 단어 수
    total_words = len(words)

    # 자주 등장하는 단어 상위 10개
    common_words = word_count.most_common(10)

    analysis = {
        "total_words": total_words,
        "common_words": common_words,
    }

    return analysis

def save_analysis_to_json(analysis, filename="analysis_result.json"):
    """
    분석 결과를 JSON 파일로 저장합니다.

    Args:
        analysis (dict): 분석된 데이터
        filename (str): 저장할 파일 이름
    """
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(analysis, json_file, ensure_ascii=False, indent=4)
        print(f"분석 결과가 '{filename}' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

# 예시: 유튜브 동영상 ID로 자막을 추출하고 분석 후 JSON 파일로 저장
video_id = "DsOG8sk2aaY"  # 유튜브 동영상의 ID로 변경

# 자막 가져오기
transcript_text = get_transcript(video_id)

if transcript_text:
    print("자막 텍스트:\n", transcript_text[:200], "...\n")  # 처음 200자만 출력

    # 자막 분석하기
    analysis = analyze_transcript(transcript_text)

    print("자막 분석 결과:")
    print(f"총 단어 수: {analysis['total_words']}")
    print("자주 등장하는 단어 상위 10개:", analysis["common_words"])

    # 분석 결과를 JSON 파일로 저장
    save_analysis_to_json(analysis, "video_analysis_result.json")

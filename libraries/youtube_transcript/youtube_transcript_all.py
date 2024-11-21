#유튜브 자막 전체를 json 파일로 불러오기
from youtube_transcript_api import YouTubeTranscriptApi
import json

def get_transcript(video_id, language='ko'):
    """
    유튜브 동영상의 자막을 가져옵니다.

    Args:
        video_id (str): 유튜브 동영상 ID
        language (str): 자막 언어 (기본값: 'ko' - 한국어)

    Returns:
        transcript (list): 자막 항목 리스트
    """
    try:
        # 자막을 가져옴
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        return transcript

    except Exception as e:
        print(f"자막을 가져오지 못했습니다: {e}")
        return None

def save_transcript_to_json(transcript, filename="transcript_result.json"):
    """
    자막 텍스트와 관련 정보를 JSON 파일로 저장합니다.

    Args:
        transcript (list): 자막 항목 리스트
        filename (str): 저장할 파일 이름
    """
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(transcript, json_file, ensure_ascii=False, indent=4)
        print(f"자막이 '{filename}' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

# 예시: 유튜브 동영상 ID로 자막을 추출하고 JSON 파일로 저장
video_id = "4mN1AJEDBV"  # 유튜브 동영상의 ID로 변경

# 자막 가져오기
transcript = get_transcript(video_id)

if transcript:
    # 자막 정보를 JSON 파일로 저장
    save_transcript_to_json(transcript, "video_transcript.json")

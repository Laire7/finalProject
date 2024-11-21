import yt_dlp
import cv2
import os
import re
import time
import google.generativeai as genai
import IPython.display  # 동영상 플레이어 출력을 위해 추가
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ffmpeg 경로를 명확히 지정
ffmpeg_path = 'C:\Users\syoun\FinalProject\video_analysis\[;/ffmpeg.exe'  # 실제 경로로 수정

ydl_opts = {
    'ffmpeg_location': ffmpeg_path,  # ffmpeg 경로 설정
    'format': 'bestvideo+bestaudio/best',  # 최적의 비디오와 오디오 포맷 선택
    'outtmpl': 'downloads/%(id)s.%(ext)s',  # 다운로드 경로 및 파일명 형식
}

# 동영상 파일 업로드 하기 (로컬 경로)
file_path = 'C:/Users/SBA/gcloud/video_llm/videos/subway.mp4'
uploaded_file = genai.upload_file(path=file_path)
print("uploaded_file.uri:", uploaded_file.uri)

# 영상 상태 체크 (업로드 완료까지 대기)
while uploaded_file.state.name == "PROCESSING":
    print("processing video...")
    time.sleep(5)  # 5초마다 상태 체크
    uploaded_file = genai.get_file(name=uploaded_file.name)  # 파일 상태 갱신

print("File processing complete!")

# Gemini에 동영상 Q&A
model = genai.GenerativeModel(model_name="gemini-1.5-pro")
prompt = """
- 동영상을 분석하고 주요 장면마다 어떤 사건이 일어나는지, 대사 내용, 배경음악과 효과음의 분위기를 설명해 주세요.
"""
timeout = 60 * 2
contents = [prompt, uploaded_file]  # Multi Modal 요청
responses = model.generate_content(contents, stream=True, request_options={"timeout": timeout})

# Gemini 응답 처리 및 텍스트 파싱 (시간 범위 추출)
gemini_analysis = ""
for response in responses:
    gemini_analysis += response.text.strip()

print("Gemini 분석 결과:", gemini_analysis)

# 유튜브 동영상 URL
video_url = "https://www.youtube.com/watch?v=DsOG8sk2aaY"  # 예시 URL
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

# yt-dlp를 사용하여 비디오 다운로드
def download_video(video_url, output_dir):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_file = ydl.prepare_filename(info_dict)  # 다운로드 후 비디오 파일 경로 반환
        return video_file

# 프레임 추출 함수 정의
def extract_frames(video_file, gemini_analysis, output_dir):
    try:
        capture = cv2.VideoCapture(video_file)

        # Gemini 분석 결과에서 시간 정보 추출 (정규 표현식 사용)
        time_ranges = re.findall(r"\(([\d:]+-[\d:]+)\)", gemini_analysis)

        for i, time_range in enumerate(time_ranges):
            start_time_str, end_time_str = time_range.split("-")

            # 시간 문자열을 초 단위로 변환
            start_time = sum(int(x) * 60**i for i, x in enumerate(reversed(start_time_str.split(':'))))
            end_time = sum(int(x) * 60**i for i, x in enumerate(reversed(end_time_str.split(':'))))

            # 시작 시간과 끝 시간 사이의 중간 지점 프레임 추출
            mid_time = (start_time + end_time) / 2
            capture.set(cv2.CAP_PROP_POS_MSEC, mid_time * 1000)
            ret, frame = capture.read()

            if ret:
                output_path = os.path.join(output_dir, f"frame_{i:04d}.jpg")
                cv2.imwrite(output_path, frame)
                print(f"프레임 {i} 저장 완료: {output_path}, 시간: {mid_time}초")
            else:
                print(f"프레임 {i} 읽기 실패")

        capture.release()

    except Exception as e:
        print(f"오류 발생: {e}")

# 비디오 다운로드 및 프레임 추출 실행
video_file = download_video(video_url, output_dir)
extract_frames(video_file, gemini_analysis, output_dir)

# 동영상 플레이어 출력 (IPython)
IPython.display.display(IPython.display.Video(video_file, width=800, embed=True))

#   File "C:\Users\SBA\anaconda3\envs\streamlit101\lib\site-packages\yt_dlp\YoutubeDL.py", line 1090, in report_error
#     self.trouble(f'{self._format_err("ERROR:", self.Styles.ERROR)} {message}', *args, **kwargs)
#   File "C:\Users\SBA\anaconda3\envs\streamlit101\lib\site-packages\yt_dlp\YoutubeDL.py", line 1029, in trouble
#     raise DownloadError(message, exc_info)
# yt_dlp.utils.DownloadError: ERROR: You have requested merging of multiple formats but ffmpeg is not installed. Aborting due to --abort-on-error
# PS C:\Users\SBA\gcloud\video_llm>
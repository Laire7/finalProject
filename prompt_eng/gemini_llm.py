# st_chatbot.py
import google.generativeai as genai 
import streamlit as st
from dotenv import load_dotenv
import os

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Gemini-Bot")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash',
            generation_config=generation_config)
    print("model loaded...")
    return model

def text_speech(text):
    tts = gTTS(text=text, lang='en')
    speech_bytes = io.BytesIO()
    tts.write_to_fp(speech_bytes)
    speech_bytes.seek(0)

    # Convert speech to base64 encoding
    speech_base64 = base64.b64encode(speech_bytes.read()).decode('utf-8')
    return speech_base64

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

model = load_model()

# streamlit에서 chat사용시 history관리를 해줘야 한다.
if "chat_session" not in st.session_state:    
    st.session_state["chat_session"] = model.start_chat(history=[]) 

# 채팅 메시지를 출력
for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)
        audio=text_to_audio(content.parts[0].text,language='en',cleanup_hook=None)
        autoplay_audio(audio)

if prompt := st.chat_input("메시지를 입력하세요."):    
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)
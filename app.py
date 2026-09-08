import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid, datetime, time, re, json
from datetime import datetime as dt

st.set_page_config(page_title="Aditya AI - Belpahar 500 Lines Final", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff}
.stChatMessage{background:rgba(255,255,255,0.08)!important;border-radius:18px!important;border:1px solid rgba(255,255,255,0.1);padding:18px;margin:12px 0;backdrop-filter:blur(10px)}
.stChatMessage[data-testid*="user"]{background:linear-gradient(135deg,#667eea,#764ba2)!important}
h1{color:#00f2fe;text-align:center;font-weight:800;text-shadow:0 0 20px #00f2fe}
h2,h3{color:#f0f0f0}
.stButton>button{background:linear-gradient(90deg,#00f2fe,#4facfe);color:#000;font-weight:700;border-radius:10px;border:none;transition:0.3s}
.stButton>button:hover{transform:scale(1.03);box-shadow:0 0 15px #00f2fe}
#MainMenu{visibility:hidden} footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "msgs" not in st.session_state:
    st.session_state.msgs = []
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"c1": {"title": "New Chat Belpahar", "msgs": [], "created": str(dt.now())}}
if "cid" not in st.session_state:
    st.session_state.cid = "c1"
if "last_hash" not in st.session_state:
    st.session_state.last_hash = ""
if "last_text" not in st.session_state:
    st.session_state.last_text = ""
if "voice" not in st.session_state:
    st.session_state.voice = True
if "search_q" not in st.session_state:
    st.session_state.search_q = ""
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

SYSTEM_PROMPT = """
You are Aditya AI, created by Aditya from Belpahar, Odisha, India.
You are NOT ChatGPT, NOT Meta AI, you are Aditya AI.
Rules:
- Hindi input -> Hindi output, English -> English, Hinglish -> Hinglish (Haan bhai yaar style)
- Photoshop, Photo Editing, Graphic Design expert
- Friendly, helpful, from Belpahar
- Never output Urdu/Arabic script, always convert to Hinglish
- Keep answers clear, useful, practical
"""

def is_hindi(text):
    return any("\u0900" <= c <= "\u097F" for c in text)

def is_urdu(text):
    return any("\u0600" <= c <= "\u06FF" for c in text)

def clean_text(t):
    t = t.replace("*", "").replace("#", "")
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def text_to_speech(text):
    try:
        if not text or len(text) < 2:
            return None
        clean = clean_text(text)[:450]
        lang = "hi" if is_hindi(clean) or "bhai" in clean.lower() or "yaar" in clean.lower() else "en"
        tts = gTTS(text=clean, lang=lang, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"TTS error {e}")
        return None

def speech_to_text(audio_file):
    try:
        data = audio_file.getvalue()
        if len(data) < 2500:
            return None
        transcription = client.audio.transcriptions.create(
            file=("voice.wav", data, "audio/wav"),
            model="whisper-large-v3",
            response_format="text",
           

import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid, datetime, time

st.set_page_config(page_title="Aditya AI - Final", page_icon="🤖", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages=[]
if "all_chats" not in st.session_state: st.session_state.all_chats={"chat_1":{"title":"New Chat","messages":[]}}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id="chat_1"
if "page" not in st.session_state: st.session_state.page="chat"
if "voice_enabled" not in st.session_state: st.session_state.voice_enabled=True
if "last_audio_hash" not in st.session_state: st.session_state.last_audio_hash=None
if "last_text" not in st.session_state: st.session_state.last_text=None

SYSTEM="You are Aditya AI from Belpahar, Odisha. NOT ChatGPT. Hindi->Hindi, English->English, Hinglish like Haan bhai."

def speak(t):
    try:
        lang='hi' if any('\u0900'<=c<='\u097F' for c in t) else 'en'
        c=t[:400].replace('*','')
        tts=gTTS(c,lang=lang)
        b=io.BytesIO(); tts.write_to_fp(b); b.seek(0); return b
    except: return None

def transcribe(a):
    try:
        d=a.getvalue()
        if len(d)<2000: return None
        r=client.audio.transcriptions.create(file=("a.wav",d,"audio/wav"),model="whisper-large-v3",response_format="text",prompt="Hindi Hinglish English")
        txt=r if isinstance(r,str) else r.text
        txt=txt.strip()
        if any('\u0600'<=c<='\u06FF' for c in txt):
            cc=client.chat.completions.create(model="openai/gpt-oss-20b",messages=[{"role":"system","content":"Urdu to Hinglish"},{"role":"user","content":txt}],max_tokens=100)
            txt=cc.choices[0].message.content
        return txt
    except Exception as e: st.error(e); return None

with st.sidebar:
    st.markdown("## ✨ Aditya AI")
    if st.button("💬 Chat Page",use_container_width=True): st.session_state.page="chat"; st.rerun()
    if st.button("📝 Blog / About",use_container_width=True): st.session_state.page="blog"; st.rerun()
    if st.button("🎤 Voice Chat",use_container_width=True): st.session_state.page="voice"; st.rerun()
    st.divider()
    st.session_state.voice_enabled=st.toggle("🔊 Voice ON",value=st.session_state.voice_enabled)
    st.divider()
    if st.button("➕ New Chat",use_container_width=True):
        nid=f"chat_{uuid.uuid4().hex[:4]}"; st.session_state.current_chat_id=nid; st.session_state.messages=[]; st.session_state.all_chats[nid]={"title":"New Chat","messages":[]}; st.session_state.last_audio_hash=None; st.rerun()
    st.divider()
    st.markdown("### 📜 History")
    for cid,data in list(st.session_state.all_chats.items())[::-1][:10]:
        if st.button(f"{data['title'][:20]}",key=f"h_{cid}",use_container_width=True):
            st.session_state.current_chat_id=cid
            

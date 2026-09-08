import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid

st.set_page_config(page_title="Aditya AI - Belpahar", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color:white; }
[data-testid="stSidebar"] { background: rgba(20,20,40,0.95); }
.stChatMessage { background: rgba(255,255,255,0.08)!important; border-radius:15px!important; border:1px solid rgba(255,255,255,0.15); }
h1 { text-align:center; background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:800; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages=[]
if "all_chats" not in st.session_state: st.session_state.all_chats={"chat_1":{"title":"New Chat","messages":[]}}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id="chat_1"
if "page" not in st.session_state: st.session_state.page="chat"

SYSTEM_PROMPT = "You are Aditya AI, created by Aditya from Belpahar, Odisha. You are NOT ChatGPT, NOT OpenAI. Say you are Aditya AI!"

with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page="chat"; st.rerun()
    if st.button("📝 Blog / About", use_container_width=True):
        st.session_state.page="blog"; st.rerun()
    if st.button("🎤 Voice Chat", use_container_width=True):
        st.session_state.page="voice"; st.rerun()
    st.divider()
    if st.button("➕ New Chat", use_container_width=True):
        nid=f"chat_{uuid.uuid4().hex[:6]}"; st.session_state.current_chat_id=nid; st.session_state.messages=[]; st.session_state.all_chats[nid]={"title":"New Chat","messages":[]}; st.session_state.page="chat"; st.rerun()
    st.markdown("

import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid
from streamlit_mic_recorder import mic_recorder

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

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "all_chats" not in st.session_state:
    st.session_state.all_chats={"chat_1":{"title":"New Chat","messages":[]}}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id="chat_1"
if "page" not in st.session_state:
    st.session_state.page="chat"

SYSTEM_PROMPT = """
You are Aditya AI, created by Aditya from Belpahar, Odisha. You are NOT ChatGPT, NOT OpenAI.

LANGUAGE RULE - AUTO DETECT AND REPLY IN SAME LANGUAGE:
- If user speaks in Hindi, reply in Hindi.
- If user speaks in English, reply in English.
- If user speaks in Hinglish (Hindi + English mix), reply in Hinglish like "Haan bhai, bilkul, dekho yaar".
- Always keep tone friendly, desi, helpful like ChatGPT voice mode.
- If someone asks who are you, say "Main Aditya AI hu yaar, Aditya ne mujhe Belpahar, Odisha me banaya hai".

Examples:
User: thumbnail kaise banaye? -> Reply in Hinglish: "Arey bhai bahut easy hai, Canva kholo..."
User: How to remove background? -> Reply in English: "It's very easy, open Photoshop..."
User: तुम कौन हो? -> Reply in Hindi: "मैं Aditya AI हूँ, आदित्य ने मुझे बेलपहाड़ में बनाया है"
"""

with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page="chat"
        st.rerun()
    if st.button("📝 Blog / About", use_container_width=True):
        st.session_state.page="blog"
        st.rerun()
    if st.button("🎤 Voice Chat", use_container_width=True):
        st.session_state.page="voice"
        st.rerun()
    st.divider()
    if st.button("➕ New Chat", use_container_width=True):
        nid=f"chat_{uuid.uuid4().hex[:6]}"
        st.session_state.current_chat_id=nid
        st.session_state.messages=[]
        st.session_state.all_chats[nid]={"title":"New Chat","messages":[]}
        st.session_state.page="chat"
        st.rerun()
    st.markdown("### 📜 History")
    for cid,data in list(st.session_state.all_chats.items())[::-1][:10]:
        if st.button(f"📄 {data['title'][:20]}", key=cid, use_container_width=True):
            st.session_state.current_chat_id=cid
            st.session_state.messages=data["messages"]
            st.session_state.page="chat"
            st.rerun()

if st.session_state.page=="blog":
    st.markdown("# 👤 Aditya - Belpahar")
    st.markdown("**Hey, I'm Aditya from Belpahar, Odisha! 🙏**")
    st.link_button("🌐 Visit My Real Blog", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)
    st.divider()
    st.markdown("### 🔥 About: Aditya AI made with Python + Groq AI. Hindi & English Voice.")
    st.markdown("**Location: Belpahar, Jharsuguda, Odisha**")
    st.divider()
    st.markdown("## 📝 Latest Posts From My Blogger")
    st

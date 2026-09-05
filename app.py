import streamlit as st
from groq import Groq
import io
import uuid
import time
from datetime import datetime

# ============================================================
# TTS
# ============================================================
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# ============================================================
# SAFE KEY LOADER - WILL NOT GO BLANK
# ============================================================
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("Add GROQ_API_KEY in Secrets")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ============================================================
# SIMPLE PREMIUM CSS - SINGLE LINE - NO TRIPLE QUOTES - NO ERROR
# ============================================================
st.markdown('<style>[data-testid="stSidebar"]{background:#0f0f12;} div[data-testid="stButton"]>button{background:#1e1e26!important;border:1px solid #2a2a35!important;color:#ccc!important;border-radius:12px!important;height:42px!important;} div[data-testid="stButton"]>button:hover{border-color:#ff6a00!important;color:white!important;}</style>', unsafe_allow_html=True)
st.markdown('<div style="position:fixed;top:0;left:0;right:0;height:0px;"></div>', unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[st.session_state.current_chat_id] = {"title": "New Chat", "messages": [], "time": datetime.now().strftime("%d %b")}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

def new_chat():
    if st.session_state.messages:
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = st.session_state.messages[0]["content"][:35]
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    nid = str(uuid.uuid4())
    st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title": "New Chat", "messages": [], "time": datetime.now().strftime("%d %b")}
    st.session_state.messages = []

def load_chat(cid):
    st.session_state.current_chat_id = cid
    st.session_state.messages = st.session_state.all_chats[cid]["messages"]

# ============================================================
# SIDEBAR - PREMIUM LOOK - SIMPLE CODE
# ============================================================
with st.sidebar:
    st.title("🔥 Aditya AI")
    st.caption("Next-Gen Voice AI v5.1 FINAL")
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()
    st.markdown("📍 Belpahar, Odisha ● LIVE")
    st.markdown("**💬 History**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if cid == st.session_state.current_chat_id:
            continue
        if not chat["messages"]:

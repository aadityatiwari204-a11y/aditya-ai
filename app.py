import streamlit as st
from groq import Groq
import uuid
import base64
from datetime import datetime

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- CSS ---
st.markdown('''
<style>
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f12 0%, #1a1a22 100%);
        border-right: 1px solid #2a2a35;
    }
   .sidebar-logo {
        font-size: 28px; font-weight: 800;
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
   .sidebar-card {
        background: #21212a; padding: 12px; border-radius: 12px;
        border: 1px solid #2f2f3d; margin: 10px 0;
    }
    div[data-testid="stButton"] > button {
        font-size: 12.5px!important; border-radius: 12px!important;
        background: #1e1e26!important; border: 1px solid #2a2a35!important;
        height: 42px!important;
    }
    div[data-testid="stButton"] > button:hover {
        background: #2a2a38!important; border-color: #ff6a00!important; color: white!important;
    }
    [data-testid="stTextInput"] input {
        border-radius: 24px!important; height: 48px!important;
        background: #252530!important; border: 1px solid #333!important;
    }
   .img-card {
        background: #1e1e26; border: 1px dashed #3a3a4a;
        border-radius: 16px; padding: 14px; margin-bottom: 8px;
    }
   .ready-dot { display:flex; gap:6px; align-items:center; font-size:11px; color:#00ff88; }
   .ready-dot span { width:6px; height:6px; background:#00ff88; border-radius:50%; box-shadow:0 0 8px #00ff88; display:inline-block; }
</style>
''', unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[st.session_state.current_chat_id] = {"title": "New Chat", "messages": [], "time": datetime.now().strftime("%d %b")}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "img_b64" not in st.session_state:
    st.session_state.img_b64 = None

def new_chat():
    if st.session_state.messages:
        title = st.session_state.messages[0]["content"][:30] + "..."
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = title
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    nid = str(uuid.uuid4())
    st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title": "New Chat", "messages": [], "time": datetime.now().strftime("%d %b")}
    st.session_state.messages = []
    st.session_state.img_b64 = None

def load_chat(cid):
    st.session_state.current_chat_id = cid
    st.session_state.messages = st.session_state.all_chats[cid]["messages"]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI")
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()
    st.markdown('<div class="sidebar-card" style="display:flex; justify-content:space-between;"><span>📍 Belpahar, Odisha</span><span style="font-size:10px; background:#00ff8820; color:#00ff88; padding:4px 8px; border-radius:20px;">● LIVE</span></div>', unsafe_allow_html=True)
    st.markdown("**💬 History**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if cid == st.session_state.current_chat_id: continue
        if not chat["messages"]: continue
        if st.button(f"📝 {chat['title']}", key=cid, use_container_width=True):
            load_chat(cid)
            st.rerun()
    st.markdown("---")
    st.markdown

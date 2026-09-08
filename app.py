import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import uuid
from streamlit_mic_recorder import mic_recorder
import datetime

# ============================================================
# PAGE CONFIG - Aditya AI Belpahar
# ============================================================
st.set_page_config(
    page_title="Aditya AI - Belpahar",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - Gradient Background
# ============================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color:white;
}
[data-testid="stSidebar"] {
    background: rgba(20,20,40,0.95);
    border-right: 1px solid rgba(255,255,255,0.1);
}
.stChatMessage {
    background: rgba(255,255,255,0.08)!important;
    border-radius:15px!important;
    border:1px solid rgba(255,255,255,0.15);
    padding: 15px;
}
h1 {
    text-align:center;
    background: linear-gradient(90deg, #00f2fe, #4facfe);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-weight:800;
    font-size: 3rem;
}
.stButton>button {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# GROQ CLIENT INIT
# ============================================================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("GROQ_API_KEY nahi mila secrets me. Streamlit secrets me add karo.")
    st.stop()

# ============================================================
# SESSION STATE INIT - Saare variables
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {
        "chat_1": {"title": "New Chat", "messages": [], "time": str(datetime.datetime.now())}
    }

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# ============================================================
# SYSTEM PROMPT - FINAL FIX FOR HINDI + ENGLISH + HINGLISH
# ============================================================
SYSTEM_PROMPT = """
You are Aditya AI, created by Aditya from Belpahar, Odisha, India.
You are NOT ChatGPT, you are NOT made by OpenAI.

LANGUAGE RULE - THIS IS MOST IMPORTANT:
You must automatically detect user's language and reply in SAME language.
- If user writes in Hindi like "तुम कौन हो" -> Reply in pure Hindi: "मैं Aditya AI हूँ..."
- If user writes in English like "Who are you?" -> Reply in pure English: "I am Aditya AI..."
- If user writes in Hinglish like "bhai tu kaun hai?" or "thumbnail kaise banaye" -> Reply in Hinglish: "Haan bhai main Aditya AI hu yaar, Aditya ne mujhe Belpahar me banaya hai, dekho thumbnail banana bahut easy hai..."

Style: Friendly, helpful, short, like a friend from Odisha.
Always be helpful for Photoshop, Editing, Design questions.
"""

# ============================================================
# SIDEBAR - Navigation + History + Search
# ============================================================
with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    st.caption("Made by Aditya | Belpahar, Jharsuguda")

    st.divider()

    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()

    if st.button("📝 Blog / About", use_container_width=True):
        st.session_state.page = "blog"
        st.rerun()

    if st.button("🎤 Voice Chat", use_container_width=True):
        st.session_state.page = "voice"
        st.rerun()

    st.divider()

    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        nid = f"chat_{uuid.uuid4().hex[:6]}"
        st.session_state.current_chat_id = nid
        st.session_state.messages = []
        st.session_state.all_chats[nid] = {
            "title": "New Chat",
            "messages": [],
            "time": str(datetime.datetime.now())
        }
        st.session_state.page = "chat"
        st.rerun()

    st.markdown("### 🔍 Search Chats")
    search_input = st.text_input(
        "search",
        placeholder="Search...",
        label_visibility="collapsed"
    )

    st.markdown("### 📜 History")

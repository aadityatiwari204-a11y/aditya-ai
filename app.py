import streamlit as st
from groq import Groq
import io
import uuid
import time
from datetime import datetime

# ============================================================
# IMPORT TTS - Optional
# ============================================================
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

# ============================================================
# PAGE CONFIG - MUST BE FIRST
# ============================================================
st.set_page_config(
    page_title="Aditya AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SAFE API KEY LOADER - PREVENTS BLANK SCREEN
# ============================================================
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    if not GROQ_KEY:
        st.error("GROQ_API_KEY is empty in Secrets")
        st.stop()
except Exception as e:
    st.error("⚠️ GROQ_API_KEY not found! Go to Streamlit Dashboard > Your App > Settings > Secrets and add:")
    st.code('GROQ_API_KEY = "gsk_xxxx"')
    st.write(f"Error detail: {e}")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ============================================================
# BIG PREMIUM CSS - FULLY EXPANDED
# ============================================================
BIG_CSS = '''
<style>
    /* ============================================ */
    /* GLOBAL RESET AND DARK THEME */
    /* ============================================ */
    header[data-testid="stHeader"] {
        background: transparent!important;
    }
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }

    /* ============================================ */
    /* SIDEBAR - PREMIUM DARK GRADIENT */
    /* ============================================ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f12 0%, #1a1a22 100%);
        border-right: 1px solid #2a2a35;
    }

   .sidebar-logo {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.5px;
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 4s ease infinite;
        margin-bottom: 4px;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

   .sidebar-card {
        background: #21212a;
        padding: 12px 14px;
        border-radius: 12px;
        border: 1px solid #2f2f3d;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* ============================================ */
    /* MOBILE TOP BAR - LIKE CHATGPT */
    /* ============================================ */
    @media (max-width: 768px) {
       .mobile-top-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 56px;
            background: rgba(15,15,18,0.92);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid #2a2a35;
            display: flex;
            align-items: center;
            padding-left: 52px;
            z-index: 999;
        }
       .mobile-logo {
            font-weight: 800;
            font-size: 18px;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
       .block-container {
            padding-top: 70px!important;
        }
        div[data-testid="stHorizontalBlock"] {
            gap: 8px!important;
        }
        [data-testid="stColumn"] {
            width: calc(50% - 4px)!important;
            flex: 1 1 calc(50% - 4px)!important;
            min-width: calc(50% - 4px)!important;
        }
    }

    @media (min-width: 769px) {
       .mobile-top-bar {
            display: none;
        }
    }

    /* ============================================ */
    /* SUGGESTION BUTTONS - PREMIUM */
    /* ============================================ */
    div[data-testid="stButton"] > button {
        font-size: 12.5px!important;
        padding: 0 10px!important;
        border-radius: 12px!important;
        background: #1e1e26!important;
        border: 1px solid #2a2a35!important;
        color: #ccc!important;
        height: 42px!important;
        min-height: 42px!important;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    div[data-testid="stButton"] > button:hover {
        background: #2a2a38!important;
        border-color: #ff6a00!important;
        color: white!important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255,106,0,0.2);
    }

    /* ============================================ */
    /* CHAT MESSAGE SLIDE UP ANIMATION */
    /* ============================================ */
    [data-testid="stChatMessage"] {
        animation: slideUp 0.35s ease-out;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ============================================ */
    /* INPUT FOCUS GLOW */
    /* ============================================ */
    [data-testid="stChatInput"]:focus-within {
        border-color: #ff6a00!important;
        box-shadow: 0 0 0 3px #ff6a0030!important;
    }

    /* ============================================ */
    /* THINKING BUBBLE - CHATGPT STYLE */
    /* ============================================ */
   .thinking-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #1c1c24;
        border: 1px solid #2a2a35;
        padding: 14px 18px;
        border-radius: 16px;
        width: fit-content;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }

   .thinking-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff6a00, #ee0979);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulseGlow 2s infinite;
        font-size: 16px;
    }

   .dots {
        display: flex;
        gap: 4px;
        margin-top: 4px;
    }

   .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #ff6a00;
        animation: bounceDot 1.4s infinite;
    }

   .dot:nth-child(2) {
        animation-delay: 0.2s;
        background: #ff8a33;
    }

   .dot:nth-child(3) {
        animation-delay: 0.4s;
        background: #ee0979;
    }

    @keyframes bounceDot {
        0%, 80%, 100% {
            transform: translateY(0);
            opacity: 0.5;
        }
        40% {
            transform: translateY(-6px);
            opacity: 1;
        }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(255,106,0,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255,106,0,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,106,0,0); }
    }

   .shimmer-text {
        background: linear-gradient(90deg, #888 0%, #fff 50%, #888 100%);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 1.5s infinite linear;
        font-size: 13px;
        font-weight: 500;
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

   .ready-dot {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        color: #00ff88;
        margin: 6px 0 4px 2px;
        font-weight: 600;
    }

   .ready-dot span {
        width: 6px;
        height: 6px;
        background: #00ff88;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #00ff88;
        animation: blink 2s infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

   .voice-sub {
        font-size: 12px;
        color: #888;
        margin-bottom: 8px;
    }
</style>

<div class="mobile-top-bar">
    <div class="mobile-logo">🔥 Aditya AI</div>
</div>
'''

st.markdown(BIG_CSS, unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[st.session_state.current_chat_id] = {
        "title": "New Chat",
        "messages": [],
        "time": datetime.now().strftime("%d %b")
    }

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ============================================================
# CHAT HISTORY FUNCTIONS
# ============================================================
def new_chat():
    # Save current before creating new
    if st.session_state.messages:
        title = st.session_state.messages[0]["content"][:35]
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = title
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages

    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.all_chats[new_id] = {
        "title": "New Chat",
        "messages": [],
        "time": datetime.now().strftime("%d %b")
    }
    st.session_state.messages = []

def load_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = st.session_state.all_chats[chat_id]["messages"]

# ============================================================
# SIDEBAR UI
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI • Belpahar")

    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()

    st.markdown("""
    <div class="sidebar-card" style="display:flex; justify-content:space-between; align-items:center">
        <span style="font-size:13px">📍 Belpahar, Odisha</span>
        <span style="font-size:10px; background:#00ff8820; color:#00ff88; padding:4px 8px; border-radius:20px;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**💬 History**")

    # Render history
    chat_items = list(st.session_state.all_chats.items())
    for cid, chat in reversed(chat_items):
        if cid == st.session_state.current_chat_id:
            continue
        if not chat["messages"]:
            continue
        display_title = chat["title"][:28] + ".." if len(chat["title"]) > 28 else chat["title"]
        if st.button(f"📝 {display_title}", key=cid, use_container_width=True):
            load_chat(cid)
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div class="sidebar-card" style="font-size:12px; color:#888; text-align:center; line-height:1.6">
        Made with ❤️ in Belpahar<br>
        <b>v4.5 BIG</b> • Streaming + History + Voice<br>
        Groq • Whisper • Llama 3.3 70B<br>
        Attractiveness 100% Kept
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN CHAT - WELCOME SCREEN
# ============================================================
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.markdown('<div class="ready-dot"><span></span> Aditya AI is ready • v4.5 BIG</div>', unsafe_allow_html=True)
        st.caption("Built by Aditya from Belpahar — Ask me anything. Voice + Streaming + History all working.")

        # Suggestion Buttons Row 1
        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("💡 What can you do?", use_container_width=True, key="s1"):
                st.session_state.pending_prompt = "What can you do?"
                st.rerun()
        with col2:
            if st.button("💻 Python help", use_container_width=True, key="s2"):
                st.session_state.pending_prompt = "Help me write Python code for beginners"
                st.rerun()

        # Row 2
        col3, col4 = st.columns(2, gap="small")
        with col3:
            if st.button("🌐 Today's news", use_container_width=True, key="s3"):
                st.session_state.pending_prompt = "Tell me today's top news in India"
                st.rerun()
        with col4:
            if st.button("🧠 Explain physics", use_container_width=True, key="s4"):
                st.session_state.pending_prompt = "Explain quantum physics in simple words"
                st.rerun()

        st.markdown("")
        st.info("💡 Tip: Use 🎙️ Voice Chat below to talk, or type in the box.")

else:
    # Show existing chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ============================================================
# VOICE CHAT SECTION
# ============================================================
st.markdown("#### 🎙️ Voice Chat")
st.markdown('<div class="voice-sub">Tap the microphone icon to start speaking in Hindi or English</div>', unsafe_allow_html=True)

audio_data = st.audio_input("Record your voice")

transcribed_text = None

if audio_data is not None:
    holder = st.empty()
    holder.markdown('<div style="color:#ff5555; font-size:13px">🔴 Recording received — transcribing with Whisper...</div>', unsafe_allow_html=True)
    try:
        transcription_result = client.audio.transcriptions.create(
            file=("audio.wav", audio_data.getvalue(), "audio/wav"),
            model="whisper-large-v3",
            response_format="text",
            language="hi"
        )
        transcribed_text = str(transcription_result)
        holder.empty()
        st.success(f"🎤 You said: {transcribed_text}")
    except Exception as err:
        holder.empty()
        st.error(f"Voice Error: {err}")

# ============================================================
# TEXT INPUT
# ============================================================
text_input = st.chat_input("🎙️ Ask anything... or use mic above ↑")

# Handle suggestion click
if st.session_state.pending_prompt:
    text_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# Handle voice
if transcribed_text:
    text_input = transcribed_text

# ============================================================
# FINAL PROCESSING WITH STREAMING
# ============================================================
if text_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": text_input})

    # Update chat title
    if len(st.session_state.messages) == 1:
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = text_input[:35]

    with st.chat_message("user"):
        st.markdown(text_input)

    with st.chat_message("assistant"):
        thinking_box = st.empty()
        thinking_box.markdown("""
        <div class="thinking-wrap">
            <div class="thinking-avatar">🔥</div>

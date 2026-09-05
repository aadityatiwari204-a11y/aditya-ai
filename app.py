import streamlit as st
from groq import Groq
import io
import uuid
from datetime import datetime

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- KEEP ALL YOUR PREMIUM CSS ---
st.markdown("""
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
        background-size: 200% 200%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: gradientMove 4s ease infinite;
    }
    @keyframes gradientMove {
        0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}
    }
 .sidebar-card {
        background: #21212a; padding: 12px; border-radius: 12px;
        border: 1px solid #2f2f3d; margin: 10px 0;
    }
 .new-chat-btn {
        background: linear-gradient(90deg, #ff6a00, #ee0979)!important;
        color: white!important; border: none!important;
        border-radius: 10px!important; font-weight: 600!important;
    }
 .chat-history-item {
        padding: 8px 10px; border-radius: 8px; font-size: 13px;
        color: #bbb; cursor: pointer; margin: 3px 0;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        border: 1px solid transparent;
    }
 .chat-history-item:hover { background: #2a2a38; color: white; border-color: #2f2f3d; }
 .chat-history-active { background: #2a2a38!important; color: white!important; border-color: #ff6a00!important; }

    @media (max-width: 768px) {
      .mobile-top-bar {
            position: fixed; top: 0; left: 0; right: 0; height: 56px;
            background: rgba(15,15,18,0.92); backdrop-filter: blur(12px);
            border-bottom: 1px solid #2a2a35;
            display: flex; align-items: center; padding-left: 52px; z-index: 999;
        }
      .mobile-logo {
            font-weight: 800; font-size: 18px;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
      .block-container { padding-top: 70px!important; }
        div[data-testid="stHorizontalBlock"] { gap: 8px!important; }
        [data-testid="stColumn"] {
            width: calc(50% - 4px)!important;
            flex: 1 1 calc(50% - 4px)!important;
            min-width: calc(50% - 4px)!important;
        }
    }
    @media (min-width: 769px) {.mobile-top-bar { display: none; } }

    div[data-testid="stButton"] > button {
        font-size: 12.5px!important; padding: 0 10px!important;
        border-radius: 12px!important; background: #1e1e26!important;
        border: 1px solid #2a2a35!important; color: #ccc!important;
        height: 42px!important; min-height: 42px!important;
        transition: all 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        background: #2a2a38!important; border-color: #ff6a00!important;
        color: white!important; transform: translateY(-1px);
    }
    [data-testid="stChatMessage"] { animation: slideUp 0.3s ease-out; }
    @keyframes slideUp { from { opacity:0; transform: translateY(10px);} to { opacity:1; transform: translateY(0);} }
    [data-testid="stChatInput"]:focus-within {
        border-color: #ff6a00!important; box-shadow: 0 0 0 3px #ff6a0030!important;
    }
  .thinking-wrap {
        display: flex; align-items: center; gap: 12px;
        background: #1c1c24; border: 1px solid #2a2a35;
        padding: 14px 18px; border-radius: 16px; width: fit-content;
    }
  .thinking-avatar {
        width: 32px; height: 32px; border-radius: 50%;
        background: linear-gradient(135deg, #ff6a00, #ee0979);
        display: flex; align-items: center; justify-content: center;
        animation: pulseGlow 2s infinite;
    }
  .dots { display: flex; gap: 4px; }
  .dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #ff6a00; animation: bounceDot 1.4s infinite;
    }
  .dot:nth-child(2) { animation-delay: 0.2s; background: #ff8a33; }
  .dot:nth-child(3) { animation-delay: 0.4s; background: #ee0979; }
    @keyframes bounceDot { 0%, 80%, 100% { transform: translateY(0); opacity: 0.5; } 40% { transform: translateY(-6px); opacity: 1; } }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(255,106,0,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255,106,0,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,106,0,0); }
    }
  .shimmer-text {
        background: linear-gradient(90deg, #888 0%, #fff 50%, #888 100%);
        background-size: 200% 100%; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 1.5s infinite linear; font-size: 13px;
    }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
  .ready-dot {
        display: flex; align-items: center; gap: 6px;
        font-size: 11px; color: #00ff88; margin: 6px 0 4px 2px;
    }
  .ready-dot span {
        width: 6px; height: 6px; background: #00ff88; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 8px #00ff88;
    }
  .voice-sub { font-size: 12px; color: #888; margin-bottom: 8px; }
</style>
<div class="mobile-top-bar"><div class="mobile-logo">🔥 Aditya AI</div></div>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- CHAT HISTORY LOGIC ---
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
    # Save current chat if not empty
    if st.session_state.messages:
        if len(st.session_state.messages) > 0:
            title = st.session_state.messages[0]["content"][:30] + "..."
            st.session_state.all_chats[st.session_state.current_chat_id]["title"] = title
            st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    # Create new
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.all_chats[new_id] = {"title": "New Chat", "messages": [], "time": datetime.now().strftime("%d %b")}
    st.session_state.messages = []

def load_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = st.session_state.all_chats[chat_id]["messages"]

# SIDEBAR
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI")

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
    # Show history newest first
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if cid == st.session_state.current_chat_id:
            continue
        if not chat["messages"]:
            continue
        if st.button(f"📝 {chat['title']}", key=cid, use_container_width=True):
            load_chat(cid)
            st.rerun()

    st.markdown("---")
    st.markdown("**☰ Menu**")
    st.markdown('<div class="sidebar-card" style="font-size:12px; color:#888; text-align:center">Made with ❤️ in Belpahar<br>v3.0 • History Added</div>', unsafe_allow_html=True)

# MAIN CHAT
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.markdown('<div class="ready-dot"><span></span> Aditya AI is ready</div>', unsafe_allow_html=True)
        st.caption("Built by Aditya from Belpahar — Try one below")

        r1c1, r1c2 = st.columns(2, gap="small")
        with r1c1:
            if st.button("💡 What can you do?", use_container_width=True, key="s1"):
                st.session_state.pending_prompt = "What can you do?"
                st.rerun()
        with r1c2:
            if st.button("💻 Python help", use_container_width=True, key="s2"):
                st.session_state.pending_prompt = "Help me write Python code"
                st.rerun()
        r2c1, r2c2 = st.columns(2, gap="small")
        with r2c1:
            if st.button("🌐 Today's news", use_container_width=True, key="s3"):
                st.session_state.pending_prompt = "Tell me today's news"
                st.rerun()
        with r2c2:
            if st.button("🧠 Explain physics", use_container_width=True, key="s4"):
                st.session_state.pending_prompt = "Explain quantum physics simply"
                st.rerun()
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.markdown("#### 🎙️ Voice Chat")
st.markdown('<div class="voice-sub">Tap the microphone to start speaking</div>', unsafe_allow_html=True)
audio = st.audio_input("Record")
transcribed_text = None
if audio:
    ph = st.empty()
    ph.markdown('<div style="color:#ff5555; font-size:13px">🔴 Recording captured — transcribing...</div>', unsafe_allow_html=True)
    try:
        txt = client.audio.transcriptions.create(
            file=("audio.wav", audio.getvalue(), "audio/wav"),
            model="whisper-large-v3", response_format="text", language="hi"
        )
        transcribed_text = str(txt)
        ph.empty()
        st.success(f"🎤 You said: {transcribed_text}")
    except Exception as e:
        ph.empty()
        st.error(f"Voice Error: {e}")

user_input = st.chat_input("🎙️ Ask anything... or use mic above ↑")
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
if transcribed_text:
    user_input = transcribed_text

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Save title
    if len(st.session_state.messages) == 1:
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = user_input[:35]
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("""
        <div class="thinking-wrap">
            <div class="thinking-avatar">🔥</div>
            <div>
                <div class="shimmer-text">Aditya AI is thinking...</div>
                <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        try:
            system_msg = {"role": "system", "content": "You are Aditya AI, created by Aditya from Belpahar, Odisha. NOT ChatGPT."}
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[system_msg] + st.session_state.messages
            )
            reply = res.choices[0].message.content
            thinking_placeholder.empty()
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
            if TTS:
                try:
                    lang_code = 'hi' if any('\u0900' <= c <= '\u097F' for c in reply) else 'en'
                    tts = gTTS(text=reply[:500], lang=lang_code)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3", autoplay=True)
                except:
                    pass
        except Exception as e:
            thinking_placeholder.empty()
            st.error(f"Error: {e}")For current news, recent events, current prices, current facts, weather, or other time-sensitive
questions, use your available web-search capability. For calculations and technical tasks,
use available tools when they improve accuracy. Do not invent sources, facts, or capabilities.
""".strip()


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
<style>
:root {
    --bg: #09090d;
    --panel: rgba(255,255,255,0.055);
    --panel-strong: rgba(255,255,255,0.085);
    --border: rgba(255,255,255,0.10);
    --muted: #9b9ba8;
    --text: #f6f6f8;
    --accent1: #ff7a18;
    --accent2: #ff2d8d;
}

.stApp {
    background:
        radial-gradient(circle at 15% 5%, rgba(255, 122, 24, .12), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(255, 45, 141, .10), transparent 28%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.25rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background: rgba(12, 12, 18, .96);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

.brand {
    font-size: 1.55rem;
    font-weight: 850;
    letter-spacing: -.03em;
    background: linear-gradient(90deg, var(--accent1), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-sub {
    color: var(--muted);
    font-size: .78rem;
    margin-top: -4px;
}

.sidebar-card,
.hero-card,
.feature-card,
.status-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 14px 45px rgba(0,0,0,.18);
}

.sidebar-card {
    padding: 15px;
    margin: 12px 0;
}

.status-row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    align-items: center;
    color: #dddde5;
    font-size: .86rem;
}

.live-pill {
    color: #8df3ad;
    background: rgba(50, 210, 100, .10);
    border: 1px solid rgba(50, 210, 100, .20);
    border-radius: 999px;
    padding: 3px 8px;
    font-size: .72rem;
    font-weight: 700;
}

.hero-card {
    text-align: center;
    padding: 42px 24px 32px;
    margin: 10px auto 24px;
    max-width: 850px;
}

.hero-icon {
    width: 76px;
    height: 76px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
    border-radius: 24px;
    font-size: 3rem;
    background: linear-gradient(135deg, rgba(255,122,24,.18), rgba(255,45,141,.16));
    border: 1px solid rgba(255,255,255,.10);
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3rem);
    line-height: 1.05;
    font-weight: 850;
    letter-spacing: -.05em;
    margin-bottom: 12px;
}

.hero-gradient {
    background: linear-gradient(90deg, #fff, #ffb06e, #ff75b5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.ready {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    color: #9df3b5;
    background: rgba(50,210,100,.08);
    border: 1px solid rgba(50,210,100,.18);
    border-radius: 999px;
    padding: 6px 11px;
    font-size: .8rem;
    font-weight: 650;
}

.ready-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #65e890;
    box-shadow: 0 0 12px #65e890;
}

.hero-desc {
    max-width: 650px;
    margin: 16px auto 0;
    color: var(--muted);
    line-height: 1.65;
}

.section-label {
    color: #d9d9e2;
    font-size: .88rem;
    font-weight: 700;
    margin: 12px 0 9px;
}

.feature-card {
    padding: 17px;
    height: 100%;
}

.feature-icon {
    font-size: 1.35rem;
    margin-bottom: 8px;
}

.feature-title {
    font-weight: 750;
    margin-bottom: 4px;
}

.feature-text {
    color: var(--muted);
    font-size: .82rem;
    line-height: 1.45;
}

.footer-note {
    color: #6f6f7c;
    text-align: center;
    font-size: .75rem;
    padding: 12px 0;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.045);
    color: #f4f4f6;
    transition: .18s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: rgba(255,122,24,.55);
    background: rgba(255,122,24,.10);
}

[data-testid="stChatMessage"] {
    border-radius: 16px;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: .7rem;
        padding-right: .7rem;
        padding-top: .8rem;
    }
    .hero-card {
        padding: 30px 15px 25px;
    }
    .hero-icon {
        width: 64px;
        height: 64px;
        font-size: 2.4rem;
        border-radius: 20px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# API
# ============================================================

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("GROQ_API_KEY is missing. Add it under Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "regenerate" not in st.session_state:
    st.session_state.regenerate = False
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None


def sync_chat():
    st.session_state.all_chats[st.session_state.current_chat_id] = {
        "messages": list(st.session_state.messages),
        "updated": datetime.now().strftime("%d %b %Y, %H:%M"),
    }


def create_new_chat():
    sync_chat()
    st.session_state.current_chat_id = f"chat_{int(datetime.now().timestamp() * 1000)}"
    st.session_state.messages = []
    st.session_state.pending_prompt = None
    st.session_state.regenerate = False
    st.rerun()


def chat_title(messages):
    for msg in messages:
        if msg.get("role") != "user":
            continue
        content = msg.get("content", "")
        if isinstance(content, str):
            title = " ".join(content.split())
        else:
            title = "Image conversation"
        return title[:34] + ("..." if len(title) > 34 else "")
    return "New chat"


def image_to_data_url(uploaded_file):
    data = uploaded_file.getvalue()
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("Please use an image smaller than 4 MB.")
    mime = uploaded_file.type
    if mime not in {"image/jpeg", "image/png", "image/webp"}:
        raise ValueError("Supported image formats: JPG, PNG, and WEBP.")
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def transcribe_audio(audio_file):
    audio_bytes = audio_file.getvalue()
    stream = io.BytesIO(audio_bytes)
    stream.name = getattr(audio_file, "name", None) or "recording.wav"
    result = client.audio.transcriptions.create(
        file=stream,
        model=WHISPER_MODEL,
        response_format="text",
    )
    if isinstance(result, str):
        return result.strip()
    return getattr(result, "text", str(result)).strip()


def make_tts(text):
    if not GTTS_AVAILABLE or not text.strip():
        return None
    try:
        has_devanagari = any("\u0900" <= ch <= "\u097F" for ch in text)
        lang = "hi" if has_devanagari else "en"
        buf = io.BytesIO()
        gTTS(text=text[:3000], lang=lang, slow=False).write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None


def has_image(messages):
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, list):
            if any(part.get("type") == "image_url" for part in content):
                return True
    return False


def call_text_model(messages):
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
    result = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=api_messages,
    )
    return result.choices[0].message.content or ""


def call_vision_model(messages):
    vision_system = (
        "You are Aditya AI, a helpful multimodal assistant. "
        "You are not ChatGPT. Analyze the provided image carefully, "
        "answer the user's question, and say when something is unclear."
    )
    api_messages = [{"role": "system", "content": vision_system}]
    for msg in messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
    result = client.chat.completions.create(
        model=VISION_MODEL,
        messages=api_messages,
    )
    return result.choices[0].message.content or ""


def regenerate_last():
    if not st.session_state.messages:
        return
    if st.session_state.messages[-1].get("role") == "assistant":
        st.session_state.messages.pop()
    if st.session_state.messages and st.session_state.messages[-1].get("role") == "user":
        st.session_state.regenerate = True
        st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown('<div class="brand">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Fast • Multimodal • Web-enabled</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("＋ New chat", use_container_width=True, key="new_chat_sidebar"):
        create_new_chat()

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="status-row">
                <span>📍 Belpahar, Odisha</span>
                <span class="live-pill">● LIVE</span>
            </div>
            <div style="color:#888894;font-size:.76rem;margin-top:9px;line-height:1.5;">
                Web search • Code • Vision • Voice
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### RECENT CHATS")
    if not st.session_state.all_chats:
        st.caption("Your recent chats will appear here.")
    else:
        items = list(st.session_state.all_chats.items())
        items.reverse()
        for chat_id, data in items[:10]:
            if chat_id == st.session_state.current_chat_id:
                continue
            if st.button(chat_title(data["messages"]), key=f"chat_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.messages = list(data["messages"])
                st.rerun()

    st.markdown("---")
    st.markdown("### ✨ CAPABILITIES")
    st.caption("🌐 Current web information")
    st.caption("💻 Coding & calculations")
    st.caption("👁️ Image understanding")
    st.caption("🎙️ Voice input")
    st.caption("🔊 Optional voice replies")
    st.caption("💬 Session chat history")

    st.markdown("---")
    st.caption("Created by Aditya")


# ============================================================
# MAIN HEADER
# ============================================================

head_left, head_right = st.columns([7, 1])
with head_left:
    st.markdown("## 🔥 Aditya AI")
    st.caption("A fast, multimodal AI assistant")
with head_right:
    if st.button("🆕", help="Start a new chat", key="new_chat_top"):
        create_new_chat()


# ============================================================
# WELCOME
# ============================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-icon">🔥</div>
            <div class="hero-title">Hi! I'm <span class="hero-gradient">Aditya AI</span></div>
            <div class="ready"><span class="ready-dot"></span> Ready to help</div>
            <div class="hero-desc">
                Ask questions, write code, analyze images, search the web,
                calculate, or talk by voice.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">🚀 Try something</div>', unsafe_allow_html=True)
    q1, q2 = st.columns(2)

    with q1:
        if st.button("💡 What can you do?", use_container_width=True, key="quick_1"):
            st.session_state.pending_prompt = "What can you do?"
            st.rerun()
        if st.button("💻 Help me with Python", use_container_width=True, key="quick_2"):
            st.session_state.pending_prompt = "Help me learn Python with a simple beginner example."
            st.rerun()

    with q2:
        if st.button("🌐 What's happening today?", use_container_width=True, key="quick_3"):
            st.session_state.pending_prompt = "What are the most important current news stories today?"
            st.rerun()
        if st.button("🧪 Explain physics", use_container_width=True, key="quick_4"):
            st.session_state.pending_prompt = "Explain an interesting physics concept simply."
            st.rerun()

    st.write("")
    f1, f2, f3 = st.columns(3)
    feature_data = [
        (f1, "🌐", "Web-aware", "Get current information when a question needs it."),
        (f2, "👁️", "Vision", "Upload an image and ask questions about it."),
        (f3, "🎙️", "Voice", "Record a question and turn speech into text."),
    ]
    for col, icon, title, text in feature_data:
        with col:
            st.markdown(
                f'<div class="feature-card"><div class="feature-icon">{icon}</div>'
                f'<div class="feature-title">{title}</div><div class="feature-text">{text}</div></div>',
                unsafe_allow_html=True,
            )


# ============================================================
# CHAT HISTORY DISPLAY
# ============================================================

for index, message in enumerate(st.session_state.messages):
    role = message.get("role")
    avatar = "👤" if role == "user" else "🔥"

    with st.chat_message(role, avatar=avatar):
        content = message.get("content", "")

        if isinstance(content, list):
            for part in content:
                if part.get("type") == "text":
                    st.markdown(part.get("text", ""))
                elif part.get("type") == "image_url":
                    try:
                        st.image(part["image_url"]["url"], use_container_width=True)
                    except Exception:
                        st.caption("Image preview unavailable.")
        else:
            st.markdown(content)

        if role == "assistant":
            st.download_button(
                "💾 Save",
                data=str(content),
                file_name="aditya_ai_response.txt",
                mime="text/plain",
                key=f"save_{index}",
            )
            if message.get("audio"):
                st.audio(message["audio"], format="audio/mp3")


# ============================================================
# TOOLS
# ============================================================

with st.expander("🧰 Attachments & Voice"):
    tool_left, tool_right = st.columns(2)
    with tool_left:
        uploaded_image = st.file_uploader(
            "🖼️ Upload an image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Maximum 4 MB for reliable base64 vision requests.",
            key="image_uploader",
        )
    with tool_right:
        audio_input = st.audio_input(
            "🎙️ Record your question",
            sample_rate=16000,
            key="audio_recorder",
        )


# ============================================================
# VOICE
# ============================================================

voice_prompt = None
if audio_input is not None:
    raw_audio = audio_input.getvalue()
    audio_hash = hashlib.sha256(raw_audio).hexdigest()
    if audio_hash != st.session_state.last_audio_hash:
        with st.spinner("🎙️ Transcribing..."):
            try:
                voice_prompt = transcribe_audio(audio_input)
                st.session_state.last_audio_hash = audio_hash
                if voice_prompt:
                    st.info(f"🎙️ I heard: {voice_prompt}")
            except Exception as exc:
                st.error("I couldn't transcribe that recording.")
                with st.expander("Technical details"):
                    st.code(str(exc))


# ============================================================
# INPUT
# ============================================================

chat_input = st.chat_input("Ask anything... or use the tools above")
prompt = None
regenerating = False

if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
elif voice_prompt:
    prompt = voice_prompt
elif chat_input:
    prompt = chat_input
elif st.session_state.regenerate:
    regenerating = True
    st.session_state.regenerate = False
    if st.session_state.messages and st.session_state.messages[-1].get("role") == "assistant":
        st.session_state.messages.pop()
    if st.session_state.messages and st.session_state.messages[-1].get("role") == "user":
        last_user = st.session_state.messages[-1]["content"]
        if isinstance(last_user, str):
            prompt = last_user
        else:
            prompt = ""


# ============================================================
# SEND / GENERATE
# ============================================================

if prompt and prompt.strip():
    prompt = prompt.strip()
    image_data_url = None

    if uploaded_image is not None and not regenerating:
        try:
            image_data_url = image_to_data_url(uploaded_image)
        except Exception as exc:
            st.error(str(exc))
            st.stop()

    if not regenerating:
        if image_data_url:
            user_message = {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        else:
            user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)

    use_vision = has_image(st.session_state.messages)

    with st.chat_message("assistant", avatar="🔥"):
        with st.spinner("Thinking..."):
            try:
                if use_vision:
                    answer = call_vision_model(st.session_state.messages)
                else:
                    answer = call_text_model(st.session_state.messages)
            except Exception as exc:
                answer = None
                st.error("Aditya AI couldn't generate a response.")
                with st.expander("Technical details"):
                    st.code(str(exc))

        if answer:
            st.markdown(answer)
            audio_bytes = make_tts(answer)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                "💾 Save response",
                data=answer,
                file_name="aditya_ai_response.txt",
                mime="text/plain",
                key=f"save_new_{datetime.now().timestamp()}",
            )
            assistant_message = {"role": "assistant", "content": answer}
            if audio_bytes:
                assistant_message["audio"] = audio_bytes
            st.session_state.messages.append(assistant_message)
            sync_chat()
            st.rerun()


# ============================================================
# ACTIONS
# ============================================================

if st.session_state.messages and st.session_state.messages[-1].get("role") == "assistant":
    action1, action2, _ = st.columns([1.2, 1.2, 5])
    with action1:
        if st.button("🔄 Regenerate", use_container_width=True, key="regenerate_btn"):
            st.session_state.regenerate = True
            st.rerun()
    with action2:
        if st.button("＋ New chat", use_container_width=True, key="new_chat_bottom"):
            create_new_chat()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-note">🔥 Aditya AI • Built with Streamlit + Groq</div>',
    unsafe_allow_html=True,
)

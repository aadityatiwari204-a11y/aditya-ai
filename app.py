import streamlit as st
from groq import Groq
import io
import uuid
import base64
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
 .img-card {
        background: linear-gradient(135deg, #1e1e26, #21212a);
        border: 1px dashed #3a3a4a; border-radius: 16px;
        padding: 16px; transition: all 0.3s ease;
    }
 .img-card:hover { border-color: #ff6a00; background: #252530; }
 .upload-title { font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 4px; }
 .upload-sub { font-size: 12px; color: #888; margin-bottom: 10px; }
    [data-testid="stTextInput"] input{ border-radius:24px!important; height:48px!important; background:#252530!important; }
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
if "img_b64" not in st.session_state:
    st.session_state.img_b64 = None

def new_chat():
    if st.session_state.messages:
        if len(st.session_state.messages) > 0:
            title = st.session_state.messages[0]["content"][:30] + "..."
            st.session_state.all_chats[st.session_state.current_chat_id]["title"] = title
            st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.all_chats[new_id] = {"title": "New Chat", "messages": [], "time": datetime.now().strftime("%d %b")}
    st.session_state.messages = []
    st.session_state.img_b64 = None

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
    st.markdown('<div class="sidebar-card" style="display:flex; justify-content:space-between; align-items:center"><span style="font-size:13px">📍 Belpahar, Odisha</span><span style="font-size:10px; background:#00ff8820; color:#00ff88; padding:4px 8px; border-radius:20px;">● LIVE</span></div>', unsafe_allow_html=True)
    st.markdown("**💬 History**")
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

# --- PREMIUM IMAGE UPLOAD (FIXED - SINGLE) ---
st.markdown("""
<div class="img-card">
  <div class="upload-title">📷 Send Image + Ask AI</div>
  <div class="upload-sub">Drop a photo and ask anything about it — powered by vision AI</div>
</div>
""", unsafe_allow_html=True)

img_file = st.file_uploader("img_uploader_309", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="img_309_line_unique")

if img_file is not None:
    b64 = base64.b64encode(img_file.getvalue()).decode("utf-8")
    st.session_state.img_b64 = b64
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(img_file, use_container_width=True)
    with c2:
        st.success("✅ Image loaded")
        if st.button("❌ Remove image", key="remove_309"):
            st.session_state.img_b64 = None
            st.rerun()

# --- WHATSAPP SINGLE BAR (FIXED - UNIQUE KEYS) ---
st.markdown("<br>", unsafe_allow_html=True)
col_text, col_mic = st.columns([6,1], vertical_alignment="bottom")
with col_text:
    wa_text = st.text_input("wa_309_input", placeholder="Ask anything... 💬", label_visibility="collapsed", key="wa_309_text_unique")
with col_mic:
    audio = st.audio_input("mic_309", label_visibility="collapsed", key="mic_309_unique")

transcribed_text = None
if audio:
    try:
        txt = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text", language="hi")
        transcribed_text = str(txt)
        st.toast(f"🎤 {transcribed_text}")
    except Exception as e:
        st.error(f"Voice Error: {e}")

user_input = None
if wa_text: user_input = wa_text
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
if transcribed_text: user_input = transcribed_text

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    msgs = [{"role":"system","content":"You are Aditya AI, built by Aditya from Belpahar, Odisha. Helpful, friendly, concise."}]
    if st.session_state.img_b64:
        msgs.append({"role":"user","content":[{"type":"text","text":user_input},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{st.session_state.img_b64}"}}]

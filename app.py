import streamlit as st
from groq import Groq
import uuid
from datetime import datetime
import io

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- PREMIUM CSS FROM YOUR SCREENSHOT ---
st.markdown("""
<style>
.stApp { background: #09090d; }
.block-container { max-width: 780px; padding-top: 1rem; }
[data-testid="stSidebar"] { background: #0f0f12; border-right: 1px solid #222; }
.hero-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    padding: 32px 20px;
    text-align: center;
    margin: 10px 0 20px 0;
}
.hero-icon {
    width: 72px; height: 72px; margin: 0 auto 12px;
    background: linear-gradient(135deg, rgba(255,106,0,0.2), rgba(238,9,121,0.2));
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    display: flex; align-items: center; justify-content: center;
    font-size: 36px;
}
.hero-title { font-size: 32px; font-weight: 800; }
.hero-title span { background: linear-gradient(90deg,#ffb86a,#ff6eb6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.ready-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.2);
    color: #7CFFB2; padding: 5px 12px; border-radius: 999px; font-size: 13px; margin: 10px 0;
}
.ready-dot { width: 7px; height: 7px; background: #00ff88; border-radius: 50%; box-shadow: 0 0 10px #00ff88; }
.hero-desc { color: #9a9aa8; font-size: 15px; line-height: 1.6; margin-top: 8px; }
.try-label { font-weight: 700; margin: 18px 0 10px 0; }
div[data-testid="stButton"] > button {
    background: #1a1a22!important; border: 1px solid #2a2a35!important;
    color: #ddd!important; border-radius: 14px!important; height: 48px!important;
}
div[data-testid="stButton"] > button:hover { border-color: #ff6a00!important; color: white!important; }
.blog-card {
    background: #1e1e26; border: 1px solid #2a2a35; border-radius: 12px;
    padding: 10px 12px; margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    try:
        key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("Add GROQ_API_KEY in Secrets"); st.stop()
    return Groq(api_key=key)
client = get_client()

if "messages" not in st.session_state: st.session_state.messages = []
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[st.session_state.current_chat_id] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
if "pending_prompt" not in st.session_state: st.session_state.pending_prompt = None

def new_chat():
    if st.session_state.messages:
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = st.session_state.messages[0]["content"][:30]
    nid = str(uuid.uuid4())
    st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
    st.session_state.messages = []

# SIDEBAR WITH BLOG OPTION
with st.sidebar:
    st.markdown("## 🔥 Aditya AI")
    st.caption("A fast, multimodal AI assistant")
    if st.button("🆕 NEW", use_container_width=True): new_chat(); st.rerun()

    st.markdown('<div class="blog-card">📝 <a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;font-weight:600;">Blog</a><div style="font-size:11px;color:#888;">Tutorials & Updates</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**💬 History**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if not chat["messages"]: continue
        if cid == st.session_state.current_chat_id: continue
        if st.button(f"📝 {chat['title'][:28]}", key=cid, use_container_width=True):
            st.session_state.current_chat_id = cid
            st.session_state.messages = chat["messages"]
            st.rerun()

# MAIN HEADER LIKE SCREENSHOT
st.markdown("## 🔥 Aditya AI")
st.caption("A fast, multimodal AI assistant")

# HERO CARD - EXACT LIKE YOUR SCREENSHOT
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-icon">🔥</div>
        <div class="hero-title">Hi! I'm <span>Aditya AI</span></div>
        <div class="ready-pill"><div class="ready-dot"></div> Ready to help</div>
        <div class="hero-desc">Ask questions, write code, analyze images,<br>search the web, calculate, or talk by voice.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="try-label">🚀 Try something</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(1)
    if st.button("💡 What can you do?", use_container_width=True, key="t1"):
        st.session_state.pending_prompt="What can you do?"; st.rerun()
    if st.button("💻 Help me with Python", use_container_width=True, key="t2"):
        st.session_state.pending_prompt="Help me with Python with example"; st.rerun()
    if st.button("🌐 What's happening today?", use_container_width=True, key="t3"):
        st.session_state.pending_prompt="What's happening today? Give me latest news"; st.rerun()
    if st.button("🧪 Explain physics", use_container_width=True, key="t4"):
        st.session_state.pending_prompt="Explain an interesting physics concept simply"; st.rerun()
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# VOICE
st.markdown("### 🎙️ Voice")
audio = st.audio_input("Record", label_visibility="collapsed")
transcribed = None
if audio:
    try:
        txt = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text", language="hi")
        transcribed = str(txt)
        st.toast(f"🎤 {transcribed}")
    except Exception as e:
        st.error(f"Voice error: {e}")

user_input = st.chat_input("Ask anything... or use the tools above")
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
if transcribed:
    user_input = transcribed

# BLOG FOOTER
st.markdown('<div style="text-align:center;margin:20px 0;"><a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;">📝 aditya-ai-belpahar.blogspot.com</a></div>', unsafe_allow_html=True)

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        ph = st.empty(); full=""
        try:
            # 413 fix - keep only last 10
            recent = st.session_state.messages[-10:]
            msgs = [{"role":"system","content":"You are Aditya AI built by Aditya from Belpahar, Odisha. You are NOT ChatGPT. Helpful, friendly."}] + recent
            stream = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, stream=True)
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full += chunk.choices[0].delta.content
                    ph.markdown(full+"▌")
            ph.markdown(full)
        except Exception as e:
            if "413" in str(e):
                full="Request too large. New chat started."
                st.session_state.messages = st.session_state.messages[-2:]
            else:
                full=f"Error: {e}"
            ph.markdown(full)
    st.session_state.messages.append({"role":"assistant","content":full})
    st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    st.rerun()

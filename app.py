import streamlit as st
from groq import Groq
import uuid
from datetime import datetime

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- BIG PREMIUM CSS LIKE YOUR PHOTO ---
st.markdown("""
<style>
.stApp { background: #09090d; }
.block-container { max-width: 800px; padding-top: 1rem; }
[data-testid="stSidebar"] { background: #0f0f12; border-right: 1px solid #222; }
.hero-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    padding: 36px 20px;
    text-align: center;
    margin: 10px 0 20px 0;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
}
.hero-icon {
    width: 80px; height: 80px; margin: 0 auto 14px;
    background: linear-gradient(135deg, rgba(255,106,0,0.25), rgba(238,9,121,0.25));
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    display: flex; align-items: center; justify-content: center;
    font-size: 42px;
}
.hero-title { font-size: 34px; font-weight: 850; letter-spacing: -0.5px; }
.hero-title span { background: linear-gradient(90deg,#ffb86a,#ff6eb6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.ready-pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.20);
    color: #7CFFB2; padding: 6px 14px; border-radius: 999px; font-size: 13px; font-weight: 600; margin: 12px 0;
}
.ready-dot { width: 7px; height: 7px; background: #00ff88; border-radius: 50%; box-shadow: 0 0 10px #00ff88; }
.hero-desc { color: #9a9aa8; font-size: 15px; line-height: 1.7; margin-top: 6px; }
.try-label { font-weight: 750; font-size: 15px; margin: 20px 0 12px 0; color: #e5e5ea; }
div[data-testid="stButton"] > button {
    background: #1a1a22!important; border: 1px solid #2a2a35!important;
    color: #ddd!important; border-radius: 14px!important; height: 52px!important; font-size: 14px!important;
}
div[data-testid="stButton"] > button:hover { border-color: #ff6a00!important; color: white!important; background: #22222e!important; }
.blog-card { background: #1e1e26; border: 1px solid #2a2a35; border-radius: 12px; padding: 12px; margin: 12px 0; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    try: key = st.secrets["GROQ_API_KEY"]
    except: st.error("Add GROQ_API_KEY in Secrets"); st.stop()
    return Groq(api_key=key)
client = get_client()

if "messages" not in st.session_state: st.session_state.messages = []
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    nid = str(uuid.uuid4()); st.session_state.current_chat_id = nid; st.session_state.all_chats[nid] = {"title":"New Chat","messages":[]}
if "pending_prompt" not in st.session_state: st.session_state.pending_prompt = None

def new_chat():
    nid = str(uuid.uuid4()); st.session_state.current_chat_id = nid; st.session_state.all_chats[nid] = {"title":"New Chat","messages":[]}; st.session_state.messages = []; st.rerun()

with st.sidebar:
    st.markdown("## 🔥 Aditya AI")
    st.caption("A fast, multimodal AI assistant")
    if st.button("🆕 NEW CHAT", use_container_width=True): new_chat()
    st.markdown(f'<div class="blog-card">📝 <a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;font-weight:700;">Blog</a><div style="font-size:11px;color:#888;margin-top:2px;">Tutorials & Updates</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**💬 History**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if not chat.get("messages"): continue
        if cid == st.session_state.current_chat_id: continue
        if st.button(f"📝 {chat.get('title','New Chat')[:28]}", key=cid, use_container_width=True):
            st.session_state.current_chat_id = cid; st.session_state.messages = chat.get("messages",[]); st.rerun()

st.markdown("## 🔥 Aditya AI")
st.caption("A fast, multimodal AI assistant")

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
    if st.button("💡 What can you do?", use_container_width=True, key="t1"): st.session_state.pending_prompt="What can you do?"; st.rerun()
    if st.button("💻 Help me with Python", use_container_width=True, key="t2"): st.session_state.pending_prompt="Help me with Python with a simple beginner example"; st.rerun()
    if st.button("🌐 What's happening today?", use_container_width=True, key="t3"): st.session_state.pending_prompt="What's happening today? Give me latest news"; st.rerun()
    if st.button("🧪 Explain physics", use_container_width=True, key="t4"): st.session_state.pending_prompt="Explain an interesting physics concept simply"; st.rerun()

    f1,f2,f3 = st.columns(3)
    with f1: st.markdown('<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:14px;"><div style="font-size:20px;">🌐</div><div style="font-weight:700;margin:4px 0;">Web-aware</div><div style="font-size:12px;color:#888;">Get current info</div></div>', unsafe_allow_html=True)
    with f2: st.markdown('<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:14px;"><div style="font-size:20px;">👁️</div><div style="font-weight:700;margin:4px 0;">Vision</div><div style="font-size:12px;color:#888;">Upload & ask</div></div>', unsafe_allow_html=True)
    with f3: st.markdown('<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:14px;"><div style="font-size:20px;">🎙️</div><div style="font-weight:700;margin:4px 0;">Voice</div><div style="font-size:12px;color:#888;">Speak to AI</div></div>', unsafe_allow_html=True)
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

# Voice + Input
audio = st.audio_input("Record your question", label_visibility="collapsed")
transcribed = None
if audio:
    try:
        txt = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text", language="hi")
        transcribed = str(txt); st.toast(f"🎤 {transcribed}")
    except Exception as e: st.error(f"Voice error: {e}")

user_input = st.chat_input("Ask anything... or use the tools above")
if st.session_state.pending_prompt: user_input = st.session_state.pending_prompt; st.session_state.pending_prompt = None
if transcribed: user_input = transcribed

st.markdown('<div style="text-align:center;margin:22px 0 10px;"><a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;font-size:13px;">📝 aditya-ai-belpahar.blogspot.com</a></div>', unsafe_allow_html=True)

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        ph = st.empty(); full=""
        msgs = [{"role":"system","content":"You are Aditya AI created by Aditya from Belpahar, Odisha. You are NOT ChatGPT, NOT OpenAI. Be friendly, helpful, concise."}] + st.session_state.messages[-8:]
        try:
            # MAIN MODEL - 2026 WORKING
            res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs)
            full = res.choices[0].message.content
            ph.markdown(full)
        except Exception as e:
            try:
                res = client.chat.completions.create(model="groq/compound", messages=msgs)
                full = res.choices[0].message.content
                ph.markdown(full)
            except Exception as e2:
                full = f"Groq updating models, try again after 30 sec. {e2}"
                ph.markdown(full)
    st.session_state.messages.append({"role":"assistant","content":full})
    st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = list(st.session_state.messages)
    st.session_state.all_chats[st.session_state.current_chat_id]["title"] = st.session_state.messages[0]["content"][:30]
    st.rerun()

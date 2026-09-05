import streamlit as st
from groq import Groq
import uuid
from datetime import datetime

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

st.markdown("""
<style>
.stApp { background: #09090d; }
.block-container { max-width: 780px; padding-top: 1rem; }
[data-testid="stSidebar"] { background: #0f0f12; }
.hero-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 32px; text-align: center; margin: 10px 0; }
.hero-icon { width: 72px; height: 72px; margin: 0 auto 12px; background: linear-gradient(135deg, #ff6a0030, #ee097930); border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 36px; }
.hero-title { font-size: 32px; font-weight: 800; }.hero-title span { background: linear-gradient(90deg,#ffb86a,#ff6eb6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.ready-pill { display: inline-flex; gap: 6px; background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.2); color: #7CFFB2; padding: 5px 12px; border-radius: 999px; font-size: 13px; margin: 10px 0; }
.ready-dot { width: 7px; height: 7px; background: #00ff88; border-radius: 50%; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    try: key = st.secrets["GROQ_API_KEY"]
    except: st.error("Add GROQ_API_KEY in Secrets"); st.stop()
    return Groq(api_key=key)
client = get_client()

# RESET OLD BROKEN HISTORY AUTOMATICALLY
if "messages" not in st.session_state: st.session_state.messages = []
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in st.session_state.all_chats:
    nid = str(uuid.uuid4())
    st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
if "pending_prompt" not in st.session_state: st.session_state.pending_prompt = None

def new_chat():
    try:
        cid = st.session_state.current_chat_id
        if cid in st.session_state.all_chats and st.session_state.messages:
            st.session_state.all_chats[cid]["messages"] = st.session_state.messages
    except: pass
    nid = str(uuid.uuid4())
    st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
    st.session_state.messages = []

with st.sidebar:
    st.markdown("## 🔥 Aditya AI")
    if st.button("🆕 NEW CHAT", use_container_width=True): new_chat(); st.rerun()
    st.markdown(f'<div style="background:#1e1e26;padding:10px;border-radius:10px;border:1px solid #333;margin:10px 0;"><a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;font-weight:700;">📝 Blog</a><div style="font-size:11px;color:#888;">Tutorials</div></div>', unsafe_allow_html=True)
    st.markdown("**💬 History**")
    for cid, chat in list(reversed(list(st.session_state.all_chats.items())))[:10]:
        if not chat.get("messages"): continue
        if cid == st.session_state.current_chat_id: continue
        if st.button(f"📝 {chat.get('title','New Chat')[:28]}", key=cid, use_container_width=True):
            st.session_state.current_chat_id = cid
            st.session_state.messages = chat.get("messages",[])
            st.rerun()

st.markdown("## 🔥 Aditya AI")
st.caption("A fast, multimodal AI assistant")

if not st.session_state.messages:
    st.markdown('<div class="hero-card"><div class="hero-icon">🔥</div><div class="hero-title">Hi! I\'m <span>Aditya AI</span></div><div class="ready-pill"><div class="ready-dot"></div> Ready to help</div><div style="color:#9a9aa8;">Ask questions, write code, analyze images, search the web, or talk by voice.</div></div>', unsafe_allow_html=True)
    st.markdown("🚀 **Try something**")
    if st.button("💡 What can you do?", use_container_width=True): st.session_state.pending_prompt="What can you do?"; st.rerun()
    if st.button("💻 Help me with Python", use_container_width=True): st.session_state.pending_prompt="Help me with Python"; st.rerun()
    if st.button("🌐 What's happening today?", use_container_width=True): st.session_state.pending_prompt="What's happening today?"; st.rerun()
    if st.button("🧪 Explain physics", use_container_width=True): st.session_state.pending_prompt="Explain physics simply"; st.rerun()
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

audio = st.audio_input("Record", label_visibility="collapsed")
transcribed = None
if audio:
    try:
        txt = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text", language="hi")
        transcribed = str(txt); st.toast(f"🎤 {transcribed}")
    except Exception as e: st.error(f"Voice error: {e}")

user_input = st.chat_input("Ask anything...")
if st.session_state.pending_prompt: user_input = st.session_state.pending_prompt; st.session_state.pending_prompt = None
if transcribed: user_input = transcribed

st.markdown('<div style="text-align:center;margin:15px;"><a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;">📝 aditya-ai-belpahar.blogspot.com</a></div>', unsafe_allow_html=True)

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        ph = st.empty(); full=""
        try:
            msgs = [{"role":"system","content":"You are Aditya AI from Belpahar. You are NOT ChatGPT."}] + [{"role":m["role"],"content":str(m["content"])[:2000]} for m in st.session_state.messages[-8:]]
            stream = client.chat.completions.create(model="groq/compound", messages=msgs, stream=True)
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full += chunk.choices[0].delta.content
                    ph.markdown(full+"▌")
            ph.markdown(full)
        except:
            try:
                res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=msgs)
                full = res.choices[0].message.content; ph.markdown(full)
            except Exception as e: full=f"Error: {e}"; ph.markdown(full)
    # SAFE SAVE - THIS LINE FIXES YOUR 156 ERROR
    try:
        st.session_state.messages.append({"role":"assistant","content":full})
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = list(st.session_state.messages)
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = st.session_state.messages[0]["content"][:30]
    except: pass
    st.rerun()

import streamlit as st
from groq import Groq
import io, uuid, time
from datetime import datetime

try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("Add GROQ_API_KEY in Secrets")
    st.stop()

client = Groq(api_key=GROQ_KEY)

st.markdown('<style>[data-testid="stSidebar"]{background:#0f0f12;} div[data-testid="stButton"]>button{background:#1e1e26!important;border:1px solid #2a2a35!important;color:#ccc!important;border-radius:12px!important;height:42px!important;} div[data-testid="stButton"]>button:hover{border-color:#ff6a00!important;color:white!important;}</style>', unsafe_allow_html=True)

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[st.session_state.current_chat_id] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
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
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
    st.session_state.messages = []

def load_chat(cid):
    st.session_state.current_chat_id = cid
    st.session_state.messages = st.session_state.all_chats[cid]["messages"]

with st.sidebar:
    st.title("🔥 Aditya AI")
    st.caption("Next-Gen Voice AI v5.1 FINAL")
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()
    st.markdown("📍 Belpahar, Odisha ● LIVE")
    st.markdown("**💬 History**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if cid == st.session_state.current_chat_id: continue
        if not chat["messages"]: continue
        if st.button("📝 " + chat["title"][:30], key=cid, use_container_width=True):
            load_chat(cid)
            st.rerun()
    st.markdown("---")
    st.markdown("v5.1 FINAL BIG PREMIUM - Zero Errors")

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I am Aditya AI")
        st.markdown("Aditya AI is ready - v5.1 FINAL")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💡 What can you do?", use_container_width=True, key="s1"):
                st.session_state.pending_prompt = "What can you do?"
                st.rerun()
        with c2:
            if st.button("💻 Python help", use_container_width=True, key="s2"):
                st.session_state.pending_prompt = "Help me write Python code"
                st.rerun()
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.markdown("#### 🎙️ Voice Chat")
audio_file = st.audio_input("Record")
transcribed_text = None
if audio_file is not None:
    with st.spinner("Transcribing..."):
        try:
            r = client.audio.transcriptions.create(file=("audio.wav", audio_file.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text", language="hi")
            transcribed_text = str(r)
            st.success("🎤 You said: " + transcribed_text)
        except Exception as e:
            st.error("Voice Error: " + str(e))

user_input = st.chat_input("Ask anything...")
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
if transcribed_text:
    user_input = transcribed_text

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    if len(st.session_state.messages) == 1:
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = user_input[:35]
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        ph = st.empty()
        ph.markdown("Aditya AI is thinking...")
        try:
            stream = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"You are Aditya AI from Belpahar."}] + st.session_state.messages, stream=True)
            ph.empty()
            out = st.empty()
            full = ""
            for ch in stream:
                d = ch.choices[0].delta.content
                if d:
                    full += d
                    out.markdown(full + "▌")
            out.markdown(full)
            st.session_state.messages.append({"role":"assistant","content":full})
            st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
        except Exception as e:
            ph.empty()
            st.error("Reply Error: " + str(e))

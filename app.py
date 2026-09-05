import streamlit as st
from groq import Groq
import io, uuid, time
from datetime import datetime

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- SAFE SECRET LOAD ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ GROQ_API_KEY not found in Secrets! Go to Streamlit > Settings > Secrets and add it.")
    st.stop()

client = Groq(api_key=api_key)

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
    st.caption("Next-Gen Voice AI")
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()
    st.info("📍 Belpahar, Odisha ● LIVE")
    st.write("**💬 History**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if cid == st.session_state.current_chat_id: continue
        if not chat["messages"]: continue
        if st.button(f"📝 {chat['title']}", key=cid, use_container_width=True):
            load_chat(cid)
            st.rerun()
    st.caption("v4.4 SAFE MODE - Working")

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI - SAFE MODE ONLINE")
        st.success("App is working! No blank screen now.")
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
audio = st.audio_input("Record")
transcribed = None
if audio is not None:
    with st.spinner("🔴 Transcribing..."):
        try:
            r = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text", language="hi")
            transcribed = str(r)
            st.success(f"🎤 You said: {transcribed}")
        except Exception as e:
            st.error(f"Voice Error: {e}")

user_input = st.chat_input("Ask anything...")
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
if transcribed:
    user_input = transcribed

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    if len(st.session_state.messages) == 1:
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = user_input[:35]
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        ph = st.empty()
        ph.markdown("**Aditya AI is thinking...**")
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
            st.error(f"Reply Error: {e}")

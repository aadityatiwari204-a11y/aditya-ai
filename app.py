import streamlit as st
from groq import Groq
import uuid
from datetime import datetime

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

st.markdown("""
<style>
.stApp { background: #09090d; }
.block-container { max-width: 820px; padding-top: 1.2rem; }
[data-testid="stSidebar"] { background: #0f0f12; border-right: 1px solid #1f1f25; }
.hero-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 28px; padding: 40px 24px; text-align: center; margin: 14px 0 24px 0;
}
.hero-icon {
    width: 86px; height: 86px; margin: 0 auto 16px;
    background: radial-gradient(120% 120% at 30% 20%, #ff8a3d 0%, #ff3d6e 55%, #8b5cf6 100%);
    border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 44px;
}
.hero-title { font-size: 36px; font-weight: 850; color: white; }
.hero-title span { background: linear-gradient(90deg,#ffb86a,#ff6eb6,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.ready-pill { display: inline-flex; align-items: center; gap: 8px; background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.22); color: #7CFFB2; padding: 6px 14px; border-radius: 999px; font-size: 13px; font-weight: 700; margin: 14px 0; }
.ready-dot { width: 8px; height: 8px; background: #00ff88; border-radius: 50%; }
.hero-desc { color: #9a9aa8; font-size: 15px; line-height: 1.7; }
.try-label { font-weight: 750; font-size: 15px; margin: 22px 0 14px 0; color: #e5e5ea; }
div[data-testid="stButton"] > button { background: #1a1a22!important; border: 1px solid #2a2a35!important; color: #d8d8df!important; border-radius: 16px!important; height: 54px!important; }
div[data-testid="stButton"] > button:hover { border-color: #ff6a00!important; color: white!important; }
.feature-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 16px; height: 92px; }
.blog-card { background: #1e1e26; border: 1px solid #333340; border-radius: 14px; padding: 14px; margin: 12px 0; }
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
    nid = str(uuid.uuid4()); st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[]}
if "pending_prompt" not in st.session_state: st.session_state.pending_prompt = None
if "last_audio_id" not in st.session_state: st.session_state.last_audio_id = None
if "last_user_text" not in st.session_state: st.session_state.last_user_text = ""

def create_new_chat():
    nid = str(uuid.uuid4()); st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[]}
    st.session_state.messages = []; st.session_state.last_user_text = ""; st.rerun()

with st.sidebar:
    st.markdown("## Aditya AI")
    st.caption("A fast, multimodal AI assistant")
    if st.button("NEW CHAT", use_container_width=True): create_new_chat()
    st.markdown('<div class="blog-card"><a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;font-weight:800;">Blog & Updates</a><div style="font-size:11px;color:#888;">Tutorials & News</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Recent Chats**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if not chat.get("messages"): continue
        if cid == st.session_state.current_chat_id: continue
        if st.button(chat.get("title","New Chat")[:28], key=f"hist_{cid}", use_container_width=True):
            st.session_state.current_chat_id = cid; st.session_state.messages = list(chat.get("messages",[])); st.rerun()

st.markdown("## Aditya AI")
st.caption("A fast, multimodal AI assistant")

if not st.session_state.messages:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-icon">🔥</div>
        <div class="hero-title">Hi! I'm <span>Aditya AI</span></div>
        <div class="ready-pill"><div class="ready-dot"></div> Ready to help • Online</div>
        <div class="hero-desc">Ask questions, write code, analyze images, search the web,<br>calculate, or talk by voice.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="try-label">Try something</div>', unsafe_allow_html=True)
    if st.button("What can you do?", use_container_width=True, key="b1"):
        st.session_state.pending_prompt = "What can you do?"; st.rerun()
    if st.button("Help me with Python", use_container_width=True, key="b2"):
        st.session_state.pending_prompt = "Help me with Python with example"; st.rerun()
    if st.button("What's happening today?", use_container_width=True, key="b3"):
        st.session_state.pending_prompt = "What's happening today?"; st.rerun()
    if st.button("Explain physics simply", use_container_width=True, key="b4"):
        st.session_state.pending_prompt = "Explain physics simply"; st.rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='feature-card'><div style='font-size:22px;'>Web</div><div style='font-weight:700;margin:6px 0;'>Web-Aware</div><div style='font-size:12px;color:#888;'>Current info</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><div style='font-size:22px;'>Fast</div><div style='font-weight:700;margin:6px 0;'>Super Fast</div><div style='font-size:12px;color:#888;'>Powered by Groq</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-card'><div style='font-size:22px;'>Voice</div><div style='font-weight:700;margin:6px 0;'>Voice Chat</div><div style='font-size:12px;color:#888;'>Speak to AI</div></div>", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

audio = st.audio_input("Record", label_visibility="collapsed", key="voice_input")
transcribed_text = None
if audio and audio.file_id!= st.session_state.last_audio_id:
    st.session_state.last_audio_id = audio.file_id
    try:
        result = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text")
        transcribed_text = str(result).strip()
        if len(transcribed_text) < 2: transcribed_text = None
        else: st.toast(f"You said: {transcribed_text}")
    except Exception as e: st.error(f"Voice error: {e}")

final_input = None
if st.session_state.pending_prompt: final_input = st.session_state.pending_prompt; st.session_state.pending_prompt = None
elif transcribed_text: final_input = transcribed_text

chat_box = st.chat_input("Ask anything...")
if chat_box: final_input = chat_box

st.markdown('<div style="text-align:center;margin-top:22px;"><a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;font-size:13px;">aditya-ai-belpahar.blogspot.com</a></div>', unsafe_allow_html=True)

if final_input and final_input.strip()!= "":
    if st.session_state.last_user_text == final_input.strip() and st.session_state.messages and st.session_state.messages[-1].get("role") == "user":
        st.stop()
    st.session_state.last_user_text = final_input.strip()
    st.session_state.messages.append({"role":"user","content":final_input})
    with st.chat_message("user"): st.markdown(final_input)
    with st.chat_message("assistant"):
        ph = st.empty(); full_answer = ""
        try:
            msgs = [{"role":"system","content":"You are Aditya AI built by Aditya from Belpahar. You are NOT ChatGPT. Be helpful and concise."}]
            for m in st.session_state.messages[-8:]: msgs.append({"role":m["role"],"content":str(m["content"])[:2000]})
            res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=1500)
            full_answer = res.choices[0].message.content
            ph.markdown(full_answer)
        except Exception as e:
            try:
                res = client.chat.completions.create(model="groq/compound", messages=msgs, max_tokens=1500)
                full_answer = res.choices[0].message.content; ph.markdown(full_answer)
            except Exception as e2:
                full_answer = f"Please try again after 20 sec. Error: {e2}"; ph.markdown(full_answer)
    st.session_state.messages.append({"role":"assistant","content":full_answer})
    st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = list(st.session_state.messages)
    st.session_state.all_chats[st.session_state.current_chat_id]["title"] = final_input[:35]
    st.rerun()

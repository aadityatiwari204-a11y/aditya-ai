import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid

st.set_page_config(page_title="Aditya AI - Belpahar", page_icon="🤖", layout="wide")
# --- ANIME THEME - PASTE THIS, DON'T CHANGE ANYTHING ELSE ---
st.markdown("""
<style>
/* Import Anime Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main App Background - Anime Night Sky */
.stApp {
    background: radial-gradient(ellipse at top, #1e1b4b 0%, #0f0a19 60%, #000000 100%);
    background-attachment: fixed;
}

/* Sidebar - Glassmorphism like Gojo's Infinity */
section[data-testid="stSidebar"] {
    background: rgba(20, 20, 40, 0.8) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(139, 92, 246, 0.2);
}

/* Chat Messages - Anime Bubbles */
div[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px !important;
    padding: 16px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* User Message - Red Akatsuki Glow */
div[data-testid="stChatMessage"]:nth-child(odd) {
    border-left: 3px solid #ef4444;
}

/* AI Message - Blue Aditya Glow */
div[data-testid="stChatMessage"]:nth-child(even) {
    border-left: 3px solid #38bdf8;
}

/* Title - Aditya AI Neon */
h1, h2, h3 {
    background: linear-gradient(90deg, #38bdf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
}

/* Buttons - Don't change function, only look */
.stButton > button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: white !important;
    transition: 0.2s;
}
.stButton > button:hover {
    background: rgba(139, 92, 246, 0.2) !important;
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
}

/* Input Box - Glowing */
div[data-testid="stChatInput"] {
    background: rgba(20, 20, 40, 0.9) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 20px !important;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
}

/* Scrollbar - Anime Style */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #8b5cf6;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
# --- ANIME THEME END ---
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color:white; }
[data-testid="stSidebar"] { background: rgba(20,20,40,0.95); }
.stChatMessage { background: rgba(255,255,255,0.08)!important; border-radius:15px!important; border:1px solid rgba(255,255,255,0.15); }
h1 { text-align:center; background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:800; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages=[]
if "all_chats" not in st.session_state: st.session_state.all_chats={"chat_1":{"title":"New Chat","messages":[]}}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id="chat_1"
if "page" not in st.session_state: st.session_state.page="chat"

SYSTEM_PROMPT = "You are Aditya AI, created by Aditya from Belpahar, Odisha. You are NOT ChatGPT, NOT OpenAI. Say you are Aditya AI!"

with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page="chat"; st.rerun()
    if st.button("📝 Blog / About", use_container_width=True):
        st.session_state.page="blog"; st.rerun()
    if st.button("🎤 Voice Chat", use_container_width=True):
        st.session_state.page="voice"; st.rerun()
    st.divider()
    if st.button("➕ New Chat", use_container_width=True):
        nid=f"chat_{uuid.uuid4().hex[:6]}"; st.session_state.current_chat_id=nid; st.session_state.messages=[]; st.session_state.all_chats[nid]={"title":"New Chat","messages":[]}; st.session_state.page="chat"; st.rerun()
    st.markdown("### 📜 History")
    for cid,data in list(st.session_state.all_chats.items())[::-1][:10]:
        if st.button(f"📄 {data['title'][:20]}", key=cid, use_container_width=True):
            st.session_state.current_chat_id=cid; st.session_state.messages=data["messages"]; st.session_state.page="chat"; st.rerun()

if st.session_state.page=="blog":
    st.markdown("# 👤 Aditya - Belpahar")
    st.markdown("**Hey, I'm Aditya from Belpahar, Odisha! 🙏**")
    st.link_button("🌐 Visit My Real Blog", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)
    st.divider()
    st.markdown("### 🔥 About: Aditya AI made with Python + Groq AI. Hindi & English Voice.")
    st.markdown("**Location: Belpahar, Jharsuguda, Odisha**")
    st.divider()
    st.markdown("## 📝 Latest Posts From My Blogger")
    st.markdown("#### 1. Aditya AI Now Has Voice Chat!")
    st.caption("Sep 05, 2026 - aditya-ai-belpahar.blogspot.com")
    st.link_button("📖 Read on Blogger - Voice Chat Post", "https://aditya-ai-belpahar.blogspot.com", key="b1")
    st.markdown("#### 2. Privacy Policy and About Us")
    st.caption("Sep 04, 2026")
    st.link_button("📖 Read Privacy Policy", "https://aditya-ai-belpahar.blogspot.com", key="b2")
    st.divider()
    st.link_button("🚀 Open aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)
    st.divider()
    if st.button("⬅️ Back to Chat"):
        st.session_state.page="chat"; st.rerun()
    st.stop()

if st.session_state.page=="voice":
    st.markdown("# 🎤 Voice Chat")
    audio = st.audio_input("Record your voice")
    if audio:
        with st.spinner("Sun raha hu..."):
            try:
                transcription = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3-turbo", language="hi")
                user_text = transcription.text
                st.success(f"You said: {user_text}")
                r = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_text}], max_tokens=1000)
                ans = r.choices[0].message.content
                st.markdown(ans)
                lang='hi' if any('\u0900'<=c<='\u097F' for c in ans) else 'en'
                tts=gTTS(text=ans[:400], lang=lang); b=io.BytesIO(); tts.write_to_fp(b); b.seek(0); st.audio(b, format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"Error: {e}")
    if st.button("⬅️ Back to Chat"): st.session_state.page="chat"; st.rerun()
    st.stop()

st.markdown("# 😊 Aditya AI")
st.caption("Photoshop • Editing • Design • Hindi + English Voice")
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
inp = st.chat_input("Type...")
if inp:
    st.session_state.messages.append({"role":"user","content":inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        msgs=[{"role":"system","content":SYSTEM_PROMPT}] + [{"role":x["role"],"content":x["content"]} for x in st.session_state.messages]
        r=client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=1500)
        ans=r.choices[0].message.content
        st.markdown(ans)
        st.session_state.messages.append({"role":"assistant","content":ans})
    st.session_state.all_chats[st.session_state.current_chat_id]["messages"]=st.session_state.messages

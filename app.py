import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import uuid
import datetime

# Try to import mic_recorder, if not available use audio_input
try:
    from streamlit_mic_recorder import mic_recorder
    MIC_AVAILABLE = True
except:
    MIC_AVAILABLE = False

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Aditya AI - Belpahar",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS - PROPER UI
# ============================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color:white;
}
[data-testid="stSidebar"] {
    background: rgba(20,20,40,0.98);
}
.stChatMessage {
    background: rgba(255,255,255,0.08)!important;
    border-radius:15px!important;
    border:1px solid rgba(255,255,255,0.15);
}
h1 {
    text-align:center;
    background: linear-gradient(90deg, #00f2fe, #4facfe);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-weight:800;
}
.search-box input {
    background: rgba(255,255,255,0.1)!important;
    color: white!important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CLIENT
# ============================================================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ============================================================
# SESSION STATE
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {
        "chat_1": {
            "title": "New Chat",
            "messages": [],
            "time": str(datetime.datetime.now())
        }
    }

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"

if "page" not in st.session_state:
    st.session_state.page = "chat"

# ============================================================
# SYSTEM PROMPT - FINAL TRILINGUAL
# ============================================================
SYSTEM_PROMPT = """
You are Aditya AI, created by Aditya from Belpahar, Odisha, India.
You are NOT ChatGPT.

CRITICAL LANGUAGE RULE:
- If user speaks Hindi (तुम कौन हो, कैसे हो) -> Reply in pure Hindi.
- If user speaks English (Who are you, how to do) -> Reply in pure English.
- If user speaks Hinglish (bhai tu kaun hai, thumbnail kaise banaye) -> Reply in Hinglish like "Haan bhai main Aditya AI hu yaar, Belpahar se"

Always say you are Aditya AI from Belpahar when asked.
Be helpful for Photoshop, Editing, Design.
Keep answers short and friendly.
"""

# ============================================================
# SIDEBAR WITH SEARCH AND MIC INFO
# ============================================================
with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    st.caption("Made by Aditya | Belpahar, Jharsuguda, Odisha")
    st.divider()

    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()

    if st.button("📝 Blog / About", use_container_width=True):
        st.session_state.page = "blog"
        st.rerun()

    if st.button("🎤 Voice Chat Page", use_container_width=True):
        st.session_state.page = "voice"
        st.rerun()

    st.divider()

    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        nid = f"chat_{uuid.uuid4().hex[:6]}"
        st.session_state.current_chat_id = nid
        st.session_state.messages = []
        st.session_state.all_chats[nid] = {
            "title": "New Chat",
            "messages": [],
            "time": str(datetime.datetime.now())
        }
        st.session_state.page = "chat"
        st.rerun()

    st.divider()

    # ================= SEARCH BAR - FIXED =================
    st.markdown("### 🔍 Search Chats")
    search_text = st.text_input(
        "Search",
        placeholder="Type to search history...",
        label_visibility="collapsed",
        key="search_bar_main"
    )

    st.markdown("### 📜 Chat History")

    all_chats_items = list(st.session_state.all_chats.items())

    # Filter by search
    if search_text:
        all_chats_items = [
            (cid, data) for cid, data in all_chats_items
            if search_text.lower() in data["title"].lower()
        ]

    if not all_chats_items:
        st.info("No chats found.")

    for cid, data in all_chats_items[::-1][:15]:
        display_title = data["title"][:24]
        if st.button(f"📄 {display_title}", key=f"hist_{cid}", use_container_width=True):
            st.session_state.current_chat_id = cid
            st.session_state.messages = data["messages"]
            st.session_state.page = "chat"
            st.rerun()

    st.divider()
    st.markdown("**📍 Belpahar, Odisha**")
    st.caption("Aditya AI v2.0 with Mic + Search")

# ============================================================
# BLOG PAGE
# ============================================================
if st.session_state.page == "blog":
    st.markdown("# 👤 Aditya - Belpahar")
    st.markdown("**Hey, I'm Aditya from Belpahar, Odisha! 🙏**")
    st.link_button("🌐 Visit My Real Blog", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)
    st.divider()
    st.markdown("### 🔥 About: Aditya AI made with Python + Groq AI. Hindi & English + Hinglish Voice.")
    st.markdown("**Location: Belpahar, Jharsuguda, Odisha**")
    st.divider()
    st.markdown("## 📝 Latest Posts From My Blogger")
    st.markdown("#### 1. Aditya AI Now Has Voice Chat!")
    st.caption("Sep 05, 2026")
    st.link_button("📖 Read on Blogger", "https://aditya-ai-belpahar.blogspot.com", key="b1", use_container_width=True)
    st.markdown("#### 2. Privacy Policy and About Us")
    st.caption("Sep 04, 2026")
    st.link_button("📖 Read Privacy Policy", "https://aditya-ai-belpahar.blogspot.com", key="b2", use_container_width=True)
    st.divider()
    if st.button("⬅️ Back to Chat", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()
    st.stop()

# ============================================================
# VOICE PAGE
# ============================================================
if st.session_state.page == "voice":
    st.markdown("# 🎤 Voice Chat")
    st.caption("Bolo, main sun raha hu...")

    st.markdown("#### 🎙️ Record Here:")
    audio = st.audio_input("Record your voice")

    if audio:
        with st.spinner("Sun raha hu..."):
            try:
                transcription = client.audio.transcriptions.create(
                    file=(audio.name, audio.getvalue()),
                    model="whisper-large-v3-turbo"
                )
                user_text = transcription.text
                st.success(f"You said: {user_text}")
                r = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_text}],
                    max_tokens=1000,
                    temperature=0.7
                )
                ans = r.choices[0].message.content
                st.markdown(ans)
                lang = 'hi' if any('\u0900' <= c <= '\u097F' for c in ans) else 'en'
                tts = gTTS(text=ans[:400], lang=lang)
                b = io.BytesIO()
                tts.write_to_fp(b)
                b.seek(0)
                st.audio(b, format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("⬅️ Back to Chat"):
        st.session_state.page = "chat"
        st.rerun()
    st.stop()

# ============================================================
# MAIN CHAT PAGE - WITH SEARCH + MIC VISIBLE
# ============================================================
st.markdown("# 😊 Aditya AI")
st.caption("Photoshop • Editing • Design • Hindi + English + Hinglish • Mic + Search")

# Show chat history messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.divider()

# ------------------------------------------------------------
# NEW INPUT AREA - BIG MIC BUTTON + SEARCH INFO
# ------------------------------------------------------------
st.markdown("### 🎤 Bolke Poocho / Type Karo:")

# First row - Mic buttons
mic_col1, mic_col2, mic_col3 = st.columns([1, 1, 6])

final_input = None

with mic_col1:
    if MIC_AVAILABLE:
        st.markdown("**Mic:**")
        mic_audio = mic_recorder(
            start_prompt="🎤 Start",
            stop_prompt="⏹️ Stop",
            just_once=True,
            use_container_width=True,
            key="main_mic"
        )
        if mic_audio:
            with st.spinner("Samajh raha hu..."):
                try:
                    transcription = client.audio.transcriptions.create(
                        file=("audio.wav", mic_audio['bytes']),
                        model="whisper-large-v3-turbo"
                    )
                    final_input = transcription.text
                    st.toast(f"🎤 Bola: {final_input}")
                except Exception as e:
                    st.error(f"Mic Error: {e}")
    else:
        mic_audio = None

with mic_col2:
    st.markdown("**Or:**")
    audio_input_chat = st.audio_input("🎙️ Record", key="chat_audio_input", label_visibility="collapsed")

    if audio_input_chat:
        with st.spinner("Transcribe kar raha hu..."):
            try:
                transcription = client.audio.transcriptions.create(
                    file=(audio_input_chat.name, audio_input_chat.getvalue()),
                    model="whisper-large-v3-turbo"
                )
                final_input = transcription.text
                st.success(f"🎙️ Sun liya: {final_input}")
            except Exception as e:
                st.error(f"Error: {e}")

with mic_col3:
    st.info("💡 Tip: Mic dabao, bolo, fir AI jawab dega Hindi/English/Hinglish me")

# Second row - Text input
text_input = st.chat_input("Type here... (Hindi / English / Hinglish)")

if text_input:
    final_input = text_input

# ------------------------------------------------------------
# AI RESPONSE LOGIC
# ------------------------------------------------------------
if final_input:
    st.session_state.messages.append({"role":"user","content":final_input})

    with st.chat_message("user"):
        st.markdown(final_input)

    with st.chat_message("assistant"):
        with st.spinner("Aditya AI soch raha hai..."):
            msgs = [{"role":"system","content":SYSTEM_PROMPT}] + [
                {"role": x["role"], "content": x["content"]} for x in st.session_state.messages
            ]

            r = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=msgs,
                max_tokens=1500,
                temperature=0.7
            )
            ans = r.choices[0].message.content
            st.markdown(ans)

            # Voice output
            try:
                lang = 'hi' if any('\u0900' <= c <= '\u097F' for c in ans) else 'en'
                tts = gTTS(text=ans[:350], lang=lang)
                b = io.BytesIO()
                tts.write_to_fp(b)
                b.seek(0)
                st.audio(b, format="audio/mp3")
            except:
                pass

            st.session_state.messages.append({"role":"assistant","content":ans})

    # Update title
    if st.session_state.all_chats[st.session_state.current_chat_id]["title"] == "New Chat":
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = final_input[:30]

    st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    st.rerun()

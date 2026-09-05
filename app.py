import streamlit as st
from groq import Groq
import io

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- FIXED POLISHED CSS ---
st.markdown("""
<style>
    header[data-testid="stHeader"] { background: transparent; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f12 0%, #1a1a22 100%);
        border-right: 1px solid #2a2a35;
    }
   .sidebar-logo {
        font-size: 28px; font-weight: 800;
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
   .sidebar-card {
        background: #21212a; padding: 14px; border-radius: 12px;
        border: 1px solid #2f2f3d; margin: 12px 0;
    }
   .sidebar-link {
        display: block; padding: 10px 14px;
        background: #2a2a38; border-radius: 8px;
        color: white!important; text-decoration: none; margin: 6px 0;
    }
   .sidebar-link:hover { background: #3a3a4d; }

    /* MOBILE HEADER - FIXED NO OVERLAP */
    @media (max-width: 768px) {
       .mobile-top-bar {
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 56px;
            background: rgba(15,15,18,0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid #2a2a35;
            display: flex;
            align-items: center;
            padding-left: 52px; /* Leave space for Streamlit's ☰ button */
            z-index: 999;
        }
       .mobile-logo {
            font-weight: 800; font-size: 18px;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
       .block-container { padding-top: 70px!important; }
        [data-testid="stChatInput"] {
            background: #1e1e26; border-radius: 20px; border: 1px solid #3a3a4d;
        }
    }
    @media (min-width: 769px) {
       .mobile-top-bar { display: none; }
    }
</style>

<div class="mobile-top-bar">
    <div class="mobile-logo">🔥 Aditya AI</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR = YOUR MENU (☰) ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI")
    
    # This is now INSIDE menu, not overlapping on top
    st.markdown("""
    <div class="sidebar-card" style="display:flex; justify-content:space-between; align-items:center">
        <span style="font-size:13px">📍 Belpahar, Odisha</span>
        <span style="font-size:10px; background:#00ff8820; color:#00ff88; padding:4px 8px; border-radius:20px; border:1px solid #00ff8830;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <b>👨‍💻 Creator</b><br>
        <span style='color:#aaa; font-size:13px'>Aditya from Belpahar<br>Student • Developer • Dreamer</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**☰ Menu**")
    st.markdown('<a class="sidebar-link" href="https://aditya-ai-belpahar.blogspot.com" target="_blank">📝 My Blog</a>', unsafe_allow_html=True)
    st.markdown('<a class="sidebar-link" href="https://github.com" target="_blank">⭐ Fork on GitHub</a>', unsafe_allow_html=True)
    st.markdown('<a class="sidebar-link" href="#" target="_blank">📍 Belpahar • LIVE Status</a>', unsafe_allow_html=True)

    st.markdown("<br><div class='sidebar-card' style='text-align:center; font-size:12px; color:#888'>Made with ❤️ in Belpahar<br>v2.0</div>", unsafe_allow_html=True)

# --- MAIN ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.markdown("Built by **Aditya from Belpahar** — Ask me anything!")
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.markdown("#### 🎙️ Voice Chat")
audio = st.audio_input("Record")
transcribed_text = None
if audio:
    with st.spinner("Sun raha hu..."):
        try:
            txt = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text", language="hi")
            transcribed_text = str(txt)
            st.success(f"You said: {transcribed_text}")
        except Exception as e:
            st.error(f"Voice Error: {e}")

user_input = st.chat_input("Ask me anything...")
if transcribed_text:
    user_input = transcribed_text

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hu..."):
            try:
               

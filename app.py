import streamlit as st
from groq import Groq
import io

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- PREMIUM SIDEBAR CSS ---
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f12 0%, #1a1a22 100%);
        border-right: 1px solid #2a2a35;
    }
   .sidebar-logo {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
   .sidebar-card {
        background: #21212a;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #2f2f3d;
        margin: 12px 0;
    }
   .sidebar-link {
        display: block;
        padding: 10px 14px;
        background: #2a2a38;
        border-radius: 8px;
        color: white!important;
        text-decoration: none;
        margin: 6px 0;
        transition: 0.2s;
    }
   .sidebar-link:hover {
        background: #3a3a4d;
        transform: translateX(3px);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR PREMIUM ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI")

    st.markdown("""
    <div class="sidebar-card">
        <b>👨‍💻 Creator</b><br>
        <span style='color:#aaa; font-size:13px'>Aditya from Belpahar, Odisha<br>Student • Developer • Dreamer</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**✨ Features**")
    st.markdown("""
    - 🎙️ Hindi & English Voice
    - 🧠 Super Fast Groq AI
    - 🔊 Speaks Back
    - 💬 Remembers Chat
    """)

    st.markdown("---")
    st.markdown("**🔗 Connect**")
    st.markdown('<a class="sidebar-link" href="https://aditya-ai-belpahar.blogspot.com" target="_blank">📝 My Blog</a>', unsafe_allow_html=True)
    st.markdown('<a class="sidebar-link" href="https://github.com" target="_blank">💻 GitHub</a>', unsafe_allow_html=True)

    st.markdown("<br><div class='sidebar-card' style='text-align:center; font-size:12px; color:#888'>Made with ❤️ in Belpahar<br>v2.0 • 2026</div>", unsafe_allow_html=True)

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
            txt = client.audio.transcriptions.create(
                file=("audio.wav", audio.getvalue(), "audio/wav"),
                model="whisper-large-v3",
                response_format="text",
                language="hi"
            )
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
                system_msg = {"role": "system", "content": "You are Aditya AI, created by Aditya from Belpahar, Odisha, India. You are NOT ChatGPT. Say you are Aditya AI built by Aditya. Reply in Hindi/English as user asks."}
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[system_msg] + st.session_state.messages
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                if TTS:
                    try:
                        lang = 'hi' if any('\u0900' <= c <= '\u097F' for c in reply) else 'en'
                        tts = gTTS(text=reply[:500], lang=lang)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        st.audio(fp, format="audio/mp3", autoplay=True)
                    except:
                        pass
            except Exception as e:
                st.error(f"Error: {e}")

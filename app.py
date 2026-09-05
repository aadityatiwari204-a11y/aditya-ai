import streamlit as st
from groq import Groq
import io

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- PREMIUM ANIMATIONS + UI ---
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

    /* MOBILE HEADER */
    @media (max-width: 768px) {
      .mobile-top-bar {
            position: fixed; top: 0; left: 0; right: 0;
            height: 56px;
            background: rgba(15,15,18,0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid #2a2a35;
            display: flex; align-items: center;
            padding-left: 52px; z-index: 999;
        }
      .mobile-logo {
            font-weight: 800; font-size: 18px;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
      .block-container { padding-top: 70px!important; }
    }
    @media (min-width: 769px) {
      .mobile-top-bar { display: none; }
    }

    /* ✨ THINKING ANIMATION */
  .thinking-wrap {
        display: flex; align-items: center; gap: 12px;
        background: #1c1c24;
        border: 1px solid #2a2a35;
        padding: 14px 18px;
        border-radius: 16px;
        width: fit-content;
    }
  .thinking-avatar {
        width: 32px; height: 32px; border-radius: 50%;
        background: linear-gradient(135deg, #ff6a00, #ee0979);
        display: flex; align-items: center; justify-content: center;
        animation: pulseGlow 2s infinite;
    }
  .dots { display: flex; gap: 4px; }
  .dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #ff6a00;
        animation: bounceDot 1.4s infinite;
    }
  .dot:nth-child(2) { animation-delay: 0.2s; background: #ff8a33; }
  .dot:nth-child(3) { animation-delay: 0.4s; background: #ee0979; }

    @keyframes bounceDot {
        0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
        40% { transform: translateY(-6px); opacity: 1; }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(255,106,0,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255,106,0,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,106,0,0); }
    }
  .shimmer-text {
        background: linear-gradient(90deg, #888 0%, #fff 50%, #888 100%);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 1.5s infinite linear;
        font-size: 13px;
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* Voice listening animation */
  .listening {
        display: flex; align-items: center; gap: 8px;
        color: #ff6a00; font-size: 13px;
        animation: pulseText 1s infinite;
    }
    @keyframes pulseText { 0%,100% { opacity: 0.6 } 50% { opacity: 1 } }
</style>

<div class="mobile-top-bar">
    <div class="mobile-logo">🔥 Aditya AI</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI")
    st.markdown("""
    <div class="sidebar-card" style="display:flex; justify-content:space-between; align-items:center">
        <span style="font-size:13px">📍 Belpahar, Odisha</span>
        <span style="font-size:10px; background:#00ff8820; color:#00ff88; padding:4px 8px; border-radius:20px;">● LIVE</span>
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

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.markdown("Built by **Aditya from Belpahar**")
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.markdown("#### 🎙️ Voice Chat")
audio = st.audio_input("Record")
transcribed_text = None

if audio:
    # Animated listening state
    listen_ph = st.empty()
    listen_ph.markdown('<div class="listening">🔴 Listening... transcribing...</div>', unsafe_allow_html=True)
    try:
        txt = client.audio.transcriptions.create(
            file=("audio.wav", audio.getvalue(), "audio/wav"),
            model="whisper-large-v3",
            response_format="text",
            language="hi"
        )
        transcribed_text = str(txt)
        listen_ph.empty()
        st.success(f"You said: {transcribed_text}")
    except Exception as e:
        listen_ph.empty()
        st.error(f"Voice Error: {e}")

user_input = st.chat_input("Ask me anything...")
if transcribed_text:
    user_input = transcribed_text

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # ✨ SUBTLE THINKING ANIMATION
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("""
        <div class="thinking-wrap">
            <div class="thinking-avatar">🔥</div>
            <div>
                <div class="shimmer-text">Aditya AI is thinking...</div>
                <div class="dots">
                    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            system_msg = {
                "role": "system",
                "content": "You are Aditya AI, created by Aditya from Belpahar. NOT ChatGPT."
            }
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[system_msg] + st.session_state.messages
            )
            reply = res.choices[0].message.content

            thinking_placeholder.empty()
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            if TTS:
                try:
                    if any('\u0900' <= c <= '\u097F' for c in reply):
                        lang_code = 'hi'
                    else:
                        lang_code = 'en'
                    tts = gTTS(text=reply[:500], lang=lang_code)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3", autoplay=True)
                except:
                    pass
        except Exception as e:
            thinking_placeholder.empty()
            st.error(f"Error: {e}")

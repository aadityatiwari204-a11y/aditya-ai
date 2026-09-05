import streamlit as st
from groq import Groq

# Page config
st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="centered")

# Sidebar - CLEAN
st.sidebar.title("🔥 Aditya AI")
st.sidebar.markdown("Built by Aditya from Belpahar")

# Header
st.markdown("<p style='font-size:16px; color:gray; margin-top:2px;'>Built by Aditya from Belpahar</p>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. CHAT AREA WELCOME CARD ---
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.markdown("Ask me anything in Hindi or English. I can chat, code, and help with your studies!")
        st.markdown("*Built with 🔥 by Aditya from Belpahar*")
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --- 4. POLISHED VOICE CHAT ---
st.markdown("#### 🎙️ Voice Chat (Hindi/English)")
voice_status = st.empty()
voice_status.markdown("🎙️ **Tap to speak** - Click mic to start")

audio = st.audio_input("🔴 Listening... Tap mic to record")

transcribed_text = None

if audio:
    voice_status.warning("🔴 Listening... Recording captured!")
    with st.spinner("🧠 Thinking... Sun raha hu... transcribing..."):
        try:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio.getvalue(), "audio/wav"),
                model="whisper-large-v3",
                response_format="text",
                language="hi"
            )
            transcribed_text = transcription
            st.success(f"You said: {transcribed_text}")
            voice_status.empty()
        except Exception as e:
            st.error(f"Error: {e}")
            voice_status.empty()

# --- CHAT INPUT ---
user_input = st.chat_input("Ask me anything...")

# If voice was transcribed, use it as input
if transcribed_text:
    user_input = transcribed_text

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Aditya AI soch raha hai..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

# Footer Blog
st.markdown("---")
st.markdown("[📝 Visit Blog : aditya-ai-belpahar.blogspot.com](https://aditya-ai-belpahar.blogspot.com)")

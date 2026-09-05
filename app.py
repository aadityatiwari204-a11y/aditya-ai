import streamlit as st
from groq import Groq
import io

# Speaking module - safe import
try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="centered")

st.sidebar.title("🔥 Aditya AI")
st.sidebar.markdown("Built by Aditya from Belpahar")
st.sidebar.markdown("[📝 Blog](https://aditya-ai-belpahar.blogspot.com)")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.markdown("Ask in **Hindi or English** — I can chat, code & help in studies!")
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.markdown("#### 🎙️ Voice Chat")
voice_status = st.empty()
voice_status.info("🎙️ Tap to speak")

audio = st.audio_input("Record")
transcribed_text = None

if audio:
    voice_status.warning("🔴 Recording captured!")
    with st.spinner("Sun raha hu..."):
        try:
            text = client.audio.transcriptions.create(
                file=("audio.wav", audio.getvalue(), "audio/wav"),
                model="whisper-large-v3",
                response_format="text",
                language="hi"
            )
            transcribed_text = str(text)
            st.success(f"You said: {transcribed_text}")
            voice_status.empty()
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
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.messages
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

st.markdown("---")
st.markdown("[📝 Blog](https://aditya-ai-belpahar.blogspot.com)")

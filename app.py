import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

st.set_page_config(page_title="Aditya AI", page_icon="🔥")
st.sidebar.markdown("## 🔥 Aditya AI")
st.markdown("""
<h2 style='margin-bottom:0px;'>🔥 Aditya AI</h2>
<p style='font-size:16px; color:gray; margin-top:2px;'>Built by Aditya from Belpahar</p>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.markdown("Ask me anything in Hindi or English. I can chat, code, and help with your studies!")
        st.markdown("*Built with 🔥 by Aditya from Belpahar*")
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --- OFFICIAL VOICE RECORDER - POLISHED ---
st.markdown("#### 🎤 Voice Chat (Hindi/English)")
voice_status = st.empty()
voice_status.markdown("🎙️ **Tap to speak** - Click mic to start")

audio = st.audio_input("🔴 Listening... Tap mic to record")

transcribed_text = None
user_input = None

if audio:
    voice_status.warning("🔴 **Listening...** - Recording captured!")
    with st.spinner("🧠 **Thinking...** - Sun raha hu... transcribing..."):
        try:
        try:
            # Groq Whisper transcription
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio.getvalue(), "audio/wav"),
                model="whisper-large-v3",
                response_format="text",
                language="hi"
            )
            transcribed_text = transcription
            st.success(f"You said: {transcribed_text}")
            user_input = transcribed_text
        except Exception as e:
            st.error(f"Transcription Error: {e}")

# Text input also
text_input = st.chat_input("Type or speak...")

if text_input:
    user_input = text_input

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are Aditya AI built by Aditya from Belpahar, Odisha. Reply in SAME language user uses. If user speaks Hindi, reply in pure Hindi (Devanagari). If English, reply in English. Keep answer short, helpful for Indian students."},
                    *st.session_state.messages
                ]
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

            # Auto Speak Reply - FIXED HINDI VOICE
            safe = ans.replace('"', ' ').replace("'", ' ').replace("\n", " ")[:600]
            components.html(f"""
                <script>
                speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance("{safe}");
                var isHindi = /[\\u0900-\\u097F]/.test("{safe}");
                u.lang = isHindi? 'hi-IN' : 'en-IN';
                u.rate=0.95;
                speechSynthesis.speak(u);
                </script>
                <button onclick="var u=new SpeechSynthesisUtterance('{safe}'); var isHindi=/[\\u0900-\\u097F]/.test('{safe}'); u.lang=isHindi?'hi-IN':'en-IN'; u.rate=0.95; speechSynthesis.speak(u);" style="background:#FF4B4B;color:white;border:none;padding:8px 15px;border-radius:20px;cursor:pointer;margin-right:10px;">🔊 Replay Voice</button>
                <button onclick="speechSynthesis.cancel()" style="background:#333;color:white;border:none;padding:8px 15px;border-radius:20px;cursor:pointer;">⏹️ Stop</button>
            """, height=60)

        except Exception as e:
            st.error(f"Error: {e} - Check GROQ_API_KEY in Secrets")

st.markdown("---")
st.link_button("🔗 Visit Blog - aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com")

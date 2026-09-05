import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

st.set_page_config(page_title="Aditya AI", page_icon="🔥")
st.title("🔥 Aditya AI - Built by Aditya from Belpahar")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- OFFICIAL VOICE RECORDER ---
st.markdown("#### 🎤 Voice Chat (Hindi/English)")
audio = st.audio_input("Tap to record, then it auto-sends")

transcribed_text = None
if audio:
    with st.spinner("🎧 Sun raha hu... transcribing..."):
        try:
            # Groq Whisper transcription
            transcription = client.audio.transcriptions.create(
                file=(audio.name, audio.getvalue()),
                model="whisper-large-v3",
                language="en", # auto detects hi/en
                response_format="text"
            )
            transcribed_text = transcription
            st.success(f"✅ You said: {transcribed_text}")
        except Exception as e:
            st.error(f"Voice error: {e}")

# If voice transcribed OR typed
prompt = transcribed_text
typed = st.chat_input("Or type here...")

if typed:
    prompt = typed

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role":"system","content":"You are Aditya AI built by Aditya from Belpahar, Odisha, India. Be helpful, friendly, short answer for voice."}] + st.session_state.messages
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role":"assistant","content":ans})

            # Auto Speak Reply
            safe = ans.replace("'"," ").replace('"'," ").replace("\n"," ")[:600]
            components.html(f"""
                <script>
                speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance("{safe}");
                u.lang='en-IN'; u.rate=0.95;
                speechSynthesis.speak(u);
                </script>
                <button onclick="var u=new SpeechSynthesisUtterance('{safe}');u.lang='en-IN';speechSynthesis.cancel();speechSynthesis.speak(u);" style="background:#4ECDC4;color:white;border:none;padding:8px 15px;border-radius:20px;cursor:pointer;">🔊 Replay Voice</button>
                <button onclick="speechSynthesis.cancel()" style="background:#333;color:white;border:none;padding:6px 10px;border-radius:15px;margin-left:5px;">🔇 Stop</button>
            """, height=50)

        except Exception as e:
            st.error(f"Error: {e} - Check GROQ_API_KEY in Secrets")

st.markdown("---")
st.link_button("🔗 Visit Blog - aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)

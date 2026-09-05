import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

st.set_page_config(page_title="Aditya AI", page_icon="🔥")
st.title("🔥 Aditya AI - Built by Aditya from Belpahar")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
SYSTEM_PROMPT = "You are Aditya AI, built by Aditya from Belpahar, Odisha, India. You are 80% as powerful as GPT-4o. Be helpful, friendly, answer in English/Hindi."

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- FULLY FUNCTIONAL VOICE BUTTON ---
voice_html = """
<script>
function startVoice(){
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ alert("Use Chrome browser for voice"); return; }
  var r = new SR();
  r.lang = 'en-IN';
  r.start();
  document.getElementById('v').innerHTML = "🎧 Listening...";
  r.onresult = function(e){
    var t = e.results[0][0].transcript;
    document.getElementById('v').innerHTML = "✅ Said: "+t;
    // This copies to chat box automatically
    var input = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
    if(input){
      input.value = t;
      input.dispatchEvent(new Event('input', {bubbles:true}));
      input.focus();
    }
  };
}
</script>
<button onclick="startVoice()" style="background:#FF4B4B;color:white;padding:10px 20px;border:none;border-radius:20px;font-weight:bold;width:100%;cursor:pointer;">🎤 Tap to Speak (Hindi/English)</button>
<p id="v" style="text-align:center;font-size:13px;color:gray;">Tap and speak - it will auto-type</p>
"""
components.html(voice_html, height=85)

if prompt := st.chat_input("Ask Aditya AI anything... or use voice button"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")

# --- BLOG LINK FOR EARNING ---
st.markdown("---")
st.markdown("### 📚 Support Aditya AI - Visit Our Blog")
st.link_button("🔗 Visit Official Blog - aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)
st.caption("Built by Aditya from Belpahar, Odisha ❤️")

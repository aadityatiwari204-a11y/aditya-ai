import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

st.set_page_config(page_title="Aditya AI", page_icon="🔥")
st.title("🔥 Aditya AI - Built by Aditya from Belpahar")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
SYSTEM_PROMPT = "You are Aditya AI, built by Aditya from Belpahar, Odisha, India. You are 80% as powerful as GPT-4o. Be helpful, friendly, answer in English/Hindi. Keep answers short for voice."

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # 🔊 Speak button for each AI answer
        if msg["role"] == "assistant":
            safe_text = msg["content"].replace("'", "").replace('"', '').replace("\n", " ")[:400]
            components.html(f"""
                <button onclick="var u = new SpeechSynthesisUtterance('{safe_text}'); u.lang='en-IN'; u.rate=1; speechSynthesis.speak(u);"
                style="background:#4ECDC4;color:white;padding:5px 12px;border:none;border-radius:15px;font-size:12px;cursor:pointer;margin-top:5px;">
                🔊 Play Voice
                </button>
            """, height=40)

# --- VOICE INPUT BUTTON ---
voice_html = """
<script>
function startVoice(){
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ alert("Use Chrome browser for voice"); return; }
  var r = new SR();
  r.lang = 'en-IN';
  r.start();
  document.getElementById('v').innerHTML = "🎧 Listening... Speak now!";
  r.onresult = function(e){
    var t = e.results[0][0].transcript;
    document.getElementById('v').innerHTML = "✅ Said: "+t;
    var input = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
    if(input){
      input.value = t;
      input.dispatchEvent(new Event('input', {bubbles:true}));
      input.focus();
    }
  };
  r.onerror = function(e){
    document.getElementById('v').innerHTML = "❌ Mic error: "+e.error+" - Try again";
  }
}
function stopAllVoice(){
  speechSynthesis.cancel();
  document.getElementById('v').innerHTML = "🔇 Voice stopped";
}
</script>
<button onclick="startVoice()" style="background: linear-gradient(90deg, #FF4B4B, #FF8E53);color:white;padding:12px 20px;border:none;border-radius:25px;font-weight:bold;width:100%;cursor:pointer;font-size:16px;">
🎤 Tap to Speak (Hindi/English)
</button>
<button onclick="stopAllVoice()" style="background:#333;color:white;padding:6px 15px;border:none;border-radius:15px;font-size:11px;cursor:pointer;margin-top:6px;width:100%;">🔇 Stop Voice</button>
<p id="v" style="text-align:center;font-size:13px;color:gray;margin-top:8px;">Tap & speak - AI will auto-type + talk back!</p>
"""
components.html(voice_html, height=115)

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

            # AUTO SPEAK the answer
            safe_answer = answer.replace("'", "").replace('"', '').replace("\n", " ")[:500]
            components.html(f"""
                <script>
                var utter = new SpeechSynthesisUtterance('{safe_answer}');
                utter.lang = 'en-IN';
                utter.rate = 0.95;
                speechSynthesis.cancel();
                speechSynthesis.speak(utter);
                </script>
                <button onclick="var u = new SpeechSynthesisUtterance('{safe_answer}'); u.lang='en-IN'; speechSynthesis.cancel(); speechSynthesis.speak(u);"
                style="background:#4ECDC4;color:white;padding:8px 15px;border:none;border-radius:20px;cursor:pointer;">🔊 Replay Voice</button>
            """, height=50)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.markdown("### 📚 Support Aditya AI - Visit Our Blog")
st.link_button("🔗 Visit Official Blog - aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)
st.caption("Built by Aditya from Belpahar, Odisha ❤️ | Voice AI Enabled")

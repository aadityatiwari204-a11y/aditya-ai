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

# --- SIMPLE VOICE THAT WORKS 100% ---
components.html("""
<script>
function startVoice(){
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ alert("Please use Google Chrome"); return; }
  var r = new SR();
  r.lang = 'en-IN';
  r.start();
  document.getElementById('s').innerHTML = "🎧 Listening... Boliye";
  r.onresult = function(e){
    var t = e.results[0][0].transcript;
    document.getElementById('s').innerHTML = "✅ You said: <b>"+t+"</b><br>Now press ⬆️ arrow in chat box below";
    var ta = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
    if(ta){
      ta.value = t;
      ta.dispatchEvent(new Event('input', {bubbles:true}));
      ta.focus();
    }
  };
}
</script>
<div id="s" style="text-align:center;color:#FFCC00;font-size:13px;margin-bottom:8px;">Tap mic, speak Hindi/English</div>
<button onclick="startVoice()" style="background:#FF4B4B;color:white;width:100%;padding:12px;border:none;border-radius:25px;font-weight:bold;font-size:16px;">🎤 Tap to Speak (Hindi/English)</button>
""", height=90)

prompt = st.chat_input("Type here or use mic then press ⬆️")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role":"system","content":"You are Aditya AI built by Aditya from Belpahar, Odisha. Helpful, friendly, short answer."}] + st.session_state.messages
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role":"assistant","content":ans})

            # Voice Reply
            safe = ans.replace("'"," ").replace('"'," ").replace("\n"," ")[:500]
            components.html(f"""
            <script>
            var u = new SpeechSynthesisUtterance("{safe}");
            u.lang='en-IN'; u.rate=0.95;
            speechSynthesis.cancel(); speechSynthesis.speak(u);
            </script>
            <button onclick="var u=new SpeechSynthesisUtterance('{safe}');u.lang='en-IN';speechSynthesis.cancel();speechSynthesis.speak(u);" style="background:#4ECDC4;color:white;border:none;padding:6px 14px;border-radius:20px;">🔊 Play Voice</button>
            """, height=50)
        except Exception as e:
            st.error(f"Error: {{e}} - Check GROQ_API_KEY in Secrets")

st.markdown("---")
st.link_button("🔗 Visit Blog - aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)

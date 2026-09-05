import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

st.set_page_config(page_title="Aditya AI", page_icon="🔥")
st.title("🔥 Aditya AI - Built by Aditya from Belpahar")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
SYSTEM_PROMPT = "You are Aditya AI, built by Aditya from Belpahar, Odisha. You are 80% as powerful as GPT-4o. Be helpful, short answer for voice."

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# VOICE INPUT - SUPER AUTO SEND
voice_html = """
<div id="status" style="text-align:center;color:gray;font-size:13px;margin:8px;">Tap mic and speak</div>
<button onclick="startVoice()" id="micBtn" style="background: linear-gradient(90deg, #FF4B4B, #FF8E53);color:white;padding:12px;border:none;border-radius:25px;font-weight:bold;width:100%;cursor:pointer;font-size:16px;">
🎤 Tap to Speak
</button>
<script>
var lastText = "";
function startVoice(){
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ alert("Use Chrome!"); return; }
  var r = new SR();
  r.lang = 'en-IN';
  r.start();
  document.getElementById('status').innerHTML = "🎧 Listening...";
  document.getElementById('micBtn').innerHTML = "🎧 Listening... Speak now!";
  r.onresult = function(e){
    var t = e.results[0][0].transcript;
    lastText = t;
    document.getElementById('status').innerHTML = "✅ You said: " + t + " - Sending...";
    // AUTO COPY + AUTO CLICK SEND
    setTimeout(function(){
      var doc = window.parent.document;
      var ta = doc.querySelector('textarea[data-testid="stChatInputTextArea"]');
      if(ta){
        ta.value = t;
        ta.dispatchEvent(new Event('input', {bubbles:true}));
        ta.focus();
        setTimeout(function(){
          var btn = doc.querySelector('button[data-testid="stChatInputSubmitButton"]');
          if(btn){ btn.click(); }
        }, 500);
      }
    }, 300);
  };
  r.onend = function(){
    document.getElementById('micBtn').innerHTML = "🎤 Tap to Speak";
  }
}
</script>
"""
components.html(voice_html, height=95)

prompt = st.chat_input("Ask anything...")

# Check if voice text came
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            resp = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            )
            ans = resp.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

            # AUTO SPEAK + REPLAY BUTTON
            safe = ans.replace("'", " ").replace('"', " ").replace("\n"," ")[:600]
            components.html(f"""
                <script>
                speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance("{safe}");
                u.lang = 'en-IN'; u.rate = 0.95;
                speechSynthesis.speak(u);
                </script>
                <button onclick='var x=new SpeechSynthesisUtterance("{safe}");x.lang="en-IN";speechSynthesis.cancel();speechSynthesis.speak(x);'
                style='background:#4ECDC4;color:white;padding:8px 15px;border:none;border-radius:20px;'>🔊 Replay</button>
                <button onclick='speechSynthesis.cancel()' style='background:#333;color:white;padding:8px 15px;border:none;border-radius:20px;margin-left:5px;'>🔇 Stop</button>
            """, height=60)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.link_button("🔗 Visit Blog - aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)

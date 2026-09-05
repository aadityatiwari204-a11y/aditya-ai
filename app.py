import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
import urllib.parse

st.set_page_config(page_title="Aditya AI", page_icon="🔥")
st.title("🔥 Aditya AI - Built by Aditya from Belpahar")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Check if voice came via URL?voice=...
voice_query = st.query_params.get("voice", "")
if voice_query:
    # Clear URL
    st.query_params.clear()
    prompt = voice_query
    st.session_state.messages.append({"role":"user","content":prompt})
    try:
        res = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role":"system","content":"You are Aditya AI built by Aditya from Belpahar, Odisha. Be helpful, short."}] + st.session_state.messages
        )
        ans = res.choices[0].message.content
        st.session_state.messages.append({"role":"assistant","content":ans})
    except Exception as e:
        st.session_state.messages.append({"role":"assistant","content":f"Error: {e}"})
    st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"]=="assistant":
            safe = m["content"].replace("'"," ").replace('"'," ").replace("\n"," ")[:500]
            components.html(f"""
            <button onclick="var u=new SpeechSynthesisUtterance('{safe}');u.lang='en-IN';speechSynthesis.cancel();speechSynthesis.speak(u);" style="background:#4ECDC4;color:white;border:none;padding:6px 12px;border-radius:15px;">🔊 Play Voice</button>
            <button onclick="speechSynthesis.cancel()" style="background:#333;color:white;border:none;padding:6px 12px;border-radius:15px;margin-left:5px;">🔇 Stop</button>
            """, height=40)

# VOICE BUTTON - DIRECT AUTO SEND VIA URL
components.html("""
<script>
function startVoice(){
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ alert("Use Chrome browser"); return; }
  var r = new SR(); r.lang='en-IN'; r.start();
  document.getElementById('st').innerHTML = "🎧 Listening... Boliye...";
  r.onresult = function(e){
    var t = e.results[0][0].transcript;
    document.getElementById('st').innerHTML = "✅ You said: "+t+"<br>🚀 Sending to AI...";
    // This auto-sends by reloading with?voice=text
    var url = window.parent.location.href.split('?')[0] + "?voice=" + encodeURIComponent(t);
    window.parent.location.href = url;
  };
  r.onerror = function(e){ document.getElementById('st').innerHTML = "Error: "+e.error; }
}
</script>
<div id="st" style="text-align:center;color:#FFD700;font-size:13px;margin-bottom:8px;">Tap mic & speak - Auto sends!</div>
<button onclick="startVoice()" style="background:linear-gradient(90deg,#FF4B4B,#FF8E53);color:white;width:100%;padding:14px;border:none;border-radius:25px;font-weight:bold;font-size:16px;cursor:pointer;">🎤 Tap to Speak (Hindi/English)</button>
""", height=100)

# Normal text input as backup
if prompt := st.chat_input("Or type here..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    try:
        res = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role":"system","content":"You are Aditya AI built by Aditya from Belpahar."}] + st.session_state.messages
        )
        ans = res.choices[0].message.content
        st.session_state.messages.append({"role":"assistant","content":ans})
        st.rerun()
    except Exception as e:
        st.error(str(e))

st.markdown("---")
st.link_button("🔗 Visit Blog - aditya-ai-belpahar.blogspot.com", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)

# Auto speak last answer
if st.session_state.messages and st.session_state.messages[-1]["role"]=="assistant":
    last = st.session_state.messages[-1]["content"].replace("'"," ").replace('"'," ").replace("\n"," ")[:500]
    components.html(f"""
    <script>
    var u = new SpeechSynthesisUtterance("{last}");
    u.lang='en-IN'; u.rate=0.95;
    speechSynthesis.cancel();
    setTimeout(()=>{{speechSynthesis.speak(u)}},500);
    </script>
    """, height=0)

import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid

st.set_page_config(page_title="Aditya AI - Belpahar", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color:white; }
[data-testid="stSidebar"] { background: rgba(20,20,40,0.95); border-right: 1px solid #444; }
.stChatMessage { background: rgba(255,255,255,0.08)!important; border-radius:15px!important; backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.15); }
h1 { text-align:center; background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:800; }
div[data-testid="stColumn"] button { background: rgba(255,255,255,0.12)!important; border-radius:20px!important; border:1px solid rgba(255,255,255,0.2)!important; color:white!important; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages=[]
if "all_chats" not in st.session_state: st.session_state.all_chats={"chat_1":{"title":"New Chat","messages":[]}}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id="chat_1"
if "last_voice" not in st.session_state: st.session_state.last_voice=None
if "page" not in st.session_state: st.session_state.page="chat"

# --- SIDEBAR: Blog + Voice + Chat ---
with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    if st.button("💬 Chat"): st.session_state.page="chat"; st.rerun()
    if st.button("📝 Blog / About"): st.session_state.page="blog"; st.rerun()
    if st.button("🎤 Voice Chat"): st.session_state.page="voice"; st.rerun()
    st.markdown("---")
    if st.button("➕ New Chat"):
        nid=f"chat_{uuid.uuid4().hex[:6]}"; st.session_state.current_chat_id=nid; st.session_state.messages=[]; st.session_state.all_chats[nid]={"title":"New Chat","messages":[]}; st.rerun()
    st.markdown("### 📜 History")
    for cid,data in list(st.session_state.all_chats.items())[::-1]:
        if st.button(f"📝 {data['title'][:28]}", key=cid):
            st.session_state.current_chat_id=cid; st.session_state.messages=data["messages"]; st.session_state.page="chat"; st.rerun()

# BLOG PAGE
if st.session_state.page=="blog":
    st.markdown("# 📝 Blog - Aditya AI")
    st.markdown("**Made in Belpahar, Odisha** by Aditya")
    st.markdown("""
    - Photoshop tutorials in Hindi
    - Photo editing tricks
    - YouTube thumbnail designs
    - AI tools guide

    Follow: **Aditya Edits Belpahar** on Instagram & YouTube
    """)
    st.stop()

# MAIN CHAT AREA
st.markdown("# 🤖 Aditya AI")
st.markdown("<p style='text-align:center; opacity:0.7'>Your Smart AI from Belpahar — Hindi + English Voice</p>", unsafe_allow_html=True)

# --- SUGGESTED QUESTION BAR (This was missing) ---
st.markdown("#### 💡 Suggested:")
c1,c2,c3,c4 = st.columns(4)
suggestions = ["Photoshop kya hai?", "Background blur kaise kare?", "Best editing apps?", "Thumbnail kaise banaye?"]
for i,col in enumerate([c1,c2,c3,c4]):
    with col:
        if st.button(suggestions[i], key=f"sug_{i}"):
            st.session_state["suggested_prompt"] = suggestions[i]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if st.session_state.last_voice:
    st.audio(st.session_state.last_voice, format="audio/mp3")

# --- VOICE CHAT OPTION (This was missing) ---
voice_text = None
if st.session_state.page=="voice":
    st.info("🎤 Voice Chat Mode - Bol ke puchho!")
    audio = st.audio_input("Record your question...")
    if audio:
        try:
            trans = client.audio.transcriptions.create(model="whisper-large-v3", file=("audio.wav", audio.getvalue()))
            voice_text = trans.text
            st.success(f"You said: {voice_text}")
        except Exception as e:
            st.error(f"Voice error: {e}. Add `gTTS` in requirements.txt and enable mic.")

final_input = st.session_state.pop("suggested_prompt", None) or voice_text or st.chat_input("Photoshop kya hai? / What is Photoshop?")

if final_input:
    st.session_state.messages.append({"role":"user","content":final_input})
    with st.chat_message("user"): st.markdown(final_input)
    with st.chat_message("assistant"):
        ph=st.empty(); full=""
        msgs=[{"role":x["role"],"content":x["content"]} for x in st.session_state.messages]
        try:
            r=client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, max_tokens=2000)
            full=r.choices[0].message.content; ph.markdown(full)
        except:
            try:
                r=client.chat.completions.create(model="gemma2-9b-it", messages=msgs, max_tokens=2000)
                full=r.choices[0].message.content; ph.markdown(full)
            except Exception as e2: full=f"Server busy: {e2}"; ph.markdown(full)
        st.session_state.messages.append({"role":"assistant","content":full})
        try:
            lang='hi' if any('\u0900'<=c<='\u097F' for c in full) else 'en'
            tts=gTTS(text=full[:500], lang=lang, slow=False); buf=io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
            st.session_state.last_voice=buf; st.audio(buf, format="audio/mp3")
        except: pass
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"]=list(st.session_state.messages)
        st.session_state.all_chats[st.session_state.current_chat_id]["title"]=final_input[:35]
        st.rerun()

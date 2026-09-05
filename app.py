import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid

st.set_page_config(page_title="Aditya AI - Belpahar", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color:white; }
[data-testid="stSidebar"] { background: rgba(20,20,40,0.95); }
.stChatMessage { background: rgba(255,255,255,0.08)!important; border-radius:15px!important; border:1px solid rgba(255,255,255,0.15); }
h1 { text-align:center; background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:800; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages=[]
if "all_chats" not in st.session_state: st.session_state.all_chats={"chat_1":{"title":"New Chat","messages":[]}}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id="chat_1"
if "page" not in st.session_state: st.session_state.page="chat"

SYSTEM_PROMPT = "You are Aditya AI, created by Aditya from Belpahar, Odisha. You are NOT ChatGPT, NOT OpenAI. Say you are Aditya AI!"

with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page="chat"; st.rerun()
    if st.button("📝 Blog / About", use_container_width=True):
        st.session_state.page="blog"; st.rerun()
    if st.button("🎤 Voice Chat", use_container_width=True):
        st.session_state.page="voice"; st.rerun()
    st.divider()
    if st.button("➕ New Chat", use_container_width=True):
        nid=f"chat_{uuid.uuid4().hex[:6]}"; st.session_state.current_chat_id=nid; st.session_state.messages=[]; st.session_state.all_chats[nid]={"title":"New Chat","messages":[]}; st.session_state.page="chat"; st.rerun()
    st.markdown("### 📜 History")
    for cid,data in list(st.session_state.all_chats.items())[::-1][:10]:
        if st.button(f"📄 {data['title'][:20]}", key=cid, use_container_width=True):
            st.session_state.current_chat_id=cid; st.session_state.messages=data["messages"]; st.session_state.page="chat"; st.rerun()

if st.session_state.page=="blog":
    st.markdown("# 👤 Aditya - Belpahar")
    st.markdown("**Hey, I'm Aditya from Belpahar, Odisha! 🙏 I love making cool things with AI & Photoshop.**")
    st.divider()
    st.markdown("### 🔥 About This AI: Aditya AI, made with Python + Groq AI. Chat Hindi & English, Voice support.")
    st.markdown("**Location: Belpahar, Jharsuguda, Odisha**")
    st.divider()
    st.markdown("## 📝 My Blog Posts - Click to Read")
    with st.expander("📸 Post 1: How I Built Aditya AI - My First AI Project", expanded=True):
        st.write("Date: 6 Sep 2026 | Belpahar\n\nMaine socha apna khud ka AI banau? Python + Streamlit + Groq AI use karke aditya-ai-belpahar.streamlit.app LIVE kar diya! 2 din lage par ho gaya. First project!")
    with st.expander("🎨 Post 2: Photoshop Tips for Beginners"):
        st.write("Photoshop mein 3 cheez: Layers alag rakho, Background Blur - Filter > Gaussian Blur, Thumbnail - Bold text + bright bg.")
    with st.expander("💡 Post 3: Why I Built This for Belpahar Friends"):
        st.write("Belpahar mein talent hai par resources kam. Isliye Hindi mein help ke liye Aditya AI banaya. Next: Image Generator add karunga.")
    st.divider()
    if st.button("⬅️ Back to Chat"):
        st.session_state.page="chat"; st.rerun()
    st.stop()

if st.session_state.page=="voice":
    st.markdown("# 🎤 Voice Chat")
    audio = st.audio_input("Record your voice")
    if audio:
        with st.spinner("Sun raha hu..."):
            try:
                transcription = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3-turbo", language="hi")
                user_text = transcription.text
                st.success(f"You said: {user_text}")
                r = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_text}], max_tokens=1000)
                ans = r.choices[0].message.content
                st.markdown(ans)
                lang='hi' if any('\u0900'<=c<='\u097F' for c in ans) else 'en'
                tts=gTTS(text=ans[:400], lang=lang); b=io.BytesIO(); tts.write_to_fp(b); b.seek(0); st.audio(b, format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"Error: {e}")
    if st.button("⬅️ Back to Chat"): st.session_state.page="chat"; st.rerun()
    st.stop()

st.markdown("# 😊 Aditya AI")
st.caption("Photoshop • Editing • Design • Hindi + English Voice")
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
inp = st.chat_input("Type...")
if inp:
    st.session_state.messages.append({"role":"user","content":inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        msgs=[{"role":"system","content":SYSTEM_PROMPT}] + [{"role":x["role"],"content":x["content"]} for x in st.session_state.messages]
        r=client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=1500)
        ans=r.choices[0].message.content
        st.markdown(ans)
        st.session_state.messages.append({"role":"assistant","content":ans})
    st.session_state.all_chats[st.session_state.current_chat_id]["messages"]=st.session_state.messages

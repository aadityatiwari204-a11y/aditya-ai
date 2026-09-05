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

with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    if st.button("💬 Chat"): st.session_state.page="chat"; st.rerun()
    if st.button("📝 Blog / About"): st.session_state.page="blog"; st.rerun()
    if st.button("🎤 Voice Chat"): st.session_state.page="voice"; st.rerun()
    st.divider()
    if st.button("➕ New Chat"):
        nid=f"chat_{uuid.uuid4().hex[:6]}"; st.session_state.current_chat_id=nid; st.session_state.messages=[]; st.session_state.all_chats[nid]={"title":"New Chat","messages":[]}; st.rerun()
    st.markdown("### 📜 History")
    for cid,data in list(st.session_state.all_chats.items())[::-1][:10]:
        if st.button(f"📝 {data['title'][:22]}", key=cid):
            st.session_state.current_chat_id=cid; st.session_state.messages=data["messages"]; st.session_state.page="chat"; st.rerun()

if st.session_state.page=="blog":
    st.markdown("# 📝 Blog - Aditya AI Belpahar")
    st.write("Photoshop Tutorials, Editing Tricks by Aditya. Instagram: Aditya Edits Belpahar")
    st.stop()

st.markdown("# 🤖 Aditya AI")
st.caption("Photoshop • Editing • Design • Hindi + English Voice")

c1,c2,c3,c4 = st.columns(4)
for i, txt in enumerate(["Photoshop kya hai?", "Background blur kaise kare?", "Best editing apps?", "Thumbnail kaise banaye?"]):
    with [c1,c2,c3,c4][i]:
        if st.button(txt, key=f"s{i}"): st.session_state.sug=txt

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

inp = st.session_state.pop("sug", None) or st.chat_input("Type...")

if inp:
    st.session_state.messages.append({"role":"user","content":inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        ph=st.empty()
        try:
            msgs=[{"role":x["role"],"content":x["content"]} for x in st.session_state.messages]
            r=client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=1500)
            ans=r.choices[0].message.content
        except Exception as e:
            try:
                r=client.chat.completions.create(model="openai/gpt-oss-120b", messages=msgs, max_tokens=1500)
                ans=r.choices[0].message.content
            except Exception as e2: ans=f"Error: {e2}"
        ph.markdown(ans)
        st.session_state.messages.append({"role":"assistant","content":ans})
        try:
            lang='hi' if any('\u0900'<=c<='\u097F' for c in ans) else 'en'
            tts=gTTS(text=ans[:400], lang=lang); b=io.BytesIO(); tts.write_to_fp(b); b.seek(0); st.audio(b, format="audio/mp3")
        except: pass
    st.session_state.all_chats[st.session_state.current_chat_id]["messages"]=st.session_state.messages
    st.session_state.all_chats[st.session_state.current_chat_id]["title"]=inp[:30]

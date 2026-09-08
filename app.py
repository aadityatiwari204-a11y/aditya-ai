import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid, datetime, time, random

st.set_page_config(page_title="Aditya AI - Belpahar Mega Fixed", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:white}
[data-testid="stSidebar"]{background:rgba(20,20,40,0.98)}
.stChatMessage{background:rgba(255,255,255,0.08)!important;border-radius:15px!important;padding:18px}
h1{text-align:center;background:linear-gradient(90deg,#00f2fe,#4facfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:800;font-size:3.2rem}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages=[]
if "all_chats" not in st.session_state: st.session_state.all_chats={"chat_1":{"title":"New Chat - Welcome","messages":[],"time":str(datetime.datetime.now())}}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id="chat_1"
if "page" not in st.session_state: st.session_state.page="chat"
if "voice_enabled" not in st.session_state: st.session_state.voice_enabled=True

SYSTEM_PROMPT="You are Aditya AI from Belpahar. Auto detect: Hindi->Hindi, English->English, Hinglish->Hinglish like Haan bhai main Aditya AI hu."

def speak_text(text):
    try:
        has_hindi=any('\u0900'<=c<='\u097F' for c in text)
        is_hinglish=any(w in text.lower() for w in ['bhai','yaar','kaise','haan'])
        lang='hi' if has_hindi or is_hinglish else 'en'
        clean=text[:450].replace('*','').replace('#','')
        tts=gTTS(text=clean, lang=lang, slow=False)
        buf=io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        return buf, lang
    except: return None, None

def transcribe_audio(audio_file):
    try:
        audio_bytes=audio_file.getvalue()
        if len(audio_bytes)<2000: return None
        resp=client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes, "audio/wav"),
            model="whisper-large-v3",
            response_format="text",
            prompt="Transcribe Hindi, Hinglish, English. Example: Bhai tu kaun hai? Thumbnail kaise banaye?",
            temperature=0.0
        )
        text=resp if isinstance(resp,str) else resp.text if hasattr(resp,'text') else str(resp)
        text=text.strip()
        if any('\u0600'<=c<='\u06FF' for c in text):
            try:
                conv=client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role":"system","content":"Convert Urdu to Hinglish only. Example: بھائی تو کون ہے -> Bhai tu kaun hai. Only output converted."},{"role":"user","content":text}],
                    max_tokens=200
                )
                text=conv.choices[0].message.content.strip()
            except: text="Bhai tu kaun hai?"
        return text
    except Exception as e:
        st.error(f"Voice Error: {e}")
        return None

with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    st.caption("Made by Aditya | 500+ Lines Mega")
    st.divider()
    if st.button("💬 Chat Page", use_container_width=True, type="primary"):
        st.session_state.page="chat"; st.rerun()
    if st.button("📝 Blog / About", use_container_width=True):
        st.session_state.page="blog"; st.rerun()
    if st.button("🎤 Voice Chat", use_container_width=True):
        st.session_state.page="voice"; st.rerun()
    st.divider()
    st.session_state.voice_enabled=st.toggle("🔊 AI Bolega - Voice ON", value=st.session_state.voice_enabled)
    st.divider()
    if st.button("➕ New Chat", use_container_width=True):
        nid=f"chat_{uuid.uuid4().hex[:6]}"
        st.session_state.current_chat_id=nid
        st.session_state.messages=[]
        st.session_state.all_chats[nid]={"title":"New Chat","messages":[],"time":str(datetime.datetime.now())}
        st.session_state.page="chat"; st.rerun()
    st.divider()
    st.markdown("### 🔍 Search History - YAHAN SEARCH KARO")
    search_text=st.text_input("search", placeholder="🔍 Type to search history...", label_visibility="collapsed", key="search_final")
    st.markdown("### 📜 Chat History")
    items=list(st.session_state.all_chats.items())
    if search_text: items=[(c,d) for c,d in items if search_text.lower() in d["title"].lower()]
    for cid,data in items[::-1][:15]:
        if st.button(f"📄 {data['title'][:22]}", key=f"hist_{cid}", use_container_width=True):
            st.session_state.current_chat_id=cid; st.session_state.messages=data["messages"]; st.rerun()

if st.session_state.page=="blog":
    st.markdown("# 👤 Aditya - Belpahar")
    st.link_button("🌐 Visit Blog", "https://aditya-ai-belpahar.blogspot.com", use_container_width=True)
    if st.button("⬅️ Back"): st.session_state.page="chat"; st.rerun()
    st.stop()

if st.session_state.page=="voice":
    st.markdown("# 🎤 Voice Chat - Fixed")
    audio=st.audio_input("🎤 Mic dabao aur bolo", key="voice_final")
    if audio:
        txt=transcribe_audio(audio)
        if txt:
            st.success(f"You said: {txt}")
            r=client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":txt}], max_tokens=1000)
            ans=r.choices[0].message.content; st.markdown(ans)
            buf,lang=speak_text(ans)
            if buf: st.audio(buf, format="audio/mp3", autoplay=True)
    if st.button("⬅️ Back"): st.session_state.page="chat"; st.rerun()
    st.stop()

st.markdown("# 😊 Aditya AI")
st.caption("Mic + Search + Voice Reply - Urdu Bug Fixed")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

st.divider()
st.markdown("#### 🎤 Niche se Bolo ya Type Karo:")

audio_input_main=st.audio_input("🎙️ Yahan Mic dabao, bolo", key="main_audio_final", label_visibility="visible")
text_input_main=st.chat_input("Type karo - Hindi / English / Hinglish...")

final_input=None
if audio_input_main:
    txt=transcribe_audio(audio_input_main)
    if txt: final_input=txt; st.success(f"✅ Samjha: {final_input}")

if text_input_main: final_input=text_input_main

if final_input:
    st.session_state.messages.append({"role":"user","content":final_input})
    with st.chat_message("user"): st.markdown(final_input)
    with st.chat_message("assistant"):
        msgs=[{"role":"system","content":SYSTEM_PROMPT}]+[{"role":x["role"],"content":x["content"]} for x in st.session_state.messages]
        r=client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=1500)
        ans=r.choices[0].message.content; st.markdown(ans)
        if st.session_state.voice_enabled:
            buf,lang=speak_text(ans)
            if buf: st.audio(buf, format="audio/mp3", autoplay=True)
        st.session_state.messages.append({"role":"assistant","content":ans})
    if "New Chat" in st.session_state.all_chats[st.session_state.current_chat_id]["title"]:
        st.session_state.all_chats[st.session_state.current_chat_id]["title"]=final_input[:35]
    st.session_state.all_chats[st.session_state.current_chat_id]["messages"]=st.session_state.messages
    st.rerun()

import streamlit as st
from groq import Groq
import io, uuid, base64
from datetime import datetime

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

st.markdown("""
<style>
header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer{visibility:hidden}
[data-testid="stSidebar"]{background:#0f0f12;border-right:1px solid #2a2a35}
.sidebar-logo{font-size:28px;font-weight:800;background:linear-gradient(90deg,#ff6a00,#ee0979);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sidebar-card{background:#21212a;padding:12px;border-radius:12px;border:1px solid #2f2f3d;margin:10px 0}
@media(max-width:768px){.mobile-top-bar{position:fixed;top:0;left:0;right:0;height:56px;background:rgba(15,15,18,0.92);display:flex;align-items:center;padding-left:52px;z-index:999}.mobile-logo{font-weight:800;font-size:18px;background:linear-gradient(90deg,#ff6a00,#ee0979);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.block-container{padding-top:70px!important}div[data-testid="stHorizontalBlock"]{gap:8px!important}[data-testid="stColumn"]{width:calc(50% - 4px)!important;flex:1 1 calc(50% - 4px)!important;min-width:calc(50% - 4px)!important}}
@media(min-width:769px){.mobile-top-bar{display:none}}
div[data-testid="stButton"]>button{font-size:12.5px!important;border-radius:12px!important;background:#1e1e26!important;border:1px solid #2a2a35!important;color:#ccc!important;height:42px!important}
</style>
<div class="mobile-top-bar"><div class="mobile-logo">🔥 Aditya AI</div></div>
""", unsafe_allow_html=True)

try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("Add GROQ_API_KEY in Secrets")
    st.stop()

client = Groq(api_key=GROQ_KEY)

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[st.session_state.current_chat_id] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "img_b64" not in st.session_state:
    st.session_state.img_b64 = None

def new_chat():
    if st.session_state.messages:
        t = st.session_state.messages[0]["content"][:30]
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = t
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    nid = str(uuid.uuid4())
    st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
    st.session_state.messages = []
    st.session_state.img_b64 = None

def load_chat(cid):
    st.session_state.current_chat_id = cid
    st.session_state.messages = st.session_state.all_chats[cid]["messages"]

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI")
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()
    st.markdown('<div class="sidebar-card">📍 Belpahar, Odisha ● LIVE</div>', unsafe_allow_html=True)
    st.markdown("**💬 History**")
    for cid, chat in reversed(list(st.session_state.all_chats.items())):
        if cid == st.session_state.current_chat_id:
            continue
        if not chat["messages"]:
            continue
        if st.button("📝 " + chat["title"], key=cid, use_container_width=True):
            load_chat(cid)
            st.rerun()
    st.markdown("---")
    st.caption("Made with love in Belpahar")

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### 👋 Hi! I'm Aditya AI")
        st.caption("Built by Aditya from Belpahar")
        st.markdown("**🚀 Choose mode**")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🎓 Student", use_container_width=True, key="a1"):
                st.session_state.pending_prompt = "I am a Student, be my study buddy"
                st.rerun()
        with c2:
            if st.button("💻 Developer", use_container_width=True, key="a2"):
                st.session_state.pending_prompt = "I am a Developer, be my coding partner"
                st.rerun()
        with c3:
            if st.button("💭 Dreamer", use_container_width=True, key="a3"):
                st.session_state.pending_prompt = "I am a Dreamer, motivate me"
                st.rerun()
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.markdown("#### 📷 Send Image")
img = st.file_uploader("Upload", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
if img:
    b64 = base64.b64encode(img.getvalue()).decode('utf-8')
    st.session_state.img_b64 = b64
    st.image(img, width=250)
    st.success("Image ready! Ask below")

st.markdown("#### 🎙️ Voice")
aud = st.audio_input("Record")
txt_voice = None
if aud:
    try:
        t = client.audio.transcriptions.create(file=("audio.wav", aud.getvalue(), "audio/wav"), model="whisper-large-v3", response_format="text

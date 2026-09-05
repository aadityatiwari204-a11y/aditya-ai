import streamlit as st
from groq import Groq
import uuid
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- 2. PREMIUM CSS - EXACT LIKE YOUR SCREENSHOT ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
.stApp { background: #09090d; font-family: 'Inter', sans-serif; }
.block-container { max-width: 820px; padding-top: 1.2rem; padding-bottom: 2rem; }
[data-testid="stSidebar"] { background: #0f0f12; border-right: 1px solid #1f1f25; }
.hero-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 28px; padding: 40px 24px; text-align: center; margin: 14px 0 24px 0;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.hero-icon {
    width: 86px; height: 86px; margin: 0 auto 16px;
    background: radial-gradient(120% 120% at 30% 20%, #ff8a3d 0%, #ff3d6e 55%, #8b5cf6 100%);
    border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 44px;
    box-shadow: 0 10px 30px rgba(255,106,61,0.3);
}
.hero-title { font-size: 36px; font-weight: 850; letter-spacing: -0.8px; color: white; }
.hero-title span { background: linear-gradient(90deg,#ffb86a,#ff6eb6,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.ready-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.22);
    color: #7CFFB2; padding: 6px 14px; border-radius: 999px; font-size: 13px; font-weight: 700; margin: 14px 0;
}
.ready-dot { width: 8px; height: 8px; background: #00ff88; border-radius: 50%; box-shadow: 0 0 12px #00ff88; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
.hero-desc { color: #9a9aa8; font-size: 15px; line-height: 1.7; }
.try-label { font-weight: 750; font-size: 15px; margin: 22px 0 14px 0; color: #e5e5ea; }
div[data-testid="stButton"] > button {
    background: #1a1a22!important; border: 1px solid #2a2a35!important;
    color: #d8d8df!important; border-radius: 16px!important; height: 54px!important; font-weight: 600!important;
    transition: all 0.2s ease!important;
}
div[data-testid="stButton"] > button:hover { border-color: #ff6a00!important; color: white!important; background: #23232f!important; transform: translateY(-1px); }
.feature-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 16px; height: 92px; }
.blog-card { background: linear-gradient(135deg, #1e1e26, #252530); border: 1px solid #333340; border-radius: 14px; padding: 14px; margin: 12px 0; }
.stChatMessage { background: transparent; }
</style>
""", unsafe_allow_html=True)

# --- 3. GROQ CLIENT - CACHED ---
@st.cache_resource
def get_client():
    try:
        key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("❌ Add GROQ_API_KEY in Streamlit Secrets"); st.stop()
    return Groq(api_key=key)
client = get_client()

# --- 4. SESSION - ANTI-REPEAT SAFE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    nid = str(uuid.uuid4()); st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
if "pending_prompt" not in st.session_state: st.session_state.pending_prompt = None
if "last_audio_id" not in st.session_state: st.session_state.last_audio_id = None
if "last_user_text" not in st.session_state: st.session_state.last_user_text = ""

def create_new_chat():
    cid = st.session_state.current_chat_id
    if cid in st.session_state.all_chats and st.session_state.messages:
        st.session_state.all_chats[cid]["messages"] = list(st.session_state.messages)
        st.session_state.all_chats[cid]["title"] = st.session_state.messages[0]["content"][:32]
    nid = str(uuid.uuid4()); st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {"title":"New Chat","messages":[],"time":datetime.now().strftime("%d %b")}
    st.session_state.messages = []; st.session_state.last_user_text = ""
    st.rerun()

# --- 5. SIDEBAR WITH BLOG ---
with st.sidebar:
    st.markdown("## 🔥 Aditya AI")
    st.caption("A fast, multimodal AI assistant")
    st.markdown("")
    if st.button("🆕 NEW CHAT", use_container_width=True, type="primary"): create_new_chat()

    st.markdown(f"""
    <div class="blog-card">
        <div style="display:flex;align-items:center;gap:8px;">
            <div style="font-size:22px;">📝</div>
            <div>
                <a href="https://aditya-ai-belpahar.blogspot.com" target="_blank" style="color:#ff8a3d;text-decoration:none;font-weight:800;font-size:14px;">Blog & Updates</a>
                <div style="font-size:11px;color:#888;margin-top:1px;">Tutorials, prompts, news</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**💬 Recent Chats**")
    if not any(c.get("messages") for c in st.session_state.all_chats.values()):
        st.caption("No chats yet")
    else:
        for cid, chat in reversed(list(st.session_state.all_chats.items())):
            if not chat.get("messages"): continue
            if cid == st.session_state.current_chat_id: continue
            t = chat.get("title","New Chat")[:30]
            if st.button(f"💭 {t}", key=f"hist_{cid}", use_container_width=True):
                st.session_state.current_chat_id = cid
                st.session_state.messages = list(chat.get("messages",[]))
                st.rerun()

# --- 6. MAIN HEADER ---
st.markdown("## 🔥 Aditya AI")
st.caption("A fast, multimodal AI assistant • Built by Aditya, Belpahar")

# --- 7. HERO SECTION - ONLY WHEN NO CHAT ---
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-icon">🔥</div>
        <div class="hero-title">Hi! I'm <span>Aditya AI</span></div>
        <div class="ready-pill"><div class="ready-dot"></div> Ready to help • Online</div>
        <div class="hero-desc">Ask questions, write code, analyze images, search the web,<br>calculate, or talk by voice. I remember your chats.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="try-label">🚀 Try something</div>', unsafe_allow_html=True)
    if st.button("💡 What can you do? Explain your features", use_container_width=True, key="b1"):
        st.session_state.pending_prompt = "What can you do? Explain your features in detail"; st.rerun()
    if st.button("💻 Help me with Python - give a beginner example", use_container_width=True, key="b2"):
        st.session_state.pending_prompt = "Help me with Python with a simple beginner example"; st.rerun()
    if st.button("🌐 What's happening today? Latest news", use_container_width=True, key="b3"):
        st.session_state.pending_prompt = "What's happening today? Give me latest news headlines"; st.rerun()
    if st.button("🧪 Explain a cool physics concept simply", use_container_width=True, key="b4"):
        st.session_state.pending_prompt = "Explain an interesting physics concept in simple words"; st.rerun()

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown('<div class="feature-card"><div style="font-size:22px;">🌐</div><div style="font-weight:700;margin:6px 0 2px;">Web-Aware</div><div style="font-size:12px;color:#888;">Gets current info from web</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="feature-card"><div style="font-size:22px;">⚡</div><div style="font-weight:700;margin:6px 0 2px;">Super Fast</div><div style="font

import streamlit as st
from groq import Groq
import io
import uuid
import time
from datetime import datetime

# ============================================================
# OPTIONAL TTS IMPORT
# ============================================================
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

# ============================================================
# PAGE CONFIG - MUST BE FIRST
# ============================================================
st.set_page_config(
    page_title="Aditya AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SAFE SECRET LOADER - PREVENTS BLANK SCREEN - FIXED BEFORE
# ============================================================
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    if not GROQ_KEY:
        st.error("GROQ_API_KEY is empty in Secrets")
        st.stop()
except Exception as e:
    st.error("⚠️ GROQ_API_KEY not found! Go to Streamlit Dashboard > Settings > Secrets")
    st.code('GROQ_API_KEY = "gsk_xxx"')
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ============================================================
# ULTRA PREMIUM BIG CSS - EXPANDED PREMIUM LOOK
# ONLY SINGLE TRIPLE QUOTE USED - NO DOUBLE TRIPLE QUOTE
# ============================================================
BIG_CSS = '''
<style>
    /* Global */
    header[data-testid="stHeader"]{background:transparent!important;}
    #MainMenu,footer{visibility:hidden;}

    /* Sidebar Premium */
    [data-testid="stSidebar"]{
        background: linear-gradient(180deg, #0f0f12 0%, #14141a 30%, #1a1a22 100%);
        border-right: 1px solid #2a2a35;
    }

 .sidebar-logo{
        font-size:30px;
        font-weight:900;
        letter-spacing:0.6px;
        background: linear-gradient(90deg, #ff6a00, #ee0979, #ff6a00);
        background-size:300% 300%;
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        animation: gradientMove 4s ease infinite;
        margin-bottom:6px;
        filter: drop-shadow(0 2px 8px rgba(255,106,0,0.25));
    }

    @keyframes gradientMove{
        0%{background-position:0% 50%;}
        50%{background-position:100% 50%;}
        100%{background-position:0% 50%;}
    }

 .sidebar-card{
        background: linear-gradient(135deg, #21212a 0%, #252530 100%);
        padding:13px 15px;
        border-radius:14px;
        border:1px solid #2f2f3d;
        margin:11px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.05);
    }

    /* Mobile top bar like ChatGPT */
    @media (max-width: 768px){
     .mobile-top-bar{
            position:fixed;
            top:0;left:0;right:0;
            height:58px;
            background: rgba(15,15,18,0.92);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom:1px solid #2a2a35;
            display:flex;
            align-items:center;
            padding-left:54px;
            z-index:999;
        }
     .mobile-logo{
            font-weight:900;
            font-size:19px;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        }
     .block-container{padding-top:76px!important;}
        div[data-testid="stHorizontalBlock"]{gap:9px!important;}
        [data-testid="stColumn"]{
            width: calc(50% - 4.5px)!important;
            flex:1 1 calc(50% - 4.5px)!important;
            min-width: calc(50% - 4.5px)!important;
        }
    }
    @media (min-width: 769px){.mobile-top-bar{display:none;}}

    /* Suggestion buttons premium */
    div[data-testid="stButton"] > button{
        font-size:13px!important;
        font-weight:500!important;
        padding:0 12px!important;
        border-radius:14px!important;
        background: linear-gradient(135deg, #1e1e26 0%, #23232e 100%)!important;
        border:1px solid #2a2a35!important;
        color:#cccccc!important;
        height:44px!important;
        min-height:44px!important;
        transition: all 0.22s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    }
    div[data-testid="stButton"] > button:hover{
        background: linear-gradient(135deg, #2a2a38 0%, #323240 100%)!important;
        border-color:#ff6a00!important;
        color:white!important;
        transform: translateY(-1.5px);
        box-shadow: 0 6px 16px rgba(255,106,0,0.22);
    }

    /* Chat animation */
    [data-testid="stChatMessage"]{animation: slideUp 0.38s ease-out;}
    @keyframes slideUp{
        from{opacity:0;transform:translateY(14px);}
        to{opacity:1;transform:translateY(0);}
    }

    [data-testid="stChatInput"]:focus-within{
        border-color:#ff6a00!important;
        box-shadow:0 0 0 3px #ff6a0033!important;
    }

    /* Thinking bubble premium */
 .thinking-wrap{
        display:flex;
        align-items:center;
        gap:13px;
        background: linear-gradient(135deg, #1c1c24 0%, #242430 100%);
        border:1px solid #2a2a35;
        padding:15px 20px;
        border-radius:18px;
        width:fit-content;
        box-shadow: 0 6px 20px rgba(0,0,0,0.28);
    }
 .thinking-avatar{
        width:34px;height:34px;
        border-radius:50%;
        background: linear-gradient(135deg, #ff6a00, #ee0979);
        display:flex;align-items:center;justify-content:center;
        animation: pulseGlow 2s infinite;
        font-size:17px;
    }
 .dots{display:flex;gap:5px;margin-top:5px;}
 .dot{width:6.5px;height:6.5px;border-radius:50%;background:#ff6a00;animation:bounceDot 1.4s infinite;}
 .dot:nth-child(2){animation-delay:0.2s;background:#ff8a33;}
 .dot:nth-child(3){animation-delay:0.4s;background:#ee0979;}
    @keyframes bounceDot{
        0%,80%,100%{transform:translateY(0);opacity:0.5;}
        40%{transform:translateY(-6px);opacity:1;}
    }
    @keyframes pulseGlow{
        0%{box-shadow:0 0 0 0 rgba(255,106,0,0.45);}
        70%{box-shadow:0 0 0 12px rgba(255,106,0,0);}
        100%{box-shadow:0 0 0 0 rgba(255,106,0,0);}
    }
 .shimmer-text{
        background: linear-gradient(90deg, #888 0%, #fff 50%, #888 100%);
        background-size:200% 100%;
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        animation: shimmer 1.6s infinite linear;
        font-size:13.5px;font-weight:500;
    }
    @keyframes shimmer{
        0%{background-position:-200% 0;}
        100%{background-position:200% 0;}
    }
 .ready-dot{
        display:flex;align-items:center;gap:7px;
        font-size:11.5px;color:#00ff88;
        margin:7px 0 5px 2px;font-weight:600;
    }
 .ready-dot span{
        width:7px;height:7px;background:#00ff88;
        border-radius:50%;display:inline-block;
        box-shadow:0 0 9px #00ff88;
    }
 .voice-sub{font-size:12.5px;color:#888;margin-bottom:10px;}
 .premium-badge{
        display:inline-block;
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        color:white;
        font-size:10px;
        font-weight:700;
        padding:3px 8px;
        border-radius:20px;
        letter-spacing:0.5px;
    }
</style>
<div class="mobile-top-bar"><div class="mobile-logo">🔥 Aditya AI</div></div>
'''

st.markdown(BIG_CSS, unsafe_allow_html=True)

# ============================================================
# SESSION STATE - HISTORY KEPT EXACTLY AS FIXED BEFORE
# ============================================================
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[st.session_state.current_chat_id] = {
        "title": "New Chat",
        "messages": [],
        "time": datetime.now().strftime("%d %b")
    }
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ============================================================
# CHAT FUNCTIONS - KEPT SAME AS CORRECTED
# ============================================================
def new_chat():
    if st.session_state.messages:
        title = st.session_state.messages[0]["content"][:35]
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = title
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    nid = str(uuid.uuid4())
    st.session_state.current_chat_id = nid
    st.session_state.all_chats[nid] = {
        "title": "New Chat",
        "messages": [],
        "time": datetime.now().strftime("%d %b")
    }
    st.session_state.messages = []

def load_chat(cid):
    st.session_state.current_chat_id = cid
    st.session_state.messages = st.session_state.all_chats[cid]["messages"]

# ============================================================
# SIDEBAR - PREMIUM BIG
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔥 Aditya AI</div>', unsafe_allow_html=True)
    st.markdown('<span class="premium-badge">PREMIUM • v4.8</span>', unsafe_allow_html=True)
    st.caption("Next-Gen Voice AI • Built in Belpahar, Odisha")

    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()

    st.markdown('<div class="sidebar-card" style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:13.5px">📍 Belpahar, Odisha</span><span style="font-size:10px;background:#00ff8820;color:#00ff88;padding:5px 10px;border-radius:20px;">● LIVE</span></div>', unsafe_allow_html=True)

    st.markdown("**💬 History**")

    all_items = list(st.session_state.all_chats.items())
    for cid, chat in reversed(all_items):
        if cid == st.session_state.current_chat_id:
            continue
        if not chat["messages"]:
            continue
        short = chat["title"][:30]
        if st.button(f'📝 {short}', key=cid, use_container_width=True):
            load_chat(cid)
            st.rerun()

    st.markdown("---")

    st.markdown('<div class="sidebar-card" style="font-size:12.5px;color:#999;text

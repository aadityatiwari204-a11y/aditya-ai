import streamlit as st
from groq import Groq
import io
import uuid
import time
from datetime import datetime

try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide", initial_sidebar_state="expanded")

try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    if not GROQ_KEY:
        st.error("GROQ_API_KEY empty")
        st.stop()
except Exception:
    st.error("⚠️ Add GROQ_API_KEY in Secrets")
    st.code('GROQ_API_KEY = "gsk_xxx"')
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ============================================================
# CSS BUILT WITH NO TRIPLE QUOTES - BULLETPROOF
# ============================================================
css_lines = []
css_lines.append("<style>")
css_lines.append('header[data-testid="stHeader"]{background:transparent!important;}')
css_lines.append("#MainMenu,footer{visibility:hidden;}")
css_lines.append('[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f12 0%,#1a1a22 100%);border-right:1px solid #2a2a35;}')
css_lines.append('.sidebar-logo{font-size:30px;font-weight:900;letter-spacing:0.6px;background:linear-gradient(90deg,#ff6a00,#ee0979,#ff6a00);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:gradientMove 4s ease infinite;margin-bottom:6px;}')
css_lines.append("@keyframes gradientMove{0%{background-position:0% 50%;}50%{background-position:100% 50%;}100%{background-position:0% 50%;}}")
css_lines.append('.sidebar-card{background:linear-gradient(135deg,#21212a 0%,#252530 100%);padding:13px 15px;border-radius:14px;border:1px solid #2f2f3d;margin:11px 0;box-shadow:0 4px 16px rgba(0,0,0,0.25);}')
css_lines.append("@media (max-width:768px){.mobile-top-bar{position:fixed;top:0;left:0;right:0;height:58px;background:rgba(15,15,18,0.92);backdrop-filter:blur(14px);border-bottom:1px solid #2a2a35;display:flex;align-items:center;padding-left:54px;z-index:999;}.mobile-logo{font-weight:900;font-size:19px;background:linear-gradient(90deg,#ff6a00,#ee0979);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}.block-container{padding-top:76px!important;}div[data-testid='stHorizontalBlock']{gap:9px!important;}[data-testid='stColumn']{width:calc(50% - 4.5px)!important;flex:1 1 calc(50% - 4.5px)!important;min-width:calc(50% - 4.5px)!important;}}")
css_lines.append("@media (min-width:769px){.mobile-top-bar{display:none;}}")
css_lines.append("div[data-testid='stButton'] > button{font-size:13px!important;font-weight:500!important;padding:0 12px!important;border-radius:14px!important;background:linear-gradient(135deg,#1e1e26 0%,#23232e 100%)!important;border:1px solid #2a2a35!important;color:#ccc!important;height:44px!important;min-height:44px!important;transition:all 0.22s ease;}")
css_lines.append("div[data-testid='stButton'] > button:hover{background:linear-gradient(135deg,#2a2a38 0%,#323240 100%)!important;border-color:#ff6a00!important;color:white!important;transform:translateY(-1.5px);box-shadow:0 6px 16px rgba(255,106,0,0.22);}")
css_lines.append('[data-testid="stChatMessage"]{animation:slideUp 0.38s ease-out;}')
css_lines.append("@keyframes slideUp{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}")
css_lines.append('[data-testid="stChatInput"]:focus-within{border-color:#ff6a00!important;box-shadow:0 0 0 3px #ff6a0033!important;}')
css_lines.append('.thinking-wrap{display:flex;align-items:center;gap:13px;background:linear-gradient(135deg,#1c1c24 0%,#242430 100%);border:1px solid #2a2a35;padding:15px 20px;border-radius:18px;width:fit-content;}')
css_lines.append('.thinking-avatar{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#ff6a00,#ee0979);display:flex;align-items:center;justify-content:center;animation:pulseGlow 2s infinite;}')
css_lines.append('.dots{display:flex;gap:5px;margin-top:5px;}')
css_lines.append('.dot{width:6.5px;height:6.5px;border-radius:50%;background:#ff6a00;animation:bounceDot 1.4s infinite;}')
css_lines.append('.dot:nth-child(2){animation-delay:0.2s;background:#ff8a33;}')
css_lines.append('.dot:nth-child(3){animation-delay:0.4s;background:#ee0979;}')
css_lines.append('@keyframes bounceDot{0%,80%,100%{transform:translateY(0);opacity:0.5;}40%{transform:translateY(-6px);opacity:1;}}')
css_lines.append('@keyframes pulseGlow{0%{box-shadow:0 0 0 0 rgba(255,106,0,0.45);}70%{box-shadow:0 0 0 12px rgba(255,106,0,0);}100%{box-shadow:0 0 0 0 rgba(255,106,0,0);}}')
css_lines.append('.shimmer-text{background:linear-gradient(90deg,#888 0%,#fff 50%,#888 100%);background-size:200% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 1.6s infinite linear;font-size:13.5px;}')
css_lines.append('@keyframes shimmer{0%{background-position:-200% 0;}100%{background-position:200% 0;}}')
css_lines.append('.ready-dot{display:flex;align-items:center;gap:7px;font-size:11.5px;color:#00ff88;margin:7px 0 5px 2px;font-weight:600;}')
css_lines.append('.ready-dot span{width:7px;height:7px;background:#00ff88;border-radius:50%;display:inline-block;box-shadow:0 0 9px #00ff88;}')
css_lines.append

import streamlit as st
from groq import Groq
import io
import uuid
import time
from datetime import datetime

# ============================================================
# OPTIONAL TTS
# ============================================================
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Aditya AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SAFE KEY LOADER - NO BLANK SCREEN
# ============================================================
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    if not GROQ_KEY:
        st.error("GROQ_API_KEY empty")
        st.stop()
except Exception:
    st.error("⚠️ Add GROQ_API_KEY in Streamlit Secrets")
    st.code('GROQ_API_KEY = "gsk_xxx"')
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ============================================================
# BIG PREMIUM CSS - 100% TRIPLE SINGLE QUOTE ONLY
# ============================================================
BIG_CSS = '''
<style>
    header[data-testid="stHeader"]{background:transparent!important;}
    #MainMenu,footer{visibility:hidden;}
    [data-testid="stSidebar"]{
        background: linear-gradient(180deg, #0f0f12 0%, #1a1a22 100%);
        border-right:1px solid #2a2a35;
    }
  .sidebar-logo{
        font-size:30px;font-weight:900;
        background: linear-gradient(90deg, #ff6a00, #ee0979, #ff6a00);
        background-size:300% 300%;
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        animation: gradientMove 4s ease infinite;
    }
    @keyframes gradientMove{
        0%{background-position:0% 50%;}
        50%{background-position:100% 50%;}
        100%{background-position:0% 50%;}
    }
  .sidebar-card{
        background: linear-gradient(135deg, #21212a 0%, #252530 100%);
        padding:13px 15px;border-radius:14px;
        border:1px solid #2f2f3d;margin:11px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    @media (max-width:768px){
     .mobile-top-bar{
            position:fixed;top:0;left:0;right:0;height:58px;
            background: rgba(15,15,18,0.92);
            backdrop-filter: blur(14px);
            border-bottom:1px solid #2a2a35;
            display:flex;align-items:center;padding-left:54px;z-index:999;
        }
     .mobile-logo{
            font-weight:900;font-size:19px;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        }
     .block-container{padding-top:76px!important;}
        div[data-testid="stHorizontalBlock"]{gap:9px!important;}
        [data-testid="stColumn"]{
            width: calc(50% - 4.5px)!important;
            flex:1 1 calc(50% - 4.5px)!important;
            min-width: calc(50% - 4.5px)!important;
        }
    }
    @media (min-width:769px){.mobile-top-bar{display:none;}}
    div[data-testid="stButton"] > button{
        font-size:13px!important;font-weight:500!important;
        padding:0 12px!important;border-radius:14px!important;
        background: linear-gradient(135deg, #1e1e26 0%, #23232e 100%)!important;
        border:1px solid #2a2a35!important;color:#ccc!important;
        height:44px!important;min-height:44px!important;
        transition: all 0.22s ease;
    }
    div[data-testid="stButton"] > button:hover{
        background: linear-gradient(135deg, #2a2a38 0%, #323240 100%)!important;
        border-color:#ff6a00!important;color:white!important;
        transform: translateY(-1.5px);
        box-shadow: 0 6px 16px rgba(255,106,0,0.22);
    }
    

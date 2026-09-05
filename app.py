import streamlit as st
from groq import Groq
import io
import uuid
import base64
from datetime import datetime

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

# --- KEEP ALL YOUR PREMIUM CSS ---
st.markdown('''
<style>
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f12 0%, #1a1a22 100%);
        border-right: 1px solid #2a2a35;
    }
   .sidebar-logo {
        font-size: 28px; font-weight: 800;
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        background-size: 200% 200%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: gradientMove 4s ease infinite;
    }
    @keyframes gradientMove {
        0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}
    }
   .sidebar-card {
        background: #21212a; padding: 12px; border-radius: 12px;
        border: 1px solid #2f2f3d; margin: 10px 0;
    }
    .chat-history-item {
        padding: 8px 10px; border-radius: 8px; font-size: 13px;
        color: #bbb; cursor: pointer; margin: 3px 0;
    }
    .chat-history-item:hover { background: #2a2a38; color: white; }
    @media (max-width: 768px) {
       .mobile-top-bar {
            position: fixed; top: 0; left: 0; right: 0; height: 56px;
            background: rgba(15,15,18,0.92); backdrop-filter: blur(12px);
            border-bottom: 1px solid #2a2a35;
            display: flex; align-items: center; padding-left: 52px; z-index: 999;
        }
       .mobile-logo {
            font-weight: 800; font-size: 18px;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
       .block-container { padding-top: 70px!important; }
    }
   

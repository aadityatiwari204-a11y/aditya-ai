import streamlit as st
from groq import Groq
import io
import uuid
from datetime import datetime
import time

try:
    from gtts import gTTS
    TTS = True
except:
    TTS = False

st.set_page_config(page_title="Aditya AI", page_icon="🔥", layout="wide")

st.markdown("""
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
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }
    .sidebar-card {
        background: #21212a; padding: 12px; border-radius: 12px;
        border: 1px solid #2f2f3d; margin: 10px 0;
    }
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
        div[data-testid="stHorizontalBlock"] { gap: 8px!important; }
        [data-testid="stColumn"] {
            width: calc(50% - 4px)!important;
            flex: 1 1 calc(50% - 4px)!important;
            min-width: calc(50% - 4px)!important;
        }
    }
    @media (min-width: 769px) {.mobile-top-bar { display: none; } }
    div[data-testid="stButton"] > button {
        font-size: 12.5px!important; padding: 0 10px!important;
        border-radius: 12px!important; background: #1e1e26!important;
        border: 1px solid #2a2a35!important; color: #ccc!important;
        height: 42px!important; min-height: 42px!important; transition: all 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        background: #2a2a38!important; border-color: #ff6a00!important;
        color: white!important; transform: translateY(-1px);
    }
    [data-testid="stChatMessage"] { animation: slideUp 0.3s ease-out; }
    @keyframes slideUp { from { opacity:0; transform: translateY(10px);} to { opacity:1; transform: translateY(0);} }
    [data-testid="stChatInput"]:focus-within {
        border-color: #ff6a00!important; box-shadow: 0 0 0 3px #ff6a0030!important;
    }
    .thinking-wrap {
        display: flex; align-items: center; gap: 12px;
        background: #1c1c24; border: 1px solid #2a2a35;
        padding: 14px 18px; border-radius: 16px; width: fit-content;
    }
    .thinking-avatar {
        width: 32px; height: 32px; border-radius: 50%;
        background: linear-gradient(135deg, #ff6a00, #ee0979);
        display: flex; align-items: center; justify-content: center;
        animation: pulseGlow 2s infinite;
    }
    .dots { display: flex; gap: 4px; }
    .dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #ff6a00; animation: bounceDot 1.4s infinite;
    }
    .dot:nth-child(2) { animation-delay: 0.2s; background: #ff8a33; }
    .dot:nth-child(3) { animation-delay: 0.4s; background: #ee0979; }
    @keyframes bounceDot { 0%, 80%, 100% { transform: translateY(0); opacity: 0.5; } 40% { transform: translateY(-6px); opacity: 1; } }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(255,106,0,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255,106,0,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,106,0,0); }
    }
    .shimmer-text {
        background: linear-gradient(90deg, #888 0%, #fff 50%, #888 100%);
        background-size: 200% 100%; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 1.5s infinite linear; font-size: 13px;
    }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
    .ready-dot {
        display: flex; align-items: center; gap: 6px

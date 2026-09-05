import base64
import hashlib
import io
import json
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

import streamlit as st
from groq import Groq

# ============================================================
# OPTIONAL TTS
# ============================================================
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# ============================================================
# PAGE CONFIG - MUST BE FIRST
# ============================================================
st.set_page_config(
    page_title="Aditya AI - Fast Multimodal Assistant",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Aditya AI by Aditya from Belpahar, Odisha - Built with Groq"
    }
)

# ============================================================
# CONSTANTS AND MODELS
# ============================================================
TEXT_MODEL = "groq/compound"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
WHISPER_MODEL = "whisper-large-v3"
MAX_IMAGE_BYTES = 4 * 1024 * 1024
MAX_TOKENS = 4096
TEMPERATURE = 0.7
APP_VERSION = "2.0.0"
CREATOR = "Aditya"
LOCATION = "Belpahar, Odisha"

# ============================================================
# SYSTEM PROMPTS
# ============================================================
SYSTEM_PROMPT = """
You are Aditya AI, a helpful multimodal AI assistant created by Aditya from Belpahar, Odisha.
You are not ChatGPT and must not claim to be ChatGPT. You are Aditya AI.

Guidelines:
- Be accurate, friendly, clear, and practical.
- Answer in the user's language when practical (English, Hindi, Odia).
- For current news, recent events, current prices, current facts, weather, or other time-sensitive questions, use your available web-search capability.
- For calculations and technical tasks, use available tools when they improve accuracy.
- Do not invent sources, facts, or capabilities.
- Format code with markdown code blocks.
- Use emojis sparingly but effectively.
- Be concise unless user asks for detailed explanation.
""".strip()

VISION_SYSTEM_PROMPT = """
You are Aditya AI, a helpful multimodal assistant created by Aditya.
You are not ChatGPT. You can see images.
Analyze the provided image carefully, describe what you see, and answer the user's question.
If something is unclear or not visible, say so honestly.
Be helpful and detailed about the image content.
""".strip()

# ============================================================
# ADVANCED STYLING - 150+ LINES
# ============================================================
st.markdown(
    """
<style>
/* Root variables */
:root {
    --bg: #09090d;
    --bg2: #101017;
    --panel: rgba(255,255,255,0.055);
    --panel-strong: rgba(255,255,255,0.085);
    --panel-hover: rgba(255,255,255,0.075);
    --border: rgba(255,255,255,0.10);
    --border-strong: rgba(255,255,255,0.15);
    --muted: #9b9ba8;
    --muted2: #6f6f7c;
    --text: #f6f6f8;
    --text2: #d9d9e2;
    --accent1: #ff7a18;
    --accent2: #ff2d8d;
    --accent3: #7c5cff;
    --success: #65e890;
    --success-bg: rgba(50, 210, 100, 0.10);
    --warning: #ffb86a;
    --error: #ff5a65;
}

/* App background */
.stApp {
    background:
        radial-gradient(circle at 15% 5%, rgba(255, 122, 24, .14), transparent 32%),
        radial-gradient(circle at 90% 10%, rgba(255, 45, 141, .12), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(124, 92, 255, .08), transparent 40%),
        var(--bg);
    color: var(--text);
}

/* Container */
.block-container {
    max-width: 1220px;
    padding-top: 1.2rem;
    padding-bottom: 5rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(12, 12, 18, .98);
    border-right: 1px solid var(--border);
    backdrop-filter: blur(20px);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Brand */
.brand {
    font-size: 1.65rem;
    font-weight: 900;
    letter-spacing: -.03em;
    background: linear-gradient(90deg, var(--accent1), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.brand-sub {
    color: var(--muted);
    font-size: .78rem;
    margin-top: -2px;
    letter-spacing: .02em;
}
.brand-version {
    color: var(--muted2);
    font-size: .68rem;
    margin-top: 2px;
}

/* Cards */
.sidebar-card,
.hero-card,
.feature-card,
.status-card,
.metric-card,
.chat-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 14px 45px rgba(0,0,0,.18);
    backdrop-filter: blur(12px);
    transition: all .2s ease;
}
.sidebar-card:hover,
.feature-card:hover {
    background: var(--panel-hover);
    border-color: var(--border-strong);
    transform: translateY(-1px);
}
.sidebar-card { padding: 16px; margin: 14px 0; }
.hero-card { text-align: center; padding: 48px 28px 36px; margin: 12px auto 28px; max-width: 860px; }
.feature-card { padding: 18px; height: 100%; min-height: 110px; }

/* Status */
.status-row {
    display: flex;
    justify-content:

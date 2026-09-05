import streamlit as st
from groq import Groq
import io
import uuid
import base64
import hashlib
from datetime import datetime

# Optional text-to-speech
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
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM UI
# ============================================================

st.markdown("""
<style>

/* =========================
   GLOBAL
========================= */

:root {
    --bg: #0b0d12;
    --panel: #151821;
    --panel2: #1b1e28;
    --border: #292d39;
    --text: #f4f5f7;
    --muted: #8f95a3;
    --accent: #ff6a00;
    --accent2: #ee0979;
    --green: #00e887;
}

html, body, [class*="css"] {
    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(255,106,0,.10),
            transparent 34%
        ),
        radial-gradient(
            circle at 100% 20%,
            rgba(238,9,121,.06),
            transparent 30%
        ),
        var(--bg);

    color: var(--text);
}

header[data-testid="stHeader"] {
    background: rgba(11,13,18,.72);
    backdrop-filter: blur(14px);
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 7rem;
}


/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0d0f14 0%,
            #141720 100%
        );

    border-right: 1px solid var(--border);
}

.sidebar-brand {
    font-size: 27px;
    font-weight: 850;
    letter-spacing: -.7px;

    background:
        linear-gradient(
            90deg,
            #ff6a00,
            #ff3d3d,
            #ee0979
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-sub {
    color: var(--muted);
    font-size: 12px;
    margin-top: -4px;
    margin-bottom: 18px;
}

.status-card {
    padding: 12px 13px;

    border: 1px solid var(--border);

    background:
        rgba(255,255,255,.035);

    border-radius: 14px;

    margin:
        12px 0
        18px;
}

.status-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;

    font-size: 12px;
}

.live {
    color: var(--green);

    font-size: 10px;
    font-weight: 700;

    background:
        rgba(0,232,135,.08);

    padding:
        4px 8px;

    border-radius: 20px;
}

.history-title {
    color: #aeb3bf;

    font-size: 11px;
    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: .08em;

    margin:
        10px 0;
}

.sidebar-note {
    color: #747b89;

    font-size: 11px;

    text-align: center;

    line-height: 1.5;

    padding:
        10px 4px;
}


/* =========================
   TOP BAR
========================= */

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding:
        5px 2px
        18px;
}

.brand {
    display: flex;
    align-items: center;

    gap: 10px;
}

.brand-icon {
    width: 38px;
    height: 38px;

    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #ff6a00,
            #ee0979
        );

    box-shadow:
        0 8px 30px
        rgba(255,106,0,.18);

    font-size: 20px;
}

.brand-name {
    font-size: 19px;
    font-weight: 800;
}

.brand-status {
    color: #8d93a0;
    font-size: 11px;
}


/* =========================
   HERO
========================= */

.hero {
    text-align: center;

    padding:
        48px 10px
        28px;
}

.hero-icon {
    width: 70px;
    height: 70px;

    margin:
        0 auto
        18px;

    border-radius: 22px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #ff8a00,
            #ff3d3d,
            #ee0979
        );

    box-shadow:
        0 15px 50px
        rgba(255,106,0,.20);

    font-size: 34px;
}

.hero h1 {
    font-size:
        clamp(30px, 5vw, 48px);

    line-height: 1.05;

    margin: 0;

    letter-spacing: -1.5px;
}

.hero p {
    color: var(--muted);

    max-width: 620px;

    margin:
        13px auto 0;

    font-size: 14px;
}

.ready {
    display: inline-flex;

    align-items: center;

    gap: 7px;

    margin-top: 16px;

    padding:
        6px 11px;

    border:
        1px solid
        rgba(0,232,135,.18);

    border-radius: 999px;

    color: #00e887;

    background:
        rgba(0,232,135,.05);

    font-size: 11px;
}

.ready-dot {
    width: 6px;
    height: 6px;

    border-radius: 50%;

    background: #00e887;

    box-shadow:
        0 0 10px
        #00e887;
}


/* =========================
   BUTTONS
========================= */

div[data-testid="stButton"] > button {
    border-radius: 13px !important;

    border:
        1px solid
        var(--border) !important;

    background:
        #151821 !important;

    color:
        #d9dce3 !important;

    min-height:
        44px !important;

    transition:
        .18s ease !important;
}

div[data-testid="stButton"] > button:hover {
    border-color:
        #ff6a00 !important;

    background:
        #1b1e28 !important;

    transform:
        translateY(-1px);
}


/* =========================
   CHAT
========================= */

[data-testid="stChatMessage"] {
    border:
        1px solid
        rgba(255,255,255,.035);

    border-radius: 18px;

    margin:
        8px 0;

    padding:
        8px 14px;

    animation:
        slideUp .25s ease-out;
}

@keyframes slideUp {

    from {
        opacity: 0;
        transform:
            translateY(7px);
    }

    to {
        opacity: 1;
        transform:
            translateY(0);
    }
}


/* =========================
   CHAT INPUT
========================= */

[data-testid="stChatInput"] {
    background:
        #171a23 !important;

    border:
        1px solid
        #303442 !important;

    border-radius:
        18px !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color:
        #ff6a00 !important;

    box-shadow:
        0 0 0 3px
        rgba(255,106,0,.12) !important;
}


/* =========================
   TOOLS
========================= */

.tool-box {
    border:
        1px solid
        var(--border);

    background:
        rgba(255,255,255,.025);

    border-radius:
        16px;

    padding:
        13px 15px;

    margin:
        12px 0;
}

.tool-title {
    font-weight: 750;
    font-size: 13px;
}

.tool-sub {
    color: #7f8694;

    font-size: 11px;

    margin-top: 2px;
}


/* =========================
   THINKING ANIMATION
========================= */

.thinking {
    display: flex;

    align-items: center;

    gap: 12px;

    padding:
        12px 14px;

    width: max-content;

    max-width: 100%;

    background:
        #171a22;

    border:
        1px solid
        #2b2f3b;

    border-radius:
        16px;
}

.thinking-icon {
    width: 32px;
    height: 32px;

    border-radius:
        10px;

    display: flex;

    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #ff6a00,
            #ee0979
        );
}

.thinking-text {
    font-size: 12px;
    color: #9ba1ad;
}

.dots {
    display: flex;

    gap: 4px;

    margin-top: 5px;
}

.dot {
    width: 6px;
    height: 6px;

    border-radius: 50%;

    background:
        #ff6a00;

    animation:
        bounce 1.2s infinite;
}

.dot:nth-child(2) {
    animation-delay: .15s;
    background: #ff8a33;
}

.dot:nth-child(3) {
    animation-delay: .3s;
    background: #ee0979;
}

@keyframes bounce {

    0%, 80%, 100% {
        transform:
            translateY(0);

        opacity: .35;
    }

    40% {
        transform:
            translateY(-5px);

        opacity: 1;
    }
}


/* =========================
   FILE UPLOADER
========================= */

[data-testid="stFileUploader"] section {
    border-radius:
        14px !important;
}


/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

    .block-container {
        padding:
            1rem .75rem
            6.5rem !important;
    }

    .topbar {
        padding:
            2px
            2px
            12px;
    }

    .brand-name {
        font-size: 17px;
    }

    .brand-status {
        display: none;
    }

    .hero {
        padding:
            38px 4px
            20px;
    }

    .hero-icon {
        width: 58px;
        height: 58px;

        border-radius: 18px;

        font-size: 28px;
    }

    .hero p {
        font-size: 13px;
    }

    [data-testid="stChatMessage"] {
        border-radius: 15px;

        padding:
            6px 9px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GROQ
# ============================================================

if "GROQ_API_KEY" not in st.secrets:

    st.error(
        "⚠️ GROQ_API_KEY is missing. "
        "Add it to Streamlit Secrets."
    )

    st.stop()


client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],

    default_headers={
        "Groq-Model-Version": "latest"
    },
)


# ============================================================
# MODELS
# ============================================================

TEXT_MODEL = "groq/compound"

VISION_MODEL = (
    "meta-llama/"
    "llama-4-scout-17b-16e-instruct"
)

WHISPER_MODEL = "whisper-large-v3"


SYSTEM_PROMPT = """
You are Aditya AI, created by Aditya from Belpahar, Odisha.

You are an independent AI assistant.
Never claim that you are ChatGPT.

Be:
- helpful
- accurate
- friendly
- clear
- concise by default

Explain difficult topics in simple language when appropriate.

When a question needs current information,
use web search when available.

When calculations, data analysis, or Python
verification would improve the answer,
use code execution when available.

Never invent current facts.

If you are unsure, say so.

When using web information, provide useful
sources/citations when the system supplies them.
"""


# ============================================================
# SESSION STATE
# ============================================================

def initialize_state():

    defaults = {

        "all_chats": {},

        "current_chat_id": None,

        "messages": [],

        "pending_prompt": None,

        "pending_image": None,

        "last_audio_hash": None,

        "voice_transcript": None,

        "regenerate": False,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


    # Create first chat

    if not st.session_state.all_chats:

        chat_id = str(uuid.uuid4())

        st.session_state.current_chat_id = chat_id

        st.session_state.all_chats[chat_id] = {

            "title": "New Chat",

            "messages": [],

            "time":
                datetime.now()
                .strftime("%d %b %Y"),

        }


    elif st.session_state.current_chat_id is None:

        chat_id = next(
            reversed(
                st.session_state.all_chats
            )
        )

        st.session_state.current_chat_id = chat_id

        st.session_state.messages = (
            st.session_state
            .all_chats[chat_id]
            ["messages"]
        )


initialize_state()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def sync_chat():

    chat_id = (
        st.session_state
        .current_chat_id
    )

    if chat_id in st.session_state.all_chats:

        st.session_state.all_chats[
            chat_id
        ]["messages"] = (
            st.session_state.messages
        )


def new_chat():

    sync_chat()

    chat_id = str(uuid.uuid4())

    st.session_state.current_chat_id = chat_id

    st.session_state.all_chats[chat_id] = {

        "title": "New Chat",

        "messages": [],

        "time":
            datetime.now()
            .strftime("%d %b %Y"),

    }

    st.session_state.messages = []

    st.session_state.pending_image = None

    st.session_state.pending_prompt = None

    st.session_state.voice_transcript = None


def load_chat(chat_id):

    if chat_id not in st.session_state.all_chats:

        return

    st.session_state.current_chat_id = chat_id

    st.session_state.messages = (
        st.session_state
        .all_chats[chat_id]
        ["messages"]
    )

    st.session_state.pending_image = None

    st.session_state.pending_prompt = None

    st.session_state.voice_transcript = None


def make_title(text):

    text = " ".join(
        text.strip().split()
    )

    if len(text) > 42:

        return text[:42] + "…"

    return text


def message_text(message):

    content = message.get(
        "content",
        ""
    )

    if isinstance(content, str):

        return content


    if isinstance(content, list):

        texts = []

        for part in content:

            if (
                isinstance(part, dict)
                and
                part.get("type") == "text"
            ):

                texts.append(
                    part.get(
                        "text",
                        ""
                    )
                )

        return " ".join(texts).strip()


    return ""


def encode_image(uploaded_file):

    raw = uploaded_file.getvalue()

    encoded = (
        base64
        .b64encode(raw)
        .decode("utf-8")
    )

    mime = (
        uploaded_file.type
        or "image/jpeg"
    )

    return {

        "b64": encoded,

        "mime": mime,

        "name":
            uploaded_file.name,

    }


def transcribe_audio(audio_bytes):

    result = (
        client
        .audio
        .transcriptions
        .create(

            file=(
                "recording.wav",
                audio_bytes,
                "audio/wav"
            ),

            model=WHISPER_MODEL,

            response_format="json",

            temperature=0.0,

        )
    )

    return result.text.strip()


def text_to_speech(text):

    if not TTS_AVAILABLE:

        return None

    if not text:

        return None

    try:

        # Hindi if Devanagari is detected,
        # otherwise English.

        language = (
            "hi"
            if any(
                "\u0900" <= char <= "\u097F"
                for char in text
            )
            else "en"
        )

        audio_buffer = io.BytesIO()

        speech = gTTS(
            text=text[:700],
            lang=language
        )

        speech.write_to_fp(
            audio_buffer
        )

        audio_buffer.seek(0)

        return audio_buffer

    except Exception:

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">'
        '🔥 Aditya AI'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-sub">'
        'Fast • Multimodal • Web-enabled'
        '</div>',
        unsafe_allow_html=True
    )


    # NEW CHAT

    if st.button(
        "＋  New chat",
        use_container_width=True,
        type="primary"
    ):

        new_chat()

        st.rerun()


    # STATUS

    st.markdown(
        """
        <div class="status-card">

            <div class="status-row">

                <span>
                    📍 Belpahar, Odisha
                </span>

                <span class="live">
                    ● LIVE
                </span>

            </div>

            <div
                style="
                    color:#737987;
                    font-size:10px;
                    margin-top:7px;
                "
            >
                Web search • Code execution
                • Vision • Voice
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # HISTORY

    st.markdown(
        '<div class="history-title">'
        'Recent chats'
        '</div>',
        unsafe_allow_html=True
    )


    history = [

        (chat_id, chat)

        for chat_id, chat
        in st.session_state.all_chats.items()

        if chat.get("messages")

    ]


    if not history:

        st.caption(
            "Your conversations will appear here."
        )

    else:

        for chat_id, chat in reversed(history):

            title = (
                chat.get("title")
                or "New Chat"
            )

            if len(title) > 38:

                title = title[:38] + "…"


            if st.button(
                "🟠 " + title,
                key="history_" + chat_id,
                use_container_width=True
            ):

                load_chat(chat_id)

                st.rerun()


    st.markdown("---")


    st.markdown(
        '<div class="history-title">'
        'Features'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div style="
            color:#8a909d;
            font-size:11px;
            line-height:1.9;
        ">

        🔎 Live web search<br>
        💻 Code execution<br>
        🖼️ Image understanding<br>
        🎙️ Voice input<br>
        🔊 AI voice output<br>
        💬 Chat history

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    st.markdown(
        '<div class="sidebar-note">'
        'Made with ❤️ by Aditya<br>'
        'Aditya AI v4.0'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    """
    <div class="topbar">

        <div class="brand">

            <div class="brand-icon">
                🔥
            </div>

            <div>

                <div class="brand-name">
                    Aditya AI
                </div>

                <div class="brand-status">
                    Your personal AI assistant
                </div>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="hero">

            <div class="hero-icon">
                🤖
            </div>

            <h1>
                Hi! I'm Aditya AI
            </h1>

            <div class="ready">

                <span class="ready-dot"></span>

                Ready to help

            </div>

            <p>
                Ask questions, write code,
                analyze images, search the web,
                calculate, or talk by voice.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # QUICK PROMPTS

    c1, c2 = st.columns(
        2,
        gap="small"
    )


    with c1:

        if st.button(
            "💡  What can you do?",
            use_container_width=True,
            key="quick_1"
        ):

            st.session_state.pending_prompt = (
                "What

import base64
import hashlib
import io
from datetime import datetime

import streamlit as st
from groq import Groq

# Optional text-to-speech
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


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
# MODELS
# ============================================================

TEXT_MODEL = "groq/compound"
WHISPER_MODEL = "whisper-large-v3"

# We DON'T blindly use one vision model anymore.
# The app checks which of these are actually available
# to your Groq API key.
VISION_MODELS = [
    "qwen/qwen3.6-27b",
    "qwen/qwen3.8-27b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
]

MAX_IMAGE_BYTES = 20 * 1024 * 1024


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Aditya AI, a helpful multimodal AI assistant.

You are not ChatGPT and must not claim to be ChatGPT.

Be:
- accurate
- friendly
- clear
- practical
- concise when the question is simple
- detailed when the user asks for detail

Answer in the user's language when practical.

For current information, news, recent events, prices,
weather, live information, or anything time-sensitive,
use your available web-search tools.

For calculations and technical tasks, use available tools
when they improve accuracy.

For coding:
- provide working code
- explain important parts
- avoid unnecessary complexity
- do not invent libraries, APIs, or features

For images:
- carefully inspect the image
- describe only what you can actually determine
- say when something is unclear
- never pretend to see something that is not visible

Do not invent sources, facts, capabilities, or tool results.
""".strip()


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
<style>

:root {
    --bg: #09090d;
    --panel: rgba(255,255,255,0.055);
    --panel-strong: rgba(255,255,255,0.085);
    --border: rgba(255,255,255,0.10);
    --muted: #9b9ba8;
    --text: #f6f6f8;
    --accent1: #ff7a18;
    --accent2: #ff2d8d;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(255, 122, 24, .12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(255, 45, 141, .10),
            transparent 28%
        ),
        var(--bg);

    color: var(--text);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.25rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background: rgba(12, 12, 18, .96);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

.brand {
    font-size: 1.55rem;
    font-weight: 850;
    letter-spacing: -.03em;

    background:
        linear-gradient(
            90deg,
            var(--accent1),
            var(--accent2)
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-sub {
    color: var(--muted);
    font-size: .78rem;
    margin-top: -4px;
}

.sidebar-card,
.hero-card,
.feature-card,
.status-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 14px 45px rgba(0,0,0,.18);
}

.sidebar-card {
    padding: 15px;
    margin: 12px 0;
}

.status-row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    align-items: center;
    color: #dddde5;
    font-size: .86rem;
}

.live-pill {
    color: #8df3ad;
    background: rgba(50, 210, 100, .10);
    border: 1px solid rgba(50, 210, 100, .20);
    border-radius: 999px;
    padding: 3px 8px;
    font-size: .72rem;
    font-weight: 700;
}

.hero-card {
    text-align: center;
    padding: 42px 24px 32px;
    margin: 10px auto 24px;
    max-width: 850px;
}

.hero-icon {
    width: 76px;
    height: 76px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin: 0 auto 14px;

    border-radius: 24px;
    font-size: 3rem;

    background:
        linear-gradient(
            135deg,
            rgba(255,122,24,.18),
            rgba(255,45,141,.16)
        );

    border: 1px solid rgba(255,255,255,.10);
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3rem);
    line-height: 1.05;
    font-weight: 850;
    letter-spacing: -.05em;
    margin-bottom: 12px;
}

.hero-gradient {
    background:
        linear-gradient(
            90deg,
            #fff,
            #ffb06e,
            #ff75b5
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.ready {
    display: inline-flex;
    align-items: center;
    gap: 7px;

    color: #9df3b5;

    background: rgba(50,210,100,.08);
    border: 1px solid rgba(50,210,100,.18);

    border-radius: 999px;
    padding: 6px 11px;

    font-size: .8rem;
    font-weight: 650;
}

.ready-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;

    background: #65e890;
    box-shadow: 0 0 12px #65e890;
}

.hero-desc {
    max-width: 650px;
    margin: 16px auto 0;

    color: var(--muted);

    line-height: 1.65;
}

.section-label {
    color: #d9d9e2;
    font-size: .88rem;
    font-weight: 700;
    margin: 12px 0 9px;
}

.feature-card {
    padding: 17px;
    height: 100%;
}

.feature-icon {
    font-size: 1.35rem;
    margin-bottom: 8px;
}

.feature-title {
    font-weight: 750;
    margin-bottom: 4px;
}

.feature-text {
    color: var(--muted);
    font-size: .82rem;
    line-height: 1.45;
}

.footer-note {
    color: #6f6f7c;
    text-align: center;
    font-size: .75rem;
    padding: 12px 0;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;

    border: 1px solid rgba(255,255,255,.10);

    background: rgba(255,255,255,.045);

    color: #f4f4f6;

    transition: .18s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: rgba(255,122,24,.55);
    background: rgba(255,122,24,.10);
}

[data-testid="stChatMessage"] {
    border-radius: 16px;
}

@media (max-width: 700px) {

    .block-container {
        padding-left: .7rem;
        padding-right: .7rem;
        padding-top: .8rem;
    }

    .hero-card {
        padding: 30px 15px 25px;
    }

    .hero-icon {
        width: 64px;
        height: 64px;
        font-size: 2.4rem;
        border-radius: 20px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# API KEY
# ============================================================

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error(
        "GROQ_API_KEY is missing. "
        "Add it under Streamlit Cloud → Settings → Secrets."
    )
    st.stop()


# ============================================================
# GROQ CLIENT
# ============================================================

try:
    client = Groq(api_key=api_key)
except Exception as exc:
    st.error("Could not initialize Groq.")
    st.code(str(exc))
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "regenerate" not in st.session_state:
    st.session_state.regenerate = False

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

if "available_models" not in st.session_state:
    st.session_state.available_models = None

if "vision_model" not in st.session_state:
    st.session_state.vision_model = None


# ============================================================
# MODEL DISCOVERY
# ============================================================

@st.cache_resource(ttl=600)
def get_available_model_ids():
    """
    Ask Groq which models are available to this API key.

    This prevents the app from blindly calling a model that
    your particular API key/project cannot access.
    """

    try:
        models = client.models.list()

        ids = set()

        for model in models.data:
            model_id = getattr(model, "id", None)

            if model_id:
                ids.add(model_id)

        return ids

    except Exception:
        return set()


def choose_vision_model():
    """
    Select the first vision model from our known list that
    is actually available to the current API key.

    If no known vision model is available, return None.
    """

    available = get_available_model_ids()

    if not available:
        return None

    for model in VISION_MODELS:
        if model in available:
            return model

    return None


# Determine the vision model once.
if st.session_state.vision_model is None:
    st.session_state.vision_model = choose_vision_model()


# ============================================================
# CHAT HELPERS
# ============================================================

def sync_chat():
    st.session_state.all_chats[
        st.session_state.current_chat_id
    ] = {
        "messages": list(st.session_state.messages),
        "updated": datetime.now().strftime(
            "%d %b %Y, %H:%M"
        ),
    }


def create_new_chat():
    sync_chat()

    st.session_state.current_chat_id = (
        f"chat_{int(datetime.now().timestamp() * 1000)}"
    )

    st.session_state.messages = []
    st.session_state.pending_prompt = None
    st.session_state.regenerate = False

    st.rerun()


def chat_title(messages):
    for msg in messages:

        if msg.get("role") != "user":
            continue

        content = msg.get("content", "")

        if isinstance(content, str):
            title = " ".join(content.split())
        else:
            title = "Image conversation"

        return (
            title[:34] +
            ("..." if len(title) > 34 else "")
        )

    return "New chat"


# ============================================================
# IMAGE
# ============================================================

def image_to_data_url(uploaded_file):

    data = uploaded_file.getvalue()

    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError(
            "Please use an image smaller than 20 MB."
        )

    mime = uploaded_file.type

    allowed = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if mime not in allowed:
        raise ValueError(
            "Supported image formats: JPG, PNG, and WEBP."
        )

    encoded = base64.b64encode(data).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def has_image(messages):

    for msg in messages:

        content = msg.get("content")

        if isinstance(content, list):

            for part in content:

                if part.get("type") == "image_url":
                    return True

    return False


# ============================================================
# VOICE
# ============================================================

def transcribe_audio(audio_file):

    audio_bytes = audio_file.getvalue()

    stream = io.BytesIO(audio_bytes)

    stream.name = (
        getattr(audio_file, "name", None)
        or "recording.wav"
    )

    result = client.audio.transcriptions.create(
        file=stream,
        model=WHISPER_MODEL,
        response_format="text",
    )

    if isinstance(result, str):
        return result.strip()

    return getattr(
        result,
        "text",
        str(result)
    ).strip()


# ============================================================
# TEXT TO SPEECH
# ============================================================

def make_tts(text):

    if not GTTS_AVAILABLE:
        return None

    if not text.strip():
        return None

    try:

        has_devanagari = any(
            "\u0900" <= ch <= "\u097F"
            for ch in text
        )

        lang = "hi" if has_devanagari else "en"

        buf = io.BytesIO()

        gTTS(
            text=text[:3000],
            lang=lang,
            slow=False,
        ).write_to_fp(buf)

        return buf.getvalue()

    except Exception:
        return None


# ============================================================
# API MESSAGE CLEANING
# ============================================================

def prepare_api_messages(messages):

    api_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for msg in messages:

        role = msg.get("role")
        content = msg.get("content")

        if role not in {"user", "assistant"}:
            continue

        # Assistant audio is UI-only and must not be sent.
        if isinstance(content, str):
            api_messages.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        elif isinstance(content, list):

            clean_parts = []

            for part in content:

                part_type = part.get("type")

                if part_type == "text":

                    clean_parts.append(
                        {
                            "type": "text",
                            "text": part.get(
                                "text",
                                ""
                            ),
                        }
                    )

                elif part_type == "image_url":

                    image_url = (
                        part
                        .get("image_url", {})
                        .get("url")
                    )

                    if image_url:

                        clean_parts.append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                },
                            }
                        )

            if clean_parts:

                api_messages.append(
                    {
                        "role": role,
                        "content": clean_parts,
                    }
                )

    return api_messages


# ============================================================
# TEXT MODEL
# ============================================================

def call_text_model(messages):

    api_messages = prepare_api_messages(messages)

    result = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=api_messages,
    )

    content = result.choices[0].message.content

    return content or ""


# ============================================================
# VISION MODEL
# ============================================================

def call_vision_model(messages):

    vision_model = st.session_state.vision_model

    if not vision_model:
        raise RuntimeError(
            "No vision model available for your current "
            "Groq API key. Your text chat still works."
        )

    api_messages = prepare_api_messages(messages)

    try:

        result = client.chat.completions.create(
            model=vision_model,
            messages=api_messages,
            temperature=0.7,
            max_completion_tokens=2048,
        )

        content = result.choices[0].message.content

        return content or ""

    except Exception as first_error:

        # If the selected model suddenly becomes unavailable,
        # refresh the model list and try another available
        # vision model automatically.

        try:
            get_available_model_ids.clear()
        except Exception:
            pass

        new_model = choose_vision_model()

        if new_model and new_model != vision_model:

            st.session_state.vision_model = new_model

            result = client.chat.completions.create(
                model=new_model,
                messages=api_messages,
                temperature=0.7,
                max_completion_tokens=2048,
            )

            content = result.choices[0].message.content

            return content or ""

        raise first_error


# ============================================================
# REGENERATE
# ============================================================

def regenerate_last():

    if not st.session_state.messages:
        return

    if (
        st.session_state.messages[-1].get("role")
        == "assistant"
    ):
        st.session_state.messages.pop()

    if (
        st.session_state.messages
        and
        st.session_state.messages[-1].get("role")
        == "user"
    ):

        st.session_state.regenerate = True

        st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">🔥 Aditya AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-sub">'
        'Fast • Multimodal • Web-enabled'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "＋ New chat",
        use_container_width=True,
        key="new_chat_sidebar",
    ):
        create_new_chat()

    vision_status = (
        "Vision ready"
        if st.session_state.vision_model
        else "Vision unavailable"
    )

    st.markdown(
        f"""
        <div class="sidebar-card">

            <div class="status-row">
                <span>🔥 Aditya AI</span>
                <span class="live-pill">● LIVE</span>
            </div>

            <div style="
                color:#888894;
                font-size:.76rem;
                margin-top:9px;
                line-height:1.6;
            ">
                🌐 Web search<br>
                💻 Code & calculations<br>
                👁️ {vision_status}<br>
                🎙️ Voice input
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### RECENT CHATS")

    if not st.session_state.all_chats:

        st.caption(
            "Your recent chats will appear here."
        )

    else:

        items = list(
            st.session_state.all_chats.items()
        )

        items.reverse()

        for chat_id, data in items[:10]:

            if (
                chat_id
                == st.session_state.current_chat_id
            ):
                continue

            if st.button(
                chat_title(data["messages"]),
                key=f"chat_{chat_id}",
                use_container_width=True,
            ):

                st.session_state.current_chat_id = chat_id

                st.session_state.messages = list(
                    data["messages"]
                )

                st.rerun()

    st.markdown("---")

    st.markdown("### ✨ CAPABILITIES")

    st.caption("🌐 Current web information")
    st.caption("💻 Coding & calculations")
    st.caption("👁️ Image understanding")
    st.caption("🎙️ Voice input")
    st.caption("🔊 Optional voice replies")
    st.caption("💬 Session chat history")

    st.markdown("---")

    st.caption("Created by Aditya")


# ============================================================
# MAIN HEADER
# ============================================================

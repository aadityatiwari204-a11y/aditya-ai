import base64
import hashlib
import io
from datetime import datetime

import streamlit as st
from groq import Groq


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
# MODEL CONFIG
# ============================================================

TEXT_MODELS = [
    "groq/compound",
    "openai/gpt-oss-120b",
    "llama-3.3-70b-versatile",
]

VISION_MODELS = [
    "qwen/qwen3.6-27b",
    "qwen/qwen3.8-27b",
]

WHISPER_MODELS = [
    "whisper-large-v3",
    "whisper-large-v3-turbo",
]

MAX_IMAGE_BYTES = 20 * 1024 * 1024
MAX_AUDIO_BYTES = 25 * 1024 * 1024
MAX_HISTORY_MESSAGES = 24

SYSTEM_PROMPT = """
You are Aditya AI, a helpful, intelligent and friendly multimodal AI assistant.

You are not ChatGPT and must never claim to be ChatGPT.

Your goals:
- Give accurate and useful answers.
- Be clear and easy to understand.
- Answer in the user's language when appropriate.
- Help with coding and programming.
- Help with mathematics and calculations.
- Explain difficult topics simply.
- Analyze images when an image is provided.
- Use available web capabilities when current information is required.
- Never invent facts, sources, links, or capabilities.
- If you are unsure, clearly say so.
- For code, provide complete and practical solutions whenever appropriate.
""".strip()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

:root {
    --bg: #09090d;
    --panel: rgba(255,255,255,0.055);
    --panel2: rgba(255,255,255,0.075);
    --border: rgba(255,255,255,0.10);
    --text: #f5f5f7;
    --muted: #a0a0ad;
    --orange: #ff7a18;
    --pink: #ff2d8d;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(255,122,24,.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(255,45,141,.10),
            transparent 30%
        ),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background: rgba(10,10,15,.97);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
}

.brand {
    font-size: 1.65rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    background: linear-gradient(
        90deg,
        var(--orange),
        var(--pink)
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-sub {
    color: var(--muted);
    font-size: .78rem;
    margin-top: -5px;
}

.hero {
    max-width: 900px;
    margin: 20px auto 25px;
    padding: 42px 25px 35px;
    text-align: center;
    border-radius: 24px;
    background: var(--panel);
    border: 1px solid var(--border);
    box-shadow: 0 20px 60px rgba(0,0,0,.20);
}

.hero-icon {
    width: 78px;
    height: 78px;
    margin: 0 auto 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 24px;
    font-size: 3rem;
    background:
        linear-gradient(
            135deg,
            rgba(255,122,24,.18),
            rgba(255,45,141,.18)
        );
    border: 1px solid rgba(255,255,255,.10);
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 850;
    letter-spacing: -.055em;
    line-height: 1.05;
}

.gradient-text {
    background:
        linear-gradient(
            90deg,
            #ffffff,
            #ffae6b,
            #ff70b3
        );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 680px;
    margin: 15px auto 0;
    color: var(--muted);
    line-height: 1.65;
}

.ready {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    margin-top: 14px;
    padding: 6px 12px;
    border-radius: 999px;
    color: #9af3b2;
    background: rgba(60,210,100,.08);
    border: 1px solid rgba(60,210,100,.18);
    font-size: .8rem;
    font-weight: 700;
}

.ready-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #65e890;
    box-shadow: 0 0 12px #65e890;
}

.section-title {
    margin: 15px 0 10px;
    font-size: .9rem;
    font-weight: 750;
}

.feature-card {
    min-height: 125px;
    padding: 18px;
    border-radius: 18px;
    background: var(--panel);
    border: 1px solid var(--border);
}

.feature-icon {
    font-size: 1.4rem;
    margin-bottom: 8px;
}

.feature-title {
    font-weight: 750;
}

.feature-description {
    margin-top: 5px;
    color: var(--muted);
    font-size: .82rem;
    line-height: 1.45;
}

.sidebar-card {
    padding: 15px;
    margin: 12px 0;
    border-radius: 17px;
    background: var(--panel);
    border: 1px solid var(--border);
}

.status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    font-size: .82rem;
}

.status-good {
    color: #8df3ad;
}

.footer {
    margin-top: 35px;
    padding: 15px;
    text-align: center;
    color: #70707d;
    font-size: .75rem;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.045);
    color: #f5f5f7;
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
        padding-top: .7rem;
    }

    .hero {
        padding: 30px 15px 26px;
        border-radius: 20px;
    }

    .hero-icon {
        width: 65px;
        height: 65px;
        font-size: 2.4rem;
    }

    .feature-card {
        margin-bottom: 10px;
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
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = ""

if not API_KEY:
    st.error(
        "GROQ_API_KEY is missing. "
        "Add GROQ_API_KEY in Streamlit → Settings → Secrets."
    )
    st.stop()

client = Groq(api_key=API_KEY)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "messages": [],
    "all_chats": {},
    "current_chat_id": "chat_1",
    "pending_prompt": None,
    "regenerate": False,
    "last_audio_hash": None,
    "selected_model": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# MODEL DISCOVERY
# ============================================================

@st.cache_resource(ttl=600)
def get_available_models():
    try:
        response = client.models.list()
        return {
            model.id
            for model in response.data
            if getattr(model, "id", None)
        }
    except Exception:
        return set()


def choose_model(candidates):
    available = get_available_models()

    if not available:
        return candidates[0]

    for model in candidates:
        if model in available:
            return model

    return None


def refresh_models():
    get_available_models.clear()


# ============================================================
# CHAT FUNCTIONS
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


def new_chat():
    if st.session_state.messages:
        sync_chat()

    st.session_state.current_chat_id = (
        f"chat_{int(datetime.now().timestamp() * 1000)}"
    )

    st.session_state.messages = []
    st.session_state.pending_prompt = None
    st.session_state.regenerate = False

    st.rerun()


def get_chat_title(messages):
    for message in messages:

        if message.get("role") != "user":
            continue

        content = message.get("content", "")

        if isinstance(content, str):
            title = " ".join(content.split())
        else:
            title = "Image conversation"

        if not title:
            return "New chat"

        return (
            title[:34] + "..."
            if len(title) > 34
            else title
        )

    return "New chat"


# ============================================================
# IMAGE FUNCTIONS
# ============================================================

def image_to_data_url(uploaded_file):

    data = uploaded_file.getvalue()

    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError(
            "Image is too large. Please use an image "
            "smaller than 20 MB."
        )

    mime = uploaded_file.type

    allowed = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if mime not in allowed:
        raise ValueError(
            "Supported image formats are JPG, PNG and WEBP."
        )

    encoded = base64.b64encode(data).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def conversation_has_image(messages):

    for message in messages:

        content = message.get("content")

        if isinstance(content, list):

            for part in content:

                if part.get("type") == "image_url":
                    return True

    return False


# ============================================================
# MODEL MESSAGE PREPARATION
# ============================================================

def prepare_messages(messages):

    result = []

    for message in messages:

        role = message.get("role")
        content = message.get("content")

        if role not in {"user", "assistant"}:
            continue

        if isinstance(content, str):

            result.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        elif isinstance(content, list):

            parts = []

            for part in content:

                if part.get("type") == "text":

                    parts.append(
                        {
                            "type": "text",
                            "text": part.get(
                                "text",
                                ""
                            ),
                        }
                    )

                elif part.get("type") == "image_url":

                    parts.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": part[
                                    "image_url"
                                ]["url"]
                            },
                        }
                    )

            result.append(
                {
                    "role": role,
                    "content": parts,
                }
            )

    return result[-MAX_HISTORY_MESSAGES:]


# ============================================================
# TEXT MODEL
# ============================================================

def call_text_model(messages):

    model = choose_model(TEXT_MODELS)

    if model is None:
        raise RuntimeError(
            "No supported text model is currently available "
            "for this Groq API key."
        )

    api_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    api_messages.extend(
        prepare_messages(messages)
    )

    try:

        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
        )

        if not response.choices:
            raise RuntimeError(
                "The model returned no response."
            )

        return (
            response.choices[0]
            .message
            .content
            or ""
        )

    except Exception as first_error:

        for fallback in TEXT_MODELS:

            if fallback == model:
                continue

            try:

                response = client.chat.completions.create(
                    model=fallback,
                    messages=api_messages,
                )

                if response.choices:
                    return (
                        response.choices[0]
                        .message
                        .content
                        or ""
                    )

            except Exception:
                continue

        raise first_error


# ============================================================
# VISION MODEL
# ============================================================

def call_vision_model(messages):

    model = choose_model(VISION_MODELS)

    if model is None:
        raise RuntimeError(
            "Vision is not available for this Groq API key. "
            "Please check the currently available vision models."
        )

    vision_system = """
You are Aditya AI, a helpful multimodal AI assistant.

You can understand images.

Carefully inspect the provided image and answer the user's
question accurately.

If text is visible, read it carefully.
If something cannot be determined from the image, say so.
Do not invent visual details.

You are not ChatGPT.
""".strip()

    api_messages = [
        {
            "role": "system",
            "content": vision_system,
        }
    ]

    api_messages.extend(
        prepare_messages(messages)
    )

    last_error = None

    for vision_model in VISION_MODELS:

        try:

            response = client.chat.completions.create(
                model=vision_model,
                messages=api_messages,
            )

            if response.choices:

                answer = (
                    response.choices[0]
                    .message
                    .content
                    or ""
                )

                if answer:
                    return answer

        except Exception as error:
            last_error = error

    if last_error:
        raise last_error

    raise RuntimeError(
        "The vision model returned no response."
    )


# ============================================================
# VOICE / WHISPER
# ============================================================

def transcribe_audio(audio_file):

    audio_bytes = audio_file.getvalue()

    if len(audio_bytes) > MAX_AUDIO_BYTES:
        raise ValueError(
            "Audio recording is too large."
        )

    last_error = None

    for model in WHISPER_MODELS:

        try:

            stream = io.BytesIO(audio_bytes)

            stream.name = (
                getattr(
                    audio_file,
                    "name",
                    None,
                )
                or "recording.wav"
            )

            result = client.audio.transcriptions.create(
                file=stream,
                model=model,
                response_format="text",
            )

            if isinstance(result, str):
                return result.strip()

            text = getattr(
                result,
                "text",
                "",
            )

            return str(text).strip()

        except Exception as error:
            last_error = error

    if last_error:
        raise last_error

    return ""


# ============================================================
# OPTIONAL TEXT TO SPEECH
# ============================================================

def make_tts(text):

    try:
        from gtts import gTTS
    except ImportError:
        return None

    if not text.strip():
        return None

    try:

        # gTTS works best when the response is not extremely long.
        speech_text = text[:3000]

        has_devanagari = any(
            "\u0900" <= char <= "\u097F"
            for char in speech_text
        )

        language = (
            "hi"
            if has_devanagari
            else "en"
        )

        audio_buffer = io.BytesIO()

        gTTS(
            text=speech_text,
            lang=language,
            slow=False,
        ).write_to_fp(audio_buffer)

        return audio_buffer.getvalue()

    except Exception:
        return None


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
        'Your intelligent AI assistant'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "🆕 New Chat",
        use_container_width=True,
        key="sidebar_new_chat",
    ):
        new_chat()

    st.markdown(
        '<div class="sidebar-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="status">'
        '<span>AI Status</span>'
        '<span class="status-good">● Online</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Model")

    current_text_model = choose_model(
        TEXT_MODELS
    )

    current_vision_model = choose_model(
        VISION_MODELS
    )

    if current_text_model:

        st.caption(
            f"Text: `{current_text_model}`"
        )

    else:

        st.warning(
            "No text model available."
        )

    if current_vision_model:

        st.caption(
            f"Vision: `{current_vision_model}`"
        )

    else:

        st.caption(
            "Vision: unavailable"
        )

    if st.button(
        "🔄 Refresh model access",
        use_container_width=True,
        key="refresh_models",
    ):

        refresh_models()
        st.rerun()

    st.markdown("---")

    st.markdown("### 💬 Recent Chats")

    if not st.session_state.all_chats:

        st.caption(
            "Your recent chats will appear here."
        )

    else:

        chats = list(
            st.session_state.all_chats.items()
        )

        chats.reverse()

        for chat_id, chat_data in chats[:10]:

            title = get_chat_title(
                chat_data.get(
                    "messages",
                    [],
                )
            )

            if st.button(
                title,
                key=f"history_{chat_id}",
                use_container_width=True,
            ):

                st.session_state.current_chat_id = (
                    chat_id
                )

                st.session_state.messages = list(
                    chat_data.get(
                        "messages",
                        [],
                    )
                )

                st.rerun()

    st.markdown("---")

    st.markdown("### ✨ Capabilities")

    st.caption("🌐 Current information")
    st.caption("💻 Coding & programming")
    st.caption("🧮 Mathematics")
    st.caption("👁️ Image understanding")
    st.caption("🎙️ Voice input")
    st.caption("💬 Chat history")

    st.markdown("---")

    st.caption(
        "Built with Streamlit + Groq"
    )


# ============================================================
# TOP HEADER
# =====================================================

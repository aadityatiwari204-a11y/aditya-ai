import streamlit as st
from groq import Groq
import io
import base64
import hashlib
from datetime import datetime

# Optional text-to-speech
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Aditya AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CONSTANTS
# =========================================================

TEXT_MODEL = "groq/compound"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
WHISPER_MODEL = "whisper-large-v3"

MAX_IMAGE_SIZE = 4 * 1024 * 1024  # 4 MB


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(255, 90, 0, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(255, 0, 120, 0.08),
                transparent 30%
            ),
            #0b0b10;
        color: #f5f5f7;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #101017;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 1.6rem;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.05);
        color: white;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(255,120,30,0.65);
        background: rgba(255,120,30,0.12);
        transform: translateY(-1px);
    }

    /* ---------- CHAT ---------- */

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        margin-bottom: 12px;
    }

    /* ---------- HERO ---------- */

    .hero-card {
        text-align: center;
        padding: 50px 20px 30px 20px;
        margin: 10px auto 20px auto;
        max-width: 800px;
        border-radius: 26px;
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.06),
                rgba(255,255,255,0.025)
            );
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    }

    .hero-icon {
        font-size: 4rem;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #a9a9b5;
        font-size: 1rem;
        line-height: 1.6;
    }

    .ready-pill {
        display: inline-block;
        margin: 15px 0;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(50, 200, 100, 0.10);
        border: 1px solid rgba(50, 200, 100, 0.25);
        color: #8ff0ae;
        font-size: 0.85rem;
    }

    /* ---------- INFO CARD ---------- */

    .info-card {
        padding: 16px;
        border-radius: 16px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        margin-bottom: 15px;
    }

    /* ---------- SMALL TEXT ---------- */

    .muted {
        color: #9999a8;
        font-size: 0.85rem;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-top: 1rem;
        }

        .hero-card {
            padding: 35px 15px 25px 15px;
        }

        .hero-title {
            font-size: 2rem;
        }

        .hero-icon {
            font-size: 3rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# API CLIENT
# =========================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "GROQ_API_KEY is missing. Add it to your Streamlit Secrets."
    )
    st.stop()


client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# =========================================================
# SESSION STATE
# =========================================================

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "regenerate" not in st.session_state:
    st.session_state.regenerate = False

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def new_chat():
    """Create a new chat."""
    chat_id = f"chat_{datetime.now().timestamp()}"

    st.session_state.current_chat_id = chat_id
    st.session_state.messages = []
    st.session_state.pending_prompt = None
    st.session_state.regenerate = False

    st.rerun()


def sync_chat():
    """Save current conversation to session history."""
    chat_id = st.session_state.current_chat_id

    st.session_state.all_chats[chat_id] = {
        "messages": st.session_state.messages.copy(),
        "updated": datetime.now().strftime("%d %b %Y, %H:%M"),
    }


def get_chat_title(messages):
    """Generate a simple title from the first user message."""

    for message in messages:

        if message.get("role") == "user":

            content = message.get("content", "")

            if isinstance(content, str):
                title = content.strip().replace("\n", " ")

                if len(title) > 32:
                    title = title[:32] + "..."

                return title

            return "Image conversation"

    return "New chat"


def image_to_data_url(uploaded_file):
    """Convert image to a proper data URL."""

    image_bytes = uploaded_file.getvalue()

    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise ValueError(
            "Image is larger than 4 MB. "
            "Please upload a smaller image."
        )

    mime = uploaded_file.type

    if mime not in [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]:
        raise ValueError(
            "Please upload a JPG, PNG, or WEBP image."
        )

    encoded = base64.b64encode(image_bytes).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def transcribe_audio(audio_file):
    """Transcribe uploaded audio using Groq Whisper."""

    audio_bytes = audio_file.getvalue()

    audio_stream = io.BytesIO(audio_bytes)
    audio_stream.name = audio_file.name or "audio.wav"

    result = client.audio.transcriptions.create(
        file=audio_stream,
        model=WHISPER_MODEL,
        response_format="text",
    )

    if isinstance(result, str):
        return result.strip()

    return str(result).strip()


def text_to_speech(text):
    """Generate speech using gTTS."""

    if not GTTS_AVAILABLE:
        return None

    if not text.strip():
        return None

    try:

        # Detect Hindi/Devanagari
        has_devanagari = any(
            "\u0900" <= char <= "\u097F"
            for char in text
        )

        language = "hi" if has_devanagari else "en"

        audio_buffer = io.BytesIO()

        tts = gTTS(
            text=text[:3000],
            lang=language,
            slow=False,
        )

        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer.read()

    except Exception:
        return None


def clean_message_for_api(message):
    """
    Keep only the parts needed by the model.
    This prevents UI-only keys from being sent.
    """

    return {
        "role": message["role"],
        "content": message["content"],
    }


def ask_text_model(messages):
    """Ask Groq Compound."""

    api_messages = [
        {
            "role": "system",
            "content": """
You are Aditya AI.

You were created by Aditya from Belpahar, Odisha.

You are NOT ChatGPT and should never falsely claim to be ChatGPT.

Be helpful, accurate, friendly, and concise.

You can:
- answer questions
- explain concepts
- help with programming
- solve calculations
- brainstorm ideas
- summarize information
- help with writing
- search the web when current information is required
- use available tools when appropriate

When the user asks for current information, news, recent events,
prices, current facts, or anything that may have changed, use your
available web-search capability when appropriate.

When solving mathematical or programming problems, use tools when
they improve accuracy.

If you do not know something, say so rather than inventing facts.
""",
        }
    ]

    for message in messages:
        api_messages.append(
            clean_message_for_api(message)
        )

    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=api_messages,
    )

    return response.choices[0].message.content


def ask_vision_model(messages):
    """Ask the Groq vision model."""

    api_messages = [
        {
            "role": "system",
            "content": """
You are Aditya AI, a helpful multimodal AI assistant.

You can understand images and answer questions about them.

Describe only what is useful and relevant.

If something in an image is unclear, say that it is unclear
instead of guessing.

You are NOT ChatGPT.
""",
        }
    ]

    for message in messages:

        content = message["content"]

        if isinstance(content, list):
            api_messages.append(
                {
                    "role": message["role"],
                    "content": content,
                }
            )
        else:
            api_messages.append(
                {
                    "role": message["role"],
                    "content": content,
                }
            )

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=api_messages,
    )

    return response.choices[0].message.content


def has_image(messages):
    """Check whether conversation contains an image."""

    for message in messages:

        content = message.get("content")

        if isinstance(content, list):

            for part in content:

                if part.get("type") == "image_url":
                    return True

    return False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🔥 Aditya AI")

    st.caption("Fast • Multimodal • Web-enabled")

    if st.button(
        "＋ New chat",
        use_container_width=True,
    ):
        new_chat()

    st.markdown("---")

    st.markdown("### 📍 Belpahar, Odisha")

    st.success("● LIVE")

    st.caption(
        "Web search • Code • Vision • Voice"
    )

    st.markdown("---")

    st.markdown("### 💬 Recent chats")

    if not st.session_state.all_chats:

        st.caption("No previous chats yet.")

    else:

        chat_items = list(
            st.session_state.all_chats.items()
        )

        chat_items.reverse()

        for chat_id, chat_data in chat_items[:10]:

            title = get_chat_title(
                chat_data["messages"]
            )

            if st.button(
                title,
                key=f"history_{chat_id}",
                use_container_width=True,
            ):

                st.session_state.current_chat_id = chat_id

                st.session_state.messages = (
                    chat_data["messages"].copy()
                )

                st.rerun()

    st.markdown("---")

    st.markdown("### ✨ Features")

    st.caption("🌐 Web search")
    st.caption("💻 Code & calculations")
    st.caption("👁️ Image understanding")
    st.caption("🎙️ Voice input")
    st.caption("🔊 Voice responses")
    st.caption("💬 Chat history")

    st.markdown("---")

    st.caption("Aditya AI")
    st.caption("Created by Aditya")


# =========================================================
# HEADER
# =========================================================

top_left, top_right = st.columns(
    [7, 1]
)

with top_left:

    st.markdown(
        "## 🔥 Aditya AI"
    )

    st.caption(
        "Your personal multimodal AI assistant"
    )

with top_right:

    if st.button(
        "🗑️",
        help="Start a new chat",
    ):
        new_chat()


# =========================================================
# WELCOME SCREEN
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="hero-card">

            <div class="hero-icon">🔥</div>

            <div class="hero-title">
                Hi! I'm Aditya AI
            </div>

            <div class="ready-pill">
                ● Ready to help
            </div>

            <div class="hero-subtitle">
                Ask questions, write code, analyze images,
                search the web, calculate, or talk by voice.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🚀 Try something")

    q1, q2 = st.columns(2)

    with q1:

        if st.button(
            "💡 What can you do?",
            use_container_width=True,
        ):

            st.session_state.pending_prompt = (
                "What can you do?"
            )

            st.rerun()

        if st.button(
            "💻 Help me with Python",
            use_container_width=True,
        ):

            st.session_state.pending_prompt = (
                "Help me learn Python. "
                "Give me a useful beginner example."
            )

            st.rerun()

    with q2:

        if st.button(
            "🌐 What's happening today?",
            use_container_width=True,
        ):

            st.session_state.pending_prompt = (
                "What are the most important "
                "current news stories today?"
            )

            st.rerun()

        if st.button(
            "🧪 Explain physics",
            use_container_width=True,
        ):

            st.session_state.pending_prompt = (
                "Explain an interesting physics concept "
                "in a simple way."
            )

            st.rerun()


# =========================================================
# DISPLAY CHAT
# =========================================================

for index, message in enumerate(
    st.session_state.messages
):

    role = message["role"]

    if role == "user":

        with st.chat_message(
            "user",
            avatar="👤",
        ):

            content = message["content"]

            if isinstance(content, list):

                text_parts = []

                for part in content:

                    if part["type"] == "text":
                        text_parts.append(
                            part["text"]
                        )

                if text_parts:
                    st.markdown(
                        "\n".join(text_parts)
                    )

                for part in content:

                    if part["type"] == "image_url":

                        try:

                            image_url = (
                                part["image_url"]["url"]
                            )

                            st.image(
                                image_url,
                                use_container_width=True,
                            )

                        except Exception:
                            pass

            else:

                st.markdown(content)

    elif role == "assistant":

        with st.chat_message(
            "assistant",
            avatar="🔥",
        ):

            answer = message["content"]

            st.markdown(answer)

            # Save response
            st.download_button(
                label="💾 Save",
                data=answer,
                file_name="aditya_ai_response.txt",
                mime="text/plain",
                key=f"save_{index}",
            )

            # Voice response
            if message.get("audio"):

                st.audio(
                    message["audio"],
                    format="audio/mp3",
                )


# =========================================================
# ATTACHMENTS & VOICE
# =========================================================

with st.expander(
    "🧰 Attachments & Voice"
):

    col1, col2 = st.columns(2)

    with col1:

        uploaded_image = st.file_uploader(
            "🖼️ Upload an image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp",
            ],
            help="Maximum 4 MB",
        )

    with col2:

        audio_input = st.audio_input(
            "🎙️ Record your question",
            sample_rate=16000,
        )


# =========================================================
# VOICE TRANSCRIPTION
# =========================================================

voice_prompt = None

if audio_input is not None:

    audio_bytes = audio_input.getvalue()

    current_hash = hashlib.sha256(
        audio_bytes
    ).hexdigest()

    if (
        current_hash
        != st.session_state.last_audio_hash
    ):

        with st.spinner(
            "🎙️ Transcribing..."
        ):

            try:

                voice_prompt = transcribe_audio(
                    audio_input
                )

                st.session_state.last_audio_hash = (
                    current_hash
                )

                if voice_prompt:

                    st.info(
                        f"🎙️ I heard: {voice_prompt}"
                    )

            except Exception as e:

                st.error(
                    "I couldn't transcribe that audio."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.code(str(e))


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask anything..."
)


# =========================================================
# DETERMINE PROMPT
# =========================================================

prompt = None

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt

    st.session_state.pending_prompt = None

elif voice_prompt:

    prompt = voice_prompt

elif user_input:

    prompt = user_input


# =========================================================
# REGENERATE
# =========================================================

regenerating = False

if st.session_state.regenerate:

    regenerating = True

    st.session_state.regenerate = False

    # Remove previous assistant answer
    if (
        st.session_state.messages
        and st.session_state.messages[-1]["role"]
        == "assistant"
    ):

        st.session_state.messages.pop()

    # Find latest user message
    for message in reversed(
        st.session_state.messages
    ):

        if message["role"] == "user":

            if isinstance(
                message["content"],
                str,
            ):

                prompt = message["content"]

            else:

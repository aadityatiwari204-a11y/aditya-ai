import streamlit as st
from groq import Groq
from gtts import gTTS
import io

st.set_page_config(page_title="Aditya AI", page_icon="🤖", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"
    st.session_state.all_chats["chat_1"] = {"title": "New Chat", "messages": []}
if "last_voice" not in st.session_state:
    st.session_state.last_voice = None

# Sidebar
with st.sidebar:
    st.title("Aditya AI - Belpahar")
    if st.button("+ New Chat"):
        import uuid
        new_id = f"chat_{uuid.uuid4().hex[:6]}"
        st.session_state.current_chat_id = new_id
        st.session_state.messages = []
        st.session_state.all_chats[new_id] = {"title": "New Chat", "messages": []}
        st.rerun()

    for cid, data in st.session_state.all_chats.items():
        if st.button(data["title"][:30], key=cid):
            st.session_state.current_chat_id = cid
            st.session_state.messages = data["messages"]
            st.rerun()

st.title("🤖 Aditya AI")

# Show old messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Show last voice if any
if st.session_state.last_voice is not None:
    st.audio(st.session_state.last_voice, format="audio/mp3")

# Input
final_input = st.chat_input("Photoshop kya hai? / What is Photoshop?")

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.markdown(final_input)

    with st.chat_message("assistant"):
        ph = st.empty()
        full_answer = ""
        msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        try:
            # First try 70b
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=msgs,
                max_tokens=2000
            )
            full_answer = res.choices[0].message.content
            ph.markdown(full_answer)
        except Exception as e:
            # Fallback to 8b if 70b fails
            try:
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=msgs,
                    max_tokens=2000
                )
                full_answer = res.choices[0].message.content
                ph.markdown(full_answer)
            except Exception as e2:
                full_answer = f"Server busy, try again in 10 sec. Error: {e2}"
                ph.markdown(full_answer)

        st.session_state.messages.append({"role": "assistant", "content": full_answer})

        # --- Voice Hindi + English ---
        try:
            lang_code = 'hi' if any('\u0900' <= c <= '\u097F' for c in full_answer) else 'en'
            tts = gTTS(text=full_answer[:500], lang=lang_code, slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            st.session_state['last_voice'] = buf
            st.audio(buf, format='audio/mp3')
        except:
            pass

        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = list(st.session_state.messages)
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = final_input[:35]
        st.rerun()

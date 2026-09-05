import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import uuid

st.set_page_config(page_title="Aditya AI - Belpahar", page_icon="🤖", layout="wide")

# --- FANCY CSS (Your old look) ---
st.markdown("""
<style>
   .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    [data-testid="stSidebar"] {
        background: rgba(20,20,40,0.9);
        border-right: 1px solid #5a5a8a;
    }
   .stChatMessage {
        background: rgba(255,255,255,0.08)!important;
        border-radius: 15px!important;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    h1 {
        text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(79,172,254,0.5);
    }
   .stButton>button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
   .stChatInput {
        background: rgba(0,0,0,0.3)!important;
        border-radius: 25px!important;
    }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"chat_1": {"title": "New Chat", "messages": []}}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"
if "last_voice" not in st.session_state:
    st.session_state.last_voice = None

with st.sidebar:
    st.markdown("## ✨ Aditya AI - Belpahar")
    st.markdown("---")
    if st.button("➕ New Chat"):
        new_id = f"chat_{uuid.uuid4().hex[:6]}"
        st.session_state.current_chat_id = new_id
        st.session_state.messages = []
        st.session_state.all_chats[new_id] = {"title": "New Chat", "messages": []}
        st.rerun()
    st.markdown("### 💬 History")
    for cid, data in list(st.session_state.all_chats.items())[::-1]:
        if st.button(f"📝 {data['title'][:28]}", key=cid):
            st.session_state.current_chat_id = cid
            st.session_state.messages = data["messages"]
            st.rerun()

st.markdown("# 🤖 Aditya AI")
st.markdown("<p style='text-align:center; opacity:0.7;'>Your Smart AI from Belpahar — Hindi + English Voice</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if st.session_state.last_voice is not None:
    st.audio(st.session_state.last_voice, format="audio/mp3")

final_input = st.chat_input("Photoshop kya hai? / What is Photoshop?")

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.markdown(final_input)

    with st.chat_message("assistant"):
        ph = st.empty()
        full_answer = ""
        msgs = [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages]
        try:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, max_tokens=2000)
            full_answer = res.choices[0].message.content
            ph.markdown(full_answer)
        except Exception as e:
            try:
                res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=msgs, max_tokens=2000)
                full_answer = res.choices[0].message.content
                ph.markdown(full_answer)
            except Exception as e2:
                full_answer = f"Server busy, try again: {e2}"
                ph.markdown(full_answer)

        st.session_state.messages.append({"role": "assistant", "content": full_answer})

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

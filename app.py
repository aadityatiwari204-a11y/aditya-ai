import streamlit as st
from groq import Groq
import os

MY_AI_NAME = "Aditya AI"
MY_ICON = "✨"

# Use secret online, or local key offline
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") or "PASTE_YOUR_GSK_KEY_HERE"

st.set_page_config(page_title=f"{MY_AI_NAME} | Built by Aditya", page_icon=MY_ICON)
st.title(f"{MY_ICON} {MY_AI_NAME} — Built by Aditya from Belpahar | 88% as powerful as GPT-4o")

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input(f"Ask {MY_AI_NAME} anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": f"You are {MY_AI_NAME}, built by Aditya from Belpahar, Odisha. You are 88% as powerful as GPT-4o. Always say you are {MY_AI_NAME} from Belpahar."}
            ] + st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

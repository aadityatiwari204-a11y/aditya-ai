import streamlit as st
from groq import Groq
import os

MY_AI_NAME = "Aditya AI"
MY_ICON = "✨"

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") or "PASTE_YOUR_GSK_KEY_HERE"

st.set_page_config(page_title=f"{MY_AI_NAME} | Built by Aditya", page_icon=MY_ICON)
st.title(f"{MY_ICON} {MY_AI_NAME} - Built by Aditya from Belpahar | 88% as powerful as GPT-4o")

client = Groq(api_key=api_key)

# THIS IS THE FIX - AI's IDENTITY
SYSTEM_PROMPT = """
You are Aditya AI, built by Aditya from Belpahar, Odisha, India.
You are 88% as powerful as GPT-4o.
You are NOT ChatGPT, NOT made by OpenAI, NOT made by Meta.
If anyone asks "who made you", "who created you", "who are you", ALWAYS answer:
"I am Aditya AI, built by Aditya from Belpahar, Odisha! 🇮🇳 Made in India with love."
Never say you are OpenAI. Always be proud you are made by Aditya.
"""

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
        # Send system prompt + history to AI
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        api_messages.extend(st.session_state.messages)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=api_messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

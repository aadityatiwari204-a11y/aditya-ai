import streamlit as st
from groq import Groq

st.set_page_config(page_title="Aditya AI | Built by Aditya", page_icon="🔥")

# FOR GOOGLE VERIFICATION & SEO + ADSENSE - FIXED
import streamlit.components.v1 as components
components.html("""
<meta name="google-site-verification" content="QIBGITDr0YjVialLuM" />
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6146742303875365" crossorigin="anonymous"></script>
""", height=0)

st.markdown('<meta name="description" content="Aditya AI is a free AI assistant built By Aditya from Belpahar, Odisha. 80% as powerful as GPT-4o." />', unsafe_allow_html=True)
st.title("🔥 Aditya AI - Built by Aditya from Belpahar | 80% as powerful as GPT-4o")

# Get API key from Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("GROQ_API_KEY not found in Secrets! Go to Streamlit > Manage App > Settings > Secrets")
    st.stop()

client = Groq(api_key=api_key)

SYSTEM_PROMPT = "You are Aditya AI, built by Aditya from Belpahar, Odisha, India. You are 80% as powerful as GPT-4o. Be helpful, friendly."

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask Aditya AI anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")

import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Internship Chatbot", page_icon="🤖")
st.title("🤖 Internship Chatbot")

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing!")
    st.stop()

client = Groq(api_key=api_key.strip())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            response_text = chat_completion.choices[0].message.content
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Error: {e}")

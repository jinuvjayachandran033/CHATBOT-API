import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Internship Chatbot", page_icon="🤖")
st.title("🤖 Internship Chatbot")

# Fetch and clean API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key is missing! Please configure it in Streamlit Cloud Secrets.")
    st.stop()

clean_key = api_key.strip().strip('"').strip("'")
genai.configure(api_key=clean_key)

# Initialize Model
model = genai.GenerativeModel("gemini-2.0-flash")

# Session State for Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error generating response: {e}")

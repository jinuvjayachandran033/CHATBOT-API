import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Internship Chatbot", page_icon="🤖")
st.title("🤖 Internship Chatbot")

# 1. Fetch & Clean API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key is missing! Please configure it in Streamlit Cloud Secrets.")
    st.stop()

clean_key = api_key.strip().strip('"').strip("'")
genai.configure(api_key=clean_key)

# 2. Dynamically pick an available model to avoid 404 errors
@st.cache_resource
def get_working_model():
    try:
        # Find all models supported by your API key that generate content
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        # Prefer flash models if available, otherwise take the first valid model
        flash_models = [m for m in available_models if 'flash' in m]
        selected_model = flash_models[0] if flash_models else available_models[0]
        return genai.GenerativeModel(selected_model)
    except Exception:
        # Fallback default
        return genai.GenerativeModel("gemini-2.0-flash")

model = get_working_model()

# 3. Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Prompts
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

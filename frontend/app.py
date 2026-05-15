import streamlit as st
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Constants
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Support Agent", page_icon="🤖", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .chat-container {
        padding: 2rem;
        border-radius: 10px;
        background-color: #1e2127;
    }
    .user-msg {
        background-color: #2b313e;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        margin: 5px 0;
        text-align: right;
    }
    .ai-msg {
        background-color: #1f2937;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0px;
        margin: 5px 0;
        border: 1px solid #374151;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Customer Support Chatbot")
st.markdown("Ask me anything about our company's policies or FAQs.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for document upload
with st.sidebar:
    st.header("⚙️ Admin Panel")
    st.markdown("Upload company FAQ documents (PDF) to train the support agent.")
    
    uploaded_file = st.file_uploader("Upload FAQ PDF", type=["pdf"])
    if st.button("Process Document"):
        if uploaded_file is not None:
            with st.spinner("Processing document and updating knowledge base..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = httpx.post(f"{API_BASE_URL}/upload", files=files, timeout=60.0)
                    if response.status_code == 200:
                        st.success("Document processed successfully! The agent is ready.")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please upload a file first.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare payload with history (excluding current prompt)
    history_payload = [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in st.session_state.messages[:-1]
    ]
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = httpx.post(
                    f"{API_BASE_URL}/chat",
                    json={"message": prompt, "history": history_payload},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    reply = response.json().get("reply", "Sorry, I couldn't process that.")
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error("Cannot reach the backend server. Please ensure FastAPI is running.")

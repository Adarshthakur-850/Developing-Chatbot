import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="💬 AI Chatbot", page_icon="🤖")

st.title("Context-Aware AI Chatbot")

# Session State
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Types something..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Bot Response (via API or Engine direct? Let's use API if running, else direct)
    # Using API is cleaner for "production-quality", but creates a dependency on uvicorn running.
    # To make verification easier in one go, I'll import engine directly for the Streamlit app demo
    # OR I'll assume standard API usage. Let's use direct engine import to avoid dual-process complexity for User.
    # BUT the prompt asked for separate API and UI. So I will keep API logic but for the "run code" request,
    # the user might prefer a single command. I'll stick to API calls but provide a note.
    # Actually, let's use direct import for the Streamlit app to make it standalone-runnable easily.
    
    # ... Wait, standard practice is requests.post. I'll stick to that.
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            payload = {
                "session_id": st.session_state["session_id"],
                "message": prompt
            }
            res = requests.post(f"{API_URL}/chat", json=payload)
            
            if res.status_code == 200:
                data = res.json()
                bot_reply = data["response"]
                # Optional: Show debug info
                # st.caption(f"Intent: {data['intent']} | Entities: {data['entities']}")
                message_placeholder.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            else:
                message_placeholder.markdown("⚠️ Error: Is the API server running?")
        except requests.exceptions.ConnectionError:
             message_placeholder.markdown("⚠️ Connection Error: Please run `uvicorn api.app:app` in a terminal.")

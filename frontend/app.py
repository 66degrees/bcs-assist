import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="BCS Assist",
    page_icon="💬",
    layout="wide"
)

# Get conversation_id from URL query parameters
query_params = st.query_params
conversation_id = query_params.get("conversation_id", None)

# Store conversation_id in session state if provided
if conversation_id:
    st.session_state.conversation_id = conversation_id

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message (only show once)
if len(st.session_state.messages) == 0:
    welcome_msg = "👋 Welcome to BCS Assist! How can I help you today?"
    if conversation_id:
        welcome_msg += f"\n\n📋 Conversation ID: `{conversation_id}`"
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_msg
    })

# Title
st.title("💬 BCS Assist Chat")

# Display conversation ID if present
if conversation_id:
    st.info(f"🔗 **Conversation ID:** `{conversation_id}`")


iframe = """
    <iframe 
        width="100%" 
        height="900" 
        src="https://lookerstudio.google.com/embed/reporting/605e22b8-1a9d-441e-bf6f-5c115efcdee2/page/p_sw2iq48std" 
        frameborder="0" 
        style="border:0" 
        allowfullscreen 
        sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox">
    </iframe>
"""

components.html(iframe, height=920)

# st.title("Embedded Looker Studio Dashboard")

# url = "https://lookerstudio.google.com/reporting/605e22b8-1a9d-441e-bf6f-5c115efcdee2/explore?s=krrxOhZjjkQ"

# components.iframe(url, height=900, scrolling=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Placeholder for assistant response
    # TODO: Replace with actual backend API call
    with st.chat_message("assistant"):
        response = "This is a placeholder response. Backend API integration coming soon!"
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


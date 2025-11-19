import streamlit as st

# Page configuration
st.set_page_config(
    page_title="BCS Assist",
    page_icon="💬",
    layout="wide"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message (only show once)
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Welcome to BCS Assist! How can I help you today?"
    })

# Title
st.title("💬 BCS Assist Chat")

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


import streamlit as st

# CSS for styling the chat bubbles
st.markdown("""
<style>
  .chat-container {
    overflow-y: scroll;
    height: 400px;
    padding: 10px;
    margin-bottom: 10px;
  }
  .user-message, .bot-message {
    color: white;
    padding: 5px;
    border-radius: 10px;
    margin: 5px;
  }
  .user-message {
    text-align: right;
    background-color: black;
  }
  .bot-message {
    text-align: left;
    background-color: black;
  }
</style>
""", unsafe_allow_html=True)

# Session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Chat window container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state['chat_history']:
    st.markdown(message, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# User input and send button
user_input = st.text_input("Type your message:")
if st.button("Send"):
    user_message = f'<div class="user-message">You: {user_input}</div>'
    st.session_state['chat_history'].append(user_message)
    # Placeholder bot response
    bot_response = "Hello, I'm your bot!" # This can be replaced with GPT-4 response
    bot_message = f'<div class="bot-message">Bot: {bot_response}</div>'
    st.session_state['chat_history'].append(bot_message)

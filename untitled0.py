# app.py

import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os

# Streamlit Community Cloud에서 환경 변수 사용
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

chat = model.start_chat(history=[])

# Function to send a message to the Gemini model
def send_message_to_gemini(message):
    response = chat.send_message(message)
    return response.text

# HTML content (이전과 동일)
html_content = """
<!DOCTYPE html>
<html lang="ko">
... (이전과 동일한 HTML 내용) ...
</html>
"""

# Streamlit app
st.set_page_config(layout="wide")

# Display the HTML content in the Streamlit app
components.html(html_content, height=800, scrolling=True)

# Handle incoming messages from the HTML/JS frontend
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if st.session_state.get('client_message'):
    user_message = st.session_state.get('client_message')
    st.session_state['messages'].append(f"User: {user_message}")
    
    # Send message to Gemini and get response
    bot_response = send_message_to_gemini(user_message)
    st.session_state['messages'].append(f"Bot: {bot_response}")
    
    # Send bot response back to the HTML/JS frontend
    st.components.v1.html(
        f"""
        <script>
            window.parent.postMessage({{
                type: 'bot_response',
                message: {bot_response!r}
            }}, '*');
        </script>
        """,
        height=0,
    )

# JavaScript to handle messages from the HTML frontend
components.html(
    """
    <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'send_message') {
                window.parent.postMessage({
                    type: 'streamlit:set_state',
                    data: { client_message: event.data.message }
                }, '*');
            }
        });
    </script>
    """,
    height=0,
)

# Display chat history in Streamlit (optional, for debugging)
st.write("Chat History:")
for message in st.session_state['messages']:
    st.write(message)

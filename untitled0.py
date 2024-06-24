pip install PyPDF2

import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
from io import BytesIO
import PyPDF2

# Function to send a message to the Gemini 1.5 Pro model
def send_message_to_gemini(api_key, message, context=""):
    url = "https://api.gemini.com/v1/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "message": message,
        "context": context
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# API key for the Gemini 1.5 Pro model
API_KEY = "AIzaSyAbHQK9OtDTG5x5P1L_9YCnj7DwwoKf88w"

# Streamlit app
st.set_page_config(layout="wide")

# HTML content for the landing page
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>대전진로진학지원시스템</title>
    <style>
        /* ... (기존 CSS 스타일) ... */
        #chatbot-container {
            position: fixed;
            right: 20px;
            bottom: 20px;
            width: 350px;
            height: 500px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        #chatbot-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
        }
        .message {
            margin-bottom: 10px;
            padding: 5px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #e6f3ff;
            text-align: right;
        }
        .bot-message {
            background-color: #f0f0f0;
        }
        /* ... (나머지 CSS 스타일) ... */
    </style>
</head>
<body>
    <!-- ... (기존 HTML 내용) ... -->

    <div id="chatbot-container">
        <div id="chatbot-header">
            <h3>AI진로진학 파트너</h3>
        </div>
        <div id="chatbot-messages"></div>
        <div id="chatbot-input">
            <input type="text" id="chatbot-input-text" placeholder="메시지를 입력하세요...">
            <button onclick="sendMessage()">전송</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('chatbot-input-text');
            const message = input.value;
            input.value = '';
            
            const chatMessages = document.getElementById('chatbot-messages');
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.textContent = message;
            chatMessages.appendChild(userMessage);
            
            // Send the message to the Streamlit backend
            window.parent.postMessage({type: 'chat_message', message: message}, '*');
        }

        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'bot_response') {
                const chatMessages = document.getElementById('chatbot-messages');
                const botMessage = document.createElement('div');
                botMessage.className = 'message bot-message';
                botMessage.textContent = event.data.message;
                chatMessages.appendChild(botMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        });
    </script>
</body>
</html>
"""

# Display the HTML content in the Streamlit app
components.html(html_content, height=800, scrolling=True)

# Streamlit sidebar for PDF upload and chat history
st.sidebar.title("PDF Upload & Chat History")

uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.sidebar.success("PDF uploaded and text extracted!")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display chat history in the sidebar
st.sidebar.subheader("Chat History")
for message in st.session_state['messages']:
    st.sidebar.text(message)

# Handle incoming messages from the HTML/JS frontend
if st.session_state.get('client_message'):
    user_message = st.session_state.get('client_message')
    st.session_state['messages'].append(f"User: {user_message}")
    
    # Prepare context (including PDF content if available)
    context = pdf_text if 'pdf_text' in locals() else ""
    
    # Send message to Gemini and get response
    response = send_message_to_gemini(API_KEY, user_message, context)
    bot_response = response.get('response', 'Sorry, I could not process your request.')
    
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
            if (event.data.type === 'chat_message') {
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

# file: streamlit_app.py

import streamlit as st
import streamlit.components.v1 as components
import requests

# Function to read HTML file content
def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to send a message to the Gemini 1.5 Pro model
def send_message_to_gemini(api_key, message):
    url = "https://api.gemini.com/v1/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "message": message
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# API key for the Gemini 1.5 Pro model
API_KEY = "your_gemini_api_key_here"

# Load the HTML content from the file
html_content = load_html('/Users/yooyoungjin/Downloads/대전플젝html/AI챗봇.html')

# Display the HTML content in the Streamlit app
components.html(html_content, height=800, scrolling=True)

# JavaScript and HTML for chatbot interactivity
chatbot_script = """
<script>
function toggleChatbot() {
    const chatbot = document.getElementById('chatbot-container');
    chatbot.style.right = chatbot.style.right === '0px' ? '-400px' : '0px';
}

function sendMessage() {
    const input = document.getElementById('chatbot-input-text');
    const message = input.value;
    input.value = '';
    
    const chatContainer = document.getElementById('chatbot-content');
    const userMessage = document.createElement('div');
    userMessage.textContent = 'User: ' + message;
    chatContainer.appendChild(userMessage);
    
    // Send the message to the Streamlit backend
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.textContent = 'Bot: ' + data.response;
        chatContainer.appendChild(botMessage);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

window.onload = function() {
    document.getElementById('chatbot-icon').onclick = toggleChatbot;
    document.getElementById('chatbot-close').onclick = toggleChatbot;
    document.getElementById('send-message-btn').onclick = sendMessage;
}
</script>
"""

# Streamlit app layout
st.markdown(chatbot_script, unsafe_allow_html=True)

# Endpoint to handle message sending
if st.experimental_rerun.get_url_params():
    import json
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route('/send_message', methods=['POST'])
    def send_message():
        data = request.json
        message = data.get('message')
        response = send_message_to_gemini(API_KEY, message)
        return jsonify(response)

    if __name__ == "__main__":
        app.run(port=8501)

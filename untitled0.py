# file: streamlit_app.py

import streamlit as st
import streamlit.components.v1 as components
import requests
from flask import Flask, request, jsonify

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
API_KEY = "AIzaSyAbHQK9OtDTG5x5P1L_9YCnj7DwwoKf88w"

# HTML content embedded directly
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>대전진로진학지원시스템</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            font-family: 'Nanum Gothic', sans-serif;
            height: 100%;
            overflow: hidden;
        }
        .container {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        header {
            background-color: #ffffff;
            padding: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .logo {
            display: flex;
            align-items: center;
        }
        .logo img {
            width: 50px;
            height: auto;
            margin-right: 10px;
        }
        .logo-text {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }
        nav ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
            display: flex;
        }
        nav > ul > li {
            position: relative;
            margin-left: 20px;
        }
        nav > ul > li > a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
            padding: 10px 15px;
            display: block;
        }
        .submenu {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background-color: #fff;
            border: 1px solid #ddd;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            z-index: 1000;
        }
        .submenu > div {
            padding: 10px;
        }
        .submenu a {
            display: block;
            padding: 5px 10px;
            text-decoration: none;
            color: #333;
            white-space: nowrap;
        }
        .submenu a:hover {
            background-color: #f0f0f0;
        }
        .has-submenu:hover .submenu {
            display: block;
        }
        .hero {
            background-color: #f0f0f0;
            text-align: center;
            padding: 50px 20px;
            flex-shrink: 0;
        }
        .hero h1 {
            font-size: 36px;
            margin-bottom: 20px;
        }
        .hero p {
            font-size: 18px;
            color: #666;
        }
        .services {
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
            flex-shrink: 0;
        }
        .service-card {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            width: calc(25% - 20px);
            min-width: 200px;
            text-align: center;
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        .service-card:hover {
            transform: translateY(-5px);
        }
        .service-card img {
            width: 80px;
            height: 80px;
            margin-bottom: 15px;
        }
        .service-card h3 {
            margin-bottom: 10px;
            color: #4CAF50;
        }
        .service-card p {
            font-size: 14px;
            color: #666;
        }
        .content-section {
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            flex-shrink: 0;
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 20px 0;
            flex-shrink: 0;
        }
        /* 챗봇 관련 스타일 */
        #chatbot-icon {
            position: fixed;
            right: 20px;
            bottom: 20px;
            width: 60px;
            height: 60px;
            background-color: #4CAF50;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        #chatbot-icon img {
            width: 35px;
            height: 35px;
        }
        #chatbot-container {
            position: fixed;
            right: -400px;
            top: 0;
            width: 400px;
            height: 100vh;
            background-color: white;
            box-shadow: -2px 0 5px rgba(0,0,0,0.1);
            transition: right 0.3s ease;
            z-index: 1001;
            display: flex;
            flex-direction: column;
        }
        #chatbot-header {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        #chatbot-close {
            cursor: pointer;
        }
        #chatbot-content {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
        }
        #chatbot-input {
            display: flex;
            padding: 10px;
            border-top: 1px solid #eee;
        }
        #chatbot-input input {
            flex-grow: 1;
            border: 1px solid #ddd;
            padding: 5px;
            border-radius: 3px;
        }
        #chatbot-input button {
            margin-left: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
        }
        .chatbot-icons {
            display: flex;
            justify-content: flex-end;
            padding: 10px;
        }
        .chatbot-icons img {
            width: 24px;
            height: 24px;
            margin-left: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-content">
                <div class="logo">
                    <img src="대전광역시로고.png" alt="대전광역시교육청 로고">
                    <span class="logo-text">대전진로진학지원시스템</span>
                </div>
                <nav>
                    <ul>
                        <li class="has-submenu">
                            <a href="#">진학 정보</a>
                            <div class="submenu">
                                <div>
                                    <a href="#">고교정보/고입정보</a>
                                    <a href="#">대학정보/대입정보</a>
                                </div>
                            </div>
                        </li>
                        <li class="has-submenu">
                            <a href="#">진로정보</a>
                            <div class="submenu">
                                <div>
                                    <a href="#">진로검사</a>
                                    <a href="#">진로검사 하기</a>
                                    <a href="#">진로검사 결과보기</a>
                                    <a href="#">진로정보</a>
                                    <a href="#">직업 백과</a>
                                    <a href="#">추천 사이트</a>
                                    <a href="#">진로 자료실</a>
                                    <a href="#">교사용 진로교육 자료</a>
                                    <a href="#">진로체험</a>
                                </div>
                            </div>
                        </li>
                        <li class="has-submenu">
                            <a href="#">상담</a>
                            <div class="submenu">
                                <div>
                                    <a href="#">온라인 공개 게시판 상담</a>
                                    <a href="#">상담센터 방문 상담</a>
                                    <a href="#">직업 멘토링 1:1</a>
                                </div>
                            </div>
                        </li>
                        <li class="has-submenu">
                            <a href="#">AI진로융합</a>
                            <div class="submenu">
                                <div>
                                    <a href="#">이력관리</a>
                                    <a href="#">진로체험 이력</a>
                                    <a href="#">진로검사결과 이력</a>
                                    <a href="#">AI추천</a>
                                    <a href="#">직업/전공 추천</a>
                                    <a href="#">진로체험 추천</a>
                                    <a href="#">교과목 추천</a>
                                    <a href="#">진로 학업 설계 로드맵</a>
                                </div>
                            </div>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>

        <section class="hero">
            <h1>당신의 미래를 설계하세요</h1>
            <p>대전진로진학지원시스템이 함께합니다</p>
        </section>

        <section class="content-section">
            <h2>대전진로진학지원시스템 소개</h2>
            <p>대전진로진학지원시스템은 대전 지역 초중고등학생들의 진로와 진학을 체계적으로 지원하기 위해 만들어졌습니다. 다양한 정보와 상담 서비스를 통해 학생들이 자신의 적성과 흥미를 발견하고, 미래를 설계할 수 있도록 돕습니다.</p>
        </section>

        <section class="services">
            <div class="service-card" onclick="alert('AI진로융합 페이지로 이동합니다.')">
                <img src="https://via.placeholder.com/80" alt="AI진로융합 아이콘">
                <h3>AI진로융합</h3>
                <p>인공지능 기반 맞춤형 진로 추천</p>
            </div>
            <div class="service-card" onclick="alert('진학정보 페이지로 이동합니다.')">
                <img src="https://via.placeholder.com/80" alt="진학정보 아이콘">
                <h3>진학정보</h3>
                <p>고교 및 대학 입학 정보 제공</p>
            </div>
            <div class="service-card" onclick="alert('진로정보 페이지로 이동합니다.')">
                <img src="https://via.placeholder.com/80" alt="진로정보 아이콘">
                <h3>진로정보</h3>
                <p>진로 검사 및 직업 정보 제공</p>
            </div>
            <div class="service-card" onclick="alert('상담 페이지로 이동합니다.')">
                <img src="https://via.placeholder.com/80" alt="상담 아이콘">
                <h3>상담</h3>
                <p>온라인 및 오프라인 상담 지원</p>
            </div>
        </section>

        <footer>
            <p>&copy; 2024 대전진로진학지원시스템. All rights reserved.</p>
        </footer>
    </div>

    <!-- 챗봇 아이콘 -->
    <div id="chatbot-icon" onclick="toggleChatbot()">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z'/%3E%3C/svg%3E" alt="Chat">
    </div>

    <!-- 챗봇 컨테이너 -->
    <div id="chatbot-container">
        <div id="chatbot-header">
            <h3>AI진로진학 파트너</h3>
            <span id="chatbot-close" onclick="toggleChatbot()">×</span>
        </div>
        <div class="chatbot-icons">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%234CAF50'%3E%3Cpath d='M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z'/%3E%3C/svg%3E" alt="Copy" onclick="alert('복사 기능')">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%234CAF50'%3E%3Cpath d='M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z'/%3E%3C/svg%3E" alt="Download" onclick="alert('다운로드 기능')">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%234CAF50'%3E%3Cpath d='M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z'/%3E%3C/svg%3E" alt="Refresh" onclick="alert('새로고침 기능')">
        </div>
        <div id="chatbot-content">
            <!-- 스트림릿 앱을 위한 플레이스홀더 -->
            <div id="streamlit-app"></div>
        </div>
        <div id="chatbot-input">
            <input type="text" id="chatbot-input-text" placeholder="메시지를 입력하세요..." onkeydown="if(event.key === 'Enter') sendMessage()">
            <button id="send-message-btn" onclick="sendMessage()">전송</button>
        </div>
    </div>

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
</body>
</html>
"""

# Display the HTML content in the Streamlit app
components.html(html_content, height=1500, scrolling=False)

# Add an endpoint to handle the message sending
if 'flask_server' not in st.session_state:
    st.session_state['flask_server'] = Flask(__name__)

app = st.session_state['flask_server']

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    response = send_message_to_gemini(API_KEY, message)
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=8501)

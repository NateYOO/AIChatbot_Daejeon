# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rVQ0eIcQPQ3o9Ldzy6kUuXRwUi-VKG8y
"""

import streamlit as st
import google.generativeai as genai
from streamlit_elements import elements, dashboard, mui, html

# Gemini 모델 설정
genai.configure(api_key="AIzaSyAbHQK9OtDTG5x5P1L_9YCnj7DwwoKf88w")
model = genai.GenerativeModel('gemini-1.5-pro')

# 스트림릿 페이지 설정
st.set_page_config(page_title="대전진로진학지원시스템", layout="wide")

# HTML 및 CSS 내용
HTML_CONTENT = """
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
        }
        .container {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
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
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 20px 0;
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
</body>
</html>
"""

# 챗봇 함수
def chatbot(prompt):
    response = model.generate_content(f"""
    사용자가 원하는 한국에서의 진로진학 및 대학, 직업정보 등을 MECE 원칙에 따라 구조화하여 제공하고, 친절하게 응답해주세요.
    질문: {prompt}
    """)
    return response.text

# 메인 애플리케이션
def main():
    # 사이드바에 챗봇 배치
    with st.sidebar:
        st.title("AI진로진학 파트너")
        user_input = st.text_input("질문을 입력하세요:")
        if st.button("전송"):
            if user_input:
                response = chatbot(user_input)
                st.write("AI 응답:", response)

    # 메인 컨텐츠 영역에 HTML 랜딩 페이지 표시
    with elements("landing_page"):
        dashboard.Dashboard()
        with dashboard.Item("landing_page_item", x=0, y=0, w=12, h=40):
            mui.Box(
                html.Div(HTML_CONTENT),
                sx={
                    "height": "100%",
                    "overflow": "auto"
                }
            )

if __name__ == "__main__":
    main()
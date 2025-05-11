import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 환경 변수 불러오기 (로컬과 Streamlit Cloud 모두 지원)
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit Secrets에서도 API 키 확인 (Streamlit Cloud 배포용)
if not API_KEY and 'GOOGLE_API_KEY' in st.secrets:
    API_KEY = st.secrets['GOOGLE_API_KEY']

# API 키 확인
if not API_KEY:
    st.error("❌ API 키가 설정되지 않았습니다. .env 파일이나 Streamlit Secrets를 확인하세요.")
    st.stop()

# Google Gemini API 설정
genai.configure(api_key=API_KEY)

# 페이지 설정
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기본 프롬프트 초기화
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "당신은 친절하고 도움이 되는 AI 비서입니다. 질문에 명확하고 정확하게 답변해 주세요."

# 사이드바에 프롬프트 편집 영역 추가
with st.sidebar:
    st.subheader("프롬프트 설정")
    new_prompt = st.text_area("시스템 프롬프트 수정", st.session_state.system_prompt, height=150)
    if st.button("프롬프트 적용"):
        st.session_state.system_prompt = new_prompt
        st.success("✅ 새 프롬프트가 적용되었습니다!")

# 채팅 기록 지우기 버튼
if st.sidebar.button("채팅 기록 지우기"):
    st.session_state.messages = []
    st.rerun()

# 이전 채팅 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    # 사용자 메시지 표시
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # 모델 설정
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        
        # 고정 프롬프트와 사용자 입력을 합쳐서 전송
        full_prompt = f"{st.session_state.system_prompt}\n\n사용자: {user_input}"
        
        # 채팅 기록이 있는 경우 이전 대화 맥락 추가
        if len(st.session_state.messages) > 1:
            chat_history = ""
            for msg in st.session_state.messages[:-1]:  # 마지막 메시지(방금 입력한 것) 제외
                prefix = "사용자: " if msg["role"] == "user" else "AI: "
                chat_history += f"{prefix}{msg['content']}\n"
            full_prompt = f"{st.session_state.system_prompt}\n\n{chat_history}\n사용자: {user_input}"
        
        response = model.generate_content(full_prompt)
        
        # 봇 응답 표시
        bot_reply = response.text
        st.chat_message("assistant").markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}") 
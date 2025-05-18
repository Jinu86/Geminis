import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="나만의 GPT 챗봇", page_icon="🤖")
st.title("🤖 나만의 프롬프트 기반 Gemini 챗봇")

# API 키 설정 (안전하게 처리)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("❌ API 키 설정 오류가 발생했습니다. Streamlit Secrets에 GOOGLE_API_KEY가 설정되어 있는지 확인하세요.")
    st.stop()

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prompt" not in st.session_state:
    st.session_state.prompt = "당신은 친절한 AI 비서입니다."

# 📍 사이드바 - 프롬프트 입력 및 적용
with st.sidebar:
    st.header("🛠️ 챗봇 역할 설정")
    new_prompt = st.text_area("프롬프트를 입력하세요", value=st.session_state.prompt, height=150)
    if st.button("✅ 프롬프트 적용", use_container_width=True):
        st.session_state.prompt = new_prompt.strip()
        st.session_state.messages = []  # 대화 기록 초기화
        st.success("프롬프트가 적용되었습니다!")
        st.rerun()

# 🎯 현재 설정된 프롬프트 표시
st.info(f"🎯 현재 프롬프트: {st.session_state.prompt}")

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요.")
if user_input:
    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Gemini 응답 처리
    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            try:
                # 모델 설정 및 프롬프트 전송
                model = genai.GenerativeModel("gemini-1.5-pro")
                
                # 전체 대화 내용 구성
                prompt = st.session_state.prompt + "\n\n"
                
                # 이전 대화 내용 추가
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        prompt += f"사용자: {msg['content']}\n"
                    else:
                        prompt += f"AI: {msg['content']}\n"
                
                # 마지막 사용자 메시지는 이미 추가되었으므로 AI 응답만 추가
                prompt += "AI: "
                
                # 응답 생성
                response = model.generate_content(prompt)
                reply = response.text
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}") 
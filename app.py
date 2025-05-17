import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="나만의 GPT 챗봇", page_icon="🤖")
st.title("🤖 나만의 프롬프트 기반 Gemini 챗봇")

# Gemini API 설정
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 세션 초기화
if "chat" not in st.session_state:
    st.session_state.chat = None
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📍 사이드바 - 프롬프트 입력 및 적용
with st.sidebar:
    st.header("🛠️ 챗봇 역할 설정")
    new_prompt = st.text_area("프롬프트를 입력하세요", value=st.session_state.prompt, height=150)
    if st.button("✅ 프롬프트 적용", use_container_width=True):
        if new_prompt.strip():
            st.session_state.prompt = new_prompt.strip()
            st.session_state.messages = []  # 대화 기록 초기화
            
            # 모델 초기화
            model = genai.GenerativeModel("gemini-1.5-pro")
            st.session_state.chat = model.start_chat(
                history=[],
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            
            # 시스템 메시지 전송
            system_msg = f"당신은 다음 지침을 따라야 합니다: {st.session_state.prompt}"
            try:
                st.session_state.chat.send_message(system_msg)
                st.success("프롬프트가 적용되었습니다!")
            except Exception as e:
                st.error(f"프롬프트 적용 중 오류 발생: {e}")
                st.session_state.chat = None
        else:
            st.warning("프롬프트를 입력해주세요.")
        st.rerun()

# 🎯 현재 설정된 프롬프트 표시
if st.session_state.prompt:
    st.info(f"🎯 현재 프롬프트: {st.session_state.prompt}")

# 💬 대화 영역
if st.session_state.chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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
                    response = st.session_state.chat.send_message(user_input)
                    reply = response.text
                except Exception as e:
                    reply = f"❌ 오류 발생: {e}"
                    st.session_state.chat = None  # 오류 발생 시 채팅 세션 초기화
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    st.info("왼쪽 사이드바에서 프롬프트를 설정하고 '프롬프트 적용' 버튼을 눌러주세요.") 
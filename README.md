# Gemini 챗봇

프롬프트 설정이 가능한 Gemini AI 기반 챗봇입니다. 고정 프롬프트를 설정하고 대화 중에도 수정할 수 있습니다.

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. `.env` 파일 생성:
```
GOOGLE_API_KEY=your_api_key_here
```
- Google AI Studio(https://aistudio.google.com/)에서 API 키를 발급받아 입력하세요.

## 실행 방법

```bash
streamlit run app.py
```

## Streamlit Cloud 배포 방법

1. GitHub에 프로젝트를 업로드합니다.
2. [Streamlit Community Cloud](https://streamlit.io/cloud)에 로그인합니다.
3. "New app"을 클릭하고 GitHub 저장소를 연결합니다.
4. 고급 설정에서 secrets를 다음과 같이 설정합니다:
```toml
GOOGLE_API_KEY = "your_api_key_here"
```
5. 배포 버튼을 클릭하여 앱을 배포합니다.

## 주요 기능

- 커스텀 시스템 프롬프트 설정 및 실시간 수정
- 대화 내역 유지 및 초기화
- 사이드바를 통한 설정 관리 
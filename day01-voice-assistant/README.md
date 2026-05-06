# Day 01 — 제이미 (AI 음성 비서)

선글라스 낀 토끼 캐릭터 **제이미**, 한국어로 대화하는 음성 비서 웹 앱.

| Dark Mode | Light Mode |
|-----------|------------|
| ![dark](docs/screenshot-dark.png) | ![light](docs/screenshot-light.png) |

---

## 주요 기능

- 🎙️ **실시간 음성 인식** — 말하는 동안 텍스트가 실시간으로 표시 (Web Speech API)
- 🤖 **GPT-4o-mini 스트리밍 응답** — 토큰 단위로 답변이 흘러나옴
- 🔊 **edge-tts 자동 재생** — 문장 단위로 쪼개서 첫 문장이 빨리 시작됨 (한국어 여성/남성 보이스)
- 🌙 **다크/라이트 모드 토글** — 사이드바에서 즉시 전환
- 🛠️ **비서 커스터마이징** — 이름, 목소리, 성격(시스템 프롬프트) 모두 실시간 변경
- ⌨️ **텍스트 입력 폴백** — 마이크 사용 불가 환경 대비

---

## 기술 스택

| 영역 | 사용 기술 |
|------|----------|
| Web 프레임워크 | Streamlit 1.56 |
| STT (음성→텍스트) | Web Speech API (브라우저 내장, 무료, 한국어 지원) |
| LLM | OpenAI GPT-4o-mini (스트리밍) |
| TTS (텍스트→음성) | edge-tts — Microsoft Edge 음성, 무료, API 키 불필요 |
| 커스텀 컴포넌트 | Streamlit `declare_component` + Web Speech API HTML |
| 자동 음성 재생 | JS Audio Queue (`window.parent.postMessage` + base64 data URL) |

---

## 설치 및 실행

### 사전 요구사항
- Python 3.11+
- OpenAI API 키
- Chrome 브라우저 (Web Speech API 한국어 지원)

### 설치
```bash
pip install -r requirements.txt
```

### API 키 설정
프로젝트 폴더에 `.env` 파일을 만듭니다:
```
OPENAI_API_KEY=sk-...
```

### 실행
```bash
streamlit run app.py
```
브라우저가 자동으로 `http://localhost:8501` 열립니다.

---

## 디렉토리 구조

```
day01-voice-assistant/
├── app.py                       # 메인 Streamlit 앱
├── speech_input/                # 실시간 음성 인식 커스텀 컴포넌트
│   ├── __init__.py              #   Python 래퍼
│   └── index.html               #   Web Speech API + Streamlit 프로토콜
├── jamie_orig.jpg               # 제이미 아바타
├── .streamlit/config.toml       # 다크 테마 설정
├── requirements.txt
├── .env.example
└── docs/                        # 스크린샷
```

---

## 구현 세부

### 1. 실시간 음성 인식 (Web Speech API)
브라우저 내장 음성인식을 커스텀 Streamlit 컴포넌트로 감싸서:
- 말하는 동안 `interimResults`로 흐릿한 텍스트 실시간 표시
- 최종 결과는 보라색으로 확정 표시 후 자동으로 Streamlit으로 전송
- `streamlit:setFrameHeight`, `streamlit:setComponentValue` 메시지로 부모 프레임과 통신

### 2. 스트리밍 + 문장 단위 TTS
GPT 응답을 토큰 단위로 스트리밍하면서:
- 한 문장(`. ? ! 。`)이 완성될 때마다 edge-tts로 합성을 큐에 넣음
- JS Audio 객체로 순서대로 자동 재생
- → 첫 문장 음성이 GPT 응답 완료 전에 시작됨 (체감 속도 개선)

### 3. 다크/라이트 테마 시스템
`.streamlit/config.toml`로 기본 다크 베이스를 깔고, 토글 시 `inject_theme()` 함수가 CSS 오버라이드를 주입.

---

## 개발 회고

**5월 6일 하루 만에 완성한 작업 단위:**
1. CLI 버전 (Whisper + GPT + TTS)
2. Streamlit 웹 앱으로 전환
3. 응답 반복 버그 수정 (오디오 해시로 중복 방지)
4. 자동 재생 + 비서 커스터마이징 + GPT 스트리밍
5. 제이미 SVG 아바타 → 토끼 이미지로 교체
6. 다크/라이트 모드 토글
7. **Web Speech API 커스텀 컴포넌트로 STT 교체** — 가장 어려웠던 부분 (`isStreamlitMessage: true` 필드 빠뜨려서 iframe 0×0 문제 디버깅)

---

## 참고

- RISE사업단 기업문제해결형 AI Intensive Project (2026.05.04 ~ 2026.05.30)
- Day 01 과제: 나만의 AI 음성 비서 만들기

# AI Intensive Project

> 성균관대학교 RISE사업단 — 기업문제해결형 AI Intensive Project
> **기간**: 2026.05.04 ~ 2026.05.30 (총 64시간, 4주)

생성형 AI를 활용한 일별 실습 결과물 모음.

---

## 결과물

| 항목 | 날짜 | 주제 | 디렉토리 | 라이브 |
|---|---|---|---|---|
| Day 01 | 2026-05-06 | AI 음성 비서 제이미 | [day01-voice-assistant/](day01-voice-assistant/) | [streamlit.app](https://ai-intensive-project-eazzk9ccchozhavzngvvwy.streamlit.app/) |
| 팀 프로젝트 | 2026-05-13 ~ 30 | 생활 맥락 로봇청소기 시뮬레이터 (LG 가전 멘토링) | [team-project-lg/](team-project-lg/) | [cleaning-context.vercel.app](https://cleaning-context.vercel.app/) |

---

## Day 01 — 제이미 (AI 음성 비서)

선글라스 낀 토끼가 한국어로 대화하는 음성 비서 웹 앱.

🌐 **라이브 데모**: https://ai-intensive-project-eazzk9ccchozhavzngvvwy.streamlit.app/

![demo](day01-voice-assistant/docs/demo.gif)

- **STT**: Web Speech API (실시간 인식 표시)
- **LLM**: GPT-4o-mini (스트리밍 + Function Calling)
- **TTS**: edge-tts (한국어, 무료)
- **UI**: Streamlit + 다크/라이트 모드 토글
- **도구**: 시간 조회, 계산, 웹 검색(DuckDuckGo), 메모 저장/조회

→ 자세한 설명: [day01-voice-assistant/README.md](day01-voice-assistant/README.md)

---

## 팀 프로젝트 — 생활 맥락 로봇청소기 시뮬레이터

LG전자 가전 멘토링 트랙. 로봇청소기가 시간·날씨·이벤트 같은 상황을 종합해 어디를·언제·어떻게 청소할지 결정하고, 그 이유를 자연어로 설명하는 Physical AI Agent 시뮬레이터.

🌐 **라이브**: https://cleaning-context.vercel.app/

- **백엔드**: FastAPI + Pydantic v2 + scoring engine + LLM (Timely GPT bridge, gpt-4o-mini) + 디스크 캐시
- **프론트**: Next.js 15 + Tailwind v4 + SVG 평면도 + 4 시나리오 + 직접 입력 모드
- **배포**: Render (백) · Vercel (프)
- **팀**: 럭키 금성 — 전유성(팀장)·김준성·박주상

→ 자세한 설명: [team-project-lg/README.md](team-project-lg/README.md)

---

## 작성자

**전유성** · 성균관대학교 글로벌경영학과 · 2019312779

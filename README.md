# AI Intensive Project

> 성균관대학교 RISE사업단 — 기업문제해결형 AI Intensive Project
> **기간**: 2026.05.04 ~ 2026.05.30 (총 64시간, 4주)

생성형 AI를 활용한 일별 실습 결과물 모음.

---

## 일별 결과물

| Day | 날짜 | 주제 | 결과물 |
|-----|------|------|--------|
| 01  | 2026-05-06 | AI 음성 비서 | [day01-voice-assistant/](day01-voice-assistant/) — 제이미 |

---

## Day 01 — 제이미 (AI 음성 비서)

선글라스 낀 토끼가 한국어로 대화하는 음성 비서 웹 앱.

![preview](day01-voice-assistant/docs/screenshot-dark.png)

- **STT**: Web Speech API (실시간 인식 표시)
- **LLM**: GPT-4o-mini (스트리밍 + Function Calling)
- **TTS**: edge-tts (한국어, 무료)
- **UI**: Streamlit + 다크/라이트 모드 토글
- **도구**: 시간 조회, 계산, 웹 검색(DuckDuckGo), 메모 저장/조회

→ 자세한 설명: [day01-voice-assistant/README.md](day01-voice-assistant/README.md)

# AI Intensive Project

> 성균관대학교 RISE사업단 — 기업문제해결형 AI Intensive Project
> **기간**: 2026.05.04 ~ 2026.05.30 (총 64시간, 4주)
> **목적**: 생성형 AI 기초 활용, Agent 기반 프로그래밍, 기업 멘토링 기반 문제 해결, 최종 발표

---

## 일별 결과물

| Day | 날짜 | 주제 | 결과물 |
|-----|------|------|--------|
| 01  | 2026-05-06 | AI 음성 비서 | [day01-voice-assistant/](day01-voice-assistant/) — 제이미 |

> 자세한 일정은 [ROADMAP.md](ROADMAP.md) 참조.

---

## Day 01 — 제이미 (AI 음성 비서)

선글라스 낀 토끼가 한국어로 대화하는 음성 비서.

![preview](day01-voice-assistant/docs/screenshot-dark.png)

- **STT**: Web Speech API (실시간 인식 표시)
- **LLM**: GPT-4o-mini (스트리밍)
- **TTS**: edge-tts (한국어, 무료)
- **UI**: Streamlit + 다크/라이트 모드 토글

→ 자세한 설명: [day01-voice-assistant/README.md](day01-voice-assistant/README.md)

---

## 환경

- Python 3.11+
- Windows 11 / VS Code
- 각 일별 서브프로젝트마다 `requirements.txt` 별도 관리

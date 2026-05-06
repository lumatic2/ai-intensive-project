# ai-intensive-project

> 성균관대 RISE사업단 — 기업문제해결형 AI Intensive Project
> 기간: 2026.05.04 ~ 2026.05.30 (총 64시간, 4주)
> 목적: 생성형 AI 기초/활용, Agent 기반 프로그래밍, 기업 멘토링 기반 문제 해결, 최종 발표

## Tech Stack

- Python 3.11+
- OpenAI API (GPT, Whisper STT, TTS)
- edge-tts (오픈소스 TTS 대안)
- sounddevice / pyaudio (마이크 입력)
- 기타 라이브러리는 각 서브프로젝트 requirements.txt 참조

## Structure

```
ai-intensive-project/
├── CLAUDE.md
├── ROADMAP.md
├── day01-voice-assistant/   # 5/6: AI 음성 비서
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── ...                      # 이후 일별 서브프로젝트 추가
```

## Conventions

- 서브프로젝트 단위: `dayNN-<주제>/` 폴더
- 각 폴더에 `requirements.txt` + 간단한 `README.md`
- OpenAI API 키는 `.env` (gitignore됨), `python-dotenv`로 로드
- 커밋 단위: 일별 완성된 결과물 기준

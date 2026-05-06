import os
import tempfile
import asyncio
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import edge_tts
import pygame

load_dotenv()
client = OpenAI()

SAMPLE_RATE = 16000
CHANNELS = 1
VOICE = "ko-KR-SunHiNeural"
SYSTEM_PROMPT = "당신은 친절하고 유능한 AI 음성 비서입니다. 답변은 간결하게 2~3문장으로 해주세요."


def record_audio(duration: int = 5) -> np.ndarray:
    print(f"  녹음 중... ({duration}초) 말씀하세요!")
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
    )
    sd.wait()
    print("  녹음 완료.")
    return audio


def transcribe(audio: np.ndarray) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
    try:
        wav.write(wav_path, SAMPLE_RATE, audio)
        with open(wav_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="ko",
            )
        return result.text.strip()
    finally:
        os.unlink(wav_path)


def chat(text: str, history: list[dict]) -> str:
    history.append({"role": "user", "content": text})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
    )
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply


async def _synthesize(text: str, path: str) -> None:
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(path)


def speak(text: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        mp3_path = f.name
    try:
        asyncio.run(_synthesize(text, mp3_path))
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
    finally:
        os.unlink(mp3_path)


def main() -> None:
    print("=" * 40)
    print("      AI 음성 비서 (Whisper + GPT)")
    print("=" * 40)
    print("Enter  → 5초 녹음 시작")
    print("숫자   → 녹음 시간(초) 지정 후 녹음")
    print("q      → 종료")
    print()

    history: list[dict] = []

    while True:
        cmd = input("[Enter / 숫자 / q] > ").strip().lower()

        if cmd == "q":
            print("종료합니다.")
            break

        duration = 5
        if cmd.isdigit():
            duration = max(1, min(int(cmd), 30))

        audio = record_audio(duration)
        print("  인식 중...")
        text = transcribe(audio)

        if not text:
            print("  (음성이 인식되지 않았습니다. 다시 시도하세요.)\n")
            continue

        print(f"\n  나    : {text}")

        reply = chat(text, history)
        print(f"  비서  : {reply}\n")

        speak(reply)


if __name__ == "__main__":
    main()

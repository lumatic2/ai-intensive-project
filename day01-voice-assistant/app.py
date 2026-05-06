import os
import re
import base64
import tempfile
import asyncio
import pathlib, shutil
from dotenv import load_dotenv
from openai import OpenAI
import edge_tts
import streamlit as st
import streamlit.components.v1 as components
from speech_input import speech_input

load_dotenv()
client = OpenAI()

VOICES = {
    "여성 (Sun Hi)": "ko-KR-SunHiNeural",
    "남성 (In Joon)": "ko-KR-InJoonNeural",
}
_SENTENCE_SPLIT = re.compile(r"(?<=[.?!。？！])\s+")

import pathlib, shutil
_SRC = pathlib.Path(r"C:\Users\yusun\Desktop\동물 일러스트 레퍼런스\다운로드 (3).jpg")
_JAMIE_PATH = pathlib.Path(__file__).parent / "jamie_orig.jpg"
if not _JAMIE_PATH.exists():
    shutil.copy(_SRC, _JAMIE_PATH)
_JAMIE_B64 = base64.b64encode(_JAMIE_PATH.read_bytes()).decode()
_SVG_DATA_URL = f"data:image/jpeg;base64,{_JAMIE_B64}"

# ── 테마 CSS ──────────────────────────────────────────────────────────

_DARK = {
    "bg":           "#0D0D0D",
    "sidebar":      "#1C1C1E",
    "surface":      "#1F1F21",
    "border":       "#2D2D30",
    "text":         "#E3E3E3",
    "text_muted":   "#8A8A8E",
    "user_msg":     "#1A2744",
    "asst_msg":     "#1C1C1E",
    "input_bg":     "#2D2D30",
    "btn_bg":       "#2D2D30",
    "btn_hover":    "#3A3A3D",
    "accent":       "#6366F1",
}
_LIGHT = {
    "bg":           "#FFFFFF",
    "sidebar":      "#F7F7F8",
    "surface":      "#F0F0F2",
    "border":       "#E0E0E5",
    "text":         "#1F2937",
    "text_muted":   "#6B7280",
    "user_msg":     "#EEF2FF",
    "asst_msg":     "#F9FAFB",
    "input_bg":     "#F3F4F6",
    "btn_bg":       "#F3F4F6",
    "btn_hover":    "#E9E9EC",
    "accent":       "#4F46E5",
}


def inject_theme(dark: bool) -> None:
    c = _DARK if dark else _LIGHT
    st.markdown(
        f"""
        <style>
        /* ── 전체 배경 ── */
        html, body,
        .stApp,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stMain"],
        [data-testid="stBottom"],
        section.main,
        .main .block-container {{
            background-color: {c["bg"]} !important;
            color: {c["text"]} !important;
        }}

        /* ── 헤더/툴바 ── */
        [data-testid="stHeader"],
        [data-testid="stToolbar"] {{
            background-color: {c["bg"]} !important;
            visibility: hidden;
        }}

        /* ── 사이드바 ── */
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {c["sidebar"]} !important;
        }}

        /* ── 기본 텍스트 ── */
        p, span, li, label, div, h1, h2, h3, h4, h5,
        .stMarkdown, .stText, [data-testid="stMarkdownContainer"] {{
            color: {c["text"]} !important;
        }}
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {{
            color: {c["text_muted"]} !important;
        }}

        /* ── 입력 필드 ── */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {{
            background-color: {c["input_bg"]} !important;
            color: {c["text"]} !important;
            border-color: {c["border"]} !important;
            border-radius: 10px !important;
        }}
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {{
            color: {c["text_muted"]} !important;
        }}

        /* ── 셀렉트박스 ── */
        [data-testid="stSelectbox"] > div > div {{
            background-color: {c["input_bg"]} !important;
            color: {c["text"]} !important;
            border-color: {c["border"]} !important;
            border-radius: 10px !important;
        }}

        /* ── 버튼 ── */
        [data-testid="stButton"] > button {{
            background-color: {c["btn_bg"]} !important;
            color: {c["text"]} !important;
            border-color: {c["border"]} !important;
            border-radius: 10px !important;
            transition: background 0.15s;
        }}
        [data-testid="stButton"] > button:hover {{
            background-color: {c["btn_hover"]} !important;
            border-color: {c["accent"]} !important;
        }}

        /* ── 채팅 메시지 ── */
        [data-testid="stChatMessage"] {{
            background-color: {c["asst_msg"]} !important;
            border: 1px solid {c["border"]} !important;
            border-radius: 14px !important;
            margin-bottom: 8px !important;
        }}

        /* ── 스피너 ── */
        [data-testid="stSpinner"] {{
            color: {c["text_muted"]} !important;
        }}

        /* ── 경고 박스 ── */
        [data-testid="stAlert"] {{
            background-color: {c["surface"]} !important;
            border-color: {c["border"]} !important;
        }}

        /* ── hr 구분선 ── */
        hr {{ border-color: {c["border"]} !important; }}

        /* ── audio_recorder 컴포넌트 iframe ── */
        iframe[title="audio_recorder_streamlit.audio_recorder"] {{
            background-color: {c["bg"]} !important;
            border-radius: 12px !important;
            {"filter: invert(1) hue-rotate(180deg);" if not dark else ""}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── 핵심 함수 ─────────────────────────────────────────────────────────

def stream_chat(user_text: str, history: list[dict], system_prompt: str, placeholder):
    history.append({"role": "user", "content": user_text})
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + history,
        stream=True,
    )
    full_reply, sentences, buffer = "", [], ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        full_reply += delta
        buffer += delta
        placeholder.markdown(full_reply + "▌")
        parts = _SENTENCE_SPLIT.split(buffer)
        if len(parts) > 1:
            sentences.extend(p for p in parts[:-1] if p.strip())
            buffer = parts[-1]
    if buffer.strip():
        sentences.append(buffer.strip())
    placeholder.markdown(full_reply)
    history.append({"role": "assistant", "content": full_reply})
    return full_reply, sentences if sentences else [full_reply]


async def _tts_one(text: str, voice: str) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        path = f.name
    await edge_tts.Communicate(text, voice).save(path)
    with open(path, "rb") as f:
        data = f.read()
    os.unlink(path)
    return data


def speak_sentences(sentences: list[str], voice: str) -> list[bytes]:
    async def _all():
        return [await _tts_one(s, voice) for s in sentences]
    return asyncio.run(_all())


def autoplay_queue(audio_list: list[bytes]) -> None:
    srcs = [f"data:audio/mp3;base64,{base64.b64encode(a).decode()}" for a in audio_list]
    srcs_js = str(srcs).replace("'", '"')
    components.html(
        f"""<script>(function(){{
            const srcs={srcs_js}; let i=0;
            function next(){{if(i>=srcs.length)return;
                const a=new Audio(srcs[i++]);a.onended=next;a.play().catch(next);}}
            next();
        }})();</script>""",
        height=0,
    )


# ── 페이지 설정 & 세션 초기화 ─────────────────────────────────────────

st.set_page_config(page_title="제이미", page_icon=_SVG_DATA_URL, layout="centered")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_speech" not in st.session_state:
    st.session_state.last_speech = None

inject_theme(st.session_state.dark_mode)

# ── 사이드바 ──────────────────────────────────────────────────────────

with st.sidebar:
    # 아바타
    st.markdown(
        f'<div style="text-align:center;margin:8px 0 16px">'
        f'<img src="{_SVG_DATA_URL}" width="72"'
        f' style="border-radius:50%;object-fit:cover;aspect-ratio:1"/>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 다크/라이트 토글
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown(
            f'<p style="margin:6px 0 0;font-size:0.85rem;color:{"#8A8A8E" if st.session_state.dark_mode else "#6B7280"}">'
            f'{"🌙 다크 모드" if st.session_state.dark_mode else "☀️ 라이트 모드"}</p>',
            unsafe_allow_html=True,
        )
    with col_r:
        label = "☀️ 라이트" if st.session_state.dark_mode else "🌙 다크"
        if st.button(label, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.divider()
    st.header("🛠️ 비서 설정")
    assistant_name = st.text_input("비서 이름", value="제이미")
    voice_label = st.selectbox("목소리", list(VOICES.keys()))
    voice = VOICES[voice_label]
    system_prompt = st.text_area(
        "성격 / 역할",
        value=(
            f"당신의 이름은 '{assistant_name}'입니다. "
            "친절하고 유능한 AI 음성 비서입니다. "
            "답변은 간결하게 2~3문장으로 해주세요."
        ),
        height=150,
    )
    st.divider()
    st.subheader("⌨️ 텍스트 입력")
    st.caption("마이크가 안 될 때 사용")
    text_input = st.text_area("메시지", height=100, key="text_msg")
    send_btn = st.button("전송", use_container_width=True)


# ── 메인 UI ───────────────────────────────────────────────────────────

c = _DARK if st.session_state.dark_mode else _LIGHT

st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:20px;margin-bottom:4px">
      <img src="{_SVG_DATA_URL}" width="90"
           style="border-radius:50%;object-fit:cover;aspect-ratio:1;
                  box-shadow:0 4px 24px rgba(0,0,0,0.3)"/>
      <div>
        <h1 style="margin:0;font-size:2.4rem;color:{c['text']}">{assistant_name}</h1>
        <p style="margin:0;color:{c['text_muted']};font-size:0.85rem">
          Whisper · GPT-4o-mini · edge-tts ({voice_label})
        </p>
      </div>
    </div>
    <hr style="margin:12px 0 20px 0;border-color:{c['border']}"/>
    """,
    unsafe_allow_html=True,
)

# 대화 히스토리
for msg in st.session_state.messages:
    avatar = _SVG_DATA_URL if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 마이크 영역
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(
        f'<p style="color:{c["text_muted"]};margin:6px 0">'
        f'<b style="color:{c["text"]}">마이크를 클릭하고 말하세요</b> (멈추면 자동 전송)</p>',
        unsafe_allow_html=True,
    )
with col2:
    if st.button("🗑️ 초기화"):
        st.session_state.history = []
        st.session_state.messages = []
        st.session_state.last_speech = None
        st.rerun()

# 실시간 음성 인식 컴포넌트
recognized = speech_input(dark_mode=st.session_state.dark_mode, key="mic")


def process(user_text: str) -> None:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_text)
    with st.chat_message("assistant", avatar=_SVG_DATA_URL):
        placeholder = st.empty()
        reply, sentences = stream_chat(
            user_text, st.session_state.history, system_prompt, placeholder
        )
    with st.spinner("음성 합성 중..."):
        audio_list = speak_sentences(sentences, voice)
    autoplay_queue(audio_list)
    st.session_state.messages.append({"role": "assistant", "content": reply})


# 음성 입력 처리 (중복 방지)
if recognized and recognized != st.session_state.last_speech:
    st.session_state.last_speech = recognized
    process(recognized)

# 텍스트 입력 처리
if send_btn and text_input.strip():
    process(text_input.strip())

"""제이미가 사용하는 도구 (Function Calling) 정의."""
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import math
import streamlit as st


# ── 도구 구현 ────────────────────────────────────────────────────────

def get_current_time(timezone: str = "Asia/Seoul") -> str:
    try:
        now = datetime.now(ZoneInfo(timezone))
    except Exception:
        now = datetime.now(ZoneInfo("Asia/Seoul"))
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return now.strftime(f"%Y년 %m월 %d일 {weekdays[now.weekday()]} %H시 %M분")


def calculate(expression: str) -> str:
    """안전한 수학 계산 (math 함수만 허용)."""
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed.update({"abs": abs, "round": round, "min": min, "max": max})
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"{expression} = {result}"
    except Exception as e:
        return f"계산 오류: {e}"


def search_web(query: str, max_results: int = 3) -> str:
    """DuckDuckGo 웹 검색 (API 키 불필요)."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results, region="kr-kr"))
        if not results:
            return "검색 결과가 없습니다."
        out = []
        for i, r in enumerate(results, 1):
            out.append(f"{i}. {r['title']}\n   {r['body'][:180]}")
        return "\n".join(out)
    except Exception as e:
        return f"검색 실패: {e}"


def remember(key: str, value: str) -> str:
    """세션 메모 저장."""
    if "notes" not in st.session_state:
        st.session_state.notes = {}
    st.session_state.notes[key] = value
    return f"기억했어요: '{key}' = '{value}'"


def recall(key: str = "") -> str:
    """세션 메모 조회."""
    notes = st.session_state.get("notes", {})
    if not notes:
        return "기억하고 있는 게 없어요."
    if not key:
        items = [f"- {k}: {v}" for k, v in notes.items()]
        return "기억하고 있는 것:\n" + "\n".join(items)
    return f"{key}: {notes.get(key, '기억에 없어요.')}"


# ── OpenAI tools 스펙 ────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "현재 날짜와 시각을 반환합니다. 사용자가 시간/날짜/요일을 물어볼 때 사용하세요.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA 타임존 (예: Asia/Seoul, America/New_York). 기본값은 Asia/Seoul",
                        "default": "Asia/Seoul",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "수학 계산을 수행합니다. Python 표현식 형식을 사용하며 math 모듈 함수 사용 가능 (sqrt, sin, cos, pi 등).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "계산할 표현식 (예: '2 + 2', 'sqrt(16) * pi')",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "웹을 검색해 최신 정보를 가져옵니다. 뉴스·날씨·실시간 정보·모르는 사실에 대해 사용하세요.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "검색어"},
                    "max_results": {"type": "integer", "default": 3},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "사용자가 알려준 정보를 기억해둡니다 ('기억해줘', '저장해줘' 등).",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "기억할 항목명 (예: '내 생일')"},
                    "value": {"type": "string", "description": "기억할 내용"},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": "이전에 기억한 정보를 꺼냅니다. key 비우면 전체 목록 반환.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "조회할 항목명 (비우면 전체)"},
                },
            },
        },
    },
]


# ── 디스패처 ─────────────────────────────────────────────────────────

_REGISTRY = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "search_web": search_web,
    "remember": remember,
    "recall": recall,
}


def execute_tool(name: str, args: dict) -> str:
    func = _REGISTRY.get(name)
    if not func:
        return f"알 수 없는 도구: {name}"
    try:
        return str(func(**args))
    except Exception as e:
        return f"도구 실행 오류 ({name}): {e}"

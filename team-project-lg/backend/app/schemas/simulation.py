from typing import Literal

from pydantic import BaseModel

Mode = Literal["normal", "quiet", "delayed", "excluded"]


class ScoreContribution(BaseModel):
    source: str
    label_ko: str
    delta: int


class RoomScore(BaseModel):
    room_id: str
    base: int
    breakdown: list[ScoreContribution]
    final: int
    mode: Mode
    exclusion_reason: str | None = None


class CustomContext(BaseModel):
    current_time: str
    sleep_time: str
    user_location: str | None = None
    active_events: list[str]
    gap_rooms: list[str] = []


class SimulateRequest(BaseModel):
    scenario_id: str | None = None
    custom: CustomContext | None = None


class SimulateResponse(BaseModel):
    scenario_id: str
    context_summary: str
    rooms: list[RoomScore]
    explanation: str
    fallback: bool
    duration_ms: int

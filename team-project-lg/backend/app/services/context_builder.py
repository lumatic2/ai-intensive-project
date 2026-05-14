from dataclasses import dataclass

from app.schemas.event import Event
from app.schemas.scenario import Scenario


@dataclass(frozen=True)
class ScoringContext:
    scenario: Scenario
    resolved_events: tuple[Event, ...]
    gap_rooms: tuple[str, ...]


def build_context(
    scenario_id: str,
    scenarios: dict[str, Scenario],
    events: dict[str, Event],
) -> ScoringContext:
    sc = scenarios[scenario_id]  # KeyError → router에서 404로 변환
    resolved = tuple(events[eid] for eid in sc.active_events)
    return ScoringContext(scenario=sc, resolved_events=resolved, gap_rooms=tuple(sc.gap_rooms))

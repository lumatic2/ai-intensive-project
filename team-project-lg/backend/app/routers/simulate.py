import time

from fastapi import APIRouter, HTTPException

from app.data_loader import load_events, load_rooms, load_rules, load_scenarios
from app.schemas.simulation import SimulateRequest, SimulateResponse
from app.services import cache, llm_explainer
from app.services.context_builder import build_context
from app.services.scoring import compute_scores

router = APIRouter()


@router.post("/simulate", response_model=SimulateResponse)
def simulate(req: SimulateRequest) -> SimulateResponse:
    if not req.scenario_id:
        raise HTTPException(400, "scenario_id required (custom mode is P2)")

    scenarios = load_scenarios()
    if req.scenario_id not in scenarios:
        raise HTTPException(404, f"unknown scenario: {req.scenario_id}")

    t0 = time.perf_counter()
    ctx = build_context(req.scenario_id, scenarios, load_events())
    scores = compute_scores(ctx, load_rooms(), load_rules())

    summary = (
        f"{ctx.scenario.name_ko} · 시각 {ctx.scenario.current_time}"
        f" · 취침예정 {ctx.scenario.sleep_time}"
    )

    key = cache.cache_key(req.scenario_id)
    cached = cache.get(key)
    if cached:
        return SimulateResponse(
            **{**cached, "duration_ms": int((time.perf_counter() - t0) * 1000)}
        )

    explanation, fallback = llm_explainer.generate_explanation(summary, scores)
    response = SimulateResponse(
        scenario_id=req.scenario_id,
        context_summary=summary,
        rooms=scores,
        explanation=explanation,
        fallback=fallback,
        duration_ms=int((time.perf_counter() - t0) * 1000),
    )

    if not fallback:
        payload = response.model_dump()
        payload.pop("duration_ms", None)
        cache.put(key, payload)

    return response

from fastapi import APIRouter

from app.data_loader import load_scenarios

router = APIRouter()


@router.get("/scenarios")
def list_scenarios() -> list[dict]:
    return [
        {
            "id": s.id,
            "name_ko": s.name_ko,
            "description": s.description,
            "current_time": s.current_time,
            "user_location": s.user_location,
        }
        for s in load_scenarios().values()
    ]

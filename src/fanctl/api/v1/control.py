from fastapi import APIRouter, Depends

from ...core.config import get_config
from ...schemas.control import ControlSettings, ControlUpdate
from ...services import fan
from ..deps import require_session

router = APIRouter(prefix="/control", tags=["control"])


@router.get("", response_model=ControlSettings)
async def get_control() -> ControlSettings:
    config = get_config()
    return ControlSettings(
        manual=config.get("control.manual"),
        manual_speed=config.get("control.manual_speed"),
    )


@router.put("", status_code=204)
async def update_control(
    payload: ControlUpdate, _: None = Depends(require_session)
) -> None:
    config = get_config()
    config.set("control.manual", payload.manual)
    config.set("control.manual_speed", payload.manual_speed)
    config.save()

    if payload.manual:
        fan.set_speed(payload.manual_speed)

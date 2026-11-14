from fastapi import APIRouter, Depends

from ...core.config import (
    get_config,
    get_temperature_interval,
    get_temperature_source,
)
from ...schemas.temperature import TemperatureSettings
from ...services import scheduler
from ..deps import require_session

router = APIRouter(prefix="/temperature", tags=["temperature"])


@router.get("", response_model=TemperatureSettings)
async def get_temperature() -> TemperatureSettings:
    return TemperatureSettings(
        source=get_temperature_source(),
        interval=get_temperature_interval(),
    )


@router.put("", status_code=204)
async def update_temperature(
    payload: TemperatureSettings, _: None = Depends(require_session)
) -> None:
    config = get_config()
    config.set("temperature.source", payload.source)
    config.set("temperature.interval", payload.interval)
    config.save()
    scheduler.update_interval(payload.interval)

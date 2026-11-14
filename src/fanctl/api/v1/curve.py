from fastapi import APIRouter, Depends

from ...core.config import DEFAULTS, get_config
from ...schemas.curve import CurveSettings
from ...services.curve import CURVE_KEYS, update_from_config
from ..deps import require_session

router = APIRouter(prefix="/curve", tags=["curve"])


@router.get("", response_model=CurveSettings)
async def get_curve(defaults: bool = False) -> CurveSettings:
    config = get_config()
    return CurveSettings(
        **{
            key: config.get(
                f"curve.{key}", DEFAULTS["curve"][key], from_defaults=defaults
            )
            for key in CURVE_KEYS
        }
    )


@router.put("", status_code=204)
async def update_curve(
    payload: CurveSettings, _: None = Depends(require_session)
) -> None:
    config = get_config()
    for key in CURVE_KEYS:
        config.set(f"curve.{key}", getattr(payload, key))
    config.save()
    update_from_config()

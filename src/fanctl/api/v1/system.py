from fastapi import APIRouter, Depends

from ...core.config import get_config
from ...core.meta import get_version
from ...schemas.system import SystemInfo, SystemUpdate
from ..deps import require_session

router = APIRouter(prefix="/system", tags=["system"])


@router.get("", response_model=SystemInfo)
async def get_system() -> SystemInfo:
    return SystemInfo(title=get_config().get("system.title"), version=get_version())


@router.put("", status_code=204)
async def update_system(
    payload: SystemUpdate, _: None = Depends(require_session)
) -> None:
    config = get_config()
    config.set("system.title", payload.title)
    config.save()

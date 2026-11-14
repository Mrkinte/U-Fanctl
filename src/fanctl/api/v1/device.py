from fastapi import APIRouter

from ...schemas.device import DeviceStatus
from ...services.fan import is_i2c_valid

router = APIRouter(prefix="/device", tags=["device"])


@router.get("", response_model=DeviceStatus)
async def get_device() -> DeviceStatus:
    return DeviceStatus(i2c_valid=is_i2c_valid())

import asyncio
import json

from fastapi import APIRouter
from loguru import logger
from starlette.exceptions import WebSocketException
from starlette.websockets import WebSocket, WebSocketDisconnect

from services.fan_control import get_cpu_temperature, get_auto_speed
from services.session_manager import refresh_session_exp
from utils.config_manager import get_config

router = APIRouter(prefix="/ws", tags=["websocket"])


async def send_device_status(websocket: WebSocket):
    """定时发送设备状态"""
    config = get_config()
    _interval = config.get("control.interval")
    while True:
        try:
            status = {
                "temperature": get_cpu_temperature(),
                "fan_speed": get_auto_speed(),
            }
            await websocket.send_text(json.dumps(status))
        except WebSocketException as e:
            logger.error(e)

        await asyncio.sleep(_interval)


@router.websocket("/info")
async def info(websocket: WebSocket):
    await websocket.accept()
    send_task = asyncio.create_task(send_device_status(websocket))

    try:
        while True:
            data = await websocket.receive_text()
            if data == "heartbeat":
                refresh_session_exp()
    except WebSocketDisconnect:
        pass
    finally:
        send_task.cancel()

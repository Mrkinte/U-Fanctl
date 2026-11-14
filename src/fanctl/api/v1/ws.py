import asyncio

from fastapi import APIRouter
from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from ...core.config import get_temperature_interval
from ...schemas.common import StatusMessage
from ...services import fan
from ...services.session import is_session_valid, refresh_session_exp
from ...services.temperature import get_source, read_temperature

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/status")
async def status(websocket: WebSocket) -> None:
    if not is_session_valid(websocket.cookies.get("session_id")):
        await websocket.close(code=4001)
        return

    await websocket.accept()

    async def _heartbeat() -> None:
        try:
            while True:
                if await websocket.receive_text() == "heartbeat":
                    refresh_session_exp()
        except WebSocketDisconnect:
            pass

    heartbeat_task = asyncio.create_task(_heartbeat())
    try:
        while True:
            message = StatusMessage(
                temperature=read_temperature(),
                fan_speed=fan.get_speed(),
                source=get_source(),
            )
            await websocket.send_text(message.model_dump_json())
            # 每轮重新读取周期，设置变更后无需重连。
            await asyncio.sleep(get_temperature_interval())
    except (WebSocketDisconnect, RuntimeError) as e:
        logger.debug(f"WebSocket closed: {e}")
    finally:
        heartbeat_task.cancel()

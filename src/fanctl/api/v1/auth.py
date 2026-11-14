from fastapi import APIRouter, Depends, Response

from ...core.config import get_config
from ...core.exceptions import RequestException
from ...schemas.auth import LoginRequest, PasswordUpdate
from ...schemas.common import ErrorResponse
from ...services.session import (
    clear_session,
    create_session_id,
    has_active_session,
)
from ..deps import require_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    status_code=204,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def login(payload: LoginRequest, response: Response) -> None:
    config = get_config()
    stored_password = config.get("auth.password")
    if stored_password == "":
        raise RequestException(500, "设置的密码无效")

    if stored_password != payload.password:
        raise RequestException(401, "密码错误")

    if has_active_session():
        raise RequestException(403, "其它设备正在操作")

    session_id = create_session_id()
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=3600,
        path="/",
    )


@router.post("/logout", status_code=204)
async def logout(_: None = Depends(require_session)) -> None:
    clear_session()


@router.get("/session", status_code=204)
async def session(_: None = Depends(require_session)) -> None:
    return None


@router.put("/password", status_code=204, responses={400: {"model": ErrorResponse}})
async def update_password(
    payload: PasswordUpdate, _: None = Depends(require_session)
) -> None:
    config = get_config()
    if payload.old_password != config.get("auth.password"):
        raise RequestException(400, "密码错误")

    config.set("auth.password", payload.new_password)
    config.save()

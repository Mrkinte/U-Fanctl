import datetime

from fastapi import status, APIRouter, Depends, Response
from pydantic import BaseModel

from models.response_schemas import CustomResponse, Result, RequestException
from services.session_manager import (
    get_activate_session_id,
    create_session_id,
    SESSION_TIMEOUT_SECONDS,
    get_activate_session_exp,
    session_expired,
    clear_activate_session_id,
    clear_activate_session_exp,
)
from utils.config_manager import get_config

router = APIRouter(prefix="/auth", tags=["auth"])


class _LoginModel(BaseModel):
    password: str


@router.post("/login")
async def login(login_data: _LoginModel, response: Response):
    config = get_config()
    storage_pwd = config.get("auth.password")
    if storage_pwd == "":
        raise RequestException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="设置的密码无效",
        )

    if storage_pwd != login_data.password:
        raise RequestException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误",
        )

    if (get_activate_session_id() != "") and (
        datetime.datetime.now().timestamp() - get_activate_session_exp()
        < SESSION_TIMEOUT_SECONDS
    ):
        raise RequestException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="其它设备正在操作",
        )

    session_id = create_session_id()
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,  # 禁止 JS 访问，防 XSS
        secure=False,  # 仅 HTTPS 传输
        samesite="strict",  # 防御 CSRF（strict 更严格）
        max_age=3600,  # 过期时间（秒），1小时
        path="/",  # 全站有效
    )
    return CustomResponse(result=Result.SUCCESS, detail="登录成功")


@router.get("/logout")
async def logout(_=Depends(session_expired)):
    clear_activate_session_id()
    clear_activate_session_exp()
    return CustomResponse(result=Result.SUCCESS, detail="退出登录")


@router.get("/login-detection")
async def LoginDetection(_=Depends(session_expired)):
    return CustomResponse(result=Result.SUCCESS)

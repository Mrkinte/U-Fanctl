import datetime
import uuid

from fastapi import status, Cookie

from models.response_schemas import RequestException

SESSION_TIMEOUT_SECONDS: int = 30

_activate_session_id: str = ""
_activate_session_exp: float | int = 0


def refresh_session_exp():
    global _activate_session_exp
    _activate_session_exp = datetime.datetime.now().timestamp()


def create_session_id() -> str:
    global _activate_session_id, _activate_session_exp
    _activate_session_id = str(uuid.uuid4())
    _activate_session_exp = datetime.datetime.now().timestamp()
    return _activate_session_id


def get_activate_session_id() -> str:
    return _activate_session_id


def get_activate_session_exp() -> float | int:
    return _activate_session_exp


def clear_activate_session_id():
    global _activate_session_id
    _activate_session_id = ""


def clear_activate_session_exp():
    global _activate_session_exp
    _activate_session_exp = 0


def session_expired(session_id: str = Cookie(None)):
    """检查session状态以及更新session过期时间"""
    if session_id == "":
        raise RequestException(status_code=status.HTTP_400_BAD_REQUEST)

    if _activate_session_id == "":
        raise RequestException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="会话已过期"
        )

    if _activate_session_id != session_id:
        raise RequestException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="会话已过期"
        )

    if (
        datetime.datetime.now().timestamp() - _activate_session_exp
        >= SESSION_TIMEOUT_SECONDS
    ):
        raise RequestException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="会话已过期"
        )

    refresh_session_exp()

from fastapi import Cookie

from ..core.exceptions import RequestException
from ..services.session import is_session_valid


def require_session(session_id: str | None = Cookie(default=None)) -> None:
    if not is_session_valid(session_id):
        raise RequestException(401, "会话已过期")

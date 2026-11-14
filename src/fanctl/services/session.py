import time
import uuid

SESSION_TIMEOUT_SECONDS = 30

_session_id = ""
_session_exp = 0.0


def create_session_id() -> str:
    global _session_id, _session_exp
    _session_id = str(uuid.uuid4())
    _session_exp = time.time()
    return _session_id


def clear_session() -> None:
    global _session_id, _session_exp
    _session_id = ""
    _session_exp = 0.0


def refresh_session_exp() -> None:
    global _session_exp
    _session_exp = time.time()


def has_active_session() -> bool:
    return bool(_session_id) and time.time() - _session_exp < SESSION_TIMEOUT_SECONDS


def is_session_valid(session_id: str | None) -> bool:
    if not session_id or not _session_id or session_id != _session_id:
        return False
    if time.time() - _session_exp >= SESSION_TIMEOUT_SECONDS:
        return False

    refresh_session_exp()
    return True

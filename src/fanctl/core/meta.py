import tomllib

from .paths import PYPROJECT_PATH

_FALLBACK_VERSION = "0.0.0"
_BANNER_LINES = (
    "                                                                  ",
    "██    ██       ███████  █████  ███    ██  ██████ ████████ ██      ",
    "██    ██       ██      ██   ██ ████   ██ ██         ██    ██      ",
    "██    ██ █████ █████   ███████ ██ ██  ██ ██         ██    ██      ",
    "██    ██       ██      ██   ██ ██  ██ ██ ██         ██    ██      ",
    " ██████        ██      ██   ██ ██   ████  ██████    ██    ███████ ",
    "                                                                  ",
)
_RESET = "\033[0m"
_BOLD = "\033[1m"
_CYAN = "\033[36m"
_GREEN = "\033[32m"


def _project() -> dict:
    try:
        with PYPROJECT_PATH.open("rb") as f:
            return tomllib.load(f).get("project", {})
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def get_version() -> str:
    return str(_project().get("version") or _FALLBACK_VERSION)


def get_description() -> str:
    return str(_project().get("description") or "")


def print_welcome() -> None:
    cyan = _BOLD + _CYAN
    green = _BOLD + _GREEN
    for line in _BANNER_LINES:
        print(f"{cyan}{line}{_RESET}")
    print(f"{green}Version: {get_version()}{_RESET}")
    print(f"{green}description: 一款为万由NAS（HS-201P）开发的风扇控制软件。{_RESET}")
    print(f"{cyan}{_BANNER_LINES[0]}{_RESET}")

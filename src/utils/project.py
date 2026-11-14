import tomllib
from pathlib import Path

version = ""
description = ""

_RESET = "\033[0m"
_BOLD = "\033[1m"
_CYAN = "\033[36m"
_GREEN = "\033[32m"


def print_welcome():
    """打印软件启动欢迎横幅"""
    global version, description
    toml_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        project = data.get("project", {})
    except FileNotFoundError:
        print(f"错误：未找到 pyproject.toml")
        return

    version = project.get("version", "?.?.?")
    description = project.get("description", "")

    C = _BOLD + _CYAN
    I = _BOLD + _GREEN
    R = _RESET

    print(f"{C}                                                                  {R}")
    print(f"{C}██    ██       ███████  █████  ███    ██  ██████ ████████ ██      {R}")
    print(f"{C}██    ██       ██      ██   ██ ████   ██ ██         ██    ██      {R}")
    print(f"{C}██    ██ █████ █████   ███████ ██ ██  ██ ██         ██    ██      {R}")
    print(f"{C}██    ██       ██      ██   ██ ██  ██ ██ ██         ██    ██      {R}")
    print(f"{C} ██████        ██      ██   ██ ██   ████  ██████    ██    ███████ {R}")
    print(f"{C}                                                                  {R}")
    print(f"{I}Version: {version}{R}")
    print(f"{I}description: 一款为万由NAS（HS-201P）开发的风扇控制软件。{R}")
    print(f"{C}                                                                  {R}")

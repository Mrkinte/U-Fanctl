import sys
from pathlib import Path


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


CONFIG_PATH = app_dir() / "config.toml"
LOG_PATH = app_dir() / "log.txt"
WWWROOT_DIR = app_dir() / "wwwroot"
PYPROJECT_PATH = app_dir() / "pyproject.toml"

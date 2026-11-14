import sys
from pathlib import Path


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def resource_dir() -> Path:
    # PyInstaller 6+ 将打包数据放在 _internal 目录（sys._MEIPASS）
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", app_dir()))
    return Path(__file__).resolve().parents[2]


CONFIG_PATH = app_dir() / "config.toml"
LOG_PATH = app_dir() / "log.txt"
WWWROOT_DIR = app_dir() / "wwwroot"
PYPROJECT_PATH = resource_dir() / "pyproject.toml"

import copy
import tomllib
from pathlib import Path
from typing import Any, Optional

import tomli_w
from loguru import logger


class ConfigError(Exception):
    pass


class ConfigManager:
    def __init__(
        self, file_path: str | Path, defaults: Optional[dict[str, Any]] = None
    ) -> None:
        self._file_path = Path(file_path).resolve()
        self._defaults = defaults or {}
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self._file_path.exists():
            try:
                with self._file_path.open("rb") as f:
                    self._data = tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                raise ConfigError(
                    f"Error parsing TOML file {self._file_path}: {e}"
                ) from e
            except OSError as e:
                raise ConfigError(f"Could not read file {self._file_path}: {e}") from e
            logger.info(f"Configuration loaded from {self._file_path}")
            return

        self._data = copy.deepcopy(self._defaults)
        self.save()
        logger.info(
            f"No config file found. Created default config at {self._file_path}"
        )

    def save(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        # 先写临时文件再替换，避免写入中断损坏配置。
        temp_path = self._file_path.with_name(self._file_path.name + ".tmp")
        try:
            temp_path.write_text(tomli_w.dumps(self._data), encoding="utf-8")
            temp_path.replace(self._file_path)
            logger.info(f"Configuration saved to {self._file_path}")
        except OSError as e:
            temp_path.unlink(missing_ok=True)
            raise ConfigError(
                f"Failed to save configuration to {self._file_path}: {e}"
            ) from e

    def get(self, key: str, default: Any = None, from_defaults: bool = False) -> Any:
        node: Any = self._defaults if from_defaults else self._data
        for part in key.split("."):
            if not isinstance(node, dict):
                raise ConfigError(f"Cannot traverse key '{key}': not a table")
            if part not in node:
                return default
            node = node[part]
        return node

    def set(self, key: str, value: Any) -> None:
        keys = key.split(".")
        node = self._data
        for i, part in enumerate(keys[:-1]):
            if part not in node:
                node[part] = {}
            elif not isinstance(node[part], dict):
                raise ConfigError(
                    f"Cannot set '{key}': "
                    f"'{'.'.join(keys[: i + 1])}' already exists and is not a table"
                )
            node = node[part]
        node[keys[-1]] = value


DEFAULTS: dict[str, Any] = {
    "system": {
        "title": "U-NAS",
        "web_port": 3233,
    },
    "auth": {
        "password": "admin",
    },
    "control": {
        "manual": False,
        "manual_speed": 100,
    },
    "curve": {
        "t30": 0,
        "t40": 20,
        "t50": 40,
        "t60": 60,
        "t70": 80,
        "t80": 100,
        "t90": 100,
        "t100": 100,
    },
    "temperature": {
        "source": "cpu",
        "interval": 1,
    },
}

_config_instance: Optional[ConfigManager] = None


def init_config(path: str | Path) -> None:
    global _config_instance
    _config_instance = ConfigManager(path, DEFAULTS)


def get_config() -> ConfigManager:
    if _config_instance is None:
        raise RuntimeError("Configuration not initialized. Call init_config() first.")
    return _config_instance


def get_temperature_interval() -> int:
    config = get_config()
    value = config.get("temperature.interval")
    if value is None:
        value = config.get("control.interval")
    try:
        interval = int(value) if value is not None else 1
    except (TypeError, ValueError):
        return 1
    return max(1, min(60, interval))


def get_temperature_source() -> str:
    source = get_config().get("temperature.source")
    return source if source in ("cpu", "hdd") else "cpu"

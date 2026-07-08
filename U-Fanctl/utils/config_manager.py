import os
from typing import Any, Optional, Dict

import tomllib
import tomli_w
from loguru import logger


class ConfigError(Exception):
    """配置模块自定义异常基类"""

    pass


class ConfigManager:
    """
    TOML 配置管理器

    提供从文件加载、读取、修改、持久化配置等功能。
    键路径使用点号分隔，例如：'database.host' 对应 {'database': {'host': value}}。
    """

    def __init__(self, file_path: str, defaults: Optional[Dict[str, Any]] = None):
        """
        初始化配置管理器并自动加载配置

        :param file_path: TOML 配置文件路径
        :param defaults: 默认配置字典，当文件不存在时使用并保存
        """
        self._file_path = os.path.abspath(file_path)
        self._defaults = defaults or {}
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """
        加载配置文件到内存
        如果文件不存在，则使用默认配置并保存为新文件
        解析错误会抛出 ConfigError
        """
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "rb") as f:
                    self._data = tomllib.load(f)
                logger.info(f"Configuration loaded from {self._file_path}")
            except tomllib.TOMLDecodeError as e:
                raise ConfigError(
                    f"Error parsing TOML file {self._file_path}: {e}"
                ) from e
            except OSError as e:
                raise ConfigError(f"Could not read file {self._file_path}: {e}") from e
        else:
            self._data = self._defaults
            self.save()
            logger.info(
                f"No config file found. Created default config at {self._file_path}"
            )

    def save(self) -> None:
        """
        将当前配置原子写入硬盘
        先写入临时文件，再替换原文件，防止写入中断导致文件损坏
        """
        # 确保目标目录存在
        dir_name = os.path.dirname(self._file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # 序列化为 TOML 格式的字符串
        toml_content = tomli_w.dumps(self._data)

        # 原子写入：先写临时文件，再替换
        temp_path = self._file_path + ".tmp"
        try:
            # 写入临时文件（文本模式，UTF-8）
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(toml_content)
            # 原子替换（兼容 Windows 和 Unix）
            os.replace(temp_path, self._file_path)
            logger.info(f"Configuration saved to {self._file_path}")
        except OSError as e:
            # 清理可能残留的临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise ConfigError(
                f"Failed to save configuration to {self._file_path}: {e}"
            ) from e

    def get(self, key: str, default: Any = None, from_defaults: bool = False) -> Any:
        """
        获取配置值，支持点号分隔的路径（如 'database.host'）。

        :param key: 配置键，支持点号路径
        :param default: 键不存在时返回的默认值
        :param from_defaults: 若为 True，则从默认配置（self._defaults）中获取；
                              若为 False（默认），则从当前运行时配置（self._data）中获取
        :return: 对应的配置值
        :raises ConfigError: 当路径中间节点不是字典时抛出
        """
        node = self._defaults if from_defaults else self._data
        keys = key.split(".")
        try:
            for part in keys:
                if not isinstance(node, dict):
                    raise ConfigError(
                        f"Cannot traverse key '{key}': "
                        f"value at '{'.'.join(keys[:keys.index(part)])}' is not a table"
                    )
                node = node[part]
            return node
        except KeyError:
            return default

    def set(self, key: str, value: Any) -> None:
        """
        通过点号分隔的键路径设置配置值，自动创建中间字典

        :param key: 键路径，如 'ui.font.size'
        :param value: 要设置的值（可以是任何 TOML 支持的类型）
        :raises ConfigError: 如果路径中间存在非字典值，无法继续扩展
        """
        keys = key.split(".")
        if not keys:
            raise ConfigError("Empty key not allowed")
        node = self._data
        for i, part in enumerate(keys[:-1]):
            if part not in node:
                node[part] = {}
            elif not isinstance(node[part], dict):
                raise ConfigError(
                    f"Cannot set '{key}': '{'.'.join(keys[:i+1])}' already exists and is not a table"
                )
            node = node[part]
        node[keys[-1]] = value


# 默认配置
_defaults = {
    "system": {
        "title": "U-NAS",
        "web_port": 3233,
    },
    "auth": {
        "password": "admin",
    },
    "control": {
        "manual": False,  # 手动控制
        "manual_speed": 100,
        "interval": 1,  # 温度采集周期（秒）
    },
    # 自动控制曲线（温度:风扇转速%）
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
}

# 模块级单例对象
_config_instance: Optional[ConfigManager] = None


def init_config(path: str):
    """初始化全局配置（应在程序入口调用一次）"""
    global _config_instance
    _config_instance = ConfigManager(path, _defaults)


def get_config() -> ConfigManager:
    """获取全局配置实例（必须先调用 init_config）"""
    if _config_instance is None:
        raise RuntimeError("Configuration not initialized. Call init_config() first.")
    return _config_instance

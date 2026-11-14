import glob
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import psutil
from loguru import logger

from ..core.config import get_temperature_source

_DISK_PATTERNS = ("/dev/sd[a-z]", "/dev/nvme[0-9]n[0-9]")
_MAX_PLAUSIBLE_TEMPERATURE = 150


def get_source() -> str:
    return get_temperature_source()


def read_temperature() -> float:
    if get_source() == "hdd":
        return _read_hdd_temperature()
    return _read_cpu_temperature()


def _read_cpu_temperature() -> float:
    try:
        sensors = psutil.sensors_temperatures()
    except (AttributeError, NotImplementedError, OSError):
        return -1.0

    for name in ("coretemp", "k10temp"):
        entries = sensors.get(name)
        if entries:
            return float(entries[0].current)

    for entries in sensors.values():
        if entries:
            return float(entries[0].current)

    return -1.0


def _read_hdd_temperature() -> float:
    values = _smartctl_temperatures() or _sysfs_temperatures()
    return max(values) if values else -1.0


def _smartctl_temperatures() -> list[float]:
    smartctl = shutil.which("smartctl")
    if smartctl is None:
        return []

    values: list[float] = []
    for device in _disk_devices():
        value = _smartctl_temperature(smartctl, device)
        if value is not None:
            values.append(value)
    return values


def _disk_devices() -> list[str]:
    devices: list[str] = []
    for pattern in _DISK_PATTERNS:
        devices.extend(sorted(glob.glob(pattern)))
    return devices


def _smartctl_temperature(smartctl: str, device: str) -> float | None:
    try:
        result = subprocess.run(
            [smartctl, "--json", "--attributes", "--nocheck=standby", device],
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as e:
        logger.debug(f"smartctl failed for {device}: {e}")
        return None

    # smartctl 的退出码是位掩码，只要输出的 JSON 可解析就仍然可用。
    try:
        data = json.loads(result.stdout)
    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.debug(f"smartctl returned no parsable JSON for {device}")
        return None

    return _parse_smartctl_temperature(data)


def _parse_smartctl_temperature(data: dict[str, Any]) -> float | None:
    nvme = data.get("nvme_smart_health_information_log") or {}
    value = _plausible_temperature(nvme.get("temperature"))
    if value is not None:
        return value

    temperature = data.get("temperature") or {}
    value = _plausible_temperature(temperature.get("current"))
    if value is not None:
        return value

    table = (data.get("ata_smart_attributes") or {}).get("table") or []
    attributes = {
        item.get("id"): item for item in table if isinstance(item, dict)
    }
    for attribute_id in (194, 190):
        attribute = attributes.get(attribute_id)
        if attribute is None:
            continue
        raw = attribute.get("raw") or {}
        value = _attribute_temperature(raw.get("value"))
        if value is not None:
            return value

    return None


def _plausible_temperature(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if 0 <= number <= _MAX_PLAUSIBLE_TEMPERATURE:
        return number
    return None


def _attribute_temperature(value: Any) -> float | None:
    result = _plausible_temperature(value)
    if result is not None:
        return result

    # 部分 ATA 磁盘把温度与 min/max 打包在同一个整数里，低字节才是当前温度。
    try:
        lowered = int(value) & 0xFF
    except (TypeError, ValueError):
        return None
    return _plausible_temperature(lowered)


def _sysfs_temperatures() -> list[float]:
    values: list[float] = []
    for name_path in glob.glob("/sys/class/hwmon/hwmon*/name"):
        try:
            if Path(name_path).read_text(encoding="utf-8").strip() != "drivetemp":
                continue
            raw = Path(name_path).with_name("temp1_input").read_text(encoding="utf-8")
            values.append(float(raw.strip()) / 1000)
        except (OSError, ValueError) as e:
            logger.debug(f"Failed reading drivetemp sensor {name_path}: {e}")
    return values

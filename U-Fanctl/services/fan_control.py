import os
from collections import deque
from typing import Optional

import psutil
import smbus2
from loguru import logger

from utils.config_manager import get_config

_bus: Optional[smbus2.SMBus] = None
_curve_data = []
_i2c_is_valid = False
_temp_cache = deque(maxlen=5)   # 通过5组历史温度的平均值设置风扇转速

def init_fan_control() -> bool:
    global _bus, _i2c_is_valid
    if os.path.exists("/dev/i2c-0"):
        _bus = smbus2.SMBus(0)
        _i2c_is_valid = True
        return _i2c_is_valid
    return _i2c_is_valid


def set_speed(speed):
    if not _i2c_is_valid:
        return

    act_speed = speed
    if act_speed < 5:
        act_speed = 5  # 维持风扇正常转动的最低转速

    pwm_value = round(255 * act_speed / 100)
    if _bus is not None:
        _bus.write_byte_data(0x54, 0xf0, pwm_value)


def get_cpu_temperature() -> float | int:
    temps = psutil.sensors_temperatures()
    if "coretemp" in temps:
        # Intel CPU
        return temps["coretemp"][0].current
    elif "k10temp" in temps:
        # AMD CPU
        return temps["k10temp"][0].current
    else:
        for entries in temps.values():
            if entries:
                return entries[0].current
        return -1


def get_auto_speed() -> int:
    return round(_bus.read_byte_data(0x54, 0xf0) * 100 / 255)

def get_i2c_status() -> bool:
    return _i2c_is_valid


def regulate_fan_speed():
    config = get_config()
    if config.get("control.manual"):
        return
    if len(_curve_data) == 0:
        update_curve_data()  # 初始化

    temp = get_cpu_temperature()
    _temp_cache.append(temp)
    if _temp_cache:
        temp = sum(_temp_cache) / len(_temp_cache)
    speed = _curve_to_speed(round(temp))
    if temp <= -1:  # 获取温度失败
        speed = 100
    set_speed(speed)


def update_curve_data():
    global _curve_data
    config = get_config()
    speed_values = list(config.get("curve").values())
    _curve_data = [
        # (min_temp, max_temp, min_speed, max_speed)
        (0, 30, 0, speed_values[0]),
        (30, 40, speed_values[0], speed_values[1]),
        (40, 50, speed_values[1], speed_values[2]),
        (50, 60, speed_values[2], speed_values[3]),
        (60, 70, speed_values[3], speed_values[4]),
        (70, 80, speed_values[4], speed_values[5]),
        (80, 90, speed_values[5], speed_values[6]),
        (90, float("inf"), speed_values[6], 100),
    ]


def _curve_to_speed(temp: int) -> int:
    for seg in _curve_data:
        t_min, t_max, s_min, s_max = seg
        if t_min <= temp <= t_max:
            # 线性插值计算转速
            ratio = (temp - t_min) / (t_max - t_min)
            speed = s_min + ratio * (s_max - s_min)
            return min(max(round(speed), 5), 100)  # 限制范围
    return 100  # 默认全速

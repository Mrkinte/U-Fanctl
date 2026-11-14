import time
from collections import deque

from ..core.config import get_config
from . import fan
from .curve import speed_for_temperature
from .temperature import read_temperature

_TEMP_WINDOW = 5
_temp_history: deque[float] = deque(maxlen=_TEMP_WINDOW)


def initialize() -> bool:
    if not fan.init_fan():
        return False

    # 启动时满速运转一次，避免风扇堵转。
    fan.set_speed(100)

    config = get_config()
    if config.get("control.manual"):
        time.sleep(2)
        fan.set_speed(config.get("control.manual_speed"))

    return True


def regulate_once() -> None:
    if get_config().get("control.manual"):
        return

    temperature = read_temperature()
    if temperature < 0:
        fan.set_speed(100)
        return

    _temp_history.append(temperature)
    average = sum(_temp_history) / len(_temp_history)
    fan.set_speed(speed_for_temperature(average))

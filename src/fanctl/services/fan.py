import os
from typing import Any, Optional

from loguru import logger

I2C_DEVICE = "/dev/i2c-0"
I2C_BUS = 0
I2C_ADDRESS = 0x54
PWM_REGISTER = 0xF0
MIN_SPEED = 5

_bus: Optional[Any] = None
_i2c_valid = False


def init_fan() -> bool:
    global _bus, _i2c_valid
    if not os.path.exists(I2C_DEVICE):
        return False

    try:
        import smbus2
    except ImportError:
        logger.warning("smbus2 不可用，i2c 风扇控制已禁用")
        return False

    _bus = smbus2.SMBus(I2C_BUS)
    _i2c_valid = True
    return True


def set_speed(speed: int) -> None:
    if not _i2c_valid or _bus is None:
        return

    act_speed = max(int(speed), MIN_SPEED)
    pwm_value = round(255 * act_speed / 100)
    _bus.write_byte_data(I2C_ADDRESS, PWM_REGISTER, pwm_value)


def get_speed() -> int:
    if not _i2c_valid or _bus is None:
        return -1

    try:
        return round(_bus.read_byte_data(I2C_ADDRESS, PWM_REGISTER) * 100 / 255)
    except OSError as e:
        logger.error(f"Failed to read fan speed: {e}")
        return -1


def is_i2c_valid() -> bool:
    return _i2c_valid

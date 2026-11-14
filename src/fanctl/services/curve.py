from ..core.config import DEFAULTS, get_config

CURVE_KEYS = ("t30", "t40", "t50", "t60", "t70", "t80", "t90", "t100")

_curve: list[tuple[float, float, int, int]] = []


def update_from_config() -> None:
    global _curve
    config = get_config()
    values = [
        int(config.get(f"curve.{key}", DEFAULTS["curve"][key])) for key in CURVE_KEYS
    ]
    _curve = [
        (0, 30, 0, values[0]),
        (30, 40, values[0], values[1]),
        (40, 50, values[1], values[2]),
        (50, 60, values[2], values[3]),
        (60, 70, values[3], values[4]),
        (70, 80, values[4], values[5]),
        (80, 90, values[5], values[6]),
        (90, float("inf"), values[6], 100),
    ]


def speed_for_temperature(temperature: float) -> int:
    if not _curve:
        update_from_config()

    try:
        for t_min, t_max, s_min, s_max in _curve:
            if t_min <= temperature <= t_max:
                ratio = (temperature - t_min) / (t_max - t_min)
                speed = s_min + ratio * (s_max - s_min)
                return min(max(round(speed), 5), 100)
    except (TypeError, ValueError, ZeroDivisionError):
        return 100

    return 100

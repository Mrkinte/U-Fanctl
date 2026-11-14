from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler

from ..core.config import get_temperature_interval
from .controller import regulate_once

_JOB_ID = "fan-regulate"
_scheduler: Optional[BackgroundScheduler] = None


def start() -> None:
    global _scheduler
    if _scheduler is not None:
        return

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        regulate_once,
        "interval",
        seconds=get_temperature_interval(),
        id=_JOB_ID,
        replace_existing=True,
    )
    _scheduler.start()


def update_interval(seconds: int) -> None:
    if _scheduler is None:
        return
    _scheduler.reschedule_job(_JOB_ID, trigger="interval", seconds=seconds)


def shutdown() -> None:
    global _scheduler
    if _scheduler is None:
        return

    _scheduler.shutdown(wait=False)
    _scheduler = None

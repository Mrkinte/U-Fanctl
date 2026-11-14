from typing import Literal

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


class StatusMessage(BaseModel):
    temperature: float
    fan_speed: int
    source: Literal["cpu", "hdd"]

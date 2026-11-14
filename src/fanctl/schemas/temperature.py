from typing import Literal

from pydantic import BaseModel, Field


class TemperatureSettings(BaseModel):
    source: Literal["cpu", "hdd"]
    interval: int = Field(ge=1, le=60)

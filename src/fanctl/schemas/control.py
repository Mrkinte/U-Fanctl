from pydantic import BaseModel, Field


class ControlSettings(BaseModel):
    manual: bool
    manual_speed: int


class ControlUpdate(BaseModel):
    manual: bool
    manual_speed: int = Field(ge=5, le=100)

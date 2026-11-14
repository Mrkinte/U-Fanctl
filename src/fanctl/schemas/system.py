from pydantic import BaseModel, Field


class SystemInfo(BaseModel):
    title: str
    version: str


class SystemUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=32)

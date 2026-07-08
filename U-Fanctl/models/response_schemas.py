from enum import Enum
from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


class Result(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class CustomResponse(BaseModel, Generic[T]):
    result: Result = Result.SUCCESS
    detail: str = ""
    data: Optional[T] = {}


class RequestException(Exception):
    def __init__(self, status_code: int, detail: str = ""):
        self.status_code = status_code
        self.detail = detail

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    password: str


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str = Field(min_length=1, max_length=16, pattern=r"^[A-Za-z0-9]+$")

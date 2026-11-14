from pydantic import BaseModel


class DeviceStatus(BaseModel):
    i2c_valid: bool

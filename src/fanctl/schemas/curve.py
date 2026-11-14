from pydantic import BaseModel, Field, model_validator


class CurveSettings(BaseModel):
    t30: int = Field(ge=0, le=100)
    t40: int = Field(ge=0, le=100)
    t50: int = Field(ge=0, le=100)
    t60: int = Field(ge=0, le=100)
    t70: int = Field(ge=0, le=100)
    t80: int = Field(ge=0, le=100)
    t90: int = Field(ge=0, le=100)
    t100: int = Field(ge=0, le=100)

    @model_validator(mode="after")
    def _check_non_decreasing(self) -> "CurveSettings":
        speeds = [
            getattr(self, key)
            for key in ("t30", "t40", "t50", "t60", "t70", "t80", "t90", "t100")
        ]
        if any(later < earlier for earlier, later in zip(speeds, speeds[1:])):
            raise ValueError("曲线转速必须非递减")
        return self

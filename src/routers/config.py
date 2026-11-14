from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel, Field

from models.response_schemas import CustomResponse, Result
from services.fan_control import set_speed, get_i2c_status, update_curve_data
from utils import project
from utils.config_manager import get_config

get_router = APIRouter(prefix="/config/get", tags=["config"])
set_router = APIRouter(prefix="/config/set", tags=["config"])


class _SystemConfig(BaseModel):
    title: str


class _ControlConfig(BaseModel):
    i2c_is_valid: bool
    manual: bool
    manual_speed: int


class _CurveConfig(BaseModel):
    t30: int
    t40: int
    t50: int
    t60: int
    t70: int
    t80: int
    t90: int
    t100: int


class _PasswordConfig(BaseModel):
    old_password: str
    new_password: str = Field(min_length=1, max_length=16, pattern=r"^[A-Za-z0-9]+$")


@get_router.get("/system")
async def get_system():
    config = get_config()
    json_data = {
        "title": config.get("system.title"),
        "version": project.version,
    }
    return CustomResponse(data=json_data)


@get_router.get("/control")
async def get_control():
    config = get_config()
    json_data = {
        "i2c_is_valid": get_i2c_status(),
        "manual": config.get("control.manual"),
        "manual_speed": config.get("control.manual_speed"),
    }
    return CustomResponse(data=json_data)


@get_router.get("/curve")
async def get_curve(defaults: bool = False):
    config = get_config()
    json_data = {
        "t30": config.get("curve.t30", default=30, from_defaults=defaults),
        "t40": config.get("curve.t40", default=40, from_defaults=defaults),
        "t50": config.get("curve.t50", default=50, from_defaults=defaults),
        "t60": config.get("curve.t60", default=60, from_defaults=defaults),
        "t70": config.get("curve.t70", default=70, from_defaults=defaults),
        "t80": config.get("curve.t80", default=80, from_defaults=defaults),
        "t90": config.get("curve.t90", default=90, from_defaults=defaults),
        "t100": config.get("curve.t100", default=100, from_defaults=defaults),
    }
    return CustomResponse(data=json_data)


@set_router.post("/system")
async def set_system(conf: _SystemConfig):
    try:
        config = get_config()
        config.set("system.title", conf.title)
        config.save()
        return CustomResponse()
    except Exception as e:
        return CustomResponse(result=Result.FAILURE, detail=str(e))


@set_router.post("/control")
async def set_control(conf: _ControlConfig):
    try:
        config = get_config()
        config.set("control.manual", conf.manual)
        config.set("control.manual_speed", conf.manual_speed)
        config.save()
        if conf.manual:
            set_speed(conf.manual_speed)
            logger.info(f"Set fan speed: {conf.manual_speed}")
        return CustomResponse()
    except Exception as e:
        return CustomResponse(result=Result.FAILURE, detail=str(e))


@set_router.post("/curve")
async def set_curve(conf: _CurveConfig):
    try:
        config = get_config()
        config.set("curve.t30", conf.t30)
        config.set("curve.t40", conf.t40)
        config.set("curve.t50", conf.t50)
        config.set("curve.t60", conf.t60)
        config.set("curve.t70", conf.t70)
        config.set("curve.t80", conf.t80)
        config.set("curve.t90", conf.t90)
        config.set("curve.t100", conf.t100)
        config.save()
        update_curve_data()
        return CustomResponse()
    except Exception as e:
        return CustomResponse(result=Result.FAILURE, detail=str(e))


@set_router.post("/password")
async def reset_password(conf: _PasswordConfig):
    config = get_config()
    storage_password = config.get("auth.password")
    if conf.old_password != storage_password:
        return CustomResponse(result=Result.FAILURE, detail="密码错误")

    config.set("auth.password", conf.new_password)
    config.save()
    logger.info("Password reset successfully")
    return CustomResponse()

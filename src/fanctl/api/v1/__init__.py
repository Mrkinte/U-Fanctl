from fastapi import APIRouter

from . import auth, control, curve, device, system, temperature, ws

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(system.router)
api_router.include_router(control.router)
api_router.include_router(curve.router)
api_router.include_router(temperature.router)
api_router.include_router(device.router)
api_router.include_router(ws.router)

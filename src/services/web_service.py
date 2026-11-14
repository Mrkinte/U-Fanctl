from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from models.response_schemas import RequestException, CustomResponse, Result
from routers import websocket, config, auth
from services.session_manager import session_expired

web = FastAPI()

# 跨域中间件
web.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_auth_dependency = [Depends(session_expired)]

# 包含API路由
web.include_router(auth.router, prefix="/api/v1")
web.include_router(websocket.router, prefix="/api/v1", dependencies=_auth_dependency)
web.include_router(config.get_router, prefix="/api/v1")
web.include_router(config.set_router, prefix="/api/v1", dependencies=_auth_dependency)


web.mount("/assets", StaticFiles(directory="wwwroot/assets"), name="assets")


@web.get("/favicon.svg")
async def favicon():
    return FileResponse("wwwroot/favicon.svg")


# 通配路由
@web.get("/{full_path:path}")
async def index():
    return FileResponse("wwwroot/index.html")


@web.exception_handler(RequestException)
async def request_exception_handler(_: Request, exc: RequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content=CustomResponse(
            result=Result.FAILURE,
            detail=exc.detail,
        ).model_dump(),
    )

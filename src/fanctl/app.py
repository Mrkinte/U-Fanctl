from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api.v1 import api_router
from .core.exceptions import register_exception_handlers
from .core.meta import get_version
from .core.paths import WWWROOT_DIR

OPENAPI_TAGS = [
    {"name": "auth", "description": "登录、登出、会话校验与修改密码"},
    {"name": "system", "description": "系统信息与标题设置"},
    {"name": "control", "description": "手动/自动风扇控制"},
    {"name": "curve", "description": "温度-转速曲线"},
    {"name": "temperature", "description": "温度源与采集周期"},
    {"name": "device", "description": "设备状态"},
    {"name": "websocket", "description": "WebSocket 状态推送"},
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="U-Fanctl API",
        version=get_version(),
        description="万由 NAS 风扇控制服务的 HTTP 与 WebSocket 接口。",
        docs_url="/api/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
        openapi_tags=OPENAPI_TAGS,
    )
    register_exception_handlers(app)
    app.include_router(api_router, prefix="/api/v1")

    assets_dir = WWWROOT_DIR / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    favicon_path = WWWROOT_DIR / "favicon.svg"
    if favicon_path.is_file():

        @app.get("/favicon.svg", include_in_schema=False)
        async def favicon() -> FileResponse:
            return FileResponse(favicon_path)

    index_path = WWWROOT_DIR / "index.html"

    # 注册全部方法，避免未知 API 路径因 GET-only 兜底而返回 405
    @app.api_route(
        "/{full_path:path}",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        include_in_schema=False,
    )
    async def spa_fallback(request: Request, full_path: str) -> FileResponse:
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        if request.method != "GET":
            raise HTTPException(status_code=405)
        if not index_path.is_file():
            raise HTTPException(status_code=404)
        return FileResponse(index_path)

    return app

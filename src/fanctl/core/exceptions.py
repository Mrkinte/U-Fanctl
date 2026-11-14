from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class RequestException(Exception):
    def __init__(self, status_code: int, detail: str = "") -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestException)
    async def _request_exception_handler(
        _: Request, exc: RequestException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

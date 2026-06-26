from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from exceptions.base import BaseAppException
from logging import getLogger

logger = getLogger("jsl_app")

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAppException)
    async def custom_app_exception_handler(request: Request, exc: BaseAppException):
        logger.error(f"AppException: {exc.error_code} - {exc.message} on path {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.error_code, "message": exc.message}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception: {str(exc)} on path {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={"error_code": "INTERNAL_ERROR", "message": "An unexpected error occurred."}
        )

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions.base import BaseApplicationException
from shared.error_responses import ErrorResponse, ValidationErrorDetail
from shared.error_codes import ErrorCode
from shared.context import get_request_id, get_correlation_id
from logging import getLogger
import traceback

logger = getLogger("ExceptionHandler")

def setup_exception_handlers(app: FastAPI):
    
    @app.exception_handler(BaseApplicationException)
    async def custom_app_exception_handler(request: Request, exc: BaseApplicationException):
        # Log the error. If it's a 5xx error, log as ERROR, else INFO or WARNING
        log_msg = f"{exc.error_code} - {exc.title}: {exc.message} on path {request.url.path}"
        if exc.status_code >= 500:
            logger.error(log_msg)
        else:
            logger.info(log_msg)
            
        response = ErrorResponse(
            status_code=exc.status_code,
            error_code=exc.error_code,
            title=exc.title,
            user_message=exc.message,
            developer_message=exc.developer_message, # Only if provided
            request_id=get_request_id(),
            correlation_id=get_correlation_id(),
            path=request.url.path,
            validation_errors=exc.validation_errors
        )
        return JSONResponse(status_code=exc.status_code, content=response.model_dump(exclude_none=True))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.info(f"Validation Error on path {request.url.path}")
        
        validation_details = []
        for error in exc.errors():
            validation_details.append(
                ValidationErrorDetail(
                    loc=[str(x) for x in error.get("loc", [])],
                    msg=error.get("msg", ""),
                    type=error.get("type", "")
                ).model_dump()
            )
            
        response = ErrorResponse(
            status_code=422,
            error_code=ErrorCode.UNPROCESSABLE,
            title="Unprocessable Entity",
            user_message="The request payload is invalid or malformed.",
            request_id=get_request_id(),
            correlation_id=get_correlation_id(),
            path=request.url.path,
            validation_errors=validation_details
        )
        return JSONResponse(status_code=422, content=response.model_dump(exclude_none=True))

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.critical(f"Unhandled Exception: {str(exc)} on path {request.url.path}\n{traceback.format_exc()}")
        
        response = ErrorResponse(
            status_code=500,
            error_code=ErrorCode.INTERNAL_ERROR,
            title="Internal Server Error",
            user_message="An unexpected system error occurred. Our engineers have been notified.",
            request_id=get_request_id(),
            correlation_id=get_correlation_id(),
            path=request.url.path
        )
        # Note: We NEVER expose the stack trace in the JSONResponse for security reasons.
        return JSONResponse(status_code=500, content=response.model_dump(exclude_none=True))

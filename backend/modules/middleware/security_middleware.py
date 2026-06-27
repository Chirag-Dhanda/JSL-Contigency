from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.datastructures import MutableHeaders
from core.di import container
from modules.security.rate_limiter import RateLimiter
from modules.security.headers import SECURITY_HEADERS
from modules.validation.sanitizer import InputSanitizer
from logging import getLogger
from urllib.parse import urlencode, parse_qsl

from exceptions.base import BaseApplicationException
from fastapi.responses import JSONResponse
from shared.error_responses import ErrorResponse
from shared.context import get_request_id, get_correlation_id

logger = getLogger("SecurityMiddleware")

class EnterpriseSecurityMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        
        # 1. Rate Limiting (Mock IP extraction)
        client_ip = request.client.host if request.client else "127.0.0.1"
        try:
            limiter = container.resolve(RateLimiter)
            await limiter.check_rate_limit(client_ip)
        except BaseApplicationException as e:
            # Return JSONResponse directly since this is outside the endpoint router
            resp = ErrorResponse(
                status_code=e.status_code,
                error_code=e.error_code,
                title=e.title,
                user_message=e.message,
                request_id=get_request_id(),
                correlation_id=get_correlation_id(),
                path=request.url.path
            )
            return JSONResponse(status_code=e.status_code, content=resp.model_dump(exclude_none=True))
            
        # 2. Query Parameter Sanitization (XSS / SQLi protection)
        if request.url.query:
            sanitizer = container.resolve(InputSanitizer)
            # Parse, sanitize, and reconstruct
            query_items = parse_qsl(request.url.query, keep_blank_values=True)
            sanitized_items = [(k, sanitizer.sanitize_string(v)) for k, v in query_items]
            
            # This is a bit of a hack to mutate the request scope in Starlette
            new_query = urlencode(sanitized_items).encode("utf-8")
            request.scope["query_string"] = new_query
            
        # 3. Process Request
        response = await call_next(request)
        
        # 4. Inject Security Headers
        headers = MutableHeaders(raw=response.headers.raw)
        for header, value in SECURITY_HEADERS.items():
            headers[header] = value
            
        return response

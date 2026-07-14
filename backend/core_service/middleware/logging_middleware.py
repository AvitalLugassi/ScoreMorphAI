import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("core_service")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000

        request_id = getattr(request.state, "request_id", "-")
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"→ {response.status_code} ({duration:.1f}ms)"
        )
        return response

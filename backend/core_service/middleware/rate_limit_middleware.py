import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# Max attempts per window per IP
RATE_LIMIT_ROUTES = {"/auth/login", "/auth/register"}
MAX_ATTEMPTS = 10
WINDOW_SECONDS = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._attempts: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in RATE_LIMIT_ROUTES:
            return await call_next(request)

        ip  = request.client.host
        key = f"{ip}:{request.url.path}"
        now = time.time()

        # Keep only attempts within the current window
        self._attempts[key] = [t for t in self._attempts[key] if now - t < WINDOW_SECONDS]

        if len(self._attempts[key]) >= MAX_ATTEMPTS:
            return JSONResponse(
                status_code=429,
                content={"detail": f"Too many attempts. Try again in {WINDOW_SECONDS} seconds."},
            )

        self._attempts[key].append(now)
        return await call_next(request)

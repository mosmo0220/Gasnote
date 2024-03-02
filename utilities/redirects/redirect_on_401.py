"""401 middleware"""
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

class RedirectOn401Middleware(BaseHTTPMiddleware):
    """Application middleware to redirect 401 respondes to login page"""
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        if response.status_code == 401:
            return RedirectResponse("/login", status_code=303)
        return response

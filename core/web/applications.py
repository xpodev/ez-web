from typing import TYPE_CHECKING

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware


if TYPE_CHECKING:
    from sandbox.host import AppHost


class EZMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, host: "AppHost"):
        super().__init__(app)
        self.host = host

    async def dispatch(self, request, call_next):
        with self.host.application(self.app):
            return await call_next(request)


class EZWebApplication(Starlette):
    def __init__(self, app_host: "AppHost"):
        Starlette.__init__(self)
        self.app_host = app_host

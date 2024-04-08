from typing import TYPE_CHECKING

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware

from sandbox.applications import Application
from sandbox.security.permission import PermissionSet

from .router import EZRouter

if TYPE_CHECKING:
    from sandbox.host import AppHost


class EZMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, host: "AppHost"):
        super().__init__(app)
        self.host = host

    async def dispatch(self, request, call_next):
        with self.host.application(self.app):
            return await call_next(request)


class EZWebApplication(Application, Starlette):
    ez_router: EZRouter

    def __init__(self, app_host: "AppHost"):
        super().__init__("web", PermissionSet())
        Starlette.__init__(self)
        self.app_host = app_host
        self._initialize()

    def _initialize(self):
        self.ez_router = EZRouter()
        self.mount("/", self.ez_router)

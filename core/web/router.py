from functools import wraps
from inspect import iscoroutinefunction
from typing import Awaitable

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Router


class EZRouter(Router):
    def add_router(self, route: str, router):
        self.mount(route, router)

    def _decorator(self, route: str, methods: list[str], **kwargs):
        def decorator(func):
            from ez import lowlevel

            host = lowlevel.APP_HOST
            current_app = host.current_application

            @wraps(func)
            async def wrapper(request: Request) -> Awaitable[Response]:
                with host.application(current_app):
                    if iscoroutinefunction(func):
                        return await func(request)
                    return func(request)

            self.add_route(route, wrapper, methods=methods, **kwargs)
            return func

        return decorator

    def get(self, route: str, **kwargs):
        return self._decorator(route, ["GET"], **kwargs)
    
    def post(self, route: str, **kwargs):
        return self._decorator(route, ["POST"], **kwargs)
    
    def put(self, route: str, **kwargs):
        return self._decorator(route, ["PUT"], **kwargs)
    
    def delete(self, route: str, **kwargs):
        return self._decorator(route, ["DELETE"], **kwargs)
    
    def patch(self, route: str, **kwargs):
        return self._decorator(route, ["PATCH"], **kwargs)
    
    def options(self, route: str, **kwargs):
        return self._decorator(route, ["OPTIONS"], **kwargs)
    
    def head(self, route: str, **kwargs):
        return self._decorator(route, ["HEAD"], **kwargs)
    
    def trace(self, route: str, **kwargs):
        return self._decorator(route, ["TRACE"], **kwargs)
    
    def connect(self, route: str, **kwargs):
        return self._decorator(route, ["CONNECT"], **kwargs)
    
    def all(self, route: str, **kwargs):
        return self._decorator(route, ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"], **kwargs)

from http import HTTPStatus
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.routing import BaseRoute
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..response import _EzResponse
from .events import App
from ..events import HTTP


docs_urls = [
            "/docs",
            "/redoc",
            "/openapi.json",
        ]

STATIC_PATH = "/static"

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        import ez

        ez.request = request
        ez.response = _EzResponse()

        ez.emit(HTTP.In, request)

        result = await call_next(request)

        route = request.scope.get("endpoint")
        if not route or not getattr(route, ez.EZ_ROUTE_ATTRIBUTE, False):
            return result
        

        ez.emit(HTTP.Out, ez.response)

        return Response(
            content=ez.response.body,
            headers=ez.response.headers,
            status_code=ez.response.status_code,
        )


class EZApplication(FastAPI):
    def setup(self):
        import ez

        self.add_middleware(RequestContextMiddleware)
        self.mount(STATIC_PATH, StaticFiles(directory="public", html=True), name="static")
        self.exception_handler(Exception)(self._exception_handler)
        self.add_event_handler("startup", lambda: ez.emit(App.DidStart))
        self.add_event_handler("shutdown", lambda: ez.emit(App.WillStop))

    def _exception_handler(self, request: Request, exc: Exception):
        """
        Handles exceptions in the FastAPI app.
        """
        import ez
        import traceback

        tb = reversed(traceback.format_tb(exc.__traceback__))
        
        ez.response.text(str(exc) + '\n' + "".join(tb))

        return Response(
            content=ez.response.body,
            headers=ez.response.headers,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    
    def remove_routes_by(self, filter: Callable[[BaseRoute], bool]):
        self.routes = [route for route in self.routes if filter(route)]

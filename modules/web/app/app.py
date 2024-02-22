from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.routing import BaseRoute
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..response import EZResponse
from .events import App
from ..events import HTTP


STATIC_PATH = "/static"


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        import ez

        ez.request = request
        ez.response = EZResponse()

        ez.emit(HTTP.In, request)

        response = await call_next(request)

        route = request.scope.get("endpoint")
        if not route or not getattr(route, ez.EZ_ROUTE_ATTRIBUTE, False):
            return response

        if response.status_code >= 400:
            if not hasattr(response, "body"):
                return response

            ez.response.status(response.status_code).header(
                "Content-Type", response.media_type or "text/plain"
            )._auto_body(response.body)
            ez.emit(HTTP.Error, ez.response)

        ez.emit(HTTP.Out, ez.response)

        return ez.response()


class EZApplication(FastAPI):
    def setup(self):
        import ez

        self.add_middleware(RequestContextMiddleware)
        self.mount(
            STATIC_PATH, StaticFiles(directory="public", html=True), name="static"
        )
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

        ez.response.text(str(exc) + "\n" + "".join(tb))

        return ez.response()

    def remove_routes_by(self, filter: Callable[[BaseRoute], bool]):
        self.routes = [route for route in self.routes if filter(route)]

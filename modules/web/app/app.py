from fastapi import FastAPI, Request, Response
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
        if not route or not hasattr(route, ez.EZ_ROUTE_ATTRIBUTE) or not getattr(route, ez.EZ_ROUTE_ATTRIBUTE):
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
        
        return str(exc)

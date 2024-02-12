from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ez.web.response import _EzResponse
from ez.events import HTTP, App


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

        if request.url.path in docs_urls:
            return await call_next(request)
        
        if request.url.path.startswith("/socket.io"):
            return await call_next(request)

        if request.url.path == STATIC_PATH or request.url.path.startswith(
            f"{STATIC_PATH}/"
        ):
            result = await call_next(request)
            if result.status_code < 400:
                return result

        ez.request = request
        ez.response = _EzResponse()
        ez.emit(HTTP.In, request)

        result = await call_next(request)
        if 300 <= result.status_code < 400:
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

        return ez.response.text(str(exc))

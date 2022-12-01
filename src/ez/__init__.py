from typing import Callable
from fastapi import FastAPI, Request, Response
import uvicorn
from pyee import EventEmitter
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ez.ez_response import response
from ez.events import Plugins
from ez.events import HTTP


class _Ez(EventEmitter):
    def __init__(self):
        super().__init__()
        self.response = response
        self.request: Request = None
        self._setup()

    def add_route(self, route: str, handler: Callable):
        """
        Adds a route to the FastAPI app.
        """
        self._app.add_api_route(route, endpoint=handler)

    def run(self, **kwargs):
        """
        Runs the FastAPI app.
        """
        self._run(**kwargs)

    def _run(self, **kwargs):
        uvicorn.run(self._app, **kwargs)

    def _setup(self):
        """
        Sets up the FastAPI app.
        """
        docs_urls = [
            "/docs",
            "/redoc",
            "/openapi.json",
        ]

        class RequestContextMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
                if request.url.path in docs_urls:
                    return await call_next(request)

                Ez.request = request
                Ez.emit(HTTP.In, request)

                response = await call_next(request)
                Ez.emit(HTTP.Out, response)

                return Response(
                    content=Ez.response._body,
                    headers=Ez.response._headers,
                    status_code=Ez.response._status_code
                )

        self._app.add_middleware(RequestContextMiddleware)

    def _add_event_handler(self, event: str, k: Callable, v: Callable):
        """
        Overrides the EventEmitter._add_event_handler method to add a `on_deactivate` event handler to plugins.
        """
        current_plugin = _Ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.current_plugin

        def on_plugin_disabled(plugin: str):
            if plugin == current_plugin:
                self.remove_listener(event, k)
                self.remove_listener(Plugins.Disabled, on_plugin_disabled)

        super()._add_event_handler(Plugins.Disabled, on_plugin_disabled, on_plugin_disabled)
        return super()._add_event_handler(event, k, v)

    @property
    def _app(self):
        return _Ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.current_app

    class __INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__:
        current_plugin: str = None
        current_app = FastAPI()


Ez = _Ez()

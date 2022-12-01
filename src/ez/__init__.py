from typing import Callable
from fastapi import FastAPI, Request, Response
import uvicorn
from pyee import EventEmitter
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ez.ez_response import _EzResponse
from ez.events import Plugins
from ez.events import HTTP


class _Ez(EventEmitter):
    def __init__(self):
        super().__init__()
        self.response: _EzResponse = None
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
                Ez.response = _EzResponse()
                Ez.emit(HTTP.In, request)

                await call_next(request)
                Ez.emit(HTTP.Out, Ez.response)

                return Response(
                    content=Ez.response.body,
                    headers=Ez.response.headers,
                    status_code=Ez.response.status_code
                )

        self._app.add_middleware(RequestContextMiddleware)

    def _add_event_handler(self, event: str, k: Callable, v: Callable):
        """
        Overrides the EventEmitter._add_event_handler method to add a `on_deactivate` event handler to plugins.
        """
        current_plugin = _Ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.currently_loaded_plugin

        def remove_plugin_handler(plugin: str):
            if plugin == current_plugin:
                # Necessary for once() to work
                if event in self._events:
                    self.remove_listener(event, k)

                self.remove_listener(Plugins.Disabled, remove_plugin_handler)

        super()._add_event_handler(Plugins.Disabled, remove_plugin_handler, remove_plugin_handler)
        super()._add_event_handler(Plugins.Reloaded, remove_plugin_handler, remove_plugin_handler)
        return super()._add_event_handler(event, k, v)


    # Methods
    def get(self, route: str):
        """
        Adds a GET route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(route, endpoint=handler, methods=["GET"])
        return decorator

    def post(self, route: str):
        """
        Adds a POST route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(route, endpoint=handler, methods=["POST"])
        return decorator

    def put(self, route: str):
        """
        Adds a PUT route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(route, endpoint=handler, methods=["PUT"])
        return decorator

    def delete(self, route: str):
        """
        Adds a DELETE route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(
                route, endpoint=handler, methods=["DELETE"])
        return decorator

    def patch(self, route: str):
        """
        Adds a PATCH route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(route, endpoint=handler, methods=["PATCH"])
        return decorator

    def options(self, route: str):
        """
        Adds a OPTIONS route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(
                route, endpoint=handler, methods=["OPTIONS"])
        return decorator

    def head(self, route: str):
        """
        Adds a HEAD route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(route, endpoint=handler, methods=["HEAD"])
        return decorator

    def trace(self, route: str):
        """
        Adds a TRACE route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(route, endpoint=handler, methods=["TRACE"])
        return decorator

    def connect(self, route: str):
        """
        Adds a CONNECT route to the FastAPI app.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(
                route, endpoint=handler, methods=["CONNECT"])
        return decorator

    def all(self, route: str):
        """
        Adds a route to the FastAPI app that accepts any HTTP method.

        :param route: The route to add.
        """
        def decorator(handler: Callable):
            self._app.add_api_route(route, endpoint=handler, methods=[
                                    "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"])
        return decorator

    @property
    def _app(self):
        return _Ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.current_app

    class __INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__:
        currently_loaded_plugin: str = None
        current_app = FastAPI()


Ez = _Ez()

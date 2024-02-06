from functools import wraps
import sys
from typing import Callable
from fastapi import APIRouter, FastAPI, Request, Response
import uvicorn
from pyee import EventEmitter
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ez.ez_response import _EzResponse
from ez.events import App, Plugins, HTTP
from .ez_router import _EzRouter
import ez.log as log

# from .ez_router import EzRouter


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
        self._app.add_event_handler("startup", self.emit, App.DidStart)
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
            async def dispatch(
                self, request: Request, call_next: RequestResponseEndpoint
            ):
                if request.url.path in docs_urls:
                    return await call_next(request)

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

        self._app.add_middleware(RequestContextMiddleware)
        self._app.exception_handler(Exception)(self._exception_handler)
        self._app.add_event_handler("startup", lambda: self.emit(App.DidStart))
        self._app.add_event_handler("shutdown", lambda: self.emit(App.WillStop))

    def _add_event_handler(self, event: str, k: Callable, v: Callable):
        """
        Overrides the EventEmitter._add_event_handler method to add a `on_deactivate` event handler to plugins.
        """
        current_plugin = (
            _Ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.currently_loaded_plugin
        )

        def remove_plugin_handler(plugin: str):
            if plugin == current_plugin:
                # Necessary for once() to work
                if event in self._events:
                    self.remove_listener(event, k)

                self.remove_listener(Plugins.Disabled, remove_plugin_handler)

        super()._add_event_handler(
            Plugins.Disabled, remove_plugin_handler, remove_plugin_handler
        )
        super()._add_event_handler(
            Plugins.Reloaded, remove_plugin_handler, remove_plugin_handler
        )
        return super()._add_event_handler(event, k, v)

    def _exception_handler(self, request: Request, exc: Exception):
        """
        Handles exceptions in the FastAPI app.
        """
        return ez.response.text(str(exc))

    # region: Methods
    def get(self, route: str):
        """
        Adds a GET route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["GET"])

    def post(self, route: str):
        """
        Adds a POST route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["POST"])

    def put(self, route: str):
        """
        Adds a PUT route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["PUT"])

    def delete(self, route: str):
        """
        Adds a DELETE route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["DELETE"])

    def patch(self, route: str):
        """
        Adds a PATCH route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["PATCH"])

    def options(self, route: str):
        """
        Adds a OPTIONS route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["OPTIONS"])

    def head(self, route: str):
        """
        Adds a HEAD route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["HEAD"])

    def trace(self, route: str):
        """
        Adds a TRACE route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["TRACE"])

    def connect(self, route: str):
        """
        Adds a CONNECT route to the FastAPI app.

        :param route: The route to add.
        """
        return self._route(route, ["CONNECT"])

    def all(self, route: str):
        """
        Adds a route to the FastAPI app that accepts any HTTP method.

        :param route: The route to add.
        """
        return self._route(
            route,
            [
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "PATCH",
                "OPTIONS",
                "HEAD",
                "TRACE",
                "CONNECT",
            ],
        )

    def _route(self, route: str, methods: list[str]):
        """
        Adds a route to the FastAPI app.

        :param route: The route to add.
        :param methods: The methods to allow.
        """

        def decorator(handler: Callable):
            @wraps(handler)
            def wrapper(*args, **kwargs):
                result = handler(*args, **kwargs)
                match result:
                    case dict() | list() | int() | float() | bool():
                        return self.response.json(result)
                    case str():
                        return self.response.text(result)
                    case _:
                        self.response._body = result
                        return self.response

            log.debug(f"{methods} {route} -> {handler.__name__}")
            self._app.add_api_route(route, endpoint=wrapper, methods=methods)

        return decorator

    # endregion

    def router(self, prefix=""):
        """
        Creates a router.

        :param prefix: The prefix to add to the router.
        """
        return _EzRouter(prefix=prefix)

    def add_router(self, router: APIRouter):
        """
        Adds a router to the FastAPI app.

        :param router: The router to add.
        """
        self._app.include_router(router)

    def include_path(self, path: str):
        """
        Get the include path of the app
        """
        return f"include/{path}"

    @property
    def _app(self) -> FastAPI:
        return _Ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.current_app

    class __INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__:
        currently_loaded_plugin: str = None
        current_app = FastAPI(redirect_slashes=True)

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return getattr(__original_import__, name)


ez = _Ez()
__original_import__ = sys.modules[__name__]
sys.modules[__name__] = ez

__annotations__ = _Ez.__annotations__  # can we remove this?

import include.plugins_loader
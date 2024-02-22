from typing import Any, Awaitable, Callable, TypeAlias
from fastapi.routing import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from inspect import iscoroutinefunction
from functools import wraps

from .response import EZResponse
from .app.app import EZ_ROUTE_ATTRIBUTE

MiddlewareFunction: TypeAlias = Callable[[Request, EZResponse, Callable], None]


class EZRouter(APIRouter):
    def __init__(self, middleware: list[MiddlewareFunction] = None, *args, **kwargs):
        self.middleware = middleware
        self._current_middleware = 0
        super().__init__(*args, **kwargs)

    def add_route(
        self,
        path: str,
        endpoint: Callable[[Request], Awaitable[Response] | Response],
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
        **kwargs: Any,
    ) -> None:
        if path == "/":
            path = ""       

        super().add_route(
            path,
            self._make_wrapper(endpoint),
            methods,
            name,
            include_in_schema,
        )

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        include_in_schema: bool = True,
        **kwargs: Any,
    ) -> None:
        super().add_api_route(
            path,
            self._make_wrapper(endpoint),
            include_in_schema=include_in_schema,
            **kwargs,
        )

    def _make_wrapper(
        self,
        endpoint: Callable[..., Any],
    ):
        import ez


        if iscoroutinefunction(endpoint):

            @wraps(endpoint)
            async def wrapper(*args, **kwargs):
                result = await endpoint(*args, **kwargs)
                ez.response._auto_body(result)
        else:

            @wraps(endpoint)
            def wrapper(*args, **kwargs):
                result = endpoint(*args, **kwargs)
                ez.response._auto_body(result)

        return_endpoint = wrapper

        if self.middleware:
            i = -1

            def next_middleware():
                nonlocal i
                i += 1
                if i < len(self.middleware):
                    self.middleware[i](ez.request, ez.response, next_middleware)
                else:
                    wrapper(ez.request)
                    i = -1

            return_endpoint = next_middleware

        setattr(return_endpoint, EZ_ROUTE_ATTRIBUTE, True)
        return return_endpoint

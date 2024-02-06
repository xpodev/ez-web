from typing import Any, Awaitable, Callable, TypeAlias
from fastapi.routing import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from ez.ez_response import _EzResponse

MiddlewareFunction: TypeAlias = Callable[[Request, _EzResponse, Callable], None]


class _EzRouter(APIRouter):
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

        def wrapper(request: Request):
            result = endpoint(request)
            ez.response._body = result

        if self.middleware:
            i = -1

            def next_middleware():
                nonlocal i
                i += 1
                if i < len(self.middleware):
                    self.middleware[i](ez.request, ez.response, next_middleware)
                else:
                    wrapper(ez.request)

            return next_middleware

        return wrapper

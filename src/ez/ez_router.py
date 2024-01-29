from typing import Any, Awaitable, Callable
from fastapi.routing import APIRouter
from starlette.requests import Request
from starlette.responses import Response


class _EzRouter(APIRouter):
    def add_route(
        self,
        path: str,
        endpoint: Callable[[Request], Awaitable[Response] | Response],
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
        **kwargs: Any,
    ) -> None:
        import ez

        def wrapper(request: Request):
            result = endpoint(request)
            ez.response._body = result

        super().add_route(path, wrapper, methods, name, include_in_schema)

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        include_in_schema: bool = True,
        **kwargs: Any,
    ) -> None:
        import ez

        def wrapper(request: Request):
            result = endpoint(request)
            ez.response._body = result

        super().add_api_route(
            path,
            wrapper,
            include_in_schema=include_in_schema,
            **kwargs,
        )

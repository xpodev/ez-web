from contextvars import ContextVar
from typing import Any, TypeAlias, overload

from utilities.utils import bind

from .request import Request

from starlette.middleware.base import BaseHTTPMiddleware

import ez


RequestVar: TypeAlias = ContextVar[Request | None]
_REQUEST: RequestVar = ContextVar("request", default=None)


@bind(_REQUEST)
def get_request(var: RequestVar):
    def _get_request() -> Request:
        return var.get()
    
    return _get_request


def has_request():
    return get_request() is not None


@bind(_REQUEST)
def set_request(var: RequestVar):
    def _set_request(request: Request | None):
        var.set(request)
    
    return _set_request


@bind()
def request():
    _EMPTY: Any = object()

    @overload
    def _request() -> Request: ...
    @overload
    def _request(request: Request) -> None: ...

    def _request(request: Request = _EMPTY):
        if request is _EMPTY:
            return get_request()
        set_request(request)

    return _request


async def _on_request(request, call_next):
    set_request(Request(request))
    response = await call_next(request)
    set_request(None)
    return response


ez.lowlevel.WEB_APP.add_middleware(BaseHTTPMiddleware, dispatch=_on_request)


del _REQUEST

__all__ = [
    "get_request",
    "set_request",
    "request",
]

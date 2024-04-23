from typing import Callable

from http import HTTPStatus

from starlette import responses as res
from starlette.exceptions import HTTPException


RESPONSE_MAP: list[tuple[Callable[[object], bool], Callable[[object], res.Response]]] = []


def auto_response(value, **kwargs):
    match value:
        case dict() | list() | int() | bool() as data:
            return res.JSONResponse(data, **kwargs)
        case HTTPStatus():
            raise HTTPException(value, detail=kwargs.get("detail", value.description))
        case (int(), detail):
            raise HTTPException(value[0], detail=detail)
        case (int(),):
            raise HTTPException(value[0])
        case str():
            return res.PlainTextResponse(value, **kwargs)
        case _:
            for matcher, response in RESPONSE_MAP:
                if matcher(value):
                    return response(value, **kwargs)


def register_response(matcher: Callable[[object], bool], response: Callable[[object], res.Response]):
    RESPONSE_MAP.append((matcher, response))
    return response


def response_for(matcher: Callable[[object], bool]):
    def decorator(func):
        return register_response(matcher, func)
    return decorator



@response_for(lambda x: isinstance(x, dict))
def dict_response(x):
    return res.JSONResponse(x)

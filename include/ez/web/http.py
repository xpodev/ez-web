from enum import StrEnum
from functools import wraps
import ez.lowlevel as lowlevel


class HTTPEvent(StrEnum):
    In = "HTTP.In"
    """
    Called when a HTTP request is received.

    :param request: The request object.
    """
    Out = "HTTP.Out"
    """
    Called when a HTTP response is sent.

    :param request: The request object.
    """

    GET = "HTTP.GET"
    """
    Called when a HTTP GET request is received.

    :param request: The request object.
    """
    POST = "HTTP.POST"
    """
    Called when a HTTP POST request is received.

    :param request: The request object.
    """
    PUT = "HTTP.PUT"
    """
    Called when a HTTP PUT request is received.

    :param request: The request object.
    """
    DELETE = "HTTP.DELETE"
    """
    Called when a HTTP DELETE request is received.

    :param request: The request object.
    """
    PATCH = "HTTP.PATCH"
    """
    Called when a HTTP PATCH request is received.

    :param request: The request object.
    """
    HEAD = "HTTP.HEAD"
    """
    Called when a HTTP HEAD request is received.

    :param request: The request object.
    """
    OPTIONS = "HTTP.OPTIONS"
    """
    Called when a HTTP OPTIONS request is received.

    :param request: The request object.
    """
    TRACE = "HTTP.TRACE"
    """
    Called when a HTTP TRACE request is received.

    :param request: The request object.
    """
    CONNECT = "HTTP.CONNECT"
    """
    Called when a HTTP CONNECT request is received.

    :param request: The request object.
    """


def _wrap_endpoint(route: str, **kwargs):
    def decorator(func):
        host = lowlevel.APP_HOST
        current_app = host.current_application

        @wraps(func)
        def wrapper(request, *args, **kwargs):
            with host.application(current_app):
                return func(*args, **kwargs)

        lowlevel.WEB_APP.ez_router.add_route(route, wrapper, **kwargs)
        return func

    return decorator


def add_router(route: str, router):
    lowlevel.WEB_APP.ez_router.mount(route, router)


def router():
    from core.web.router import EZRouter as Router

    return Router()


def get(route: str, **kwargs):
    return _wrap_endpoint(route, methods=["GET"], **kwargs)


def post(route: str, **kwargs):
    return _wrap_endpoint(route, methods=["POST"], **kwargs)


def put(route: str, **kwargs):
    return _wrap_endpoint(route, methods=["PUT"], **kwargs)


def delete(route: str, **kwargs):
    return _wrap_endpoint(route, methods=["DELETE"], **kwargs)


def patch(route: str, **kwargs):
    return _wrap_endpoint(route, methods=["PATCH"], **kwargs)


def options(route: str, **kwargs):
    return _wrap_endpoint(route, methods=["OPTIONS"], **kwargs)


def head(route: str, **kwargs):
    return _wrap_endpoint(route, methods=["HEAD"], **kwargs)

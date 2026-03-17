from typing import TYPE_CHECKING, Any

from sandbox import current_plugin
from utilities.utils import bind

if TYPE_CHECKING:
    from modules.web.routing import PluginRouter
    from modules.web.context import get_request, set_request, request
    from modules.web.http import HTTPException, HTTPMethod, HTTPStatus
    from modules.web.routing import API_ROUTER
else:
    from ..context import get_request, set_request, request
    from ..http import HTTPException, HTTPMethod, HTTPStatus
    from ..routing import API_ROUTER


_EMPTY: Any = object()


@bind(API_ROUTER)
def current_router(api_router: "PluginRouter"):
    def _current_router():
        return api_router.get_router(current_plugin())
    
    return _current_router


@bind(API_ROUTER)
def router(api_router: "PluginRouter"):
    def _router(route: str = _EMPTY, **kwargs):
        plugin = current_plugin()

        if not plugin.is_root:
            plugin_router = api_router.get_router(plugin)
            if plugin_router is not None:
                if route is _EMPTY:
                    return plugin_router
                
                # TODO: better exception type
                raise Exception(f"Plugin '{plugin.oid}' already has a router mounted at '{route}'")

        if route is _EMPTY:
            route = '/' + plugin.oid

        return api_router.add_router(plugin, route, **kwargs)

    return _router


@bind(API_ROUTER)
def route(api_router: "PluginRouter"):
    def _route(route: str, methods: list[HTTPMethod | str] = _EMPTY, **kwargs):
        if methods is _EMPTY or not methods:
            methods = []

        router = current_router()
        if router is None:
            # TODO: better exception type
            raise Exception("No router found for current plugin")
        
        router.route(route, methods=list(map(str, methods)), **kwargs)
    
    return _route


def get(_route: str, **kwargs):
    return route(_route, methods=[HTTPMethod.GET], **kwargs)


def post(_route: str, **kwargs):
    return route(_route, methods=[HTTPMethod.POST], **kwargs)


def put(_route: str, **kwargs):
    return route(_route, methods=[HTTPMethod.PUT], **kwargs)


def delete(_route: str, **kwargs):
    return route(_route, methods=[HTTPMethod.DELETE], **kwargs)


def patch(_route: str, **kwargs):
    return route(_route, methods=[HTTPMethod.PATCH], **kwargs)


def options(_route: str, **kwargs):
    return route(_route, methods=[HTTPMethod.OPTIONS], **kwargs)


def head(_route: str, **kwargs):
    return route(_route, methods=[HTTPMethod.HEAD], **kwargs)


del API_ROUTER
del TYPE_CHECKING, Any
del bind


__all__ = [
    "router",
    "route",

    "get",
    "post",
    "put",
    "delete",
    "patch",
    "options",
    "head",

    "HTTPException",
    "HTTPMethod",
    "HTTPStatus",

    "get_request",
    "set_request",
    "request",
]

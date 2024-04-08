from functools import wraps
import ez.lowlevel as lowlevel


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

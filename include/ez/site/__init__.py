from functools import wraps
import ez

from ..config import config

DIR = ez.SITE_DIR
CONFIG = config


import ez.lowlevel as lowlevel


def add_router(route: str, router):
    lowlevel.WEB_APP.include_router(router, prefix=route)


def router():
    from fastapi import APIRouter
    return APIRouter()


def get(route: str, **kwargs):
    def decorator(func):
        host = lowlevel.APP_HOST
        current_app = host.current_application

        @wraps(func)
        def wrapper(*args, **kwargs):
            with host.application(current_app):
                return func(*args, **kwargs)

        lowlevel.WEB_APP.get(route, **kwargs)(wrapper)
        return func
    return decorator


del ez
del config


__all__ = ["DIR", "CONFIG"]

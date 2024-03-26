from utilities.event import Event

from .settings import Settings
from web.events import HTTP
from web.app.events import App

import ez.lowlevel


def off(event: Event, func):
    return ez.lowlevel.EZ_APP.event_system.off(event, func)


def on(event: Event):
    def decorator(func):
        return ez.lowlevel.EZ_APP.event_system.on(event, func)
    return decorator


def once(event: Event):
    def decorator(func):
        return ez.lowlevel.EZ_APP.event_system.once(event, func)
    return decorator


def emit(event: Event, *args, **kwargs):
    return ez.lowlevel.EZ_APP.event_system.emit(event, *args, **kwargs)


__all__ = [
    "Event",
    "HTTP",
    "App",
    "Settings",
    "TreeRenderer"
]

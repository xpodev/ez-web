from functools import wraps
from typing import TYPE_CHECKING

from sandbox.applications import Artifact
from sandbox.host import syscall
from utilities.event_emitter import EventEmitter as BaseEventEmitter, EventHandler


if TYPE_CHECKING:
    from ..host import AppHost


def wrap_event_handler(handler: "EventHandler", app_host: "AppHost"):
    current_application = app_host.current_application
    origin = handler.handler

    @wraps(origin)
    def wrapper(*args, **kwargs):
        with app_host.application(current_application):
            return origin(*args, **kwargs)
    handler.handler = wrapper

    return handler


class EventEmitter(BaseEventEmitter):
    def __init__(self, app_host: "AppHost") -> None:
        BaseEventEmitter.__init__(self)

        self._app_host = app_host

    def _add_event_listener(self, event: str, handler: "EventHandler"):
        current_application = self._app_host.current_application
        self._app_host.create_artifact(current_application, Artifact, lambda: self._remove_event_listener(event, handler))
        return super()._add_event_listener(event, wrap_event_handler(handler, self._app_host))
    
    @syscall
    def emit(self, event: str, *args, **kwargs):
        return super().emit(event, *args, **kwargs)
    
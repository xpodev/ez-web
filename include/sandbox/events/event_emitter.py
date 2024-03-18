from functools import wraps
from typing import TYPE_CHECKING

from sandbox.host import AppHostPermission
from sandbox.security import PermissionSet
from utilities.event import Event
from utilities.event_emitter import EventEmitter as BaseEventEmitter, EventHandler


from ..applications import Application


if TYPE_CHECKING:
    from ..host import AppHost


class EventEmitter(Application, BaseEventEmitter):
    def __init__(self, app_host: "AppHost") -> None:
        super().__init__("ee", PermissionSet(
            AppHostPermission.ManageApplications |
            AppHostPermission.RegisterEvents
        ))
        BaseEventEmitter.__init__(self)

        self._app_host = app_host

    def setup(self):
        self._app_host.register_event(type(self)._emit)

    def _add_event_listener(self, event: Event, handler: "EventHandler"):
        current_application = self._app_host.current_application
        origin = handler.handler

        @wraps(origin)
        def wrapper(*args, **kwargs):
            with self._app_host.application(current_application):
                return origin(*args, **kwargs)
        handler.handler = wrapper

        return super()._add_event_listener(event, handler)
    
    def emit(self, event: Event, *args, **kwargs):
        return self._app_host.invoke(type(self)._emit, self, event, *args, **kwargs)
    
    def _emit(self, event: Event, *args, **kwargs):
        return super().emit(event, *args, **kwargs)

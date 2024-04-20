from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..applications import Application


class Context:
    def __init__(self, host_application: "Application") -> None:
        self._host_application = host_application
        self._current_application = ContextVar("_current_application", default=host_application)

    @property
    def current_application(self) -> "Application":
        return self._current_application.get()

    @property
    def host_application(self) -> "Application":
        return self._host_application

    @contextmanager
    def application(self, application: "Application"):
        previous_application = self.current_application
        self._current_application.set(application)
        try:
            yield application
        finally:
            self._current_application.set(previous_application)

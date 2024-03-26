from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..applications import Application


class Context:
    _execution_stack: list["Application"]

    def __init__(self, host_application: "Application") -> None:
        self._execution_stack = [host_application]

    @property
    def current_application(self) -> "Application":
        return self._execution_stack[-1]

    @property
    def host_application(self) -> "Application":
        return self._execution_stack[0]

    @contextmanager
    def application(self, application: "Application"):
        self._execution_stack.append(application)
        try:
            yield application
        finally:
            self._execution_stack.pop()

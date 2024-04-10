from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from .app_host import AppHost


P = ParamSpec("P")
T = TypeVar("T")


def syscall(fn: Callable[P, T]) -> Callable[P, T]:
    current_host = AppHost.current_host
    current_application = current_host.current_application

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        with current_host._context.application(current_application):
            return fn(*args, **kwargs)

    return wrapper

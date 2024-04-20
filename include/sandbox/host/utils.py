from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar, overload

from .app_host import AppHost


P = ParamSpec("P")
T = TypeVar("T")

@overload
def syscall(fn: Callable[P, T]) -> Callable[P, T]: ...
@overload
def syscall(fn: T) -> T: ...

def syscall(fn: Any) -> Any:
    current_host = AppHost.current_host
    current_application = current_host.current_application

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        with current_host._context.application(current_application):
            return fn(*args, **kwargs)

    return wrapper

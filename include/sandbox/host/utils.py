from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar, overload

from .app_host import AppHost


P = ParamSpec("P")
T = TypeVar("T")

@overload
def syscall(fn: Callable[P, T], pass_calling_application: bool = False) -> Callable[P, T]: ...
@overload
def syscall(fn: T, pass_calling_application: bool = False) -> T: ...

def syscall(fn: Any, pass_calling_application: bool = False) -> Any:
    current_host = AppHost.current_host
    current_application = current_host.current_application

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        if pass_calling_application:
            injected_args = (current_host.current_application,)
        else:
            injected_args = ()
        with current_host._context.application(current_application):
            return fn(*injected_args, *args, **kwargs)

    return wrapper

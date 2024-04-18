from typing import Callable, ParamSpec, TypeVar


P = ParamSpec("P")
B = ParamSpec("B")
T = TypeVar("T")


def apply(fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return fn(*args, **kwargs)


def bind(*args, **kwargs) -> Callable[[Callable[B, Callable[P, T]]], Callable[P, T]]:

    def wrapper(fn: Callable[B, Callable[P, T]]) -> Callable[P, T]:
        return fn(*args, **kwargs)
    
    return wrapper

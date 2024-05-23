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


def spacify(text: str, sep: str = ' ') -> str:
    """
    Takes in a string of either PascalCase or camelCase and return it split to words
    with the given separator. 

    Default separator is a single space.
    """
    return ''.join(sep + char if char.isupper() else char.strip() for char in text).strip()


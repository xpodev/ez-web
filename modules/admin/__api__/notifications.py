from typing import Any, Iterable, overload

from seamless.types import Renderable

from ..user import User


_EMPTY: Any = object()


@overload
def push(users: Iterable[User], message: str, /) -> None: ...
@overload
def push(users: Iterable[User], message: str, /, *, title: str) -> None: ...
@overload
def push(users: Iterable[User], custom: Renderable, /) -> None: ...

def push(users: Iterable[User], message: str | Renderable, /, *, title: str = _EMPTY):
    raise NotImplementedError


@overload
def push_all(message: str, /, *, exclude: Iterable[User] | None = None) -> None: ...
@overload
def push_all(message: str, /, *, title: str, exclude: Iterable[User] | None = None) -> None: ...
@overload
def push_all(custom: Renderable, /, *, exclude: Iterable[User] | None = None) -> None: ...

def push_all(message: str | Renderable, /, *, title: str = _EMPTY, exclude: Iterable[User] | None = None):
    if exclude is None:
        exclude = []

    raise NotImplementedError

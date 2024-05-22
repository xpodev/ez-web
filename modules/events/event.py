from enum import Enum
from typing import Any, Callable, Generic, ParamSpec, Self, TypeAlias, overload

from .emit import emit
from .emitter import EMITTER


P = ParamSpec('P')

EventHandler: TypeAlias = Callable[P, None]


_EMPTY: Any = object()


class Event(Generic[P]):
    _handlers: list[EventHandler[P]] | None = None
    _name: str = _EMPTY

    def __init__(self, name: str = _EMPTY) -> None:
        if name is not _EMPTY:
            self._name = name
        else:
            self._handlers = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_standalone(self) -> bool:
        return self._handlers is not None

    def __iadd__(self, handler: EventHandler[P]) -> Self:
        self.add_listener(handler)
        return self
    
    def __isub__(self, handler: EventHandler[P]) -> Self:
        self.remove_listener(handler)
        return self
    
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        emit(self, *args, **kwargs)

    def add_listener(self, handler: EventHandler[P]) -> None:
        if self.is_standalone:
            assert self._handlers is not None
            self._handlers.append(handler)
        else:
            EMITTER.on(self._name, handler)

    def remove_listener(self, handler: EventHandler[P]) -> None:
        if self.is_standalone:
            assert self._handlers is not None
            self._handlers.remove(handler)
        else:
            EMITTER.off(self._name, handler)

    def reset(self) -> None:
        if self.is_standalone:
            assert self._handlers is not None
            self._handlers.clear()
        else:
            EMITTER.reset(self._name)


class Events(Event, Enum):
    pass


@overload
def event() -> Callable[[EventHandler[P]], Event[P]]: ...
@overload
def event(name: str, /) -> Callable[[EventHandler[P]], Event[P]]: ...
@overload
def event(handler: EventHandler[P], /) -> Event[P]: ...

def event(name_or_handler: str | EventHandler[P] | None = _EMPTY, /) -> Callable[[EventHandler[P]], Event[P]] | Event[P]:
    if name_or_handler is None:
        return lambda _: Event()
    if name_or_handler is _EMPTY:
        return lambda handler: Event(handler.__name__)
    if isinstance(name_or_handler, str):
        return lambda _: Event(name_or_handler)
    if callable(name_or_handler):
        return Event()
    raise TypeError("Invalid arguments")

from typing import Any, Callable, ParamSpec, overload, TYPE_CHECKING

from sandbox.host import syscall
from utilities.utils import bind

if TYPE_CHECKING:
    from .event import Event, EventHandler

import ez.lowlevel as lowlevel


P = ParamSpec('P')


@bind(lowlevel.EZ_APP.event_system)
def on(emitter: "lowlevel.EventEmitter"):
    def _on(event: "str | Event[P]", handler: "EventHandler[P]") -> None:
        if isinstance(event, str):
            emitter.on(event, handler)
        else:
            event.add_listener(handler)

    @overload
    def on(event: "str | Event[P]", handler: "EventHandler[P]", /) -> None: ...
    @overload
    def on(event: "str | Event[P]", /) -> Callable[["EventHandler[P]"], None]: ...

    def on(event: "str | Event[P]", handler: "EventHandler[P] | None" = None, /) -> Callable[["EventHandler[P]"], None] | None:
        if handler is not None:
            return _on(event, handler)
        return lambda handler: _on(event, handler)

    return on


@bind(lowlevel.EZ_APP.event_system)
def off(emitter: "lowlevel.EventEmitter"):
    def _off(event: "str | Event[P]", handler: "EventHandler[P]") -> None:
        if isinstance(event, str):
            emitter.off(event, handler)
        else:
            event.remove_listener(handler)

    @overload
    def off(event: "str | Event[P]", handler: "EventHandler[P]", /) -> None: ...
    @overload
    def off(event: "str | Event[P]", /) -> Callable[["EventHandler[P]"], None]: ...

    def off(event: "str | Event[P]", handler: "EventHandler[P] | None" = None, /) -> Callable[["EventHandler[P]"], None] | None:
        if handler is not None:
            return _off(event, handler)
        return lambda handler: _off(event, handler)

    return off


@bind(lowlevel.EZ_APP.event_system)
def once(emitter: "lowlevel.EventEmitter"):
    def _once(event: str, handler: "EventHandler[P]") -> None:
        if isinstance(event, str):
            emitter.once(event, handler)
        else:
            raise TypeError("Cannot use 'once' with standalone events")

    @overload
    def once(event: str, handler: "EventHandler[P]", /) -> None: ...
    @overload
    def once(event: str, /) -> Callable[["EventHandler[P]"], None]: ...

    def once(event: str, handler: "EventHandler[P] | None" = None, /) -> Callable[["EventHandler[P]"], None] | None:
        if handler is not None:
            return _once(event, handler)
        return lambda handler: _once(event, handler)

    return once


@syscall
@bind(lowlevel.EZ_APP.event_system)
def emit(emitter: "lowlevel.EventEmitter"):
    @overload
    def emit(event: str, *args: Any, **kwargs: Any) -> bool: ...
    @overload
    def emit(event: "Event[P]", *args: P.args, **kwargs: P.kwargs) -> bool: ...

    def emit(event: "str | Event[P]", *args: P.args, **kwargs: P.kwargs) -> bool:
        if isinstance(event, str):
            return emitter.emit(event, *args, **kwargs)
        else:
            return False

    return emit


del lowlevel, bind, syscall

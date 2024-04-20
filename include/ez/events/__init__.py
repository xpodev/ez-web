from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ....modules.events.event import Event, Events, event
    from ....modules.events.emit import off, on, once, emit
else:
    from ..event import Event, Events, event
    from ..emit import off, on, once, emit


__all__ = [
    "Event",
    "Events",
    "off",
    "on",
    "once",
    "emit",
    "event",
]

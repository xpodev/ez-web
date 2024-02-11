from functools import wraps
from typing import Callable
from .event import Event

class EventEmitter:
    _events: dict[Event, list[Callable[..., None]]]

    def __init__(self) -> None:
        self._events = {}

    def _add_event_listener(self, event: Event, listener: Callable[..., None], priority: int = 0):
        if priority < 0:
            raise ValueError("Priority must be greater than or equal to 0.")
        if hasattr(listener, "__ez_system__") and not priority:
            priority = -1
        listener.__ee_priority__ = priority
        if event not in self._events:
            self._events[event] = []
            self._events[event].append(listener)
        elif priority == -1:
            self._events[event].insert(0, listener)
        else:
            for i, l in enumerate(self._events[event]):
                if hasattr(l, "__ee_priority__") and l.__ee_priority__ > priority:
                    self._events[event].insert(i, listener)
                    break
            else:
                self._events[event].append(listener)
    
    def _remove_event_listener(self, event: Event, listener: Callable[..., None]):
        self._events[event].remove(getattr(listener, "__ee_key__", listener))
        if not self._events[event]:
            del self._events[event]

    def on(self, event: Event, f: Callable[..., None], priority: int = 0):
        self._add_event_listener(event, f, priority)
        return f

    def once(self, event: Event, f: Callable[..., None], priority: int = 0):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self._remove_event_listener(event, wrapper)
            return f(*args, **kwargs)
        self._add_event_listener(event, wrapper, priority)
        f.__ee_key__ = wrapper
        return f
    
    def emit(self, event: Event, *args, **kwargs) -> bool:
        """
        Emits an event. Returns True if the event was handled by at least one listener.
        """

        if event not in self._events:
            return False
        
        if not self._events[event]:
            del self._events[event]
            return False

        for listener in self._events[event]:
            listener(*args, **kwargs)
        
        return True
        
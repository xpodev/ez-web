from functools import wraps
from typing import Callable, Any


class EventHandler:
    __slots__ = ("key", "handler", "priority")

    def __init__(self, key: Any, handler: Callable, priority: int = 0) -> None:
        self.key = key
        self.handler = handler
        self.priority = priority

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)
    
    def __eq__(self, other):
        if isinstance(other, EventHandler):
            return self.key == other.key
        return self.key == other
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.key)


class EventEmitter:
    EZ_SYSTEM_ATTRIBUTE = "__ez_system__"

    _events: dict[str, list[EventHandler]]

    def __init__(self) -> None:
        self._events = {}

    def _add_event_listener(self, event: str, handler: EventHandler):
        if event not in self._events:
            self._events[event] = [handler]
        elif handler.priority == -1:
            self._events[event].insert(0, handler)
        else:
            for i, h in enumerate(self._events[event]):
                if h.priority != -1 and h.priority > handler.priority:
                    self._events[event].insert(i, handler)
                    break
            else:
                self._events[event].append(handler)
    
    def _remove_event_listener(self, event: str, listener: Callable[..., None]):
        if event in self._events:
            self._events[event].remove(listener)
        if not self._events[event]:
            del self._events[event]

    def _create_handler(self, f: Callable[..., None], key: object, priority: int) -> EventHandler:
        if priority < 0:
            raise ValueError("Priority must be greater than or equal to 0")
        if getattr(f, self.EZ_SYSTEM_ATTRIBUTE, False):
            priority = -1
        return EventHandler(key, f, priority)

    def off(self, event: str, f: Callable[..., None]):
        self._remove_event_listener(event, f)

    def on(self, event: str, f: Callable[..., None], *, key: object = None, priority: int = 0):
        self._add_event_listener(event, self._create_handler(f, key or f, priority))
        return f

    def once(self, event: str, f: Callable[..., None], *, key: object = None, priority: int = 0):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self._remove_event_listener(event, key or f)
            return f(*args, **kwargs)
        self._add_event_listener(event, self._create_handler(wrapper, key or f, priority))
        return f
    
    def emit(self, event: str, *args, **kwargs) -> bool:
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

    def reset(self, event: str):
        if event in self._events:
            del self._events[event]

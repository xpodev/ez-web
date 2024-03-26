from typing import TypeVar, Generic


_K = TypeVar("_K")
_V = TypeVar("_V")


_SENTINEL = object()


class ICache(Generic[_K, _V]):
    def cache(self, key: _K, value: _V = _SENTINEL):
        if value is _SENTINEL:
            return self.get(key)
        self.set(key, value)
        return value

    def get(self, key: _K) -> _V:
        raise NotImplementedError

    def set(self, key: _K, value: _V):
        raise NotImplementedError
    
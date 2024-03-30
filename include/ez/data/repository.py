from typing import TypeVar, Generic, TypeAlias

from utilities.icache import ICache


T = TypeVar("T")
CacheId: TypeAlias = str


class Repository(Generic[T]):
    _cache: ICache[CacheId, T] | None

    def __init__(self, cache: ICache[CacheId, T] | None) -> None:
        self._cache = cache

    @property
    def cache_enabled(self) -> bool:
        return self._cache is not None
    
    def enable_caching(self, cache: ICache[CacheId, T]) -> None:
        self._cache = cache

    def disable_caching(self) -> None:
        self.enable_caching(None)

    def get(self, key: CacheId, **kwargs) -> T:
        if not self.cache_enabled:
            return self._get(key, **kwargs)
        try:
            return self._cache.get(key)
        except KeyError:
            return self._cache.cache(key, self._get(key, **kwargs))
    
    def _get(self, key: CacheId, **kwargs) -> T:
        raise NotImplementedError
    
    def set(self, key: CacheId, value: T) -> None:
        if not self.cache_enabled:
            return self._set(key, value)
        self._cache.cache(key, value)
        self._set(key, value)

    def _set(self, key: CacheId, value: T) -> None:
        raise NotImplementedError

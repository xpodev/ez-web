from typing import TypeVar, Generic, TypeAlias

from ez.identity import ObjectIDBase
from utilities.icache import ICache


T = TypeVar("T", bound=ObjectIDBase)
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
        self._cache = None

    def get(self, key: CacheId, **kwargs) -> T:
        if not self.cache_enabled:
            return self._get(key, **kwargs)
        assert self._cache is not None
        try:
            return self._cache.get(key)
        except KeyError:
            return self._cache.cache(key, self._get(key, **kwargs))
        
    def set(self, value: T, key: CacheId | None = None):
        if key is None:
            key = value.oid
        if self.cache_enabled:
            assert self._cache is not None
            self._cache.cache(key, value)
        self._set(value, key)
    
    def _get(self, key: CacheId, **kwargs) -> T:
        raise NotImplementedError
    
    def _set(self, value: T, key: CacheId) -> None:
        raise NotImplementedError

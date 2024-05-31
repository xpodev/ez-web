from typing import TypeAlias, TypeVar, Type

from utilities.uri import UnifiedResourceIdentifier


ResourceTypeId: TypeAlias = str
URI: TypeAlias = UnifiedResourceIdentifier

ResourceT = TypeVar("ResourceT", bound="Resource")


class ResourceType:
    _id: ResourceTypeId
    _name: str

    def __init__(self, name: str, id: ResourceTypeId) -> None:
        self._name = name
        self._id = id

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id


class Resource:
    _type: ResourceType
    _uri: URI

    def __init__(self, resource_type: ResourceType, uri: str) -> None:
        self._type = resource_type
        self._uri = uri

    @property
    def type(self):
        return self._type
    
    @property
    def uri(self):
        return self._uri
    
    def cast(self, cls: Type[ResourceT], *, strict: bool = True) -> ResourceT:
        if not strict:
            return self
        if not isinstance(self, cls):
            raise TypeError(f"Resource.cast(strict=True) could not convert resource of type {type(self).__name__} to {cls.__name__}")
        return self

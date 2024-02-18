from typing import TypeAlias

from ..resource import Resource, ResourceType, URI


ResourceLoaderId: TypeAlias = str


class ResourceLoaderInfo:
    id: ResourceLoaderId
    name: str



class IResourceLoader:
    def load_resource(self, uri: URI, resource_type: ResourceType | None = None) -> Resource:
        raise NotImplementedError

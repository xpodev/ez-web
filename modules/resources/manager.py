from .machinery.loader import IResourceLoader, ResourceLoaderId
from .resource import Resource, ResourceType, URI


class ResourceManager:
    _loaders: dict[ResourceLoaderId, IResourceLoader]
    _resources: dict[URI, Resource]

    def __init__(self) -> None:
        self._loaders = {}
        self._resources = {}

    def load_resource(self, uri: URI, resource_type: ResourceType | None = None, *, enable_caching: bool = True):
        try:
            return self._resources[uri]
        except KeyError:
            resource = self._load_resource(uri, resource_type)
            if enable_caching:
                self._resources[uri] = resource
            return resource
        
    def _load_resource(self, uri: URI, resource_type: ResourceType | None = None):
        raise NotImplementedError

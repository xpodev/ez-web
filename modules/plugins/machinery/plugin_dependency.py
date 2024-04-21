from pydantic import BaseModel, Field, model_serializer, model_validator

from utilities.uri import URI
from utilities.semver import SemanticVersion as Version, SEMVER_LATEST


DEFAULT_DEPENDENCY_VERSION = SEMVER_LATEST


class PluginDependency(BaseModel):
    source: str
    package_name: str
    version: Version

    @classmethod
    def from_uri_string(cls, uri: str) -> "PluginDependency":
        uri: URI = URI.parse(uri)

        if uri.scheme is None:
            raise ValueError("Invalid plugin dependency URI: missing source")
        if uri.authority is None:
            raise ValueError("Invalid plugin dependency URI: missing package name")
        if uri.authority.host is None:
            raise ValueError("Invalid plugin dependency URI: missing package name")

        return cls(
            source=uri.scheme,
            package_name=uri.authority.host,
            version=Version.parse(uri.path.strip("/") if uri.path else DEFAULT_DEPENDENCY_VERSION)
        )

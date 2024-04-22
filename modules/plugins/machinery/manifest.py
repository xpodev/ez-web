import yaml

from pathlib import Path
from pydantic import BaseModel, Field, ValidationError, field_validator

from utilities.version import Version

from .plugin_dependency import PluginDependency

from ..errors import InvalidPackageName, InvalidPluginManifest
from ..plugin_info import PackageName, PACKAGE_NAME_REGEX


class PluginManifest(BaseModel):
    package_name: PackageName = Field(alias="package-name")

    name: str
    description: str | None
    author: str
    version: Version = Field(alias="version")

    dependencies: list[PluginDependency] = Field(default_factory=list)

    home_page: str | None = Field(alias="home-page")

    @field_validator("package_name", mode="after")
    def validate_package_name(cls, value: PackageName) -> PackageName:
        if not PACKAGE_NAME_REGEX.match(value):
            raise InvalidPackageName(f"Invalid package name: {value}. Package must begin with a lowercase letter and contain only lowercase letters, numbers, and hyphens.")
        return value
    
    @classmethod
    def from_path(cls, path: str | Path):
        if isinstance(path, str):
            path = Path(path)
        with path.open() as file:
            return cls.from_file(file, path=path)
        
    @classmethod
    def from_file(cls, file, *, path: str | Path | None = None):
        try:
            return cls.model_validate(yaml.safe_load(file))
        except ValidationError as e:
            raise InvalidPluginManifest(str(path) if path else "") from e

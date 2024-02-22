from pydantic import BaseModel

from utilities.version import Version

from .config import TEMPLATES_DEFAULT_ROOT_DIRECTORY_NAME


class TemplateMappingInfo(BaseModel):
    root: str
    mappings: dict[str, "str | TemplateMappingInfo"]


class TemplatePackageInfo(BaseModel):
    name: str
    version: Version
    author: str
    description: str | None = None
    package_name: str

    root: str = TEMPLATES_DEFAULT_ROOT_DIRECTORY_NAME
    mappings: dict[str, str | TemplateMappingInfo] | None = None

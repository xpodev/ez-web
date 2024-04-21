import re
from pydantic import BaseModel, Field
from typing import TypeAlias
from utilities.version import Version

 
from .machinery.installer import PluginInstallerId


PluginId: TypeAlias = str
PackageName: TypeAlias = str


PACKAGE_NAME_REGEX = re.compile(r"^[a-z][a-z\-0-9]*$")


class PluginInfo(BaseModel):
    name: str
    version: Version
    description: str | None
    installer_id: PluginInstallerId = Field(exclude=True)
    package_name: str
    author: str

    @property
    def id(self) -> PluginId:
        return self.package_name

    @property
    def dir_name(self) -> PackageName:
        return self.package_name

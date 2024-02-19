from dataclasses import dataclass
from typing import TypeAlias, TYPE_CHECKING
from utilities.version import Version


if TYPE_CHECKING:
    from .machinery.installer import PluginInstallerId


PluginId: TypeAlias = str
PackageName: TypeAlias = str


@dataclass
class PluginInfo:
    name: str
    version: Version
    description: str
    installer_id: "PluginInstallerId"
    package_name: str

    @property
    def id(self) -> PluginId:
        return self.package_name

    @property
    def dir_name(self) -> PackageName:
        return self.package_name

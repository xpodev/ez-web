from pydantic import BaseModel
from pathlib import Path
from typing import TypeAlias, ClassVar, TYPE_CHECKING

from utilities.version import Version

if TYPE_CHECKING:
    from ..plugin import PluginId


PluginInstallerId: TypeAlias = str


class PluginInstallerInfo(BaseModel):
    id: PluginInstallerId
    name: str


class PluginInstallationResult(BaseModel):
    installer_id: PluginInstallerId
    package_name: str
    version: Version
    previous_version: Version | None

    @property
    def is_upgrade(self) -> bool:
        return self.previous_version is not None


class IPluginInstaller:
    info: ClassVar[PluginInstallerInfo]

    def __init__(self, plugin_dir: str) -> None:
        self._plugin_dir = Path(plugin_dir)

    @property
    def plugin_dir(self) -> Path:
        return self._plugin_dir

    def install(self, path: str) -> PluginInstallationResult:
        raise NotImplementedError
    
    def upgrade(self, plugin_id: "PluginId", path: str) -> None:
        raise NotImplementedError

    def uninstall(self, plugin_id: "PluginId") -> None:
        raise NotImplementedError

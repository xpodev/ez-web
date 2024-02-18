from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias, ClassVar

from utilities.version import Version

from ..plugin_info import PluginId


PluginInstallerId: TypeAlias = str


@dataclass
class PluginInstallerInfo:
    id: PluginInstallerId
    name: str


@dataclass
class PluginInstallationResult:
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

    def uninstall(self, plugin_id: str) -> None:
        raise NotImplementedError

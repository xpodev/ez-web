from ez import EZError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .machinery.installer import PluginInstallerId
    from .machinery.loader import PluginLoaderId


class EZPluginError(EZError):
    ...


class UnknownPluginError(EZPluginError):
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name

    def __str__(self):
        return f"Unknown plugin: {self.plugin_name}"


class PluginAlreadyInstalledError(EZPluginError):
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name

    def __str__(self):
        return f"Plugin already installed: {self.plugin_name}"


class DuplicateIDError(EZPluginError):
    def __init__(self, item, id) -> None:
        self.item = item
        self.id = id

    def __str__(self):
        return f"Duplicate ID of {type(self.item).__name__}: {self.id}"


class UnknownPluginInstallerError(EZPluginError):
    def __init__(self, installer_id: "PluginInstallerId") -> None:
        self._installer_id = installer_id

    def __str__(self):
        return f"Unknown plugin installer: {self._installer_id}"


class UnknownPluginLoaderError(EZPluginError):
    def __init__(self, loader_id: "PluginLoaderId") -> None:
        self._loader_id = loader_id

    def __str__(self):
        return f"Unknown plugin loader: {self._loader_id}"


__all__ = [
    "EZPluginError",
    "UnknownPluginError",
    "PluginAlreadyInstalledError",
    "DuplicateIDError",
    "UnknownPluginInstallerError",
    "UnknownPluginLoaderError",
]

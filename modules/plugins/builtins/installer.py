from ..errors import EZPluginError
from ..machinery.installer import IPluginInstaller, PluginInstallationResult, PluginInstallerInfo


class EZPluginInstallerError(EZPluginError):
    ...


class InvalidPluginArchive(EZPluginInstallerError):
    ...


class InvalidPluginManifest(EZPluginInstallerError):
    ...


class EZPluginInstaller(IPluginInstaller):
    info = PluginInstallerInfo.model_construct(
        id="ez.plugins.installer",
        name="EZ Plugin Installer",
    )

    def install(self, path: str) -> PluginInstallationResult:
        ...

    def uninstall(self, plugin_id: str) -> None:
        ...

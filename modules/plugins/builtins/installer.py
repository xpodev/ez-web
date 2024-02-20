import yaml

from pathlib import Path
from zipfile import ZipFile, BadZipFile
from pydantic import BaseModel, Field, ValidationError

from utilities.version import Version

from ..errors import EZPluginError, PluginAlreadyInstalledError
from ..plugin_info import PackageName
from ..machinery.installer import IPluginInstaller, PluginInstallationResult, PluginInstallerInfo


class EZPluginInstallerError(EZPluginError):
    ...


class InvalidPluginArchive(EZPluginInstallerError):
    ...


class InvalidPluginManifest(EZPluginInstallerError):
    ...


class PluginManifest(BaseModel):
    name: str
    package_name: PackageName = Field(alias="package-name")
    version: Version = Field(alias="version")
    typing_file: str = Field(alias="typing-file")


class EZPluginInstaller(IPluginInstaller):
    info = PluginInstallerInfo(
        id="ez.plugins.installer",
        name="EZ Plugin Installer",
    )

    EZ_PLUGIN_MANIFEST_FILENAME = "manifest.yaml"

    def install(self, path: str) -> PluginInstallationResult:
        path: Path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        if not path.is_file():
            raise IsADirectoryError(path)
        
        try:
            zip_file = ZipFile(path)
        except BadZipFile as e:
            raise InvalidPluginArchive(path) from e
        
        with zip_file:
            manifest_file = zip_file.open(self.EZ_PLUGIN_MANIFEST_FILENAME)
            manifest_data = yaml.safe_load(manifest_file)
            try:
                manifest = PluginManifest.model_validate(manifest_data)
            except ValidationError:
                raise InvalidPluginManifest(path)
            
            plugin_dir = self.plugin_dir / manifest.package_name
            if plugin_dir.exists():
                raise PluginAlreadyInstalledError(manifest.package_name)
            plugin_dir.mkdir()

            zip_file.extractall(str(plugin_dir))

            if manifest.typing_file:
                (plugin_dir / manifest.typing_file).rename()

    def uninstall(self, plugin_id: str) -> None:
        ...

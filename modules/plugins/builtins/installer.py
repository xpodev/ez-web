import shutil

from pathlib import Path
from zipfile import ZipFile, BadZipFile

import ez.site as site

from ..machinery.manifest import PluginManifest

from ..config import PLUGINS_PUBLIC_API_DIR, PLUGIN_MANIFEST_FILENAME
from ..errors import EZPluginError, PluginAlreadyInstalledError, UnknownPluginError
from ..machinery.installer import IPluginInstaller, PluginInstallationResult, PluginInstallerInfo


class EZPluginInstallerError(EZPluginError):
    ...


class InvalidPluginArchive(EZPluginInstallerError):
    ...


class PluginArchive:
    _DIR_SOURCE = "source"
    _DIR_TEMPLATES = "templates"
    _DIR_STATIC = "public"
    _DIR_RESOURCES = "resources"

    _FILE_INSTALL = "install.py"
    _FILE_UPGRADE = "upgrade.py"

    _FILE_MANIFEST = PLUGIN_MANIFEST_FILENAME

    _file: ZipFile
    _path: Path

    def __init__(self, path: Path, file: ZipFile | None = None):
        self._path = path
        self._file = ZipFile(str(path)) if file is None else file

        self._manifest = None

    @property
    def manifest(self) -> PluginManifest:
        if self._manifest is None:
            with self._file.open(self._FILE_MANIFEST) as file:
                return PluginManifest.from_file(file, path=self._path / self._FILE_MANIFEST)
        return self._manifest
    
    @property
    def has_install_file(self):
        try:
            self._file.getinfo(self._FILE_INSTALL)
        except KeyError:
            return False
        return True
    
    @property
    def has_upgrade_file(self):
        try:
            self._file.getinfo(self._FILE_UPGRADE)
        except KeyError:
            return False
        return True

    def _extract_member(self, name: str, dest: Path, *, overwrite: bool = False, must_exist: bool = True):
        try:
            info = self._file.getinfo(name)
        except KeyError:
            if must_exist:
                raise FileNotFoundError(f"Directory not found in plugin archive: {name}")
            return
        
        if info.is_dir() and not dest.exists():
            dest.mkdir(parents=True, exist_ok=True)

        self._file.extract(info, dest)

    def extract_source(self, dest: Path, *, overwrite: bool = False, must_exist: bool = True):
        self._extract_member(self._DIR_SOURCE, dest, overwrite=overwrite, must_exist=must_exist)
    
    def extract_templates(self, dest: Path, *, overwrite: bool = False, must_exist: bool = True):
        self._extract_member(self._DIR_TEMPLATES, dest, overwrite=overwrite, must_exist=must_exist)

    def extract_static(self, dest: Path, *, overwrite: bool = False, must_exist: bool = True):
        self._extract_member(self._DIR_STATIC, dest, overwrite=overwrite, must_exist=must_exist)
    
    def extract_resources(self, dest: Path, *, overwrite: bool = False, must_exist: bool = True):
        self._extract_member(self._DIR_RESOURCES, dest, overwrite=overwrite, must_exist=must_exist)

    def extract_install_file(self, dest: Path, *, overwrite: bool = False, must_exist: bool = True):
        self._extract_member(self._FILE_INSTALL, dest, overwrite=overwrite, must_exist=must_exist)

    def extract_upgrade_file(self, dest: Path, *, overwrite: bool = False, must_exist: bool = True):
        self._extract_member(self._FILE_UPGRADE, dest, overwrite=overwrite, must_exist=must_exist)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()


class EZPluginInstaller(IPluginInstaller):
    info = PluginInstallerInfo(
        id="ez.plugins.installer",
        name="EZ Plugin Installer",
    )

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
        
        with PluginArchive(path, zip_file) as archive:
            manifest = archive.manifest
            
            package_name = manifest.package_name
            plugin_dir = self.plugin_dir / package_name

            if plugin_dir.exists():
                raise PluginAlreadyInstalledError(package_name)
            
            plugin_dir.mkdir()

            archive.extract_source(plugin_dir, overwrite=False, must_exist=False)
            public_api = plugin_dir / "__api__"
            if public_api.exists() and public_api.is_dir():
                public_api.rename(PLUGINS_PUBLIC_API_DIR / package_name)

            archive.extract_templates(site.TEMPLATES / package_name, overwrite=False, must_exist=False)
            archive.extract_static(site.STATIC / package_name, overwrite=False, must_exist=False)
            archive.extract_resources(site.RESOURCES / package_name, overwrite=False, must_exist=False)

        # TODO: call install.py

    def upgrade(self, plugin_id: str, path: str) -> None:
        plugin_dir = self.plugin_dir / plugin_id

        if not plugin_dir.exists():
            raise UnknownPluginError(plugin_id)
        
        if not plugin_dir.is_dir():
            raise NotADirectoryError(plugin_dir)
        
        self.uninstall(plugin_id)
        self.install(path)

        # TODO: call upgrade.py & prevent from self.install to call install.py

    def uninstall(self, plugin_id: str) -> None:
        plugin_dir = self.plugin_dir / plugin_id
        if not plugin_dir.exists():
            raise UnknownPluginError(plugin_id)
        
        shutil.rmtree(str(plugin_dir))

        for item in (site.TEMPLATES, site.STATIC, site.RESOURCES, PLUGINS_PUBLIC_API_DIR):
            item = item / plugin_id
            if item.exists():
                shutil.rmtree(str(item), ignore_errors=True)

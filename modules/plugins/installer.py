import ez

from pathlib import Path
from zipfile import ZipFile
from yaml import load, Loader
from shutil import rmtree

from pydantic import BaseModel

from utilities.semver import SemanticVersion

from .manager import PluginManager


def read_manifest(path: Path | str):
    if isinstance(path, str):
        path = Path(path)
    manifest_file = path / PluginInstaller.MANIFEST_FILENAME

    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifest file not found in {path}")

    with manifest_file.open("r") as file:
        data = load(file, Loader=Loader)
    for key in data:
        if '-' in key:
            new_key = key.replace('-', '_')
            data[new_key] = data.pop(key)
    manifest = PluginManifest.model_validate(data)

    return manifest


def move_file(src: Path, dest: Path, name: str = None):
    dest.mkdir(parents=True, exist_ok=True)
    if name is None:
        name = src.name
    src.rename(dest / name)


class PluginRepository(BaseModel):
    type: str
    url: str


class PluginManifest(BaseModel):
    name: str
    version: str
    description: str
    author: str
    license: str

    homepage: str
    repository: list[PluginRepository]

    typing_file: str | None
    package_name: str

    @property
    def semantic_version(self):
        if not hasattr(self, "_semantic_version"):
            self._semantic_version = SemanticVersion.parse(self.version)
        return self._semantic_version


class PluginInstaller:
    MANIFEST_FILENAME = "manifest.yaml"

    def __init__(self, manager: PluginManager) -> None:
        self.manager = manager

    def install_from_path(self, path: str):
        manifest = read_manifest(path)

        self.install_plugin(manifest, path)

    def install_plugin(self, manifest: PluginManifest, path: Path):
        plugin_dir = ez.PLUGINS_DIR / manifest.package_name
        if plugin_dir.exists():
            raise FileExistsError(f"Plugin {manifest.package_name} is already installed")
        
        plugin_content = path / manifest.package_name

        # TODO: make manifest more flexible in terms of file transfer

        if manifest.typing_file:
            ez.PLUGIN_API_DIR.mkdir(parents=True, exist_ok=True)

            target_typing_file_name = manifest.package_name.replace("-", "_") + ".pyi"
            move_file(plugin_content / manifest.typing_file, ez.PLUGIN_API_DIR, target_typing_file_name)

        plugin_dir.mkdir(parents=False, exist_ok=False)
        for file in plugin_content.iterdir():
            move_file(file, plugin_dir)
        
    def install_from_zip(self, path: str):
        path: Path = Path(path)

        with ZipFile(path) as zip_file:
            for info in zip_file.infolist():
                if Path(info.filename).name == self.MANIFEST_FILENAME:
                    break
            else:
                raise FileNotFoundError(f"Manifest file not found in {path}")
            
            tmpdir = ez.EZ_FRAMEWORK_DIR / "temp" / "plugins"
            tmpdir.mkdir(parents=True, exist_ok=True)

            tmpdir /= path.stem
            if tmpdir.exists():
                rmtree(str(tmpdir))
            tmpdir.mkdir(parents=False, exist_ok=False)

            zip_file.extractall(tmpdir)

        self.install_from_path(tmpdir)

        rmtree(str(tmpdir))

    def uninstall_plugin(self, name: str):
        raise NotImplementedError("Uninstalling plugins is not yet supported")
        # plugin_dir = ez.PLUGINS_DIR / name
        # if not plugin_dir.exists():
        #     raise FileNotFoundError(f"Plugin {name} is not installed")
        
        # for file in plugin_dir.iterdir():
        #     file.unlink()
        # plugin_dir.rmdir()

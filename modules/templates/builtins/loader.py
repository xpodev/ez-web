import yaml

from contextlib import contextmanager
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

from .template_module import TemplateModule
from .template_module_loader import TemplateModuleLoader
from .ez_template import EZTemplate

from ..template_pack import TemplatePack
from ..template_package_info import TemplatePackageInfo, TemplateMappingInfo
from ..machinery.loader import ITemplatePackLoader, TemplatePackage


def create_mapping(info: TemplateMappingInfo, path: Path) -> dict[Path, str]:
    result = {}

    if info.root:
        path = (path / info.root).resolve()

    for name, path_or_info in info.mappings.items():
        if isinstance(path_or_info, str):
            result[path / path_or_info] = name
        else:
            result |= create_mapping(path_or_info, path)

    return result


class EZTemplateLoader(ITemplatePackLoader):
    EZ_TEMPLATE_LOADER_NAME = "EZ Template Loader"

    EZ_TEMPLATE_CONFIG_FILENAME = "template-pack.yaml"

    def __init__(self, template_dir: str) -> None:
        super().__init__(template_dir)

        self._loader = TemplateModuleLoader()
        self._current_package: TemplatePackage | None = None
        self._current_pack: TemplatePack | None = None

    @property
    def current_package(self) -> TemplatePackage | None:
        return self._current_package

    @property
    def current_pack(self) -> TemplatePack | None:
        return self._current_pack
    
    @contextmanager
    def pack(self, pack: TemplatePack | None):
        pack, self._current_pack = self._current_pack, pack
        try:
            assert self.current_pack is not None
            yield self.current_pack
        finally:
            self._current_pack = pack

    def load(self, package_name: str) -> TemplatePackage | None:
        path = self.template_dir / package_name

        if not path.is_dir():
            return None

        config_file = path / self.EZ_TEMPLATE_CONFIG_FILENAME

        if not config_file.exists():
            return None

        with open(config_file, "r") as f:
            data = yaml.safe_load(f)
            data["package_name"] = package_name

            info = TemplatePackageInfo.model_validate(data)

        package = TemplatePackage(self.EZ_TEMPLATE_LOADER_NAME, info)

        self._current_package = package

        if info.mappings:
            mappings = TemplateMappingInfo.model_validate(
                {"root": "", "mappings": info.mappings}
            )
            mapping = create_mapping(mappings, path / info.root)
        else:
            mapping = {}

        with self.pack(package.pack):
            self._load_templates(
                (path / package.info.root).resolve(), mapping, package.pack
            )

        self._current_package = None

        return package

    def _load_templates(self, path: Path, mapping: dict[Path, str], pack: TemplatePack):
        if not path.is_dir():
            return

        for item in path.iterdir():
            name = mapping.get(item, item.stem)
            if item.name.startswith("_"):
                continue
            elif item.is_dir():
                with self.pack(TemplatePack(name, pack)) as pk:
                    self._load_templates(item, mapping, pk)
                if pk.items:
                    pack.add(pk)
            elif item.suffix == ".py":
                template = self._load_template(item, name)

                if template.render is None:
                    continue

                pack.add(template)

    def _load_template(self, path: Path, name: str):
        module = self._load_template_module(path)
        return EZTemplate(name, module)

    def _load_template_module(self, path: Path) -> TemplateModule:
        spec = spec_from_file_location(path.stem, path, loader=self._loader)
        if spec is None:
            raise ImportError(f"Could not load module from {path}")
        module = module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        assert isinstance(module, TemplateModule)
        return module

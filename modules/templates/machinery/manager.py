import ez

from pathlib import Path
from typing import Callable

from ..template import Template
from ..template_pack import TemplatePack
from ..template_package import TemplatePackage

from .loader import ITemplatePackLoader


class RootPack(TemplatePack):
    def __init__(self) -> None:
        super().__init__("", None)

    def add(self, item: TemplatePack | Template, alias: str = None) -> None:
        super().add(item, alias)
        item._parent = None


class TemplateManager:
    _root: RootPack

    def __init__(self, template_dir: str) -> None:
        self._root = RootPack()
        self._template_dir = Path(template_dir)
        self._loaders: list[ITemplatePackLoader] = []
        self._packages: list[TemplatePackage] = []

        self._current_loader: ITemplatePackLoader | None = None

    @property
    def current_loader(self) -> ITemplatePackLoader | None:
        return self._current_loader

    def add(self, item: TemplatePack | Template, alias: str = None) -> None:
        self._root.add(item, alias)

    def get(self, name: str) -> TemplatePack | Template:
        return self._root.get(name)

    def load_template_packs_from(self, path: Path | str):
        path: Path = Path(path)

        for item in path.iterdir():
            for loader in self._loaders:
                self._current_loader = loader
                package = loader.load(item.name)
                if package:
                    self.add_package(package)
                break
            else:
                ez.log.error("Could not load template pack:", item.name)
        self._current_loader = None

    def load_template_packs(self):
        self.load_template_packs_from(self._template_dir)

    def add_package(self, package: TemplatePackage) -> None:
        self._packages.append(package)
        self.add(package.pack)

    def add_loader(
        self, loader: ITemplatePackLoader | Callable[[str], ITemplatePackLoader]
    ) -> None:
        if isinstance(loader, ITemplatePackLoader):
            self._loaders.append(loader)
        else:
            self._loaders.append(loader(self._template_dir))

    def get_packages(self) -> list[TemplatePackage]:
        return self._packages.copy()

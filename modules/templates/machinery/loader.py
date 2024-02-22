from pathlib import Path

from ..template_package import TemplatePackage


class ITemplatePackLoader:
    def __init__(self, template_dir: str) -> None:
        self._template_dir = Path(template_dir)

    @property
    def template_dir(self) -> Path:
        return self._template_dir

    def load(self, package_name: str) -> TemplatePackage | None:
        raise NotImplementedError

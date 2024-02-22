from .template_package_info import TemplatePackageInfo
from .template_pack import TemplatePack


class TemplatePackage:
    def __init__(self, loader_name: str, info: TemplatePackageInfo) -> None:
        self._info = info
        self._pack = TemplatePack(info.package_name, None)
        self._loader_name = loader_name

    @property
    def info(self) -> TemplatePackageInfo:
        return self._info

    @property
    def pack(self) -> TemplatePack:
        return self._pack

    @property
    def loader_name(self) -> str:
        return self._loader_name

from ..errors import TemplateNotFoundError
from ..manager import TEMPLATE_MANAGER as __tm
from ..template_package import TemplatePackage
from ..template_pack import TemplatePack
from ..template import Template, template


def get(name: str) -> "TemplatePack | Template":
    return __tm.get(name)


def get_packages() -> list["TemplatePackage"]:
    return __tm.get_packages()


__all__ = [
    "get",
    "get_packages",
    "template",
]

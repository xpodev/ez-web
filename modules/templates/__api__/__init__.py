from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from modules.templates.errors import TemplateNotFoundError
    from modules.templates.template_package import TemplatePackage
    from modules.templates.template_pack import TemplatePack
    from modules.templates.template import Template, TemplateParams, template
else:
    from ..errors import TemplateNotFoundError
    from ..manager import TEMPLATE_MANAGER as __tm
    from ..template_package import TemplatePackage
    from ..template_pack import TemplatePack
    from ..template import Template, TemplateParams, template


class Empty(TemplateParams):
    pass


def get(name: str) -> "TemplatePack | Template":
    return __tm.get(name)


def get_packages() -> list["TemplatePackage"]:
    return __tm.get_packages()


__all__ = [
    "get",
    "get_packages",
    "template",
]

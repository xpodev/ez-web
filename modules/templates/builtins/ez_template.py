from ..template import FunctionalTemplate
from ..template_pack import TemplatePack

from .template_module import TemplateModule


class EZTemplate(FunctionalTemplate):
    _module: TemplateModule

    def __init__(
        self, name: str, module: TemplateModule, parent: TemplatePack | None = None
    ) -> None:
        super().__init__(name, module.render, parent)
        self._module = module

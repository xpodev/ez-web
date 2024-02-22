from ..template import Template
from ..template_pack import TemplatePack

from .template_module import TemplateModule


class EZTemplate(Template):
    _module: TemplateModule

    def __init__(
        self, name: str, module: TemplateModule, parent: TemplatePack | None = None
    ) -> None:
        super().__init__(name, parent)
        self._module = module

        self.render = self._module.render

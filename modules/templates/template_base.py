from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .template_pack import TemplatePack

from .utils import TEMPLATE_SEPARATOR, assert_valid_template_name


class TemplateBase:
    _name: str
    _parent: "TemplatePack | None"

    def __init__(self, name: str, parent: "TemplatePack | None" = None) -> None:
        assert_valid_template_name(name)
        self._name = name
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> "TemplatePack | None":
        return self._parent

    @property
    def full_name(self) -> str:
        if self._parent:
            return f"{self._parent.full_name}{TEMPLATE_SEPARATOR}{self._name}"
        return self._name

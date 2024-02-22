from .template_base import TemplateBase
from .template import Template
from .utils import TEMPLATE_SEPARATOR
from .errors import TemplateNotFoundError


class TemplatePack(TemplateBase):
    items: dict[str, "TemplatePack | Template"]

    def __init__(
        self,
        name: str,
        parent: "TemplatePack | None" = None,
        *items: "TemplatePack | Template",
    ) -> None:
        super().__init__(name, parent)
        self.items = {}
        for item in items:
            self.add(item)

    def add(self, item: "TemplatePack | Template", alias: str = None) -> None:
        if not alias:
            alias = item.name
        if alias in self.items:
            raise ValueError(f"Item with name '{alias}' already exists in the pack")
        if item.parent and item.parent != self:
            raise ValueError(f"Item '{alias}' already belongs to another pack")
        self.items[alias] = item
        item._parent = self

    def get(self, name: str) -> "TemplatePack | Template":
        parts = name.split(TEMPLATE_SEPARATOR)
        try:
            if len(parts) == 1:
                return self.items[name]
            item = self
            for part in parts:
                item = item[part]
            return item
        except KeyError:
            raise TemplateNotFoundError(name)

    def __getitem__(self, name: str) -> "TemplatePack | Template":
        return self.get(name)

    def __setitem__(self, name: str, item: "TemplatePack | Template") -> None:
        self.add(item, name)

    def __contains__(self, name: str) -> bool:
        return name in self.items

    def __iter__(self):
        return iter(self.items.values())

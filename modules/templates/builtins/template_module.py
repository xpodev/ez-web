from typing import Callable
from types import ModuleType

from ..types import RenderResult


class TemplateModule(ModuleType):
    render: Callable[..., RenderResult] | None

    def __init__(self, name: str, doc: str | None = ...) -> None:
        super().__init__(name, doc)

    def __str__(self) -> str:
        return f"<TemplateModule {self.__name__}>"

from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from jsx.html import Element
    from jsx.components import Component


HTML: TypeAlias = str | int | float | bool
RenderResult: TypeAlias = "Component | Element | HTML"

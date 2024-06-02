from inspect import signature
from typing import TYPE_CHECKING, Callable, Generic, TypeAlias, TypeVar

from .template_params import TemplateParams
from .template_base import TemplateBase
from .types import RenderResult

if TYPE_CHECKING:
    from .template_pack import TemplatePack


T = TypeVar("T", bound=TemplateParams)
Render: TypeAlias = Callable[[T], RenderResult]


class Template(TemplateBase, Generic[T]):
    def __init__(self, name: str, params: type[T] | type, parent: "TemplatePack | None" = None):
        if not isinstance(params, type) or not issubclass(params, TemplateParams):
            raise TypeError(f"Functional template parameter must be a subclass of TemplateParams. Got {params}.")

        super().__init__(name, parent)

        self._params = params

    @property
    def params(self):
        return self._params

    def render(self, args: T) -> RenderResult:
        raise NotImplementedError


class FunctionalTemplate(Template, Generic[T]):
    def __init__(self, name: str, render: Render[T], parent: "TemplatePack | None" = None) -> None:
        sig = signature(render)

        if len(sig.parameters) != 1:
            raise TypeError(f"Functional template must have exactly one parameter. Got {len(sig.parameters)}.")
        
        annotation = list(sig.parameters.values())[0].annotation

        super().__init__(name, annotation, parent)
        self._render = render

    def render(self, args: T) -> RenderResult:
        return self._render(args)


def template(name: str) -> Callable[[Render[T]], Render[T]]:
    raise NotImplementedError

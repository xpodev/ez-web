from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Generic, overload, TYPE_CHECKING

from .types import RenderResult
from .template_base import TemplateBase
from .utils import is_type, is_function, assert_valid_template_name, is_renderable


if TYPE_CHECKING:
    from .template_package import TemplatePack


T = TypeVar("T")
P = ParamSpec("P")
RenderResultT = TypeVar("RenderResultT", bound=RenderResult)


def _try_get_current_pack() -> "TemplatePack | None":
    from .manager import TEMPLATE_MANAGER

    loader = TEMPLATE_MANAGER.current_loader
    if loader is None:
        return None

    try:
        return loader.current_pack
    except AttributeError:
        return None


class Template(TemplateBase):
    def render(self, *args, **kwargs) -> RenderResult:
        raise NotImplementedError


class FunctionalTemplate(Template, Generic[P, RenderResultT]):
    def __init__(self, name: str) -> None:
        super().__init__(name, None)

    def __call__(self, *args: P.args, **kwds: P.kwargs) -> RenderResultT:
        return self.render(*args, **kwds)


def template(name: str):
    assert_valid_template_name(name)

    current_pack = _try_get_current_pack()
    if current_pack is None:
        raise TypeError(
            f"Current template pack loader does not support adding templates."
        )

    @overload
    def wrapper(cls: type[T]) -> type[T]: ...
    @overload
    def wrapper(
        cls: Callable[P, RenderResultT]
    ) -> FunctionalTemplate[P, RenderResultT]: ...

    def wrapper(cls: type[T] | Callable[P, RenderResult]):
        if is_type(cls):

            if not is_renderable(cls):
                raise TypeError(
                    f"Class '{cls.__name__}' must implement a 'render' method to be a valid template."
                )
            
            class _(Template):
                def __init__(self):
                    super().__init__(name, None)

                @wraps(cls.render)
                def render(self, *args, **kwargs) -> RenderResult:
                    return cls.render(cls(), *args, **kwargs)

            current_pack.add(type(cls.__name__, (_,), {})())
            return cls

        elif is_function(cls):

            class _(FunctionalTemplate[P]):
                def render(self, *args: P.args, **kwargs: P.kwargs) -> RenderResult:
                    return cls(*args, **kwargs)

            result = type(name, (_,), {})(name)
            current_pack.add(result)
            return result
        else:
            raise TypeError(
                f"Decorated template must either be a class or a function, not {type(cls).__name__}"
            )

    return wrapper


__all__ = [
    "Template",
    "template",
]

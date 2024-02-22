from typing import Callable, TypeVar, TypeGuard, ParamSpec, Protocol

from .types import RenderResult

TEMPLATE_SEPARATOR = "/"


T = TypeVar("T")
P = ParamSpec("P")


class Renderable(Protocol):
    def render(self) -> RenderResult: ...


def is_type(cls: type[T]) -> TypeGuard[type[T]]:
    return isinstance(cls, type)


def is_function(value: Callable[P, T]) -> TypeGuard[Callable[P, T]]:
    return callable(value)


def is_renderable(value: object) -> TypeGuard[Renderable]:
    return callable(getattr(value, "render", None))


def is_valid_template_name(name: str):
    return TEMPLATE_SEPARATOR not in name


def assert_valid_template_name(name: str):
    if not is_valid_template_name(name):
        raise ValueError(
            f"Invalid template name: {name}. Must not contain '{TEMPLATE_SEPARATOR}'"
        )

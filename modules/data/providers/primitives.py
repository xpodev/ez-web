from typing import Any, ClassVar, Generic, TypeVar

from pydantic import RootModel

from .provider import DataProviderBase

from seamless.html import Input


_T = TypeVar("_T")


# class Value(RootModel[_T], Generic[_T]):
#     ...


class Config(RootModel[_T], Generic[_T]):
    ...


class _ValueProvider(DataProviderBase[_T], Generic[_T]):
    DEFAULT: ClassVar[Any]

    def __init__(self, value: _T):
        self.value = value

    def provide(self) -> _T:
        return self.value
    
    @classmethod
    def default(cls):
        return cls(cls.DEFAULT)
    
    @classmethod
    def load(cls, config: _T):
        return cls(config)


class StringProvider(_ValueProvider[str], data_type=str):
    DEFAULT = ""

    def render_input(self):
        return Input(value=self.value)


class IntegerProvider(_ValueProvider[int], data_type=int):
    DEFAULT = 0

    def render_input(self):
        return Input(type="number", value=self.value)
    

class BooleanProvider(_ValueProvider[bool], data_type=bool):
    DEFAULT = False

    def render_input(self):
        return Input(type="checkbox", checked=self.value)

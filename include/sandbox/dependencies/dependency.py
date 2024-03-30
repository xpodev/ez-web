from typing import Generic, TypeVar


T = TypeVar('T')


class Dependency(Generic[T]):
    _dependency_type: type[T]

    def __init__(self, type_: type[T]) -> None:
        self._dependency_type = type_

    @property
    def type(self):
        return self._dependency_type

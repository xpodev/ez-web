from typing import TypeVar

from .dependency import Dependency


T = TypeVar('T')


class DependencyProvider:
    def get(self, dependency: Dependency[T]) -> T | Dependency[T]:
        """
        Try to get the value associated with the given dependency.

        If a dependency is not found, the method should return the dependency itself.
        """
        raise NotImplementedError

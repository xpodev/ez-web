from collections import OrderedDict
from enum import Enum
from typing import TypeVar, Generic


T = TypeVar('T')


class NodeStatus(Enum):
    NotVisited = 0
    Visiting = 1
    Visited = 2


class CircularDependencyException(Exception, Generic[T]):
    _chain: list[T]

    def __init__(self, *chain: T):
        self._chain = list(chain)

    @property
    def chain(self):
        return self._chain


class DependencyGraph(Generic[T]):
    _graph: dict[T, list[T]]

    def __init__(self):
        self._graph = {}

    def get_dependency_order(self) -> list[list[T]]:
        visit_status: dict[T, NodeStatus] = {
            item: NodeStatus.NotVisited for item in self._graph
        }
        _levels: dict[T, int] = {}
        _error_nodes: set[T] = set()

        def _get_max_dependency_level(dependant: T) -> int:

            if visit_status[dependant] == NodeStatus.Visited:
                return _levels[dependant]
            visit_status[dependant] = NodeStatus.Visiting

            max_dependency_level = 0
            max_dependency: T | None = None

            for dependency in self._graph[dependant]:
                # if dependency is dependant:
                #     raise CircularDependencyException[T](dependency)

                dependency_level = 0
                try:
                    match visit_status[dependency]:
                        case NodeStatus.NotVisited:
                            dependency_level = _get_max_dependency_level(dependency)
                        case NodeStatus.Visited:
                            dependency_level = _levels[dependency]
                        case NodeStatus.Visiting:
                            raise CircularDependencyException[T]()
                except CircularDependencyException as _e:
                    _e.chain.insert(0, dependency)
                    raise _e

                if dependency_level > max_dependency_level:
                    max_dependency = max_dependency
                    max_dependency_level = dependency_level

            if max_dependency is not None and max_dependency_level <= _levels[dependant]:
                raise CircularDependencyException(f"Circular dependency found: {dependant} <-> {max_dependency}")
            visit_status[dependant] = NodeStatus.Visited
            max_dependency_level += 1
            _levels[dependant] = max_dependency_level
            return max_dependency_level

        for item in self._graph:
            if item in _error_nodes:
                continue
            try:
                _get_max_dependency_level(item)
            except CircularDependencyException as e:
                for node in e.chain:
                    _error_nodes.add(node)
                e.chain.insert(0, item)
                raise e

        order = OrderedDict[int, list[T]]()

        for item, level in _levels.items():
            if level not in order:
                order[level] = list[T]()
            order[level].append(item)

        return list[list[T]](order.values())

    def add(self, dependant: T, *dependencies: T):
        if dependant not in self._graph:
            self._graph[dependant] = []
        self._graph[dependant].extend(dependencies)
        for dependency in dependencies:
            self.add(dependency)

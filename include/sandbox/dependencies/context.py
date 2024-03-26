from .provider import DependencyProvider


class Context:
    _providers: list[DependencyProvider]

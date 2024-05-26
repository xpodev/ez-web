from typing import Any, Generic, Self, TypeVar, get_args, get_origin

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class Configurable(Generic[T]):
    config: T

    def __init__(self, config: T):
        self.config = config

    def save(self) -> dict[str, Any]:
        return self.config.model_dump()

    @classmethod
    def load(cls, config: dict) -> Self:
        for base in cls.__bases__:
            origin = get_origin(base)
            if isinstance(origin, type) and issubclass(origin, Configurable):
                args = get_args(base)
                if len(args) != 1:
                    raise ValueError(f"Configurable class {cls} has more than one type argument")
                config_cls = args[0]
                if isinstance(config_cls, TypeVar):
                    raise ValueError(f"Cannot load Configurable class {cls} with a type argument that is a TypeVar")
                if not issubclass(config_cls, BaseModel):
                    raise ValueError(f"Configurable class {cls} has a type argument that is not a subclass of BaseModel")
                config: BaseModel = config_cls.model_validate(config)
                return cls(config)
        raise ValueError(f"Configurable class {cls} does not have a base class that is a subclass of Configurable")

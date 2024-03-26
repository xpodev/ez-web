from .model_scope import ModelScope
from .model_base import ModelBase


class DataSpecification:
    _models: dict[ModelScope, type[ModelBase]]

    def __init__(self) -> None:
        self._models = {}

    def __getitem__(self, key: ModelScope) -> type[ModelBase]:
        return self._models[key]
    
    def __setitem__(self, key: ModelScope, value: type[ModelBase]) -> None:
        if key not in value.allowed_scopes:
            raise ValueError(f"Model {value} is not allowed scope {key}")
        self._models[key] = value

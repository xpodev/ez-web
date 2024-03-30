from typing import Callable, TypeVar

from .model_base import ModelBase
from .model_scope import ModelScope


T = TypeVar("T", bound=ModelBase)
U = TypeVar("U", bound=ModelBase)


class Context:
    def change_model_scope(self, model: ModelBase, target_scope: ModelScope) -> ModelBase:
        if target_scope not in model.allowed_scopes:
            raise ValueError(f"Model {model} is not allowed scope {target_scope}")
        if model.data_specification is None:
            raise ValueError(f"Model {model} does not have a data specification")
        target_model = model.data_specification[target_scope]
        return self.cast(model, target_model)

    def cast(self, input_model: ModelBase, output_model_type: type[T]) -> T:
        return self.get_casting_function(type(input_model), output_model_type)(input_model)

    def get_casting_function(self, input_model: type[T], output_model: type[U]) -> Callable[[T], U]:
        ...

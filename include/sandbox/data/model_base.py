from typing import ClassVar, TYPE_CHECKING

from .model_scope import ModelScope


if TYPE_CHECKING:
    from .data_specification import DataSpecification


class ModelBase:
    allowed_scopes: ClassVar[tuple[ModelScope, ...]]
    data_specification: 'DataSpecification | None'

import warnings

from typing import Any, ClassVar

from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase

from ez.site import CONFIG


class DatabaseModel(DeclarativeBase):
    __tablename__: ClassVar[str]
    __table_args__ = {
        "extend_existing": True,
    }
    __ez_id_column__: "ClassVar[Column] | None" = None

    def __init_subclass__(cls, **kw: Any) -> None:
        if not hasattr(cls, "__tablename__"):
            table_name = cls.__name__.rstrip("Model").lower() + "s"
            warnings.warn(f"__tablename__ not set for {cls.__name__}, defaulting to {table_name}")
            cls.__tablename__ = table_name
        cls.__tablename__ = CONFIG.database.prefix + cls.__tablename__
        super().__init_subclass__(**kw)

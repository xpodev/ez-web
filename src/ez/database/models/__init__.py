import os
from sqlalchemy.orm import DeclarativeBase, declared_attr
from .. import session


class Model(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return os.environ.get("DATABASE_PREFIX", "") + (
            cls.__table_name__
            if hasattr(cls, "__table_name__")
            else cls.__name__.removesuffix("Model").lower() + "s"
        )

    @classmethod
    def all(cls):
        return session.query(cls).all()
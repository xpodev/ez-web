from typing import TypeVar

from sqlalchemy import Column, Engine, select
from sqlalchemy.orm import Session

from .database_model import DatabaseModel
from .repository import Repository


T = TypeVar("T", bound=DatabaseModel)


class DatabaseRepository(Repository[T]):
    _session: Session | None

    def __init__(self, data_type: type[T], table_name: str = None, cache=None):
        super().__init__(cache)
        self._model = data_type
        self._session = None

    @property
    def is_connected(self) -> bool:
        return self._session is not None

    def connect(self, session: Session | Engine) -> None:
        if isinstance(session, Engine):
            self._session = Session(session)
        else:
            self._session = session
        self._model.registry.metadata.reflect(bind=self._session.bind)
        self.on_connect()

    def disconnect(self) -> None:
        self._session = None
        self.on_disconnect()

    def on_connect(self): ...

    def on_disconnect(self): ...

    def all(self, limit: int = None, skip: int = None):
        return self._session.query(self._model).limit(limit).offset(skip).all()

    def _get(self, key: str, **kwargs) -> Column:
        if kwargs:
            raise ValueError("kwargs are not supported by DatabaseRepository")
        if self._model.__ez_id_column__ is None:
            return self._session.get(self._model, key)
        return self._session.scalars(
            select(self._model).where(self._model.__ez_id_column__ == key)
        ).one()

    @classmethod
    def create_type(cls, model: type[T]) -> "type[DatabaseRepository[T]]":
        return lambda *args, **kwargs: cls(model, *args, **kwargs)

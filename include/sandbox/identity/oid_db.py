from typing import TYPE_CHECKING, Any, TypeAlias

if TYPE_CHECKING:
    from ez.data.repository import Repository

from .object_id import ObjectID
from .uid import UID


Category: TypeAlias = str
ObjectPath: TypeAlias = list[str] | None


class OIDCategory:
    def add(self, value: Any, *, oid: ObjectID | None = None) -> ObjectID:
        raise NotImplementedError()
    
    def get(self, oid: ObjectID, path: ObjectPath) -> "Repository":
        raise NotImplementedError()
    
    def set(self, oid: ObjectID, path: ObjectPath, value):
        raise NotImplementedError()


class OIDCategoryRepository(OIDCategory):
    _repository: "Repository[Any]"

    def __init__(self, name: str, repository: "Repository") -> None:
        self.name = name
        self._repository = repository

    def get(self, oid: ObjectID, path: ObjectPath) -> Any:
        result = self._repository.get(oid)
        if path:
            for key in path:
                result = result[key]
        return result
    
    def set(self, oid: ObjectID, path: ObjectPath, value):
        if path:
            raise ValueError("Cannot set a value on a path in a repository")
        self._repository.set(oid, value)


class OIDCategoryDB(OIDCategory):
    _db: "ObjectDatabase"

    def __init__(self, oid_db: "ObjectDatabase") -> None:
        self._db = oid_db

    def get(self, oid: ObjectID, path: ObjectPath) -> Any:
        if not path:
            raise ValueError("Must have at least 1 path element to get a value from a repository")
        result = self._db.get_category(oid)
        uid, *path = path
        return result.get(uid, path)
    
    def set(self, oid: ObjectID, path: ObjectPath, value):
        if not path:
            raise ValueError("Must have at least 1 path element to get a value from a repository")
        result = self._db.get_category(oid)
        uid, *path = path
        result.set(uid, path, value)


class ObjectDatabase:
    _categories: dict[Category, OIDCategory]

    def __init__(self) -> None:
        self._categories = {}

        self.add_category("oid", OIDCategoryDB(self))

    def add_category(self, category: Category, repository: OIDCategory) -> None:
        self._categories[category] = repository

    def get_category(self, category: Category) -> OIDCategory:
        return self._categories[category]

    def get(self, uid: UID):
        return self.get_category(uid.category).get(*self._unpack_uid(uid))
    
    def set(self, uid: UID, value) -> None:
        self.get_category(uid.category).set(*self._unpack_uid(uid), value)

    @staticmethod
    def _unpack_uid(uid: UID) -> tuple[str, ObjectPath]:
        return uid.id, None if uid.sub_id is None else uid.sub_id.split("/")

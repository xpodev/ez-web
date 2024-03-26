from typing import TypeAlias


ObjectID: TypeAlias = str


class ObjectIDBase:
    _id: ObjectID

    def __init__(self, _id: ObjectID) -> None:
        self._id = _id

    @property
    def oid(self) -> ObjectID:
        return self._id

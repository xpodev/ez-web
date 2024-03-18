from dataclasses import dataclass
from typing import TYPE_CHECKING

from .object_id import ObjectID


if TYPE_CHECKING:
    from .oid_db import Category


@dataclass(frozen=True, slots=True)
class UID:
    category: "Category"
    id: ObjectID
    sub_id: str | None = None

    def __str__(self) -> str:
        if self.sub_id:
            return f"{self.category}://{self.id}/{self.sub_id}"
        return f"{self.category}://{self.id}"
    
    def __repr__(self) -> str:
        return f"UID({self.category!r}, {self.id!r}, {self.sub_id!r})"
    
    def __hash__(self) -> int:
        return hash((self.category, self.id, self.sub_id))

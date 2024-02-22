from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


@dataclass
class Module:
    name: str | None
    entry_point: ModuleType
    entry_point_path: Path
    priority: int = 0

    @property
    def is_package(self) -> bool:
        return self.entry_point_path.name == "__main__.py"

    def __str__(self) -> str:
        return f"{self.name} @ {self.entry_point_path.parent if self.is_package else self.entry_point_path}"

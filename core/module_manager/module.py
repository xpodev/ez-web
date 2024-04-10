from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

@dataclass
class Module:
    name: str
    entry_point: ModuleType
    entry_point_path: Path
    priority: int = 0

    def __str__(self) -> str:
        return f"{self.name} @ {self.entry_point_path.parent} ({self.priority})"
    
    def __hash__(self) -> int:
        return hash(self.entry_point_path)

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, eq=False, unsafe_hash=False)
class Config:
    module_directory_name: str = "modules"
    modules_namespace: str = "ez.global.modules"
    module_entry_filename: str = "__main__"
    exclude: list[str] = field(default_factory=lambda: ["__pycache__"])
    module_api_directory: str = "include/ez"

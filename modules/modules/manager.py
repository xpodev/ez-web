from utilities.semver import SemanticVersion
from .module import Module

from importlib.util import spec_from_file_location, module_from_spec
from importlib import reload
from pathlib import Path

import sys
THIS = sys.modules[__name__]


from . import __version__


class ModuleManager:
    PACKAGE_ENTRY_POINT = "__main__.py"
    MODULE_PREFIX = "ez.global.modules"

    def __init__(self, module_dir: Path) -> None:
        self.module_dir = module_dir
        self._modules: list[Module] = []

    def load_modules(self, *, reload: bool = True) -> bool:
        """
        Load all modules from the path given in the constructor.

        If the modules were already loaded and reload is True, this will
        reload all the modules. If reload is false, this will do nothing.

        Returns True if any module was loaded or reloaded.
        """

        # TODO: raise/log relevant errors instead of returning False

        if self._modules:
            if not reload:
                return False
            for module in self._modules:
                self.reload_module(module)
            return True
        if not self.module_dir.exists():
            return False
        if not self.module_dir.is_dir():
            return False
        for item in self.module_dir.iterdir():
            name = item.stem
            if item.is_dir():
                if not (item / self.PACKAGE_ENTRY_POINT).exists():
                    continue
                item /= self.PACKAGE_ENTRY_POINT
            if not item.is_file():
                continue
            if item.suffix != ".py":
                continue
            self._load_module_from(name, item)
        if self._modules:
            self._modules.append(Module(
                "Module Manager",
                THIS,
                Path(THIS.__file__),
                SemanticVersion.parse(THIS.__version__),
                "Module Manager by EZ Framework."
            ))
            return True
        return False

    def _load_module_from(self, name: str, path: Path):
        spec = spec_from_file_location(self.get_module_full_name(name), str(path))
        entry_point = module_from_spec(spec)
        spec.loader.exec_module(entry_point)

        if not hasattr(entry_point, "__version__"):
            raise Exception(f"Invalid module '{name}' at '{path}'")
        
        name = getattr(entry_point, "__title__", name)
        version = SemanticVersion.parse(entry_point.__version__)
        description = getattr(entry_point, "__description__", getattr(entry_point, "__doc__", ""))

        module = Module(name, entry_point, path, version, description)
        self._modules.append(module)

    def reload_module(self, module: Module):
        if module not in self._modules:
            # TODO: create a more specific exception
            raise Exception(f"Module '{module.name}' was never loaded.")

        reload(module)

    def get_modules(self):
        return self._modules.copy()

    @classmethod
    def get_module_full_name(cls, name: str):
        return cls.MODULE_PREFIX + '.' + name

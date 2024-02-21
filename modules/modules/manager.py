from types import ModuleType
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
    MODULE_NAME_ATTRIBUTE = "__module_name__"

    def __init__(self, module_dir: Path) -> None:
        self.module_dir = module_dir
        self._modules: list[Module] = []

        sys.modules[self.MODULE_PREFIX] = type("", (ModuleType,), {
            "__path__": [str(module_dir)],
            "__package__": str(self.MODULE_PREFIX)
        })(self.MODULE_PREFIX)

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

        for module in self._modules:
            module.entry_point.__spec__.loader.exec_module(module.entry_point)

            if module.name is None:
                module.name = getattr(module.entry_point, self.MODULE_NAME_ATTRIBUTE, module.name)
        
        if self._modules:
            self._modules.append(Module(
                "Module Manager",
                THIS,
                Path(THIS.__file__),
            ))

        return bool(self._modules)

    def _load_module_from(self, name: str, path: Path):
        full_name = self.get_module_full_name(name)
        package_dir = path.parent

        init_file = package_dir / "__init__.py"
        if init_file.exists():
            spec = spec_from_file_location(
                full_name, 
                init_file, 
                submodule_search_locations=[
                    str(package_dir)
                ])
            module = sys.modules[spec.name] = module_from_spec(spec)
            spec.loader.exec_module(module)

            name = getattr(module, self.MODULE_NAME_ATTRIBUTE, name)
        else:
            name = None

        spec = spec_from_file_location(
            full_name + '.__main__', 
            str(path)
        )
        entry_point = module_from_spec(spec)
        sys.modules[spec.name] = entry_point

        module = Module(name, entry_point, path)
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

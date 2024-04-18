import sys

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import TYPE_CHECKING

from utilities.dependency_graph import CircularDependencyException, DependencyGraph

if TYPE_CHECKING:
    from sandbox.host.app_host import AppHost

import ez

from .config import Config
from .module import Module


class ModuleManager:
    MODULE_PRIORITY_ATTRIBUTE = "__priority__"
    MODULE_DEPENDENCIES_ATTRIBUTE = "__deps__"

    def __init__(self, app_host: "AppHost", config: Config) -> None:
        self.app_host = app_host
        self.config = config
        self.module_dir = ez.EZ_FRAMEWORK_DIR / config.module_directory_name
        self._modules: list[Module] = []

    def load_modules(self) -> bool:
        """
        Load all modules from the path given in the constructor.

        Returns True if any module was loaded.
        """

        # TODO: raise/log relevant errors instead of returning False

        if self._modules:
            return False
        
        if not self.module_dir.exists():
            return False
        if not self.module_dir.is_dir():
            return False

        module_names: dict[str, Module] = {}

        for item in self.module_dir.iterdir():
            if not item.is_dir():
                continue

            if item.name in self.config.exclude:
                continue

            module = self._load_module_from(item)
            if module is not None:
                self._modules.append(module)
                module_names[module.name] = module

        module_api_dir = (ez.EZ_FRAMEWORK_DIR / self.config.module_api_directory).resolve()

        graph = DependencyGraph[Module]()
        for module in self._modules:
            graph.add(module, *map(module_names.__getitem__, module.dependencies))

        try:
            order = graph.get_dependency_order()
        except CircularDependencyException as e:
            print("Circular dependency detected:", e.chain)
            return False

        for modules in order:
            for module in sorted(modules, key=lambda m: m.priority, reverse=True):
                if module.entry_point is None:
                    continue
                if module.entry_point.__spec__ is None:
                    continue
                if module.entry_point.__spec__.loader is None:
                    continue

                module_api = module_api_dir / module.name

                if module_api.exists() and module_api.is_dir():
                    module_api_init = module_api / "__init__.py"
                    if module_api_init.exists():
                        spec = spec_from_file_location(
                            self.get_module_full_name(module.name) + ".__api__", 
                            module_api_init, 
                            submodule_search_locations=[str(module_api)]
                        )
                        if spec is not None and spec.loader is not None:
                            module_api_module = sys.modules[spec.name] = sys.modules[f"ez.{module.name}"] = module_from_spec(spec)
                            setattr(ez, module.name, module_api_module)
                            spec.loader.exec_module(module_api_module)
                            del sys.modules[spec.name]

                module.entry_point.__spec__.loader.exec_module(module.entry_point)

        return bool(self._modules)

    def _load_module_from(self, dir_path: Path):
        module_name = dir_path.name
        full_module_name = self.get_module_full_name(module_name)

        entry_point_file = (dir_path / self.config.module_entry_filename).with_suffix(".py")
        if not entry_point_file.exists():
            return None

        init_file = dir_path / "__init__.py"
        if init_file.exists():
            spec = spec_from_file_location(
                full_module_name, init_file, submodule_search_locations=[str(dir_path)]
            )
            if spec is None:
                raise ImportError(f"Could not load module {module_name} from {init_file}")
            if spec.loader is None:
                raise ImportError(f"Could not load module {module_name} from {init_file}")
            module = sys.modules[spec.name] = module_from_spec(spec)
            spec.loader.exec_module(module)

            priority = getattr(module, self.MODULE_PRIORITY_ATTRIBUTE, 0)
            dependencies = getattr(module, self.MODULE_DEPENDENCIES_ATTRIBUTE, [])

        else:
            module = None
            priority = 0
            dependencies = []
        
        spec = spec_from_file_location(
            full_module_name + "." + self.config.module_entry_filename, 
            str(entry_point_file)
        )
        if spec is None:
            raise ImportError(f"Could not load module {module_name} from {dir_path}")
        if spec.loader is None:
            raise ImportError(f"Could not load module {module_name} from {dir_path}")
        
        entry_point = module_from_spec(spec)
        sys.modules[spec.name] = entry_point

        return Module(module_name, entry_point, dir_path, dependencies, priority=priority)

    def get_modules(self):
        return self._modules.copy()

    def get_module_full_name(self, name: str):
        return self.config.modules_namespace + "." + name

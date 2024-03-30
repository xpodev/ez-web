from importlib.abc import Loader

from .plugin_module import PluginModule


class PluginModuleLoader(Loader):
    def create_module(self, spec):
        module = PluginModule(spec.name, None)
        module.__spec__ = spec
        return module

    def exec_module(self, module):
        assert module.__spec__ is not None
        assert module.__spec__.origin is not None

        with open(module.__spec__.origin, "r") as file:
            code = file.read()

            bytecode = compile(code, module.__spec__.origin, "exec")
            exec(bytecode, vars(module))

from importlib.abc import Loader

from .template_module import TemplateModule


class TemplateModuleLoader(Loader):
    def create_module(self, spec):
        return TemplateModule(spec.name)

    def exec_module(self, module):
        if not isinstance(module, TemplateModule):
            raise ImportError("Invalid module type")

        with open(module.__spec__.origin, "r") as file:
            code = file.read()

            bytecode = compile(code, module.__spec__.origin, "exec")
            exec(bytecode, vars(module))

        if not hasattr(module, "render"):
            module.render = None

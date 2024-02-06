import ez
from importlib import import_module

TEMPLATE_DIR = ez.include_path("templates")

# should be from config
active_template = "ez2024"


def template(template_name: str = None):
    global active_template
    if template_name:
        active_template = template_name
    return active_template


def template_path():
    return "/".join([TEMPLATE_DIR, active_template])


def template_page(name: str):
    return "/".join([template_path(), "pages", name])


def template_part(name: str):
    return "/".join([template_path(), "partials", name])


def load_template(name: str):
    module_name = "/".join([template_path(), name]).replace("/", ".")
    module = import_module(module_name)
    if hasattr(module, "render"):
        return module.render
    else:
        raise AttributeError(f"Template {name} does not have a render function")
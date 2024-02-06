from importlib import import_module
from include.builtins.template_manager.plugin import template_part

def get_header(**kwargs):
    """
    Get the header for the page.

    :param kwargs: The arguments to pass to the header.
    """
    header_path = template_part("header")
    header = import_module(header_path.replace("/", "."))
    return header.Header(**kwargs)
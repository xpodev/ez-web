import ez

from . import ez_templates


ez.extend_ez(ez_templates, "templates")


__module_name__ = "Template Manager"

__priority__ = 20

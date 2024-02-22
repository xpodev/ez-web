from .machinery.manager import TemplateManager
from .builtins.loader import EZTemplateLoader
from .config import TEMPLATE_DIRECTORY


TEMPLATE_MANAGER = TemplateManager(TEMPLATE_DIRECTORY)
TEMPLATE_MANAGER.add_loader(EZTemplateLoader)

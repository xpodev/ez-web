from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from modules.plugins.events import Plugins
else:
    from ..events import Plugins

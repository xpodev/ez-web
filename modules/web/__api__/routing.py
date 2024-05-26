from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from modules.web.routing import mount
else:
    from ..routing import mount


del TYPE_CHECKING

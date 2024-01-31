import ez
import ez.log as log

from ez.database.models.plugin import Plugin
from ez.database import select, session
from ez.html.components import Page
from .components.plugin_list import PluginList

router = ez.router("/smack")

@router.get("/")
def home_page(request):
    plugins = select(Plugin).where(Plugin.id > 2)
    return Page(
        PluginList(session.scalars(plugins)),
    )

log.info("Plugin Manager loaded")

ez.add_router(router)
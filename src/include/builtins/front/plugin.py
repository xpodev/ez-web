import ez

from ez.database.models.plugin import PluginModel
from ez.database import select, session
from ez.pyx import Page
from .components.plugin_list import PluginList


@ez.get("/plugins")
def home_page():
    plugins = select(PluginModel)
    return Page(
        PluginList(session.scalars(plugins)),
    )


@ez.get("/post/{post_id}")
def post_page(post_id: int):
    post = select(PluginModel).where(PluginModel.id == post_id).first()
    return Page(
        PluginList([post]),
    )
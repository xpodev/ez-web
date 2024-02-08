from importlib import import_module
from fastapi import Request

import ez
from ez.utilities import pascal_case_to_snake_case, make_object

from ez.database.models.plugin import PluginModel
from ez.database import select, session
from ez.pyx import Page, Div
from .components.plugin_list import PluginList


@ez.get("/plugins")
def home_page():
    plugins = select(PluginModel)
    return Page(
        PluginList(session.scalars(plugins)),
    )

@ez.get("/plugins/{id}")
def get_plugin(id):
    return PluginModel.get(id)


@ez.get("/post/{post_id}")
def post_page(post_id: int):
    post = select(PluginModel).where(PluginModel.id == post_id).first()
    return Page(
        PluginList([post]),
    )


@ez.post("/c/{component}")
async def get_component(component: str, request: Request):
    props = await request.json()
    file_name = pascal_case_to_snake_case(component)
    module = import_module(f"include.builtins.front.components.{file_name}")
    if hasattr(module, component):
        object_props = {
            k: make_object(v) for k, v in props.items()
        }
        return getattr(module, component)(**object_props).to_json()
    return {"error": "Component not found"}


@ez.get("/react-test")
def react_test():
    return Page(
        Div(
            id="root"
        ),
        title="React Test",
    )
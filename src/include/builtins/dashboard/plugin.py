# from ez import ez
import ez
from ..tree_renderer.pyx.components.page import Page


@ez.get("/page/{page}")
def on_page(page: str):
    return Page(page, title=f"EZ Web Framework - Page : {page}")

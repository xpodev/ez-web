# from ez import ez
import ez
from ..pyx.components.page import Page

from .admin.home_controller import admin_home_router
ez.add_router(admin_home_router)

@ez.get("/page/{page}")
def on_page(page: str):
    return Page(page, title=f"EZ Web Framework - Page : {page}")


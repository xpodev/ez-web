import ez
from include.builtins.tree_renderer.events import TreeRenderer
from ...builtins.tree_renderer.transpiler.pyx.components.page import Page
from include.builtins.tree_renderer.transpiler.tree_node import EzTree

@ez.on(TreeRenderer.WillRender)
def update_title(page: Page):
    page.title = "EZ Web - Blah"



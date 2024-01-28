import ez
from include.builtins.pyx.events import TreeRenderer
from ez.html.components import Page

@ez.on(TreeRenderer.WillRender)
def update_title(page: Page):
    page.title = "EZ Web - Blah"



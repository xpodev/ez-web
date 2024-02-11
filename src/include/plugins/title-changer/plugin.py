import ez
from pyx.events import TreeRenderer
# from ez.pyx import Page



# class TitleChanger:
#     def change_title(self, page: Page):
#         page.title = "EZ Web - Blah"


@ez.on(TreeRenderer.WillRender)
def update_title(page: ...):
    page.title = "EZ Web - Blah"


@ez.get("/title")
def title():
    return "EZ Web - Blah"


__api__ = object()

from pyx.html import *
from pyx.components import *
from pyx.style import *
from ez.database.models.page import PageModel


def render(**props):
    return Page(
        SinglePage(
            **props,
        ),
    )


class SinglePage(Page):
    def __init__(self, page: PageModel, **props):
        self.page = page
        super().__init__(**props)

    def body(self):
        return Div(
            H1(
                self.page.title,
                class_name="bg-primary text-white p-3 mb-3 text-center",
            ),
            Div(
                self.page.content,
                class_name="p-3",
                style=Style(
                    {
                        "background-color": Color.MEDIUM_PURPLE,
                        "color": "white",
                        "padding": "10px",
                        "font-family": "sans-serif",
                    }
                ),
            ),
        )

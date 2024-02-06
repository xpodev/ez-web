from ez.pyx import *


def render(**props):
    return Page(
        PostPage(
            **props,
        ),
    )

class PostPage(Page):
    def body(self):
        return Div(
            H1(
                self.props["page"].title,
                class_name="bg-primary text-white p-3 mb-3 text-center",
            ),
            Div(
                self.props["page"].content,
                class_name="p-3",
                style=Style().font_size("1.5em").font_family("sans-serif")
            ),
        )

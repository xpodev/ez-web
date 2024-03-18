from jsx.components import ContainerComponent
from jsx.html import Fragment, Html, Head, Body, Title, Link, Script


class Page(ContainerComponent):
    def __init__(self, *children, title="Ez Web"):
        super().__init__(*children)
        self.title = title

    def render(self):
        return Fragment(
            "<!DOCTYPE html>",
            Html(
                Head(
                    Title(self.title),
                    Link(
                        rel="stylesheet",
                        href="https://unpkg.com/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                    ),
                    Script(src="/_jsx/main.js"),
                ),
                Body(
                    self.body(),
                ),
            ),
        )

    def body(self):
        return Fragment(*self.children)

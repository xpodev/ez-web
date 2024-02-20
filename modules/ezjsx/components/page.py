from jsx.components import Component
from jsx.html import Fragment, Html, Head, Body, Title, Link, Script


class Page(Component):
    def __init__(self, *children, title="Ez Web", **props):
        self.title = title
        self.children = children
        self.props = props

    def render(self):
        return Fragment(
            "<!DOCTYPE html>",
            Html(
                Head(
                    Title(self.title),
                    Link(
                        rel="stylesheet",
                        href="https://unpkg.com/browse/bootstrap@5.3.2/dist/css/bootstrap.min.css",
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

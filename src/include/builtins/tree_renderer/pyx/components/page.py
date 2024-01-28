from ..html import Fragment, Html, Head, Title, Link, Body
from .component import Component


class Page(Component):
    def __init__(self, *children, title=""):
        self.title = title
        self.children = children

    def render(self):
        return Fragment(
            "<!DOCTYPE html>",
            Html(
                Head(
                    Title(self.title),
                    Link(
                        rel="stylesheet",
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                    ),
                ),
                Body(
                    *self.children,
                ),
            ),
        )

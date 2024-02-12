from .component import Component
from pyx.utilities import get_header


class Page(Component):
    def __init__(self, *children, title="", **kwargs):
        self.title = title
        self.children = children
        self.props = kwargs

    def render(self):
        from ..html import Fragment, Html, Body
        return Fragment(
            "<!DOCTYPE html>",
            Html(
                get_header(title=self.title),
                Body(
                    self.body(),
                ),
            ),
        )
    
    def body(self):
        from ..html import Fragment
        return Fragment(*self.children)

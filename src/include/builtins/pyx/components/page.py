from ..html import Fragment, Html, Body
from .component import Component
from ..utilities import get_header


class Page(Component):
    def __init__(self, *children, title="", **kwargs):
        self.title = title
        self.children = children
        self.props = kwargs

    def render(self):
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
        return Fragment(*self.children)

from jsx.components import Component
from jsx.html import Div

class Card(Component):
    def __init__(self, *children, **props):
        self.children = children
        props["class_name"] = [props.get("class_name", ""), "card"]
        self.props = props

    def render(self):
        return Div(
            *self.children,
            **self.props,
        )
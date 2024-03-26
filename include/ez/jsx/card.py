from jsx.components import ContainerComponent
from jsx.html import Div


class Card(ContainerComponent):
    def __init__(self, *children, **props):
        super().__init__(*children)
        
        class_name = props.get("class_name", [])
        if isinstance(class_name, list):
            class_name.append("card")
        else:
            class_name = [class_name, "card"]

        props["class_name"] = class_name
        self.props = props

    def render(self):
        return Div(
            *self.children,
            **self.props,
        )

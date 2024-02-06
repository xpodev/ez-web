from ..components.component import Component


class Element:
    def __init__(
        self,
        *children: tuple["Element | Component | str"],
        class_name=None,
        html_for=None,
        inline=False,
        **kwargs
    ):
        self.children = [
            child.render() if isinstance(child, Component) else child
            for child in children
            if child is not None
        ]
        self.inline = inline
        kwargs["class"] = class_name
        kwargs["for"] = html_for
        self.props = kwargs

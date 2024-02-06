from .components.component import Component
from .html.element import Element
from html import escape


def render(component: Element | str) -> str:
    if isinstance(component, Component):
        component = component.render()

    if not isinstance(component, Element):
        return component

    tag_name = getattr(component, "tag_name", None)
    children = "".join([render(child) for child in component.children])

    if not tag_name:
        return children

    props = {k: v for k, v in component.props.items() if v not in [None, False]}

    if component.inline:
        if component.children != []:
            raise Exception("Inline components cannot have children")
        return f"<{tag_name} {render_props(props)}/>"

    props_string = render_props(props)
    if props_string != "":
        props_string = " " + props_string

    return f"<{tag_name}{props_string}>{children}</{tag_name}>"


def render_props(props: dict) -> str:
    return " ".join(f'{key}="{escape(str(value))}"' for key, value in props.items())

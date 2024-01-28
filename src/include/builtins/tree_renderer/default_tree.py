from .pyx.style.color import Color
from .pyx.style.style import Style
from .pyx.html import *
from .pyx.components import Page


def default_tree() -> Element:
    return Page(
        Div(
            "Hello, World!",
            Div(
                "This is a div!",
                style="background-color: red; color: white; padding: 10px;",
                class_name="some-div",
            ),
            style=Style(
                {
                    "background-color": Color.MEDIUM_PURPLE,
                    "color": "white",
                    "padding": "10px",
                    "font-family": "sans-serif",
                }
            ).font_size("32px"),
        ),
        title="EZ Web Framework",
    )

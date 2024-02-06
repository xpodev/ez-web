from ez.pyx import Component, Head, Link, Title


class Header(Component):
    def __init__(self, title="") -> None:
        self.title = title

    def render(self):
        return Head(
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
            ),
            Title(self.title),
        )

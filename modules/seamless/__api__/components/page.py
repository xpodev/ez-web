from seamless.components import Page as _Page
from seamless.html import Link, Script


class Page(_Page):
    def __init__(self, title="Ez Web"):
        super().__init__(title)
        # self.title = title

    def head(self):
        yield from super().head()
        yield Link(
            rel="stylesheet",
            href="https://unpkg.com/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        )
        yield Script(src="/_jsx/main.js")

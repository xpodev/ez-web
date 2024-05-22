from . import events

from ..page import Page

class PageManager:
    _pages: list[Page]

    def __init__(self) -> None:
        self._pages = []

    @property
    def pages(self) -> list[Page]:
        return self._pages

    def add(self, page: Page) -> None:
        # TODO: make syscall when events become protected
        self._pages.append(page)
        events.on_page_added(page)

    def remove(self, page: Page) -> None:
        try:
            self._pages.remove(page)
        except ValueError:
            pass
        else:
            events.on_page_removed(page)

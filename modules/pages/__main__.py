import ez

from ez.database import engine

from .dbi import PAGE_REPOSITORY, PageInfoModel
from .router import pages_api_router


from jsx.html import *

import ez.templates


def make_page_route(page: PageInfoModel):
    if not page.slug.startswith("/"):
        page.slug = f"/{page.slug}"

    render = ez.templates.get(page.template_name).render

    def page_route():
        return render(page)

    ez.get(page.slug)(page_route)


def setup():
    PAGE_REPOSITORY.connect(engine)

    pages = PAGE_REPOSITORY.all()
    for page in pages:
        make_page_route(page)


def main():
    setup()


main()

ez.add_router("/api/pages", pages_api_router)


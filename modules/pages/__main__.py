import inspect

import ez

from ez.database import engine
import ez.web

from .dbi import PAGE_REPOSITORY, PageInfoModel, PAGES_HISTORY_REPOSITORY
from .router import pages_api_router

from starlette.responses import HTMLResponse


from jsx.renderer import render

import ez.templates

def make_page_route(page: PageInfoModel):
    if not page.slug.startswith("/"):
        page.slug = f"/{page.slug}"


    template = ez.templates.get(page.template_name)

    def page_route():
        return HTMLResponse(render(template.render(page=page)))
    
    # page_route.__signature__ = new_signature

    ez.web.get(page.slug)(page_route)


def setup():
    PAGE_REPOSITORY.connect(engine)
    PAGES_HISTORY_REPOSITORY.connect(engine)

    pages = PAGE_REPOSITORY.all()
    for page in pages:
        make_page_route(page)


setup()


ez.web.add_router("/api/pages", pages_api_router)


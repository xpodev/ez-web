import ez

from ez.database import engine

from . import pages, router as _
from .dbi import PAGE_REPOSITORY, PageInfoModel, PAGES_HISTORY_REPOSITORY
from .page_info import PageInfo
from .routing import PAGE_ROUTER


def make_page_route(page_info: PageInfoModel):
    info = PageInfo.model_validate({
        "title": page_info.title,
        "config": page_info.config,
        "slug": page_info.slug,
        "template_name": page_info.template_name
    })
    page = pages.create_page(info)
    pages.add_page(page)


@ez.events.on("App.Started")
def setup():
    PAGE_REPOSITORY.connect(engine)
    PAGES_HISTORY_REPOSITORY.connect(engine)

    pages = PAGE_REPOSITORY.all()
    for page in pages:
        make_page_route(page)


ez.web.routing.mount(ez.site.SITE_URL, PAGE_ROUTER)

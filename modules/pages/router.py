import ez
from .dbi import PAGE_REPOSITORY, PageInfoModel

def page_result(page: PageInfoModel, content=True):
    page_data = {
        "id": page.id,
        "title": page.title,
        "slug": page.slug,
        "template_name": page.template_name,
    }

    if content:
        page_data["content"] = page.content

    return page_data

pages_api_router = ez.router()


@pages_api_router.get("")
async def get_pages(content=True):
    allPages = PAGE_REPOSITORY.all()
    return [page_result(page, content) for page in allPages]


@pages_api_router.get("/{page_id}")
async def get_page(page_id: int):
    return page_result(PAGE_REPOSITORY.get(id=page_id))
from json import dumps, loads
from fastapi import Request
import ez
from ezjsx.components import page
from .dbi import (
    PAGE_REPOSITORY,
    PageInfoModel,
    PAGES_HISTORY_REPOSITORY,
    PagesHistoryModel,
)


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


def page_history_result(page: PagesHistoryModel):
    return {
        "id": page.id,
        "title": page.title,
        "page_id": page.page_id,
        "content_data": loads(page.content_data),
        "date": page.date.timestamp(),
    }


pages_api_router = ez.router()


@pages_api_router.get("")
async def get_pages(content=True):
    allPages = PAGE_REPOSITORY.all()
    return [page_result(page, content) for page in allPages]


@pages_api_router.get("/{page_id}")
async def get_page(page_id: int):
    page = PAGE_REPOSITORY.get(key=page_id)
    return page_result(page)


@pages_api_router.post("")
async def create_page(request: Request):
    page = PageInfoModel(**await request.json())
    PAGE_REPOSITORY.set(value=page)


@pages_api_router.put("/{page_id}")
async def update_page(page_id: int, request: Request):
    page = PAGE_REPOSITORY.get(key=page_id)
    page_update = await request.json()
    page.content = page_update.get("content", page.content)
    page.title = page_update.get("title", page.title)
    page.slug = page_update.get("slug", page.slug)
    page.template_name = page_update.get("template_name", page.template_name)
    PAGE_REPOSITORY.set(value=page)


@pages_api_router.get("/{page_id}/history")
async def get_page_history(page_id: int, latest: bool = False, limit: int = 10):
    all = (
        PAGES_HISTORY_REPOSITORY.query()
        .filter(PagesHistoryModel.page_id == page_id)
        .order_by(
            PagesHistoryModel.date.desc() if latest else PagesHistoryModel.date.asc()
        )
        .limit(limit)
        .all()
    )
    if len(all) == 0:
        return []
    if latest:
        return page_history_result(all[0])
    return [page_history_result(page) for page in all]


@pages_api_router.post("/{page_id}/history")
async def create_page_history(page_id: int, request: Request):
    history = await request.json()
    history["content_data"] = dumps(history["content_data"], separators=(",", ":"))
    history["page_id"] = page_id
    page = PagesHistoryModel(**history)
    PAGES_HISTORY_REPOSITORY.set(value=page)

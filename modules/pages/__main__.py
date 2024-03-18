import inspect

import ez

from ez.database import engine

from .dbi import PAGE_REPOSITORY, PageInfoModel, PAGES_HISTORY_REPOSITORY
from .router import pages_api_router

from fastapi.responses import HTMLResponse


from jsx.html import *
from jsx.renderer import render

import ez.templates

def make_page_route(page: PageInfoModel):
    if not page.slug.startswith("/"):
        page.slug = f"/{page.slug}"


    template = ez.templates.get(page.template_name)
    signature = inspect.signature(template.render)
    inject_kwargs = {}
    parameters = []
    for param in signature.parameters.values():
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            parameters.append(param)
        elif isinstance(annotation, type) and issubclass(annotation, ez.templates.PageData):
            if param.kind in { param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY }:
                inject_kwargs[param.name] = ez.templates.PageData(
                    id=page.id,
                    title=page.title,
                    content=page.content,
                    slug=page.slug,
                    template_name=page.template_name
                )
            elif param.kind == param.POSITIONAL_ONLY:
                raise ValueError("Page parameter may not be positional-only")
            else:
                raise ValueError(f"Invalid parameter kind for page: {param.kind}")
        else:
            parameters.append(param)

    new_signature = signature.replace(parameters=parameters)

    def page_route(*args, **kwargs):
        return HTMLResponse(render(template.render(*args, **inject_kwargs, **kwargs)))
    
    page_route.__signature__ = new_signature

    ez.site.get(page.slug)(page_route)


def setup():
    PAGE_REPOSITORY.connect(engine)
    PAGES_HISTORY_REPOSITORY.connect(engine)

    pages = PAGE_REPOSITORY.all()
    for page in pages:
        make_page_route(page)


def main():
    setup()


main()

ez.site.add_router("/api/pages", pages_api_router)


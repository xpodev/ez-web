from seamless import render

from starlette.responses import HTMLResponse
from starlette.routing import Route

from ez.data import DataProviderBase
from ez.templates import Template

from .page_info import PageInfo


class Page(Route):
    def __init__(self, info: PageInfo, template: Template, providers: dict[str, DataProviderBase], slug: str) -> None:
        super().__init__(slug, self.html, methods=["GET"])
        self._info = info
        self.template = template
        self.providers = providers

    @property
    def info(self):
        return self._info

    @property
    def slug(self):
        return self.path
    
    @slug.setter
    def slug(self, value: str):
        if not value.startswith("/"):
            value = f"/{value}"
        self.path = value

    def get_args(self):
        return self.template.params.model_validate({
            provider_name: provider.provide()
            for provider_name, provider in self.providers.items()
        })

    def render(self):
        return self.template.render(self.get_args())

    def render_html(self):
        return render(self.render())
    
    def html(self, request):
        print(request)
        return HTMLResponse(self.render_html())

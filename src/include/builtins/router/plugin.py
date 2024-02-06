# from ez import ez
import ez
from ez.events import HTTP
from ez.database.models.page import PageModel
from include.builtins.template_manager.plugin import load_template

pages = PageModel.all()


@ez.on(HTTP.In)
def on_http_in(request):
    ez.emit(HTTP[request.method], request)


def create_page_router(page: PageModel):
    def page_router():
        return load_template(f"pages/{page.template_name}")(page=page)

    return page_router


for page in pages:

    ez.get(f"/{page.slug}")(create_page_router(page))

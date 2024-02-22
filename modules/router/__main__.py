from functools import wraps
import ez
from ez.database.models.page import PageModel
from importlib.util import spec_from_file_location, module_from_spec

all_pages = PageModel.all()


def make_page_route(page: PageModel):
    template_path = ez.SITE_DIR / "templates" / f"{page.template_name}.py"

    spec = spec_from_file_location(f"templates.{template_path.stem}", template_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    if module.render.__kwdefaults__ is None:
        module.render.__kwdefaults__ = {}

    module.render.__kwdefaults__["page"] = page

    @wraps(module.render)
    def page_route(*args, **kwargs):
        return module.render(*args, **kwargs)
    
    ez.get(page.slug if page.slug.startswith("/") else f"/{page.slug}")(page_route)
    


for page in all_pages:
    make_page_route(page)
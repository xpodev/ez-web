from fastapi.exceptions import HTTPException
import ez

from .errors import TemplateNotFoundError
from .template import Template
from .template_pack import TemplatePack
from .manager import TEMPLATE_MANAGER

def to_json(item: Template | TemplatePack) -> dict:
    return {
        "name": item.name,
        "type": "template" if isinstance(item, Template) else "pack",
        **({
            "items": [
                to_json(sub_item) for sub_item in item
            ]
        } if isinstance(item, TemplatePack) else {})
    }


router = ez.site.router()


@router.get("")
def get_templates() -> dict:
    return {
        "packages": [
            {
                "name": package.info.package_name,
                "items": [
                    to_json(item) for item in package
                ]
            } for package in TEMPLATE_MANAGER.get_packages()
        ]
    }


@router.get("/{name:path}")
def get_template(name: str) -> dict:
    try:
        item = TEMPLATE_MANAGER.get(name)
    except TemplateNotFoundError as exc:
        raise HTTPException(404, str(exc))
    return to_json(item)


ez.site.add_router("/api/templates", router)

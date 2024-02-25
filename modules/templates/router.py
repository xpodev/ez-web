from fastapi.exceptions import HTTPException
import ez
from . import ez_templates as api


def to_json(item: api.Template | api.TemplatePack) -> dict:
    return {
        "name": item.name,
        "type": "template" if isinstance(item, api.Template) else "pack",
        **({
            "items": [
                to_json(sub_item) for sub_item in item
            ]
        } if isinstance(item, api.TemplatePack) else {})
    }


router = ez.router()


@router.get("")
def get_templates():
    return {
        "packages": [
            {
                "name": package.info.package_name,
                "items": [
                    to_json(item) for item in package
                ]
            } for package in api.get_packages()
        ]
    }


@router.get("/{name:path}")
def get_template(name: str):
    try:
        item = api.get(name)
    except api.TemplateNotFoundError as exc:
        raise HTTPException(404, str(exc))
    return to_json(item)


ez.add_router("/api/templates", router)

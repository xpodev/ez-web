from os import name
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

import ez
import ez.web

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


router = ez.web.http.router("/templates")


@router.get("/")
def get_templates(_) -> JSONResponse:
    return JSONResponse({
        "packages": [
            {
                "name": package.info.package_name,
                "items": [
                    to_json(item) for item in package
                ]
            } for package in TEMPLATE_MANAGER.get_packages()
        ]
    })


@router.get("/{name:path}")
def get_template(request) -> JSONResponse:
    name = request.path_params["name"]
    try:
        item = TEMPLATE_MANAGER.get(name)
    except TemplateNotFoundError as exc:
        raise HTTPException(404, str(exc))
    return JSONResponse(to_json(item))

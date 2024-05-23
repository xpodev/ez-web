from typing import Any, Iterable

import ez

# from ez.data.providers import DataProviderBase
from ez.data import DataProviderBase

from .manager import PAGE_MANAGER
from .page import Page
from .page_info import PageInfo
from .routing import PAGE_ROUTER


def _load_providers(config: Iterable[tuple[str, type[DataProviderBase], Any]]) -> dict[str, DataProviderBase]:
    return {
        name: tp.load(args)
        for name, tp, args in config
    }


def _zip_providers(providers: dict[str, Any], template: "ez.templates.Template") -> Iterable[tuple[str, type[DataProviderBase], Any]]:
    for name, config in providers.items():
        field = template.params.model_fields.get(name)
        if not field:
            raise ValueError(f"Provider {name} not found in template")
        annotation = field.annotation
        if not isinstance(annotation, type):
            raise ValueError(f"Invalid data type for parameter {name} in {template.name}")
        provider_type = ez.data.providers.get_provider_type(annotation)
        yield name, provider_type, config


def create_page(info: PageInfo) -> Page:
    template = ez.templates.get(info.template_name)
    if not isinstance(template, ez.templates.Template):
        raise ValueError(f"Template {info.template_name} not found")
    
    providers = _load_providers(_zip_providers(info.config, template))
    return Page(info, template, providers, info.slug)


def add_page(page: Page):
    PAGE_ROUTER.routes.append(page)
    PAGE_MANAGER.add(page)


def remove_page(page: Page):
    try:
        PAGE_ROUTER.routes.remove(page)
    except ValueError:
        pass
    PAGE_MANAGER.remove(page)

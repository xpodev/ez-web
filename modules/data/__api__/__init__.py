from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from modules.data import providers
    from modules.data.providers import DataProviderBase, ModelProvider, get_provider, get_or_create_provider

else:
    from . import providers

    from .providers import DataProviderBase, ModelProvider, get_provider, get_or_create_provider

from pydantic import BaseModel, Field

from .base import BaseSiteConfig

from .. import constants as cs


class DatabaseConfig(BaseModel):
    uri: str
    prefix: str


class SiteOverwrites(BaseModel):
    plugin_directory: str = Field(alias="plugin-directory", default=cs.DEFAULT_PLUGIN_DIR)
    template_directory: str = Field(alias="template-directory", default=cs.DEFAULT_TEMPLATE_DIR)
    static_directory: str = Field(alias="static-directory", default=cs.DEFAULT_STATIC_DIR)
    resource_directory: str = Field(alias="resource-directory", default=cs.DEFAULT_RESOURCE_DIR)

    admin_url: str = Field(alias="admin-url", default=cs.DEFAULT_ADMIN_URL)
    api_url: str = Field(alias="api-url", default=cs.DEFAULT_API_URL)
    site_url: str = Field(alias="site-url", default=cs.DEFAULT_SITE_URL)
    static_url: str = Field(alias="static-url", default=cs.DEFAULT_STATIC_URL)


class SiteConfig(BaseSiteConfig):
    name: str

    database: DatabaseConfig
    overwrites: SiteOverwrites = Field(default_factory=SiteOverwrites)

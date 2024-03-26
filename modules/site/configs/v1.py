from pydantic import BaseModel

from .base import BaseSiteConfig


class DatabaseConfig(BaseModel):
    uri: str
    prefix: str


class SiteConfig(BaseSiteConfig):
    name: str

    database: DatabaseConfig

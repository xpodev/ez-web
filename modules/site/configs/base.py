from pydantic import BaseModel


class BaseSiteConfig(BaseModel):
    version: int

import json
from typing import Any

from pydantic import BaseModel
from pydantic.functional_validators import field_validator


class PageInfo(BaseModel):
    title: str
    slug: str
    config: dict[str, Any]
    template_name: str

    @field_validator("slug", mode="before")
    def slug_validator(cls, value):
        if not value.startswith("/"):
            return f"/{value}"
        return value
    
    @field_validator("config", mode="before")
    def config_validator(cls, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("Config must be a dictionary")
        if not isinstance(value, dict):
            raise ValueError("Config must be a dictionary")
        return value

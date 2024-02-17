from pydantic import BaseModel


class PluginWebModel(BaseModel):
    name: str
    id: str
    version: str
    description: str
    enabled: bool

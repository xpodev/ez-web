from . import Model
from ez.database import Column, Integer, String, Boolean, Text


class PluginModel(Model):
    id = Column(Integer, primary_key=True)
    dir_name = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    description = Column(Text())
    version = Column(String(20))
    author = Column(String(255))
    enabled = Column(Boolean, default=False)

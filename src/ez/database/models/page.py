from . import Model
from ez.database import Column, Integer, String, Text


class PageModel(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    slug = Column(String(255), unique=True)
    template_name = Column(String(255))

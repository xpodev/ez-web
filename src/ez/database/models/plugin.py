from . import Model
from ez.database import Column, Integer, String, Boolean

class Plugin(Model):
  __tablename__ = 'ez_plugins'
  
  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  description = Column(String(255))
  version = Column(String(255))
  author = Column(String(255))
  enabled = Column(Boolean, default=False)

  
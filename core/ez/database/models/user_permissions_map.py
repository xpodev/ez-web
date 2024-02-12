from . import Model
from ez.database import Column, Integer


class UserPermissionMap(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    permission_type = Column(Integer, nullable=False)
    bits = Column(Integer, nullable=False)

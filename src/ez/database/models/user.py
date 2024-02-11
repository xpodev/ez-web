from . import Model
from ez.database import Column, Integer, String, session, select
from .user_permissions_map import UserPermissionMap


class UserModel(Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    _permissions = None

    @property
    def permissions(self):
        self._permissions = (
            self._permissions
            or session.scalars(
                select(UserPermissionMap.bits)
                .where(UserPermissionMap.user_id == self.id)
                .order_by(UserPermissionMap.permission_type)
            ).all()
        )

        return self._permissions

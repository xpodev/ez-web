from uuid import uuid4
from .user import User

from . import context

USERNAME = "admin"
PASSWORD = "pwd"


ADMIN_USER = User()


def authenticate(username: str, password: str) -> context.Session | None:
    if username != USERNAME or password != PASSWORD:
        return None

    user = ADMIN_USER

    session = context.create_session(user, uuid4().hex)

    return session

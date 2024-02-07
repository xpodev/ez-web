import ez
import argon2
from ez.database.models.user import UserModel

def get_user() -> UserModel:
    return ez.request.user


def is_admin(user: UserModel=None):
    user = user or get_user()
    if user is None:
        return False

    return user.permissions[0] & 8 == 8


def login(username, password):
    user = UserModel.filter_by(username=username).first()
    if user is None:
        return False

    if argon2.verify(password, user.password):
        # todo: change to jwt
        ez.response.cookie("user_id", user.id)
        return True

    return False

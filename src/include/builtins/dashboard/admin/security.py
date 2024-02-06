import ez


def get_user():
    return ez.request.user

def is_admin(user = get_user()):
    if user is None:
        return False
    
    return user.is_admin
    

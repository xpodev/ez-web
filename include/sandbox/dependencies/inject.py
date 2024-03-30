from functools import wraps

from .context import Context


def inject(context: Context | None = None):
    def decorator(func):
        # TODO: collect the parameters to inject

        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: collect dynamic dependencies
            # TODO: inject the parameters
            return func(*args, **kwargs)

        return wrapper

    return decorator

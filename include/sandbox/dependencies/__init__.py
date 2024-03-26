from .context import Context
from .inject import inject as _inject


CONTEXT = Context()


def inject(func):
    return _inject(CONTEXT)(func)

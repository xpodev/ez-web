"""
Defines the Request class, which represents an incoming HTTP request.

As of v1, this module is a thin wrapper around Starlette's Request class.

When we move to use our own web app framework, or to a different ASGI framework,
we will replace this module with the appropriate request class.

However, the basic API should remain the same, so the rest of the application
should not have to change.
"""

from starlette.requests import Request


__all__ = [
    "Request"
]

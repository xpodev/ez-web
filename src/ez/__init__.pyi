from typing import Any, Callable, Coroutine

from fastapi import Response


def add_route(self, route: str, handler: Callable[..., Coroutine[Any, Any, Response]]):
    """
    Adds a route to the FastAPI app.
    """

def run(self, **kwargs):
    """
    Runs the FastAPI app.
    """


# Methods
def get(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a GET route to the FastAPI app.

    :param route: The route to add.
    """

def post(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a POST route to the FastAPI app.

    :param route: The route to add.
    """

def put(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a PUT route to the FastAPI app.

    :param route: The route to add.
    """

def delete(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a DELETE route to the FastAPI app.

    :param route: The route to add.
    """

def patch(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a PATCH route to the FastAPI app.

    :param route: The route to add.
    """

def options(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a OPTIONS route to the FastAPI app.

    :param route: The route to add.
    """

def head(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a HEAD route to the FastAPI app.

    :param route: The route to add.
    """

def trace(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a TRACE route to the FastAPI app.

    :param route: The route to add.
    """

def connect(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a CONNECT route to the FastAPI app.

    :param route: The route to add.
    """

def all(self, route: str) -> Callable[[Callable[..., Coroutine[Any, Any, Response]]], None]:
    """
    Adds a route to the FastAPI app that accepts any HTTP method.

    :param route: The route to add.
    """
